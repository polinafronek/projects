import sys

def all_stocks(string):
    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
        }

    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
        }

    s = string.split(",")
    without_spaces = [x.strip() for x in s]
    lens = [len(x) for x in without_spaces]

    if 0 in without_spaces:
        sys.exit(1)
    else:
        for company in without_spaces:
            if company.capitalize() in COMPANIES.keys():
                print(f"{company.capitalize()} stock price is {STOCKS[COMPANIES[company.capitalize()]]}")
            elif company.upper() in STOCKS.keys():
                for key, value in COMPANIES.items():
                    if value == company.upper():
                        print(f"{value} is a ticker symbol for {key}")
                        break
            else:
                print(f"{company} is an unknown company or an unknown ticker symbol")

if __name__ == '__main__':
    if len(sys.argv) == 1 or len(sys.argv) > 2:
        sys.exit(1)
    else:
        all_stocks(sys.argv[1])




    

