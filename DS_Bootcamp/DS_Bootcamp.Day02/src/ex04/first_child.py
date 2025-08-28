import sys

from random import randint

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

        def __init__(self, research):
            self.research = research
            self.eagle = 0
            self.tails = 0

        def counts(self):
            for i in range(len(self.research)):
                self.eagle += self.research[i][0]
                self.tails += self.research[i][1]

            return self.eagle, self.tails
        
        def Fractions(self):
            summ = self.eagle + self.tails
            if summ == 0:
                return 0.0, 0.0
            percent_eagle = 100 * self.eagle / summ
            percent_tails = 100 * self.tails / summ

            return percent_eagle, percent_tails
        
class Analytics(Research.Calculations):

    def __init__(self, research):
        self.research = research        
        
    def predict_random(self):
        predictions = []
        
        for i in range(3):
            x = randint(0, 1)
            predictions.append([x, 1 - x])

        return predictions

    def predict_last(self):
        lines = self.research
        return lines[-1]
   
def main():
    if len(sys.argv) != 2:
        print("Incorrect arguments")
        sys.exit(1)
    
    research = Research(sys.argv[1])
    data = research.file_reader()

    if not data:
        sys.exit(1)
        
    print(research.file_reader())

    calculate = Research.Calculations(data)
    print(*calculate.counts())
    print(*calculate.Fractions())

    predictions = Analytics(data)
    print(predictions.predict_random())
    print(predictions.predict_last())

if __name__ == "__main__":
    main()