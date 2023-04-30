import argparse
import csv
import requests
import sys

from bs4 import BeautifulSoup

HEADERS = {
    "authority": "finance.yahoo.com",
    "method": "GET",
    "path": "/quote/AAPL/history?ltr=1",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-GB,en;q=0.9,hr-HR;q=0.8,hr;q=0.7,mk-MK;q=0.6,mk;q=0.5,en-US;q=0.4,bs;q=0.3,pl;q=0.2",
    "cache-control": "no-cache",
    "cookie": "thamba=2; GUC=AQABCAFkTCRkc0IhEwSu&s=AQAAAMkuOCn_&g=ZErciQ; A1=d=AQABBH_cSmQCEOdZp211zgVl57tO7LEBtecFEgABCAEkTGRzZO7ubmUBAiAAAAcIe9xKZIE-5i8&S=AQAAAgsJbnSqdzxaJUT1fT3Y42Y; A3=d=AQABBH_cSmQCEOdZp211zgVl57tO7LEBtecFEgABCAEkTGRzZO7ubmUBAiAAAAcIe9xKZIE-5i8&S=AQAAAgsJbnSqdzxaJUT1fT3Y42Y; thamba=1; maex=%7B%22v2%22%3A%7B%7D%7D; A1S=d=AQABBH_cSmQCEOdZp211zgVl57tO7LEBtecFEgABCAEkTGRzZO7ubmUBAiAAAAcIe9xKZIE-5i8&S=AQAAAgsJbnSqdzxaJUT1fT3Y42Y&j=GDPR; cmp=t=1682782015&j=1&u=1---&v=79; EuConsent=CPq4U4APq4U4AAOACKENDBCgAAAAAAAAACiQAAAAAABhoAMAAQSnEQAYAAglOKgAwABBKcA; PRF=t%3DAAPL%252BYHOO",
    "dnt": "1",
    "pragma": "no-cache",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
}
URL = 'https://finance.yahoo.com/quote/'


def write_to_csv(file, stock_data):
    with open(file, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file,
                                fieldnames=["Stock", "Date", "Open", "High", "Low Close", "Adj Close", "Volume"])
        writer.writeheader()

        for i in range(len(stock_data["Date"])):
            row = {
                "Stock": stock_data["Stock"][i],
                "Date": stock_data["Date"][i],
                "Open": stock_data["Open"][i],
                "High": stock_data["High"][i],
                "Low Close": stock_data["Low Close"][i],
                "Adj Close": stock_data["Adj Close"][i],
                "Volume": stock_data["Volume"][i]
            }
            writer.writerow(row)


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

    stock_data = {"Stock": [], "Date": [], "Open": [], "High": [], "Low Close": [], "Adj Close": [], "Volume": []}

    for stock in stocks:
        response = requests.get(URL + stock + "/history", headers=HEADERS)

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class': 'W(100%) M(0)'})
        table = table.tbody.find_all('tr')

        for tr in table:
            td_values = []
            for td in tr.find_all('td'):
                td_values.append(td.span.text)
            if len(td_values) < 6:
                continue # Some table rows have dividend information, e.g. May 06, 2022	0.23 Dividen
            stock_data["Stock"].append(stock)
            stock_data["Date"].append(td_values[0])
            stock_data["Open"].append(td_values[1])
            stock_data["High"].append(td_values[2])
            stock_data["Low Close"].append(td_values[3])
            stock_data["Adj Close"].append(td_values[4])
            stock_data["Volume"].append(td_values[5])

    write_to_csv(output_file, stock_data)
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieve stock data')
    parser.add_argument('stocks', type=str, nargs='+',
                        help='list of stock symbols')
    parser.add_argument('--days', type=int, default=30,
                        help='number of days of data to retrieve (default 30)')
    parser.add_argument('--time_interval', type=int, default=1,
                        help='time interval between data points in minutes (default 12)')
    args = parser.parse_args()

    scrape_stock_data(args.stocks, args.days, args.time_interval)
