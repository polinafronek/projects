import sys 

clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
'elon@paypal.com', 'jessica@gmail.com']

participants = ['walter@heisenberg.com', 'vasily@mail.ru',
'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']

recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']

def call_center():
    return list(set(clients) - set(recipients))

def potential_clients():
    return list(set(participants) - set(clients))

def loly_program():
    return list(set(clients) - set(participants))

def main():
    if len(sys.argv) <= 1 or len(sys.argv) > 2:
        sys.exit(1)
    else:
        input = sys.argv[1]
        if input != "call_center" and input != "potential_clients" and input != "loly_program":
            sys.exit(1)

    if input == "call_center":
        print(call_center())
    elif input == "potential_clients":
        print(potential_clients())
    else:
        print(loly_program())
        
    
if __name__ == "__main__":
    main()