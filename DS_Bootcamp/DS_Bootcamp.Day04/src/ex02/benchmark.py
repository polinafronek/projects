import timeit
import sys

def loop():
    emails = ["john@gmail.com", "james@gmail.com", "alice@yahoo.com", "anna@live.com", "philipp@gmail.com"]*5
    gmail_emails = []
    for email in emails:
        email_split = email.split("@")
        if email_split[1] == "gmail.com":
            gmail_emails.append(email)
    return gmail_emails

def list_func():
    emails = ["john@gmail.com", "james@gmail.com", "alice@yahoo.com", "anna@live.com", "philipp@gmail.com"] * 5
    gmail_emails = [email for email in emails if email.split("@")[1] == "gmail.com"]
    return gmail_emails

    
def map_func():
    emails = ["john@gmail.com", "james@gmail.com", "alice@yahoo.com", "anna@live.com", "philipp@gmail.com"] * 5
    gmail_emails = [email for email in map(lambda x: x if x.split("@")[1] == "gmail.com" else None, emails) if email is not None]
    return gmail_emails

def filter_func():
    emails = ["john@gmail.com", "james@gmail.com", "alice@yahoo.com", "anna@live.com", "philipp@gmail.com"] * 5
    gmail_emails = list(filter(lambda x: x.split("@")[1] == "gmail.com", emails))
    return gmail_emails
    
def main():
    if len(sys.argv) != 3:
        sys.exit()

    request = sys.argv[1]
    numbers = int(sys.argv[2])

    if request == "loop":
        print(timeit.timeit(loop, number=numbers))
    elif request == "list_comprehension":
        print(timeit.timeit(list_func, number=numbers))
    elif request == "map":
        print(timeit.timeit(map_func, number=numbers))
    elif request == "filter":
        print(timeit.timeit(filter_func, number=numbers))
    else:
        sys.exit()

if __name__ == "__main__":
    main()


    