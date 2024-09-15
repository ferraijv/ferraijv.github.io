---
layout: post
title:  "TSA Prediction Market: Part 5 - Automated bot"
date:   2024-09-08 00:00:00 -0500
categories: data
author: "Jacob Ferraiolo"
toc: true
image: "/assets/tsa_trading_bot/plugging_it_in.webp"
---
![trading_bot](/assets/tsa_trading_bot/plugging_it_in.webp){: width="500" height="500" }

<h2> Today's post </h2>
* Table of contents
{:toc}

# Introduction
[Last time](https://ferraijv.github.io/posts/data/2024/07/28/tsa-trading-rules.html), we showed how to productionize
our model, so it would automatically run every morning and send market predictions to us every morning.

This enabled us to get a daily email with the predictions to use for manual trading. Now that it's been
a few weeks, and we have built up confidence in our model, we can automate the trading.

This is the return from my first trade using the model. It was only about $10 to test out the model, and
the results of a single trade don't mean anything, but it's always nice to start out a new strategy
with a win.

![First Kalshi TSA Trade](/assets/tsa_trading_bot/kalshi_tsa_trade.webp){: width="500" height="250" }


# Connecting to the Kalshi API

## Step 1: Create a Kalshi account

This section will detail how to connect to the [Kalshi](kalshi.com/sign-up/?referral=c9d2b0f1-b339-4878-b61c-65c4e7002b51)
API to get current contract prices and create new orders.

[If you use my referral link we both get $25 subject to their referral process
](kalshi.com/sign-up/?referral=c9d2b0f1-b339-4878-b61c-65c4e7002b51)

Note: Last I checked, their API does not support MFA, so you can not have
MFA on your account if you want to do any of the following steps.

## Step 2: Store your credentials in AWS Secrets Manager

[AWS Secrets Manager](https://aws.amazon.com/secrets-manager/) enables you to store
credentials in a secure location that is easy to access from you application code.

## Step 3: 

[Use Kalshi's official Python SDK to connect](https://github.com/Kalshi/kalshi-python). I'm
using my own code to connect to Kalshi, so the actual connection code might be a bit different.
You should probably use whatever they recommend.

# Getting floor strike for upcoming event

## Familiarize yourself with Kalshi terminology

_Market:_ A single binary market. This is a low level object which rarely will need to be exposed on its own to members. 
The usage of the term “market” here is consistent with how it’s used in the backend and API. In our case, the markets
are the individual contracts at a given passenger level. 

_Event:_ An event is a collection of markets and the basic unit that members should interact with on Kalshi.

_Series:_ A series is a collection of related events

_Ticker:_ Each series have unique ticker names to that

_Floor Strike:_ The threshold for a given market that determines the resolution of the market

This blog series has focused on TSA Passenger events. So, all of these TSA
passenger markets belong to the TSA series. Each week there is a new event consisting
of many markets. For example, for the event ending on 9/8/24, there were
markets for passengers above 2.3M, 2.35M, etc.

These definitions were taken directly from the [Kalshi API Docs](https://trading-api.readme.io/reference/terms).

## Determine the event

The TSA passenger event always goes from Monday - Sunday. The event ticker
always reflects the last day of the event, so it's generally Sunday's date.

For example, the event ticker for the event ending on 9/8/24 follows:

`tsaw-24sep08`

Where:
- `TSAW` is the series.
- `24sep08` is the specific event

We need to algorithmically determine the next event ticker using this format.

### Determine the date of the upcoming Sunday

The below code shows how we can programmatically determine the date
of the upcoming Sunday. We:
1. Calculate the number of days until Sunday
2. Add that number of days to the current date
3. Add in logic to account for the edge case for if today is Sunday
4. Format the date into the format accepted by Kalshi's API

<details>
{% highlight python %}

def get_next_sunday(skip_today_if_sunday=False):
    """
    Calculate the date of the next Sunday.

    If today is Sunday:
        - By default, return today's date.
        - If skip_today_if_sunday is True, return the date for the following Sunday (7 days later).

    Parameters:
    skip_today_if_sunday (bool): Flag to determine whether to skip today's date if it is Sunday.
    
    Returns:
    str: The date of the next Sunday in the format 'YYMonDD', where 'Mon' is the abbreviated month name.
    """
    today = datetime.date.today()
    # Calculate the number of days until the next Sunday (0 is Monday, 6 is Sunday)
    days_until_sunday = (6 - today.weekday()) % 7
    # If today is Sunday, we want the next Sunday, so we add 7 days
    if days_until_sunday == 0:
        if skip_today_if_sunday:
            days_until_sunday = 7
        else:
            days_until_sunday = 0
    next_sunday = today + datetime.timedelta(days=days_until_sunday)
    next_sunday = next_sunday.strftime("%y%b%d").upper()

    return next_sunday

{% endhighlight %}
</details>
<br>

## Query the markets in this event

Now that we have the event ticker, we can use this to query all the markets in this event. This will return
each market's ticker along with the floor strikes

The below code fetches all markets associated with a given event. It will return a dataframe containing
the market ticker, floor strike, yes and no prices.

<details>
{% highlight python %}

def get_floor_strike_and_prices(event_id):
    """
    Fetch market data for a specific event and extract relevant pricing information.

    This function logs into the exchange client, retrieves market data for the given event,
    and normalizes the response into a pandas DataFrame. It then selects and returns the
    'ticker', 'floor_strike', 'yes_ask', and 'no_ask' columns.

    Parameters:
    event_id (str or int): The ID of the event for which market data is being retrieved.

    Returns:
    pandas.DataFrame: A DataFrame containing the columns 'ticker', 'floor_strike', 'yes_ask', 
                      and 'no_ask' with corresponding market data for the event.
    """
    exchange_client = shared.login()
    df = pd.json_normalize(exchange_client.get_event(event_id)['markets'])
    prices = df[['ticker', 'floor_strike', 'yes_ask', 'no_ask']]

    return prices

{% endhighlight %}
</details>
<br>


# Generating "fair value" for each market

Now we want to determine how much we should pay for each market. If our prediction for a given week 
is 2.44M passengers, how do we translate that into specific prices? Clearly, we think the market for 
"Above 2.4M passengers" will resolve to "yes", but does that mean we should pay $0.99 for that market? That
would imply a 99% probability of more than 2.4M passengers.

This section details how we can translate our prediction into actual prices for each market.

## For each market, calculate the difference between the prediction and the floor strike

We want to start off by calculating how far off each market is from our predicted value. A market that is
1% off from our prediction should be much more likely than a market that is 10% away. 

We can use historical deviations from our prediction value to determine the likelihood of a similar discrepancy.
Consider the following example of using a predicted passenger volume of 2,440,000 to determine the price of a market
that pays out if the actual number of passengers is above 2.4M:

prediction: 2.44M
floor strike: 2.4M

The floor strike is about 1.6% below the prediction. So, this market will resolve to yes as long as the actual
passenger volume comes in at `prediction*(1-0.016)` or greater. Inversely, this market will resolve to "no" if
the deviation from our prediction is less than 1.6%. If the actual passenger volume is 2% below our prediction, 
we will have actual passenger volumes around 2.38M which is below the required threshold for this market to 
pay out.

## Check historical data for similar discrepancies

We can consult our historical data to determine how often our prediction was this far off from the actual value.
So, in this case we find all instances of historical data where the following condition is met:

`actual passengers/prediction-1 < -0.016`

This gives us a rough estimate of the likelihood that the actual passengers will be low enough to cause this
market to resolve to "no". We can use this as our estimate of the true value of a given market. 

We repeat this process for each market to get the true value of every market.


<details>
{% highlight python %}

def get_likelihoods_of_each_contract(prediction):
    """
    Calculate the likelihood of each contract being correct based on a prediction and historical data.

    This function retrieves the prediction for the upcoming Sunday, calculates the likelihood 
    of each contract's outcome (yes or no) using historical data, and compares it against current 
    market prices.

    Steps:
    1. Get the date of the next Sunday and extract the prediction value for that date.
    2. Load historical TSA data, compute raw and percent error based on predictions, and filter out 
       missing values.
    3. Retrieve current market prices and floor strike values.
    4. For each contract, determine whether the prediction is above or below the floor strike.
    5. Calculate the likelihood for either the "yes" or "no" side of the contract based on historical data.
    6. Store the likelihoods for each contract in a dictionary and return it.

    Parameters:
    prediction (dict): A dictionary containing predictions for various dates, including the next Sunday.

    Returns:
    dict: A dictionary where each key is a contract ticker and the value is a dictionary containing:
          - 'floor_strike': The floor strike value for the contract.
          - 'side': The side of the contract ('yes' or 'no').
          - 'true_value': The calculated likelihood of that side being correct.
    """

    next_sunday = datetime.datetime.strptime(shared.get_next_sunday(), "%y%b%d").strftime("%Y-%m-%d")

    prediction = prediction[next_sunday]['prediction']

    print(f"Calculating likelihoods for {prediction}")

    historical_data = pd.read_csv("data/lagged_tsa_data.csv")
    historical_data = historical_data[['passengers_7_day_moving_average', 'prediction']]
    historical_data = historical_data[~historical_data['prediction'].isna()]
    historical_data['raw_error'] = historical_data['passengers_7_day_moving_average'] - historical_data['prediction']
    historical_data['percent_error'] = historical_data['passengers_7_day_moving_average']/historical_data['prediction']-1

    likelihoods = {}

    prices = get_current_market_prices()

    print(prices)

    floor_strikes = prices[['ticker', 'floor_strike']].values.tolist()
    print(f"floor strike: {floor_strikes}")

    # floor_strike[0] is the ticker
    # floor_strike[1] is the floor_strike
    for floor_strike in floor_strikes:
        if prediction > floor_strike[1]:
            likelihoods[floor_strike[0]] = {
                'floor_strike': floor_strike[1],
                'side': "yes",
                'true_value': get_likelihood_of_yes(prediction, floor_strike[1], historical_data)
            }
        elif prediction < floor_strike[1]:
            likelihoods[floor_strike[0]] = {
                'floor_strike': floor_strike[1],
                "side": "no",
                "true_value": get_likelihood_of_no(prediction, floor_strike[1], historical_data)
            }

    print(likelihoods)

    return likelihoods
{% endhighlight %}
</details>
<br>

After running this process for each market in the event we are left with
something like this:

```
{'TSAW-24SEP08-A2.10': {'floor_strike': 2100000, 'side': 'yes', 'true_value': 1.0}, 'TSAW-24SEP08-A2.15': {'floor_strike': 2150000, 'side': 'yes', 'true_value': 1.0}, 'TSAW-24SEP08-A2.20': {'floor_strike': 2200000, 'side': 'yes', 'true_value': 0.9987789987789988}, 'TSAW-24SEP08-A2.25': {'floor_strike': 2250000, 'side': 'yes', 'true_value': 0.9914529914529915}, 'TSAW-24SEP08-A2.30': {'floor_strike': 2300000, 'side': 'yes', 'true_value': 0.978021978021978}, 'TSAW-24SEP08-A2.35': {'floor_strike': 2350000, 'side': 'yes', 'true_value': 0.7973137973137974}, 'TSAW-24SEP08-A2.40': {'floor_strike': 2400000, 'side': 'no', 'true_value': 0.9010989010989011}, 'TSAW-24SEP08-A2.45': {'floor_strike': 2450000, 'side': 'no', 'true_value': 0.989010989010989}, 'TSAW-24SEP08-A2.50': {'floor_strike': 2500000, 'side': 'no', 'true_value': 1.0}, 'TSAW-24SEP08-A2.55': {'floor_strike': 2550000, 'side': 'no', 'true_value': 1.0}, 'TSAW-24SEP08-A2.60': {'floor_strike': 2600000, 'side': 'no', 'true_value': 1.0}, 'TSAW-24SEP08-A2.65': {'floor_strike': 2650000, 'side': 'no', 'true_value': 1.0}, 'TSAW-24SEP08-A2.70': {'floor_strike': 2700000, 'side': 'no', 'true_value': 1.0}, 'TSAW-24SEP08-A2.75': {'floor_strike': 2750000, 'side': 'no', 'true_value': 1.0}, 'TSAW-24SEP08-A2.80': {'floor_strike': 2800000, 'side': 'no', 'true_value': 1.0}}
```

# Placing automated trades

Now we can use these "true values" to put in limit orders for each market.
Limit orders specify a specific price and will only be executed if another order
is placed at your specified price or better. This ensures we can set the price
we want for a given market and also allows us to bypass Kalshi's fees since there
are no fees for market makers.

In the following code we:
1. Iterate through each market
2. For each market, create a limit order for either the "no" or "yes" side to buy
3. Set the limit price at a threshold below our "true value" (I used 75% of true value arbitrarily)

<details>
{% highlight python %}


def create_limit_orders_for_all_contracts(likelihoods):
    """
    Create limit orders for all contracts based on their calculated likelihoods.

    This function logs into the exchange client in demo mode, retrieves the event ticker for the
    next TSA event, and generates limit orders for each contract based on the likelihood of
    either a "yes" or "no" outcome. Orders are created with a margin of safety, meaning the
    order price is adjusted to 75% of the calculated likelihood. Contracts with extreme
    likelihoods (greater than 95% or less than 5%) are excluded to avoid edge cases.

    Steps:
    1. Log into the exchange client in demo mode.
    2. Generate the event ticker for the next TSA event.
    3. Retrieve and print the existing orders for the event.
    4. Loop through each contract and create a limit order if the likelihood is between 5% and 95%.
    5. Adjust the order price to 75% of the likelihood value to include a margin of safety.
    6. Submit the order to the exchange and store the order details in a list.
    7. Return the list of created orders.

    Parameters:
    likelihoods (dict): A dictionary of contract likelihoods where each key is a contract ticker
                        and the value contains the likelihood data including 'true_value', 'side',
                        and 'floor_strike'.

    Returns:
    list: A list of dictionaries representing the created orders, including contract ticker,
          order parameters, and side of the contract.
    """
    exchange_client = shared.login(use_demo=True)
    event_ticker = shared.create_tsa_event_id(shared.get_next_sunday())
    print(exchange_client.get_orders(event_ticker=event_ticker)['orders'])
    orders = []
    for contract_ticker, likelihood in likelihoods.items():
        if likelihood['true_value'] < .95 and likelihood['true_value'] > .05: # Things get weird at the extremes
            order_params = {
                "action": "buy",
                "type": "limit",
                "side": likelihood['side'],
                "count": 10,
                f"{likelihood['side']}_price": int(round(likelihood['true_value']*.75, 2)*100) # Margin of safety

            }
            print(order_params)
            exchange_client.create_order(ticker=contract_ticker, client_order_id=str(uuid.uuid4()), **order_params)
            order_params['ticker'] = contract_ticker
            orders.append(order_params)

    return orders

{% endhighlight %}
</details>
<br>

# Conclusion

In today's blog post we discussed the following:
1. How to create a Kalshi account
2. Figuring out the event ticker for the next TSA event
3. Using historical data along with our predicted value to calculate an estimate of the "true" value for each contract
4. How to use this "true value" to create orders on Kalshi

Some important notes:
- This is not risk-free. You will likely lose money placing trades on Kalshi
- Please test your code extensively before automating any trading
- Use Kalshi's demo accounts to test

# Next steps
We finally have an automated trading bot. This series lasted much longer
than I anticipated, so I'm excited to move on to other ideas I have; however,
there are a few things I want to follow up on here.
- I want to implement monitoring for my bot. Anyone can check my [Kalshi account](https://kalshi.com/ideas/profiles/ferraijv) to see my progress, but I would like to make it more transparent
- Improving the model. We implemented a pretty basic model. I would like to try to improve it to see if we can increase our accuracy
- Add logic to account for trades in the middle of the week. Trading on a Monday when no days are factored into the weekly average is very different from trading on a Thursday when much of the week is already determined.

<br>

___

<br>

# The Series

Now, that the introduction is out of the way, let's get started. Below
are the different blog posts that are part of this series. 

Please reach out if you have any feedback or want to chat.

* [Part 1: Web scraping to get historical data from the TSA site](/posts/data/2024/04/14/tsa-web-scraping.html) 

* [Part 2: Finding supplementary data to help build our model](/posts/data/2024/04/16/tsa-supplementary-data.html) (Note: I ended up not using this data in the model)

* [Part 3: Exploratory data analysis](/posts/data/2024/07/05/tsa-exploratory-analysis.html)

* [Part 4: Manual trading](/posts/data/2024/07/28/tsa-trading-rules.html)

* [Part 5: Automated trading bot](/posts/data/2024/09/08/kalshi-tsa-trading-automated-bot.html)

