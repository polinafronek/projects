import sys
import os


class FileStructError(Exception):
    pass

def checking_file(lines):
    if len(lines) == 0:
        raise FileStructError("File is empty")
    
    headers = lines[0].strip().split(",")
    if len(headers) != 2 or any(header.isalpha() == False for header in headers):
        raise FileStructError("Incorrect headers")
    
    if not all(line.count(",") == 1 for line in lines) and not all(line[1].strip() == "," for line in lines[1:]):
        raise FileStructError("Wrong separator or incorrect amount of data")
    
    lines = [lines[i].strip().split(",") for i in range(len(lines))] 
    if all(len(lines[i]) == 2 for i in range(len(lines))):
        count = 0
        for x, y in lines[1:]:
            if (x == "0" or x == "1") and (y == "0" or y == "1") and x != y:
                count += 1
        if count == len(lines[1:]):
            return True
        else:
            raise FileStructError("Incorrect values")
    else:
        raise FileStructError("Incorrect number of parameters")


class Research:
    def __init__(self, file):
            self.file = file

     
    def file_reader(self):
        try:
            lines = []
            with open(self.file, "r", encoding="utf-8") as file_in:
                lines = file_in.readlines()
            checking_file(lines)
            return lines
                
        except FileStructError as e:
            print(f"ERROR: {e}")

        except FileNotFoundError:
            print("File not found")

def main():
    if len(sys.argv) != 2 or not os.path.exists(sys.argv[1]):
        print("Incorrect arguments")
        sys.exit(1)
    
    f = Research(sys.argv[1])
    if f.file_reader():
        for line in f.file_reader():
            print(line, end="")
    
if __name__ == "__main__":
    main()