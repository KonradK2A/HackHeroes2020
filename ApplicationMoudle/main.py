"""
This script is a prototype main logic file that is reffered to the GUI prototype.
It manages the input, output and feedback that application gives.

When I was coding this me, my team leader and God knew what the heck is going here. But I forgot to make comments. So now only God knows.

Version: if I only knew...
Hours wasted here: not that many lol

Made with 💖 by:
Olha Babicheva and Konrad Kihan
ZSŁ GDAŃSK 2020
"""

import json
import os
from datetime import datetime
import calendar

# clear terminal
clear = lambda: os.system('cls')

# configuration file
CONFIG_FILE = "config.json"

class MoodInputManager:
    global moodFile
    moodFile = "mood.dat"
    """ user inputs their feelings that are converted to a dat file.
    Every feeling or action has unique number value and is stored in dat file.
    Data is being saved to external file that saves input over time."""
    def __init__(self):
        pass

    # gets date and time of action
    def dateTime(self):
        self.date = str(datetime.date(datetime.now()))  # YYYY-MM-DD
        self.time = datetime.now().strftime("%H:%M:%S") # HH:MM:SS
        # print(self.date, self.time)
        return [self.date, self.time]
    
    # gets info about user's mood devided to three levels (0/1/2) "bad", "ok", "good"
    # also checks events that caused selected mood
    def getMoodInfo(self, configFile = CONFIG_FILE):
        # loads list of possible actions
        try:
            with open(configFile, "r") as f:
                events = json.load(f)
                clear
                #print(list(events.values())[0][1])
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
        try:
            checkedEvents = input(">> ")
        except ValueError:
            # will be handled again later
            pass
        # append events list actions that happened on indexes 1 and above. 
        self.checkedEvents = checkedEvents.split()

        for event in self.checkedEvents:
            try:
                if self.checkedEvents.count(event) > 1:
                    self.checkedEvents.remove(event)
            except ValueError:
                self.checkedEvents.remove(event)
        self.checkedEvents.sort()


    #loads mood data to json file that stores the mood-events data
    def loadToFile(self, moodFile = moodFile):
        try:
            with open(moodFile, "a") as f:
                data = f"{self.date}|{self.time}|{self.moodValue}|{self.checkedEvents}\n"
                f.write(data)
            print("Success!")
        except UnboundLocalError as e:
            clear
            print(f"ERROR!\n{e}")


class UserNotesManager:
    userNotesFile = "notes.dat"
    # manages user's notes
    # gets time from MoodInputManager
    MoodInputManager = MoodInputManager()
    date = MoodInputManager.dateTime()[0]
    time = MoodInputManager.dateTime()[1]
    # print(date, time)
    def createNewNote(self, userNotesFile = userNotesFile, date=date, time=time):
        # note input
        clear
        with open(userNotesFile, "a") as f:
            numLines = len(open(userNotesFile, "r").readlines())
            print(numLines)

            title = input("Enter title: ")
            content = input("Enter new note: ")
            newNote = f"{numLines}|{date}|{time}|{title}|{content}\n"
            f.write(newNote)
            

    def readNotes(self, userNotesFile = userNotesFile):
        try:
            clear 
            with open(userNotesFile, "r") as f:
                notes = f.readlines()
                print("Choose one note from all below:")# \t\t\t\t\t\t\t Q to quit")
                for note in notes:
                    note = note.split(sep="|")
                    print(f"{note[0]}, {note[1]}, {note[2]}, {note[3]}")
                choice = input(">> ")
                for note in notes:
                    note = note.split(sep="|")
                    if str(note[0]) == choice:
                        print(f"{note[3]}\t{note[1]}, {note[2]}\n{note[-1]}\n")
                    else:
                        pass
                
                    

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


