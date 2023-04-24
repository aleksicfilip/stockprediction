import argparse
import csv
import requests
import sys

from bs4 import BeautifulSoup


def scrape_stock_data(stocks, days=30, time_interval=12, output_file='data.csv'):
    """
    Scrape stock data for the given list of stocks.

    Args:
        stocks (list): A list of strings of stock symbols to retrieve data for.
        days (int): The number of days of data to retrieve (default 30).
        time_interval (int): The time interval between data points in hours (default 12; twice a day).
        output_file (string): The name of the file in which the scraped data will be saved (default data.csv)

    Returns:
        bool: If the scraping was successful
    """

    # TODO code to retrieve stock data goes here
    stock_data = {}

    # Saving the data as a CSV file
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for date, data in stock_data.items():
            writer.writerow({'Date': date, 'Open': data['Open'], 'High': data['High'],
                             'Low': data['Low'], 'Close': data['Close'], 'Volume': data['Volume']})
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieve stock data')
    parser.add_argument('stocks', type=str, nargs='+',
                        help='list of stock symbols')
    parser.add_argument('--days', type=int, default=30,
                        help='number of days of data to retrieve (default 30)')
    parser.add_argument('--time_interval', type=int, default=1,
                        help='time interval between data points in minutes (default 1)')
    args = parser.parse_args()

    scrape_stock_data(args.stocks, args.days, args.time_interval)
