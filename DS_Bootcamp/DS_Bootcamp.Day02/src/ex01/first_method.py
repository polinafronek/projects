class Research:

    def file_reader(self):
        with open("data.csv", "r", encoding='utf-8') as file_in:
            return file_in.readlines()
        
if __name__ == "__main__":
    f = Research()
    for line in f.file_reader():
        print(line, end="")

