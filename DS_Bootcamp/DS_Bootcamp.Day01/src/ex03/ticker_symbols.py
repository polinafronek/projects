import sys

def ticker():
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
    elif sys.argv[1].upper() not in COMPANIES.values():
        return "Unknown company"
    else:
        for key, value in COMPANIES.items():
            if value == sys.argv[1].upper():
                return key, STOCKS[sys.argv[1].upper()]

result = ticker()     
if __name__ == '__main__':
    if result == "Unknown company":
        print("Unknown company")
    else:
        print(*result)
