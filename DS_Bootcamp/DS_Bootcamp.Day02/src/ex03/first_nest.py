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
    lines = [[value.strip() for value in line] for line in lines]
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
    def __init__(self, file, has_header=True):
            self.file = file
            self.has_header = has_header

    def file_reader(self):
            try:
                lines = []
                with open(self.file, "r", encoding="utf-8") as file_in:  
                    lines = file_in.readlines()

                checking_file(lines)

                if self.has_header == True:
                    lines = lines[1:]
                    
                for i in range(len(lines)):
                    lines[i] = list(map(int, lines[i].strip().split(",")))

                return lines
            
            except FileStructError as e:
                print(f"ERROR: {e}")

            except FileNotFoundError:
                print("File not found")

    class Calculations:
        @staticmethod    
        def counts(data):
            if not data:
                return (0, 0)
            for i in range(len(data)):
                eagle = sum(line[0] for line in data)
                tails = sum(line[1] for line in data)

            return eagle, tails
        
        @staticmethod
        def Fractions(eagles, tails):
            summ = eagles + tails
            if summ == 0:
                return 0.0, 0.0
            percent_eagle = 100 * eagles / summ
            percent_tails = 100 * tails / summ

            return percent_eagle, percent_tails
        
def main():
    if len(sys.argv) != 2 or not os.path.exists(sys.argv[1]):
        print("Incorrect arguments")
        sys.exit(1)
    
    research = Research(sys.argv[1])
    data = research.file_reader()

    if not data:
        sys.exit(1)
        
    print(research.file_reader())

    eagles, tails = Research.Calculations.counts(data)
    eagles_percent, tails_percent = Research.Calculations.Fractions(eagles, tails)

    print(eagles, tails)
    print(eagles_percent, tails_percent)

if __name__ == "__main__":
    main()

            

    
            
             
            


        
