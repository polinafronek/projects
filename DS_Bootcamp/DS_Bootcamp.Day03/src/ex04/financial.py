import requests
from bs4 import BeautifulSoup
import time
import sys
from urllib.parse import urlparse
from requests.exceptions import RequestException

class NonExistentParam(Exception):
    pass

def is_valid_url(url):
    try:
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError
        if ".." in parsed_url.netloc:
            raise ValueError
    except ValueError:
        raise NonExistentParam("Invalid URL format")

def check_column():
    raise NonExistentParam("Column doesn't exist")

def parser(ticker, column):
    try:
        url = f"https://finance.yahoo.com/quote/{ticker.upper()}/financials/?p={ticker.lower()}"
        headers = {
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        is_valid_url(url)
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
                
            tables = soup.find_all('div', class_='tableBody')
            for table in tables:
                rows = table.find_all('div', class_='row')
                for row in rows:
                    if row.find(title=column) is not None:
                        res = row.text.split()
                        return res
            else:
                check_column()
        except RequestException as e:
            return f"ERROR: Failed to fetch URL"
    
    except NonExistentParam as e:
        return f"ERROR {e}"

def data_processing(res):
        title_array = []
        digits = []
        for value in res:
            if value.isalpha():
                title_array.append(value)
            else:
                digits.append(value)
        
        title = " ".join(title_array)
        result = [title]

        for digit in digits:
            result.append(digit)
        
        print(tuple(result))

def main():
    if len(sys.argv) != 3:
        sys.exit(1)
    
    ticker = sys.argv[1]
    column = sys.argv[2]
    res = parser(ticker, column)
    if isinstance(res, list):
        data_processing(res)
    else:
        print(res)

if __name__ == "__main__":
    main()

