"""
This script is a prototype main logic file that is reffered to the GUI prototype.
It manages the input, output and feedback that application gives.
"""

import json

class DataInputManager:
    """ user inputs their feelings that are converted to a json file.
    Every feeling or action has unique number value and is stored in json file.
    Data is being saved to external file that saves input over time.

    Json data slice structure:
    {
        'date': '<DATE OF ADDITION>',
        'time': '<TIME OF ADDITION>',
        'moodValue': '<VALUE>',
        'events':[
            '<TYPE BAD | OK | GOOD>': '<VALUE>',
            '<TYPE BAD | OK | GOOD>': '<VALUE>',
            ...
            '<TYPE BAD | OK | GOOD>': '<VALUE>',
        ],
    }
    """
    def __init__(self):
        pass

    def dateTime(self):
        from datetime import datetime
        self.date = str(datetime.date(datetime.now()))  # YYYY-MM-DD
        self.time = datetime.now().strftime("%H:%M:%S") # HH:MM:SS
        print(self.date, self.time)
    

    def getMoodInfo(self, configFile = "config.json"):
        try:
            with open(configFile, "r") as f:
                self.events = json.load(f)
                print(list(self.events.values()))
        except FileNotFoundError as e: 
            print(f"File {configFile} not found. Quitting application.")
            import time
            time.sleep(5)
            quit()

        self.moodTypes = {"Bad":0, "Ok":1, "Good":2}      
        self.moodValue = input(f"{self.moodTypes}"
                          "Input your mood > ")

        if self.moodValue == "0" or self.moodValue.lower() == "bad":
            pass
        elif self.moodValue == "1" or self.moodValue.lower() == "ok":
            pass
        elif self.moodValue == "2" or self.moodValue.lower() == "good":
            pass
        
    
    
    def loadToJSON(self):
        try:
            data = {
                "date": self.date,
                "time": self.time,
                "moodValue": self.moodValue
                
            }
        except UnboundLocalError as e:
            print(f"ERROR!\n{e}")
                
        
"""g = DataInputManager()
g.getMoodInfo()
g.dateTime()"""
