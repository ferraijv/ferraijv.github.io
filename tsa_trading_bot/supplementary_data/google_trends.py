import pandas as pd
from pytrends.request import TrendReq
import holidays
import datetime
import logging
import functools as ft

def get_single_google_keyword(keyword):
    """
    Fetches Google Trends data for a single keyword.

    Args:
        keyword (str): The keyword to fetch data for.

    Returns:
        DataFrame: A pandas DataFrame containing the Google Trends data for the keyword.
    """
    logging.info(f"Getting google trends data for keyword: {keyword}")
    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list = [keyword]
    pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m')
    data = pytrends.interest_over_time()
    logging.info(f"Finished getting Google Trends data for : {keyword}")

    return data


def get_google_trends_data():
    """
    Fetches Google Trends data for a list of keywords and combines them into a single DataFrame.

    Returns:
        DataFrame: A pandas DataFrame containing the combined Google Trends data for the keywords.
    """

    keywords = [
        "TSA wait times",
        "Airport security",
        "Airline checkin"
    ]
    dfs = []
    for keyword in keywords:
        data = get_single_google_keyword(keyword)
        data = data.reset_index()
        print(data.head())
        dfs.append(data)

    df_final = ft.reduce(lambda left, right: pd.merge(left, right), dfs)

    df = df_final.astype({"date": "datetime64[ns]"})

    df_final.to_csv("../data/google_trends.csv")

    return df_final

def get_holiday_data():
    """
    Extracts US holiday data for the years 2019 to 2024 and saves it to a CSV file.

    Returns:
        DataFrame: A pandas DataFrame containing the US holiday data with one-hot encoding for holidays.
    """
    logging.warning("Extracting holiday data...")
    years = [x for x in range(2019,2025)]
    us_holidays = holidays.US(years=years)

    data = [[date, holiday_name] for date, holiday_name in us_holidays.items()]

    df = pd.DataFrame(data, columns=['date', 'holiday'])
    one_hot = pd.get_dummies(df["holiday"])
    df = df.drop("holiday", axis=1)
    df = df.join(one_hot)

    df = df.astype({"date": "datetime64[ns]"})

    df.to_csv("../data/holiday_data.csv")

    logging.warning("Holiday data extracted and results written to csv")

    return df

def get_weekly_economic_indicator_data():
    """
    Extracts weekly economic indicator data from the Dallas Fed website and saves it to a CSV file.

    Returns:
        DataFrame: A pandas DataFrame containing the weekly economic indicator data.
    """
    logging.warning("Extracting weekly economic indicator data...")
    df = pd.read_excel(
        "https://www.dallasfed.org/-/media/documents/research/wei/weekly-economic-index.xlsx",
        sheet_name="2008-current"
    )

    df = df[["Date", "WEI"]]

    df = df.rename(columns={"Date": "date"})

    df= df.astype({"date": "datetime64[ns]"})

    df = df[df['date'] > "2019-01-01"]

    df.to_csv("../data/wei_data.csv")

    return df

def create_date_table(start='2019-01-01', end=datetime.date.today().strftime("%Y-%m-%d")):
    """
    Creates a date table containing date-related information from a given start date to an end date.

    Taken from: https://stackoverflow.com/questions/47150709/how-to-create-a-calendar-table-date-dimension-in-pandas

    Args:
        start (str): The start date for the date table in the format 'YYYY-MM-DD'. Default is '2019-01-01'.
        end (str): The end date for the date table in the format 'YYYY-MM-DD'. Default is today's date.

    Returns:
        DataFrame: A pandas DataFrame containing the date table with columns for date, day of the week, week number, quarter, year, and year half.
    """
    df = pd.DataFrame({"date": pd.date_range(start, end)})
    df["Day"] = df.date.dt.day_name()
    df["Week"] = df.date.dt.strftime("%U")
    df["Quarter"] = df.date.dt.quarter
    df["Year"] = df.date.dt.year
    df["Year_half"] = (df.Quarter + 1) // 2
    return df

def final_data_cleanup(df):
    """
    Performs final data cleanup on the DataFrame.

    Args:
        df (DataFrame): The DataFrame to clean up.

    Returns:
        DataFrame: The cleaned-up DataFrame.
    """
    df['WEI'] = df['WEI'].ffill()

    return df

def get_supplementary_data():
    """
    Retrieves and combines supplementary data including date table, Google Trends data, holiday data, and weekly economic indicator data.

    Returns:
        bool: True if the data retrieval and combination are successful.
    """
    all_data = []
    all_data.append(create_date_table())
    all_data.append(get_google_trends_data())
    all_data.append(get_holiday_data())
    all_data.append(get_weekly_economic_indicator_data())

    all_data_df = ft.reduce(lambda left, right: pd.merge(left, right, on="date", how="outer"), all_data)

    all_data_df = final_data_cleanup(all_data_df)

    all_data_df.to_csv("../data/all_supplementary_data.csv")

    return True
