from config import num_of_steps, report, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID 
from analytics import Analytics, logging
import requests
import json

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

                logging.info("Reading correct data from a list")
                return lines
            
            except FileStructError as e:
                logging.error(e)
                print(f"ERROR: {e}")

            except FileNotFoundError as e:
                logging.error("File not found")
                print("File not found")

    def Telegram(self, success=True):

        try:
            if success == True:
                message = "Отчет успешно создан"
            else:
                message = "Отчет не создан из-за ошибки"

            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                
            payload = {
                "chat_id": TELEGRAM_CHAT_ID, 
                "text": message
            }

            headers = {'Content-Type': 'application/json'}

            response = requests.post(url, data=json.dumps(payload), headers=headers)

        except Exception as e:
            logging.error(f"Failed to send Telegram message: {e}")

    class Calculations: 

        def __init__(self, research):
            self.research = research
            self.eagle = 0
            self.tails = 0

        def counts(self):
            for i in range(len(self.research)):
                self.eagle += self.research[i][0]
                self.tails += self.research[i][1]

            logging.info("Counting eagles and tails")    
            return self.eagle, self.tails
        
        def Fractions(self):
            summ = self.eagle + self.tails
            if summ == 0:
                return 0.0, 0.0
            percent_eagle = 100 * self.eagle / summ
            percent_tails = 100 * self.tails / summ

            logging.info("Counting percent of egles and percent of tails")
            return percent_eagle, percent_tails

        
def main():      
    research = Research("data.csv")
    try:
        data = research.file_reader()
        if not data:
            research.Telegram(success=False)
        else:
            research.Telegram()

        number_of_observations = len(data)
        calculate = Research.Calculations(data)
        eagles, tails = calculate.counts()
        percent_eagle, percent_tails = calculate.Fractions()
        round_percent_eagle, round_percent_tails = round(percent_eagle, 2), round(percent_tails, 2)
        analytic_class = Analytics(num_of_steps)
        analytic_class.predict_random()
        predict_eagles, predict_tails = analytic_class.account_prediction()

        
        Report = report.format(
            number_of_observations=number_of_observations,
            eagles=eagles,
            tails=tails,
            round_percent_eagle=round_percent_eagle,
            round_percent_tails=round_percent_tails,
            num_of_steps=num_of_steps,
            predict_eagles=predict_eagles,
            predict_tails=predict_tails
        )
        logging.info("Fiiling out the template")

        analytic_class.save_file(Report, "report", "txt")
        logging.info("Saving report to a file")

    except Exception:
        logging.error("Couldn't make a report")



if __name__ == "__main__":
    main()