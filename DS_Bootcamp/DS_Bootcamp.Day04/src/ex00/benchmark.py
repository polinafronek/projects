import timeit

def ineffective():
    emails = ["john@gmail.com", "james@gmail.com", "alice@yahoo.com", "anna@live.com", "philipp@gmail.com"]*5
    gmail_emails = []
    for email in emails:
        email_split = email.split("@")
        if email_split[1] == "gmail.com":
            gmail_emails.append(email)
    return gmail_emails

def effective():
    emails = ["john@gmail.com", "james@gmail.com", "alice@yahoo.com", "anna@live.com", "philipp@gmail.com"] * 5
    gmail_emails = [email for email in emails if email.split("@")[1] == "gmail.com"]
    return gmail_emails

def main():
    time_ineffective = timeit.timeit(ineffective, number=90000000)
    time_effective = timeit.timeit(effective, number=90000000)
    if time_effective < time_ineffective:
        print("it is better to use a list comprehension")
        print(f"{time_effective} vs {time_ineffective}")
    else:
        print("it is better to use a usual method")
        print(f"{time_ineffective} vs {time_effective}")
        
if __name__ == "__main__":
    main()


    