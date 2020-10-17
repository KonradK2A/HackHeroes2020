"""
This script is a prototype main logic file that is reffered to the GUI prototype.
It manages the input, output and feedback that application gives.
"""

import json
import os
from datetime import datetime

# clear terminal
clear = lambda: os.system('cls')

# configuration file
CONFIG_FILE = "config.json"

class DataInputManager:
    """ user inputs their feelings that are converted to a json file.
    Every feeling or action has unique number value and is stored in json file.
    Data is being saved to external file that saves input over time.

    Json data slice structure:
    {
        'date': '<DATE OF ADDITION>',
        'time': '<TIME OF ADDITION>',
        'moodValue': '<VALUE>
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

    # gets date and time of action
    def dateTime(self):
        self.date = str(datetime.date(datetime.now()))  # YYYY-MM-DD
        self.time = datetime.now().strftime("%H:%M:%S") # HH:MM:SS
        # print(self.date, self.time)
        return [self.date, self.time]
    
    # gets info about user's mood devided to three levels (0/1/2) "bad", "ok", "good"
    # also checks wevents caused selected mood
    def getMoodInfo(self, configFile = CONFIG_FILE):
        # loads list of possible actions
        try:
            with open(configFile, "r") as f:
                events = json.load(f)
                clear
                print(list(events.values())[0][1])
                events = list(events.values())[0]
        except FileNotFoundError as e:
            clear
            print(f"Error! File {configFile} not found. Quitting application.")
            import time
            time.sleep(5)
            quit()

        # lets user enter the mood as key or word (any accepted)
        clear
        moodTypes = {"Bad":0, "Ok":1, "Good":2}      
        self.moodValue = input(f"{moodTypes}\n"
                          "Input your mood >>")

        # asks user what kind of action / event caused previously selected mood
        # also changes self.moodValue into integer (easier AI computing)
        if self.moodValue.lower() == "bad": self.moodValue = "0"
        if self.moodValue.lower() == "ok": self.moodValue = "1"
        if self.moodValue.lower() == "good": self.moodValue = "2"

        if self.moodValue == "0":
            for i in range(len(events[0])):
                print(f"{events[0][i]} - {i}")
        if self.moodValue == "1":
            for i in range(len(events[1])):
                print(f"{events[1][i]} - {i}")
        if self.moodValue == "2":
            for i in range(len(events[2])):
                print(f"{events[2][i]} - {i}")


        clear
        print("What happened? (use spacebar as a separator)")
        # actual input
        checkedEvents = input(">> ")
        # append events list actions that happened on indexes 1 and above. 
        self.checkedEvents = checkedEvents.split()

    #loads mood data to json file that stores the mood-events data
    def loadToJSON(self):
        try:
            data = {
                "date": self.date,
                "time": self.time,
                "moodValue": self.moodValue,
                "events": self.checkedEvents                
            }
            print(data)
        except UnboundLocalError as e:
            clear
            print(f"ERROR!\n{e}")


class UserNotesManager:
    # manages user's notes
    # gets time from DataInputManager
    DataInputManager = DataInputManager()
    date = DataInputManager.dateTime()[0]
    time = DataInputManager.dateTime()[1]
    # print(date, time)
    def createNewNote(self, userNotesFile = "usernotes.json", date=date, time=time):
        # note input
        clear
        with open(userNotesFile, "a") as f:
            title = input("Enter title: ")
            content = input("Enter new note: ")
            newNote = {
                "date": date,
                "time": time,
                "title": title,
                "content": content
            }
            json.dump(newNote, f)
            f.close()

    def readNotes(self, userNotesFile = "usernotes.json"):
        try:
            clear 
            with open(userNotesFile, "r") as f:
                data = json.load(f)
                for post in data["title"]:
                    print(f"Title: {post['title']}")
                    print(f"Time: {post['date']}|{post['time']} ")
        except FileNotFoundError:
            print("Oops... You do not have any notes yet.")
        
    def makeChoice(self):
        clear
        choice = input("Do you want to create 'new' note or 'read' the old one?\n>>")

        if choice.lower() == "new":
            clear
            createNewNote()
        elif choice.lower() == "read":
            readNotes()

        
class FunnyGenerator:
    """
    function generates wholesome or funny content if user asks for it
    """
    pass

class StatsManager:
    """
    manages analitycs of mood levels input and stuff
    """
    pass

import calendar
class CallendarManager:
    def __init__(self):
        pass
    """
    manages calendar (idk how to do it)
    """
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            global firstWeekday
            firstWeekday = int(data["weekday"])
            f.close()
            
            global date
            date = str(datetime.date(datetime.now()))  # YYYY-MM-DD
            # self.date[0:4], self.date[5:7] 
    except FileNotFoundError:
        import time
        print(f"Error! File {CONFIG_FILE} not found. Quitting application.")
        #time.sleep(5)
        #quit()

    def generateSimpleCalendar(self):
        cal = calendar.TextCalendar()
        cal.setfirstweekday(firstWeekday)
        cal.formatmonth(int(date[0:4]), int(date[5:7])) #YYYY , MM ;;;; Generates callendar based on current date

    def addNewTerm(self):
        forbiddenInput = ["", " ", "  ", "\t", "\n", "q", "Q"]
        control = 0
        clear
        print("Set info about new term... | Q to quit")
        while True:
            termTitle = input("\tTitle: ")
            if termTitle.strip() in forbiddenInput[:-2]:
                control +=1
            elif termTitle.strip() in forbiddenInput[-2:]:
                print("Quitting"); break
                
            termDate = input("\tDate [YYYY-MM-DD]: ")
            if termDate.strip() in forbiddenInput[-2:]:
                print("Quitting"); break
            else:
                try:
                    datetime.datetime.striptime(termDate.strip(), "%Y-%m-d")
                except ValueError:
                    control +=10

            termTime = input("\tTime [HH:MM]: ")
            if termTime.strip() in forbiddenInput[-2:]:
                print("Quitting"); break
            else:
                try:
                    datetime.datetime.striptime(termTime.strip(), "%H:%M")
                except ValueError:
                    control +=100
            termDescription = input("\tDescription: ")
            
            if control > 0:
                continue
            else:
                break

#TODO DataInputManager.getMoodInfo() - lines 62, 67, 73 only two out of <A LOT> values printed
#TODO DataInputManager - bugfixes and security (try-except)
#TODO config.json not found

#UNM = UserNotesManager()
#UNM.makeChoice()
#UNM.readNotes()

# DIM = DataInputManager()
# DIM.dateTime()
# DIM.getMoodInfo()
# DIM.loadToJSON()

#CM = CallendarManager()
#CM.generateSimpleCalendar()
#CM.addNewTerm()