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
import time

# configuration file
CONFIG_FILE = "config.json"

# clear terminal
def clear():
    print("\n\n\n\n"*25)


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
                clear()
                #print(list(events.values())[0][1])
                events = list(events.values())[0]
        except FileNotFoundError as e:
            clear()
            print(f"Error! File {configFile} not found. Quitting application.")
            time.sleep(5)
            quit()

        # lets user enter the mood as key or word (any accepted)
        clear()
        moodTypes = {"Bad":0, "Ok":1, "Good":2}      
        self.moodValue = input(f"{moodTypes}\n"  
                          "Input your mood >>")

        # asks user what kind of action / event caused previously selected mood
        # also changes self.moodValue into integer (easier AI computing)
        try: 
            if self.moodValue.lower() == "bad" or self.moodValue == "0": self.moodValue = "-1"
            if self.moodValue.lower() == "ok" or self.moodValue == "1": self.moodValue = "0"
            if self.moodValue.lower() == "good" or self.moodValue == "2": self.moodValue = "1"
            if int(self.moodValue) > 2: print("error!"); return False
        except ValueError:
            pass

        if self.moodValue == "-1":
            for i in range(len(events[0])):
                print(f"{events[0][i]} - {i}")
        if self.moodValue == "0":
            for i in range(len(events[1])):
                print(f"{events[1][i]} - {i}")
        if self.moodValue == "1":
            for i in range(len(events[2])):
                print(f"{events[2][i]} - {i}")

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

    # reads stuff from history
    def historyRead(self, moodFile = moodFile, configFile=CONFIG_FILE):
        historyDate = input("What day do you want to check? YYYY-MM-DD\n>>")
        with open(moodFile, "r") as f:
            for i in f.readlines():
                if i.startswith(historyDate):
                    # set mood value as text to make output more user friendly
                   
                    i = i.split(sep="|")
                    eventsList = i[-1]
                    dateCheck = i[0]
                    

                    try:
                        with open(configFile, "r") as f:
                            events = json.load(f)

                            if i[2] == "-1": moodLst = list(events.values())[0][0]; mood = "bad"
                            if i[2] == "0": moodLst = list(events.values())[0][1]; mood = "ok-ish"
                            if i[2] == "1": moodLst = list(events.values())[0][2]; mood = "good"
                            
                            eventsList = eventsList.strip("['")
                            eventsList = eventsList.strip("']\n")
                            eventsList = eventsList.split(sep="', '")                     
                            try:
                                eventsHappened = []
                                for elem in eventsList:
                                    #print(moodLst[int(elem)])
                                    eventsHappened.append(moodLst[int(elem)])
                            except IndexError:
                                pass
                            
                            
                    except FileNotFoundError as e:
                        print("Configuration file not found! How did we get that far without it!")

                    eventsHappened = str(eventsHappened)
                    eventsHappened = eventsHappened.strip("[")
                    eventsHappened = eventsHappened.strip("]\n")

                    try:
                        print(f"At {historyDate} you had {mood} mood because of:\n{eventsHappened}")
                    except UnboundLocalError:
                        print("A little error ocured! Try again later!")
                    except NameError:
                        print("A little error ocured! Try again later!")
                else:
                    pass
            

        

            

    # loads mood data to json file that stores the mood-events data
    def loadToFile(self, moodFile = moodFile):
        try:
            with open(moodFile, "a") as f:
                try:
                    data = f"{self.date}|{self.time}|{self.moodValue}|{self.checkedEvents}\n"
                    f.write(data)
                    print("Success!")
                except AttributeError:
                    pass
            
        except UnboundLocalError as e:
            clear()
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
        clear()
        with open(userNotesFile, "a") as f:
            numLines = len(open(userNotesFile, "r").readlines())
            #print(numLines)

            title = input("Enter title: ")
            content = input("Enter new note: ")
            newNote = f"{numLines}|{date}|{time}|{title}|{content}\n"
            f.write(newNote)
            

    def readNotes(self, userNotesFile = userNotesFile):
        try:
            clear()
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
                input("\n\n\nPress ENTER key to continue")
                
                    

        except FileNotFoundError:
            print("Oops... You do not have any notes yet.")
        
    def makeChoice(self):
        clear()
        choice = input("Do you want to create 'new' note or 'read' the old one?\n>>")

        if choice.lower() == "new":
            clear()
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
            print(f"Error! File {moodFile} not found or is empty.")
                
        self.dateList = []
        self.moodList = []
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
            self.moodList.append(self.record[2])
        #print(self.moodList, len(self.moodList))
        #print(self.dateList, len(self.dateList))

    def generateChart(self):
        # to generate chart
        import matplotlib.pyplot as plt
        import matplotlib.dates as pld
        
        plt.plot(self.dateList, self.moodList)
        #TODO fix this non-integer Y values
        
        plt.ylabel("Mood values")
        plt.xlabel("Dates")
        plt.show()
        #converted_dates = list(map(datetime.strptime, self.datelist, len(self.dateList)*['%Y-%m-%d']))
        #x_axis = converted_dates
     

