import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.metrics import root_mean_squared_error


def plot_tsa_traffic():
    """
    This function loads TSA passenger data from a CSV file, processes the data to calculate a 7-day moving average,
    and then plots this moving average over time. It also highlights specific date ranges (early January to late
    February of each year) on the plot.

    The steps involved are:
    1. Load TSA data from a CSV file.
    2. Rename columns for clarity.
    3. Convert the date column to datetime format.
    4. Filter data to include only dates after September 1, 2021.
    5. Calculate a 7-day moving average of the number of passengers.
    6. Plot the 7-day moving average over time.
    7. Highlight specific date ranges on the plot.
    8. Set the y-axis label and display the plot.
    """

    tsa_data = pd.read_csv("../data/tsa_data.csv", index_col=0)

    # Standardize column names
    tsa_data.rename(columns={"Date": "date", "Numbers": "passengers"}, inplace=True)

    # Get date column in datetime
    tsa_data['date'] = pd.to_datetime(tsa_data['date'],format='%m/%d/%Y')

    # Older data is abnormal because of covid. Only use most recent data
    tsa_data = tsa_data[tsa_data['date'] > '2021-09-01']

    # We need weekly average passengers due to market structure
    tsa_data['passengers_7_day_moving_average'] = tsa_data['passengers'].rolling(window=7).mean()

    plt.figure()
    ax = tsa_data.plot("date", "passengers_7_day_moving_average", legend=False, title="TSA traffic")

    # Highlight specific seasonal dips
    highlight_ranges = [(datetime(2022, 1, 3), datetime(2022, 2, 20)),
                        (datetime(2023, 1, 3), datetime(2023, 2, 20)),
                        (datetime(2024, 1, 3), datetime(2024, 2, 20))]

    for start, end in highlight_ranges:
        plt.axvspan(start, end, facecolor='yellow', alpha=0.5, hatch='/', edgecolor='red', linewidth=2)

    ax.set_ylabel("TSA passengers processed (millions)")

    plt.show()

def lag_passengers():
    """
    Load TSA passenger data, process it to create lagged features, and return the processed dataframe.

    Steps:
    1. Load TSA data from a CSV file.
    2. Rename columns for clarity.
    3. Convert the date column to datetime format.
    4. Set the date column as the index and sort the index.
    5. Create a new column with passenger data from the previous year.
    6. Filter data to include only dates after June 1, 2022.
    7. Calculate a 7-day moving average of the number of passengers.
    8. Calculate a 7-day moving average of the previous year's passenger data.
    """
    # Load TSA data
    tsa_data = pd.read_csv("../data/tsa_data.csv", index_col=0)

    # Rename columns for clarity
    tsa_data.rename(columns={"Date": "date", "Numbers": "passengers"}, inplace=True)

    # Convert date column to datetime format
    tsa_data['date'] = pd.to_datetime(tsa_data['date'], format='%m/%d/%Y')

    # Set the date column as the index and sort the index
    tsa_data = tsa_data.set_index('date')
    tsa_data.sort_index(inplace=True)

    # Create a new column with passenger data from the previous year
    tsa_data['previous_year'] = tsa_data['passengers'].shift(365)

    # Filter data to include only dates after June 1, 2022
    tsa_data = tsa_data[tsa_data.index > '2022-06-01']

    # Calculate a 7-day moving average of passengers
    tsa_data['passengers_7_day_moving_average'] = tsa_data['passengers'].rolling(window=7).mean()

    # Calculate a 7-day moving average of the previous year's passenger data
    tsa_data['passengers_7_day_moving_average_previous_year'] = tsa_data['previous_year'].rolling(window=7).mean()

    return tsa_data

def get_recent_trend(tsa_data):
    """
    Calculate recent trends in TSA passenger data and create predictions based on these trends.

    Steps:
    1. Calculate the current trend as the ratio of the 7-day moving average of passengers to the previous year's 7-day moving average.
    2. Create a lagged trend feature.
    3. Generate predictions using the previous year's 7-day moving average and the lagged trend.
    """
    # Calculate the current trend
    tsa_data['current_trend'] = tsa_data['passengers_7_day_moving_average'] / tsa_data[
        'passengers_7_day_moving_average_previous_year']

    # Create a lagged trend feature (Use 2 weeks ago in case data isn't available for previous week
    tsa_data['last_weeks_trend'] = tsa_data['current_trend'].shift(2)

    # Generate predictions using the previous year's 7-day moving average and the lagged trend
    tsa_data['prediction'] = tsa_data['passengers_7_day_moving_average_previous_year'] * tsa_data['last_weeks_trend']

    return tsa_data


def graph_lagged_data():
    """
    Load TSA passenger data, process it to create lagged features and predictions, and plot the results.

    Steps:
    1. Load and process the data to create lagged features.
    2. Calculate recent trends and generate predictions.
    3. Save the processed data to a new CSV file.
    4. Plot the 7-day moving average and the predictions.
    """
    # Load and process the data to create lagged features
    tsa_data = lag_passengers()

    # Calculate recent trends and generate predictions
    tsa_data = get_recent_trend(tsa_data)

    # Save the processed data to a new CSV file
    tsa_data.to_csv("../data/tsa_data_new.csv")

    # Print the first few rows of the dataframe
    print(tsa_data.head())

    # Plot the 7-day moving average and the predictions
    plt.figure(figsize=(12, 6))
    ax = tsa_data['passengers_7_day_moving_average'].plot(label="7-Day Moving Average",
                                                          title="TSA Traffic vs. Predictive Model")
    tsa_data['prediction'].plot(ax=ax, label="7-Day Moving Prediction")

    # Set the y-axis label
    ax.set_ylabel("TSA Passengers Processed (millions)")

    # Add legend
    ax.legend()

    # Show the plot
    plt.show()


def get_model_error():
    """
    Calculate the root mean squared error (RMSE) between the actual TSA passenger data and the model predictions.

    Steps:
    1. Load and process the data to create lagged features.
    2. Calculate recent trends and generate predictions.
    3. Drop rows with missing values.
    4. Calculate and print the RMSE.
    """
    # Load and process the data to create lagged features
    tsa_data = lag_passengers()

    # Calculate recent trends and generate predictions
    tsa_data = get_recent_trend(tsa_data)

    # Drop rows with missing values
    tsa_data.dropna(inplace=True)

    rms = root_mean_squared_error(
        tsa_data['passengers_7_day_moving_average'],
        tsa_data['prediction']
    )

    print(f"RMSE: {rms}")


plot_tsa_traffic()