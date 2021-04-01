#dicePoker.py

from random import randrange
            
class Dice:
    def __init__(self):
        self.dice = [0]*5
        self.rollAll()
        
    def roll(self, which):
        for pos in which:
            self.dice[pos] = randrange(1,7)

    def rollAll(self):
        self.roll(range(5))

    def values(self):
        return self.dice[:]

    def score(self):
        # create the counts list
        counts = [0] * 7
        for value in self.dice:
            counts[value] = counts[value] + 1

        # score the hand
        if 5 in counts:
            return "Four of a Kind", 30
        elif 4 in counts:
            return "Four of a Kind", 15
        elif (3 in counts) and (2 in counts):
            return "Full House", 12
        elif 3 in counts:
            return "Three of a Kind", 8
        elif not (2 in counts) and (counts[1]==0 or counts[6] == 0):
            return "Straight", 20
        elif counts.count(2) == 2:
            return "Two Pairs", 5
        else:
            return "Garbage", 0

class PokerApp:
    def __init__(self, interface):
        self.dice = Dice()
        self.money = 100
        self.interface = interface

    def run(self):
        while self.money >= 10 and self.interface.wantToPlay():
            self.PlayRound
        self.interface.close()

    def playRound(self):
        self.money = self.money - 10
        self.interface.setMoney(self.money)
        self.doRolls()
        result, score = self.dice.score()
        self.interface.showResult(result, score)
        self.money = self.money + score
        self.interface.setMoney(self.money)

    def doRolls(self):
        self.dice.rollAll()
        roll = 1
        self.interface.setDice(self.dice.values())
        toRoll = self.interface.chooseDice()
        while roll < 3 and toRoll != []:
            self.dice.roll(toRoll)
            roll = roll + 1
            self.interface.setDice(self.dice.values())
            if roll < 3:
                toRoll = self.interface.chooseDice()
        
class TextInterface:
    def __init__(self):
        print("Welcome to video poker")

    def setMoney(self, amt):
        print("You currently have ${}.".format(amt))

    def setDice(self, values):
        print("Dice: ", values)

    def wantToPlay(self):
        ans = input("Do you wish to try your luck? ")
        return ans[0] in "Yy"

    def close(Self):
        print("\nThanks for playing!")

    def showResult(self, msg, score):
        print("{0}. you ${1}.".format(msg, score))

    def chooseDice(self):
        return eval(input("Enter list of which to change([] to stop) "))
    
