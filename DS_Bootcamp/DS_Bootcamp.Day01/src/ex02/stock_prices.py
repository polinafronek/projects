import sys

def prices():
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

    if len(sys.argv) == 1 or len(sys.argv) > 2:
        sys.exit(1)
    elif sys.argv[1].capitalize() not in COMPANIES.keys():
        return "Unknown company"
    else:
        return STOCKS[COMPANIES[sys.argv[1].capitalize()]]

print(prices())
