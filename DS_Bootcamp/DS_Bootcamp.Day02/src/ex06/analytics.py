from random import randint
import logging

logging.basicConfig(level=logging.INFO, filename="analytics.log", filemode="w", 
                    format="%(asctime)s %(message)s")

class Analytics():

    def __init__(self, num_of_steps):
        self.num_of_steps = num_of_steps
        self.predictions = []
        self.eagles = 0
        self.tails = 0
        
    def predict_random(self):        
        for i in range(self.num_of_steps):
            x = randint(0, 1)
            self.predictions.append([x, 1 - x])
        
        logging.info("Creating array woth predictions")
        return self.predictions
    
    def account_prediction(self):
        for predict in self.predictions:
            self.eagles += predict[0]
            self.tails += predict[1]

        logging.info("Counting eagles and tails from array with predictions")  
        return self.eagles, self.tails
    
    def save_file(self, data, name_of_file, expansion):
        self.data = data
        self.name_of_file = name_of_file
        self.expansion = expansion
        file = name_of_file + "." + expansion

        with open(file, "w", encoding="utf-8") as file_in:
            file_in.writelines(self.data)

        logging.info("Reading data from a file")

    


        


