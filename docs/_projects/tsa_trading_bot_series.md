---
title: "TSA Trading Bot Series"
image: "/assets/tsa_trading_bot/counting_airplanes.webp"
description: The TSA Trading Bot Series explores building an automated trading bot for the TSA Passenger Volume market on Kalshi. It covers web scraping, data analysis, predictive modeling, and algorithmic trading to forecast TSA traffic and place trades. This project is both an experiment in quantitative finance and a hands-on exercise in data engineering and machine learning. Follow along to see if data-driven trading can beat the market!
layout: project
---

![Kalshi predicting traffic](/assets/tsa_trading_bot/counting_airplanes.webp){: width="500" height="500" }


* Table of contents
{:toc}

# Introduction
Hello! This is my blog series dedicated to creating an automated trading bot for prediction markets. 
[Kalshi](kalshi.com/sign-up/?referral=c9d2b0f1-b339-4878-b61c-65c4e7002b51) is a prediction market platform
where you can buy and sell contracts for the accurate prediction of world events.

If you just want links to the blog posts in this series you can go to the bottom of 
this page.

# The market


![Kalshi TSA Event](/assets/tsa_trading_bot/kalshi_tsa.webp)
The specific event we are interested in is the **weekly TSA Passenger Volume market**. This market is for predicting
the average weekly TSA passengers from Monday - Sunday every week. They offer various binary contracts with 
different thresholds that either resolve to true or false. For example, they may offer the following contracts:

1. Weekly TSA passenger volume for the week September 8th - 15th 2024 will be above 2,300,000
2. Weekly TSA passenger volume for the week September 8th - 15th 2024 will be above 2,350,000
3. Weekly TSA passenger volume for the week September 8th - 15th 2024 will be above 2,400,000

Each of these will be a different contract that you can purchase. The prices range from $0.01 - $0.99 which
corresponds to the expected probability of that event resolving to true.

For example, the first contract resolves if that week's TSA passenger volumes is greater than 2.3M. If it's
trading at a price of $0.89, that means the market expects a probability of 89% that the passenger volumes
will be above 2.3M. Then, we would expect our other 2 markets to be priced at a lower amount because
the probability that the number of passengers is higher than 2.35M is less likely than the probability that
passengers are above 2.3M. In other words, if the second contract resovles to true, the first one will as well.

# Our goal

Our goal is to build a model to predict the TSA passenger traffic and use this model to algorithmically place
bets on this market. This makes some implicit assumptions:

1. We can build a model to somewhat accurately predict next week's TSA passenger volumes
2. This model will be more accurate than other market participants

The above points may be incorrect. Even so, it's a fun exercise that lets you use some ~~math~~ ~~applied stats~~
~~machine learning~~ artificial intelligence, programming, and data engineering.

![Trading profits](/assets/tsa_trading_bot/kalshi_tsa_trade.webp)

Ideally, we make money from this. That is unlikely -- we are competing with some very smart people who do
this full-time. So, if it's unlikely we make money from this, why do it?

**It's fun**

I've always been fascinated by markets, statistics, and programming.
This is the intersection of those 3 things. I love working in this field trying
to better understand markets and trying to build predictive models.

![statistics fun](/assets/tsa_trading_bot/venn_diagram.webp)

**Improve statistics and programming knowledge**