class StatsManager:
    """
    manages analitycs of mood levels input and stuff
    """
    def readMood(self, moodFile = moodFile):
        try:
            with open(moodFile, "r") as f:
                data = f.readlines()
        except FileNotFoundError:
            import time
            print(f"Error! File {moodFile} not found or is empty.")
                
        self.dateList = []
        for record in data:
            record = record.split(sep="|")
            
            for i in range(len(record)):
                record[2] = int(record[2])
            # conversion of this weird table (last element of record) to the legitimate list
            eventsValues = record[-1].strip('][').split(', ')

            
            for i in range(len(eventsValues)):
                eventsValues[i] = int(eventsValues[-1].strip("]\n").strip("'"))
            record[-1] = eventsValues
            # [ 'DATE YYYY-MM-DD', 'TIME HH-MM-SS', 'MOOOD_VALUE 0-2 INT', [EVENT LIST INT] ]
            self.record = record

            # creates sorted list of dates for chart generator
            self.dateList.append(self.record[0])
            print(self.dateList)

    def generateChart(self):
        # to generate chart
        import matplotlib.pyplot as plt
        # to convert dates
        import matplotlib.dates
        
        #converted_dates = list(map(datetime.strptime, self.datelist, len(self.dateList)*['%Y-%m-%d']))
        #x_axis = converted_dates

        
        plt.ylabel("Mood values")

class CalendarManager:
    global calendarFile
    calendarFile = "callendar.json"
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
        time.sleep(5)
        quit()

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
                
            termDate = input("\tDate [DD-MM-YYYY]: ")
            if termDate.strip() in forbiddenInput[-2:]:
                print("Quitting"); break
            else:
                try:
                    datetime.strptime(termDate.strip(), "%d-%m-%Y")
                except ValueError:
                    control +=10

            termTime = input("\tTime [HH:MM]: ")
            if termTime.strip() in forbiddenInput[-2:]:
                print("Quitting"); break
            else:
                try:
                    datetime.strptime(termTime.strip(), "%H:%M")
                except ValueError:
                    control +=100
            termDescription = input("\tDescription: ")
            print(control)
            if control > 0:
                continue
            else:
                break

        with open(calendarFile, "a") as f:
            newTerm = {
                "date": termDate,
                "time": termTime,
                "title": termTitle,
                "description": termDescription
            }
            json.dump(newTerm, f)
            f.close()
        
    def readSavedTerms(self):
        with open(calendarFile, "r") as f:
            x = json.loads(calendarFile)
            print(x["title"])


class MenuManager:
    pass
    def menu(self):
        print("===\tWelcome to the %APPNAME%!\t===\tv0.2\t===\n"
            "Set of actions:\n"
            "Vibe check\t1\n"
            "Notes\t\t2\n"
            "Statistics\t3\n"
            "Callendar\t4\n"
            "===\t===\t===\t===\n"
            "Quit\t\tQ\n")
        menuSelect = input(">> ")
    
        
        if menuSelect.lower() == "q":
            quit()
    
        elif menuSelect.lower() == "1":
            mim = MoodInputManager()
            mim.dateTime()
            mim.getMoodInfo()
            mim.loadToFile()
        
        elif menuSelect.lower() == "2":
            unm = UserNotesManager()
            choice = input("Do you want to create 'new' note or 'read' the old ones?\n>> ")
            if choice.lower() == "new":
                unm.createNewNote()
            elif choice.lower() == "read":
                unm.readNotes()

        elif menuSelect.lower() == "3":
            pass

        elif menuSelect.lower() == "4":
            cm = CalendarManager()
            choice = input("Do you want to create 'new' term or 'read' the old ones?\n>> ")
            
            if choice.lower() == "new":
                cm.addNewTerm()
            elif choice.lower() == "read":
                cm.readSavedTerms()



#TODO MoodInputManager - bugfixes and security (try-except)
#TODO generateChart - create chart
#TODO cosmetics like not ending app instantly and stuff

sm = StatsManager()
sm.readMood()
sm.generateChart()

# if __name__ == "__main__":
#     MM = MenuManager()
#     MM.menu()