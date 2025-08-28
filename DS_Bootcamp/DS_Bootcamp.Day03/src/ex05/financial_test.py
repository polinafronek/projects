import requests
from bs4 import BeautifulSoup
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
        return True
    except ValueError:
        raise NonExistentParam("Invalid URL format")
    
def test_check_url_1():
    try:
        is_valid_url("https://finance..com/quote/PLTR/financials/")
    except NonExistentParam as e:
        assert str(e) == "Invalid URL format"
        
def test_check_url_2():
    assert is_valid_url("https://finance.yahoo.com/quote/PLTR/financials/") is True

def test_check_url_3():
    assert is_valid_url("https://finance.yahoo.com/quote/CRWV/financials/") is True

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
        return f"ERROR: {e}"
    
def test_parser_1():
    assert parser("CRWD", "Cost of Revenue") == ['Cost', 'of', 'Revenue', '991,481', '991,481', '755,723', '601,231', '383,221']

def test_parser_2():
    assert parser("school_21", "Cost of Revenue") == "ERROR: Column doesn't exist"

def test_parser_3():
    assert isinstance(parser("MSFT", "Total Revenue"), list)

def test_parser_4():
    res = parser("MSFT", "Total Revenue")
    assert res[:2] == ["Total", "Revenue"]

def test_parser_5():
    assert parser("CRW", "Cost of Revenue") == "ERROR: Column doesn't exist"

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
        
        return tuple(result)

def test_data_processing_1():
    func = data_processing(['Cost', 'of', 'Revenue', '991,481', '991,481', '755,723', '601,231', '383,221'])
    assert isinstance(func, tuple)

def test_data_processing_2():
    func = data_processing(['Total', 'Revenue', '270,010,000', '245,122,000', '211,915,000', '198,270,000', '168,088,000'])
    assert func == ('Total Revenue', '270,010,000', '245,122,000', '211,915,000', '198,270,000', '168,088,000')

def test_data_processing_3():
    func = data_processing(['Basic', 'Average', 'Shares', '2,283,946.50', '2,250,163', '2,147,446', '2,063,793', '1,923,617'])
    assert func == ('Basic Average Shares', '2,283,946.50', '2,250,163', '2,147,446', '2,063,793', '1,923,617')

def main():
    if len(sys.argv) != 3:
        sys.exit(1)
    
    ticker = sys.argv[1]
    column = sys.argv[2]
    res = parser(ticker, column)
    if isinstance(res, list):
        print(data_processing(res))
    else:
        print(res)

if __name__ == "__main__":
    main()

