import urllib3
from bs4 import BeautifulSoup
import sys
import cProfile
import pstats 

class NonExistentParam(Exception):
    pass

def check_url(response):
    errors = ["400", "401", "403", "404", "405", "408", "429", "500", "502", "503", "504", "520"]
    if response.status in errors:
        raise NonExistentParam("URL doesn't exist or is unavailable")

def check_column():
    raise NonExistentParam("Column doesn't exist")

def parser(ticker, column):
    try:
        url = f"https://finance.yahoo.com/quote/{ticker.upper()}/financials/?p={ticker.lower()}"
        headers = {
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        http = urllib3.PoolManager()
        resp = http.request("GET", url, headers=headers)
        response = resp.data
   
        check_url(resp)
        soup = BeautifulSoup(response, "html.parser")
            
        tables = soup.find_all('div', class_='tableBody')
        for table in tables:
            rows = table.find_all('div', class_='row')
            for row in rows:
                if row.find(title=column) is not None:
                    res = row.text.split()
                    return res
        else:
            check_column()
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
    profile = cProfile.Profile()
    profile.enable()
    ticker = sys.argv[1]
    column = sys.argv[2]
    res = parser(ticker, column)

    if isinstance(res, list):
        data_processing(res)
    else:
        print(res)
    profile.disable()

    stats = pstats.Stats(profile)
    stats.sort_stats("cumtime")

    with open("pstats-cumulative.txt", "w") as f:
        stats.stream = f
        stats.print_stats()

    
if __name__ == "__main__":
    main()