I am a data engineer/scientist by trade, and I always like to improve
those fundamental skills. Projects like these are a cool way to get
end-to-end experience with the whole data stack from extraction and data storage
to predictive modeling and algorithmic trading. During this series I primarily referenced
[Hyndman and Athanasopoulos](https://otexts.com/fpp3/). They have made this
text freely available online, and I highly recommend checking it out.


## How

To accomplish this goal we will be:

- Scraping the web to gather our data
- Performing some exploratory data analysis to identify trends
- Building a simple predictive model to estimate future passenger volumes
- Setting up AWS infrastructure to host and automate everything
- Connecting to Kalshi's API to automate our trades

## Prerequisites

This series assumes you have familiarity with the following:

### Python programming
   - I wouldn't consider myself to be a particular strong Pythonista, so I won't be doing anything fancy, but basic Python is important

### Some basic math/statistics
   - I think basic models are preferred most of the time, so the modeling/stats I do will be super basic. Mostly things like correlations, means, rolling averages, etc.

That's about it. I don't know much about a lot, so nothing in this series will be too hard. It's mostly
just the tediousness of building everything that you need. If I can do it, so can you. I will include
external references whenever I can to elaborate on certain topics. 

# But wait, if you can make money from this, why are you publicizing it?

Great question! This is a common callout for people selling day trading type courses and is a very
good point. If you have a winning strategy to extract money from markets, wouldn't you be better off
keeping it a secret and making money from it instead of releasing to the public? 

I have several answers to this question:

## Liquidity

[Liquidity](https://www.investopedia.com/terms/l/liquidity.asp) in this market is very low. If I had an 
amazing model that I was highly confident in, I could probably make $20/week just because not enough 
people are trading it, so it's hard to buy more than a handful of contracts at a time. This means any 
model that predicts this market simply isn't worth very much.

## Lack of confidence in my model

I'm highly skeptical that I can build a persistently profitable model. I'm using freely available
data and applying basic techniques to estimate future values. It's not a particularly high
barrier to entry, so I think it's unlikely my model will be profitable -- even if it is, I doubt it will
be profitable for long. [Markets are just pretty efficient and they are 
hard to beat.](https://corporatefinanceinstitute.com/resources/career-map/sell-side/capital-markets/efficient-markets-hypothesis/)

## Updating my model

I plan to continously update my model over time, but I will not update my blog series. This blog series
is how I am getting started with my trading, but I expect to make changes after I'm done with this series.
So, if you build out a model using this series and don't make any additional improvements to it, I'm hoping
my updates will allow me to outperform

## Referral link

I will be using my Kalshi referral link throughout this series, so there is some financial incentive for me.
If you use the link and trade at least 100 contracts, we both get $25. Given, the lack of liquidity, I could
see this being more than I would get from actually trading the market.

Referral link rules from [Kalshi:](kalshi.com/sign-up/?referral=c9d2b0f1-b339-4878-b61c-65c4e7002b51)

![Referral link rules](/assets/tsa_trading_bot/referral_link_rules.webp)

### Disclaimer

#### You will likely lose money if you trade


> Less than 1% of the day trader population is able to predictably and reliably earn positive abnormal returns net of fees.


[Most market participants end up losing money](https://www.sciencedirect.com/science/article/abs/pii/S1386418113000190).
A disproportionate amount of profits go to a small number of market participants and you will likely not be one of those. 
Do not expect to make money doing this. In fact, I will be one of the people trying to take money away from you

#### There may be bugs in my code
I am continuously finding bugs in my code and my logic. Please check everything yourself and assume everything
I wrote is wrong/broken. I will try to update bugs I find, but it's honestly a lot of work, so I may not.

#### I will make changes to my model and process
I will continue making changes to my model, so the model you see in this series will just be a starting point
for me. Don't think using this model will make you a bunch of money. It almost certainly won't. You will likely
lose money if you only rely on the model in this series.

#### Prediction markets are a controversial topic
[Please see my post on prediction market for details](https://ferraijv.github.io/posts/data/2024/07/24/what-are-prediction-markets.html)

My thought process is, people have always and will always make predictions about future events. Currently,
most of these people are incentived, not to be accurate, but to be make the most incendiary and extreme predictions
possible in order to get social media engagement. I would rather incentivize forecasters to be accurate. Prediction
markets do that.

# Why should we trust you?

**You shouldn't**. Build what you think is best. Don't just blindly use my model and expect it to work out. That's why
I love markets. The only thing that matters is whether you make or lose money. It's impossible to fake that.

I'm not saying I'm going to make money. I'm just putting my process out there because I think
it's fun to try and make money in markets. 99.9% of my money is in [ETFs](https://business.rice.edu/wisdom/peer-reviewed-research/should-you-invest-index-funds-or-active-funds). 
**This is just my hobby.**

I have been trading based on this model (mostly manual trading as of now to test it) for a few weeks now,
and it's done surprisingly well. This can and likely will stop soon. I think of this more
as a fun way to motivate me to continue to refine my programming, statistics, and finance skills/knowledge.

![trading record](/assets/tsa_trading_bot/trading_record.webp)

[You can check my Kalshi stats and positions on my profile.](https://kalshi.com/ideas/profiles/ferraijv)

<br>

___

<br>

# The Series

Now, that the introduction is out of the way, let's get started. Below
are the different blog posts that are part of this series. 

Please reach out if you have any feedback or want to chat `ferraioloj@gmail.com`

* [Part 1: Web scraping to get historical data from the TSA site](/posts/data/2024/04/14/tsa-web-scraping.html) 

* [Part 2: Finding supplementary data to help build our model](/posts/data/2024/04/16/tsa-supplementary-data.html) (Note: I ended up not using this data in the model)

* [Part 3: Exploratory data analysis](/posts/data/2024/07/05/tsa-exploratory-analysis.html)

* [Part 4: Manual trading](/posts/data/2024/07/28/tsa-trading-rules.html)

* [Part 5: Automated trading bot](/posts/data/2024/09/08/kalshi-tsa-trading-automated-bot.html)
