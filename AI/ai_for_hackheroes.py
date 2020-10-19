import pandas as pd
data = pd.DataFrame({'Date': ['2020-10-17', '2020-10-18'], 'Time': ['12:30', '11:10'], 'Events': [['cofee', 'friends', 'shopping', 'bad_exam'], ["bad_exam", "unexpected_test", "medical_problems"]]})
l = []
def countMood():
    mood = 0
    g = ["cofee", "friends", "shopping", "party", "good_grade", "got_a_gift", "ate_good_food", "fun_activity", "did_sport", "date", "rested_well", "did_good_at_work"]
    b = ["bad_exam", "unexpected_test", "medical_problems", "hunger", "pain", "fail", "argument", "breakup", "bad_weather", "money_loss", "no_sleep"]
    for i in data['Events']:
        for j in i:
            if j in g:
                mood +=1
            if j in b:
                mood -= 1
        l.append(mood)
    data['MoodOfDay'] = l
countMood()

p = []
def addPhrase():
    for i in data['MoodOfDay']:
        if i == 0:
            p.append('Powodzenia jutro c;')
        elif i < 0:
            p.append('Hejka, jutro zapowiada się ciężki dzień :c Pamiętaj pić dużo wody i się nie stresować zbytnio! ❤')
        else:
            p.append('Ale dzień cię jutro czeka! Jupi! Baw się dobrze ❤')
    data['Phrase'] = p
addPhrase()