import sys


def working_with_files(path):
    emails = []

    with open(path, "r", encoding="utf-8") as file_in:
        for line in file_in:
            emails.append(line)

    users = []
    for email in emails:
        email = email.replace(".", " ").replace("@", " ")
        email = email.split()
        users.append(email)

    with open("employees.tsv", "w", encoding="utf-8") as file_out:
        file_out.write("Name\tSurname\tE-mail\n")
        for i in range(len(users)):
            file_out.write(f"{users[i][0].capitalize()}\t{users[i][1].capitalize()}\t{emails[i]}")


def main():
    if len(sys.argv) <= 1 or len(sys.argv) > 2:
        sys.exit(1)

    path = sys.argv[1]

    working_with_files(path)

if __name__ == "__main__":
    main()
    



    