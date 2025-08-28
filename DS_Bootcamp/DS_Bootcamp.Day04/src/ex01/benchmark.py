import timeit

def loop():
    emails = ["john@gmail.com", "james@gmail.com", "alice@yahoo.com", "anna@live.com", "philipp@gmail.com"] * 5
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
    
def main():
    print(map_func())
    print(list_func())
    print(loop())
    time_loop = timeit.timeit(loop, number=90000000)
    time_list = timeit.timeit(list_func, number=90000000)
    time_map = timeit.timeit(map_func, number=90000000)
    print("it is better to use a map")
    print(f"{time_map} vs {time_list} vs {time_loop}")

if __name__ == "__main__":
    main()


    