class CalendarManager:
    global calendarFile
    calendarFile = "calendar.dat"
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
            
            global date
            date = str(datetime.date(datetime.now()))  # YYYY-MM-DD
            # self.date[0:4], self.date[5:7] 
    except FileNotFoundError:
        print(f"Error! File {CONFIG_FILE} not found. Quitting application.")
        time.sleep(5)
        quit()

    def generateSimpleCalendar(self):
        clear()
        cal = calendar.TextCalendar()
        cal.setfirstweekday(firstWeekday)
        cal = cal.formatmonth(int(date[0:4]), int(date[5:7])) #YYYY , MM ;;;; Generates callendar based on current date
        print("\t",cal)


    def addNewTerm(self):
        forbiddenInput = ["", " ", "  ", "\t", "\n", "q", "Q"]
        print("Set info about new term... | Q to quit")
        while True:
            control = 0
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
                    pass #it's literally useless
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
                print("You made an error while creating a term.")
                if control == 1: print(f"Error at given title: {termTitle}. Try again")
                elif control == 10: print(f"Error at given date: {termDate}. Try again")
                elif control == 100: print(f"Error at given time: {termTime}. Try again")
                elif control != 1 and control != 10 and control != 100: print("Error in some parameters. Try again")
                continue
            else:
                with open(calendarFile, "a") as f:
                    numLines = len(open(calendarFile, "r").readlines())
                    #print(numLines)
                    f.write(f"{numLines}|{termDate}|{termTime}|{termTitle}|{termDescription}\n")
                    print("Success")
                    time.sleep(34)
                    
                break
        
        
    def readSavedTerms(self):
        with open(calendarFile, "r") as f:
            terms = f.readlines()
            print("Choose one note from all below:")# \t\t\t\t\t\t\t Q to quit")
            for term in terms:
                term = term.split(sep="|")
                print(f"{term[0]}, {term[1]}, {term[2]}")
            choice = input(">> ")
            for term in terms:
                term = term.split(sep="|")
                if str(term[0]) == choice:
                    print(f"{term[3]}\t{term[1]}, {term[2]}\n{term[-1]}\n")
                else:
                    pass

        input("\n\n\nPress ENTER key to continue")
                

class MenuManager:
    pass
    def menu(self):
        print("===\tWelcome to the %APPNAME%!\t===\tv0.3\t===\n"
            "Set of actions:\n"
            "Vibe check\t1\n"
            "Notes\t\t2\n"
            "Statistics\t3\n"
            "Callendar\t4\n"
            "Mood history\t5\n"
            "===\t===\t===\t===\n"
            "Quit\t\tQ\n")
        menuSelect = input(">> ")
    
        
        if menuSelect.lower().strip() == "q":
            quit()
    
        elif menuSelect.lower().strip() == "1":
            mim = MoodInputManager()
            mim.dateTime()
            mim.getMoodInfo()
            mim.loadToFile()
        
        elif menuSelect.lower().strip() == "2":
            unm = UserNotesManager()
            choice = input("Do you want to create 'new' note or 'read' the old ones?\n>> ")
            if choice.lower() == "new":
                unm.createNewNote()
            elif choice.lower() == "read":
                unm.readNotes()

        elif menuSelect.lower().strip() == "3":
            sm = StatsManager()
            sm.readMood()
            sm.generateChart()

        elif menuSelect.lower().strip() == "4":
            cm = CalendarManager()
            cm.generateSimpleCalendar()
            choice = input("Do you want to create 'new' term or 'read' the old ones?\n>> ")
            
            if choice.lower() == "new":
                cm.generateSimpleCalendar()
                cm.addNewTerm()
            elif choice.lower() == "read":
                cm.readSavedTerms()

        elif menuSelect.lower().strip() == "5":
            mim = MoodInputManager()
            mim.historyRead()

#TODO MoodInputManager - bugfixes and security (try-except)
#TODO cosmetics like not ending app instantly and stuff

if __name__ == "__main__":
    while True:
        clear()
        MM = MenuManager()
        MM.menu()
