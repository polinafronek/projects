import sys

def sending_letter(email):
    with open("employees.tsv", "r", encoding="utf-8") as f:
        lines = f.readlines()

        for line in lines[1:]:
            line = line.strip().split("\t")
            if line[2] == email:
                print(f"Dear {line[0]}, welcome to our team. We are sure that it will be a pleasure to work with you. That’s a precondition for the professionals that our company hires.")

def main():
    if len(sys.argv) <= 1 or len(sys.argv) > 2:
        sys.exit(1)

    email = sys.argv[1]

    sending_letter(email)

if __name__ == "__main__":
    main()

