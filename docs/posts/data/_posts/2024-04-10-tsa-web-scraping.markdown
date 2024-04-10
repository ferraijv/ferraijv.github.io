---
layout: post
title:  "TSA trading bot: Part 1 - Web Scraping"
date:   2024-04-08 15:20:00 -0500
categories: data
---

<h3> Introduction </h3>
This is a 5 part series on building a trading bot for next week's TSA traffic market on 
Kalshi. We will be covering the following:

* Part 1: Web scraping to get historical data from the TSA site

* Part 2: Finding supplementary data to help build our model

* Part 3: Building our predictive model

* Part 4: Evaluating and fine-tuning that model

* Part 5: Setting up automated trading on Kalshi


<h3> What is Kalshi? </h3>
[Kalshi](https://www.kalshi.com/sign-up/?referral=c9d2b0f1-b339-4878-b61c-65c4e7002b51) is a 
prediction market platform where users trade contracts based on 
the likelihood of real-world events. It offers markets in politics, finance, 
and current events, allowing users to buy and sell contracts to express their 
views and potentially profit from accurate predictions. We will talk more about 
how Kalshi works in a later section. 

<h3> Part 1: Scraping TSA Data </h3>

<h4> The data </h4>
The first thing we need to build any model is data, so 
let's create a process to quickly retrieve the historical
TSA volume data. The data is updated daily [here.](https://www.tsa.gov/travel/passenger-volumes)

As you would expect from a government agency, the data
is in an incredibly annoying format with no easy option
to download. So, we will have to build a web scraper. Luckily,
this is easy to do with Python.

![TSA Data](/assets/tsa_data_screenshot.png)

<h4> The web scraper </h4>
We could retrieve the html and parse it for the table 
and convert this to a dataframe, but pandas has done all
this work for us. Using the pandas library, we can get this
data into a dataframe in a few lines of code

{% highlight python %}

url = 'https://www.tsa.gov/travel/passenger-volumes'
header = {'User-Agent': 'Mozilla/5.0'}  # TSA website blocks bot traffic unless you include this
r = requests.get(url, headers=header)

df = pd.read_html(r.text)[0]  # Returns a list of dataframes, but we only want one

{% endhighlight %}

|     | Date      | 2024     | 2023     |
|-----|-----------|----------|----------|
| 0   | 4/8/2024  | 2484246  | 2523060  |
| 1   | 4/7/2024  | 2663438  | 2387558  |
| 2   | 4/6/2024  | 2314575  | 2093075  |
| 3   | 4/5/2024  | 2681880  | 2475896  |
| 4   | 4/4/2024  | 2619443  | 2532778  |
| 5   | 4/3/2024  | 2258815  | 2209680  |
| 6   | 4/2/2024  | 2258219  | 2080546  |
| 7   | 4/1/2024  | 2648336  | 2404966  |
| 8   | 3/31/2024 | 2586606  | 2545494  |
| 9   | 3/30/2024 | 2320492  | 2253892  |

That gets us a pandas dataframe with the current year of data! But, looking again
at the TSA page, we can see that they have data going back to 2019 on different pages.
Let's get that data too. Each historical page is structured in a similar format
but with the addition of the year appended at the end of the url. Like this...

`https://www.tsa.gov/travel/passenger-volumes/2022`

Let's create a function to retrieve any given year of data. The current year of
data has a different url structure which we will need to account for.

{% highlight python %}
def create_request_url(year_to_process, current_year):
    """Create Request URL

    Creates a URL for fetching TSA data based on the year to process and the current year.

    Args:
        year_to_process (int): The year for which the data is to be fetched.
        current_year (int): The current year.

    Returns:
        str: The URL for fetching TSA data for the specified year.
    """

    base_url = 'https://www.tsa.gov/travel/passenger-volumes'

    if year_to_process == current_year:
        url = base_url
    else:
        url = f"{base_url}/{year_to_process}"

    return url

{% endhighlight %}

Now we have a function that will generate the appropriate request url for any given
year. Next, we will create a function to use this url to actually retrieve the data.

{% highlight python %}
def fetch_year_of_tsa_data(year_to_process):
    """Fetch TSA Data for a Specific Year

    Fetches TSA (Transportation Security Administration) data for a specific year from the TSA website.

    Args:
        base_url (str): The base URL of the TSA data website.
        year_to_process (int): The year for which the data is to be fetched.

    Returns:
        pandas.DataFrame: A DataFrame containing the TSA data for the specified year.
    """

    header = {'User-Agent': 'Mozilla/5.0'}  # TSA website blocks bot traffic unless you include this
    current_year = datetime.datetime.now().year

    url = create_request_url(year_to_process, current_year)

    logging.warning(f"Processing {year_to_process}")

    r = requests.get(url, headers=header)

    df = pd.read_html(r.text)[0]

    #  Structure of current year's data is a bit different
    #  Here we change the format to match previous years
    if year_to_process == current_year:
        df = df[['Date', str(current_year)]]
        df = df.rename(columns={str(current_year): "Numbers"})

    return df

{% endhighlight %}