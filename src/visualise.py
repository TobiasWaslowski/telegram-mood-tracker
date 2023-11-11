import calendar
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from pymongo import MongoClient


def visualize_monthly_data(year: str = None, month: str = None):
    # Connect to MongoDB (replace with your connection details)
    client = MongoClient("mongodb://localhost:27017/")
    db = client.records
    collection = db.records

    if year is None or month is None:
        now = datetime.now()
        year = now.year
        month = now.month

    # Calculate the first and last day of the given month
    first_day = datetime(year, month, 1)
    last_day = datetime(year, month, calendar.monthrange(year, month)[1])

    # Filter records for the specified month
    query = {"timestamp": {"$gte": first_day.strftime('%Y-%m-%dT%H:%M:%S'),
                           "$lte": last_day.strftime('%Y-%m-%dT%H:%M:%S')}}

    # Retrieve data
    data = list(collection.find(query))

    # Process data
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.date
    df[['mood', 'sleep']] = df[['mood', 'sleep']].astype(float)

    # Calculate daily averages
    daily_avg = df.groupby('timestamp')[['mood', 'sleep']].mean().reset_index()

    plt.style.use("seaborn-v0_8-dark")

    # Plotting
    plt.figure(figsize=(10, 6))

    # Creating two y-axes
    # Creating two y-axes
    ax1 = plt.gca()
    ax2 = ax1.twinx()

    # Mood plot on ax1
    ax1.plot(daily_avg['timestamp'], daily_avg['mood'], marker='o', color='blue', label='Mood', markersize=4,
             linestyle='-')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Mood', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_ylim(-5, 5)

    # Sleep plot on ax2
    ax2.plot(daily_avg['timestamp'], daily_avg['sleep'], marker='o', color='green', label='Sleep', markersize=4,
             linestyle='--')
    ax2.set_ylabel('Sleep', color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    # Title and layout
    plt.title(f'Average Mood and Sleep for {month}/{year}')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot
    plt.savefig(f'mood_sleep_{year}_{month}.jpg', format='jpg', dpi=300)


if __name__ == '__main__':
    visualize_monthly_data()