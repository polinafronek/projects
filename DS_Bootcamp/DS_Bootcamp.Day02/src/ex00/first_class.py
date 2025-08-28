class Must_read:
    with open("data.csv", "r", encoding='utf-8') as file_in:
        for line in file_in:
            print(line, end="")

if __name__ == "__main__":
    Must_read()
