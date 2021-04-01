from graphics import *
from dieview import *
from button import Button
class GraphicInterface:
    def __init__(self):        
        self.win = GraphWin("Dice Poker", 600, 400)
        self.showHighScore()

        
        self.win.setBackground("green3")
        self.showIntro()
        self.choosePlay()
        banner = Text(Point(300,30),"Python Poker Parlor")
        banner.setSize(24)
        banner.setFill("yellow2")
        banner.setStyle("bold")
        banner.draw(self.win)
        self.msg = Text(Point(300,380), "Welcom to the Dice Table")
        self.msg.setSize(18)
        self.msg.draw(self.win)
        self.createDice(Point(300,100), 75)
        self.buttons = []
        self.addDiceButtons(Point(300,170), 75, 30)
        b = Button(self.win, Point(300, 230), 400, 40, "Roll Dice")
        self.buttons.append(b)
        b = Button(self.win, Point(300, 280), 150, 40, "Score")
        self.buttons.append(b)
        b = Button(self.win, Point(570, 375), 40, 30, "Quit")
        self.buttons.append(b)
        b = Button(self.win, Point(570, 30), 40, 30, "Help")
        self.buttons.append(b)
        self.money = Text(Point(300,325), "$100")
        self.money.setSize(18)
        self.money.draw(self.win)

    def createDice(self, center, size):
        center.move(-3*size,0)
        self.dice = []
        for i in range(5):
            view = DieView(self.win, center, size)
            self.dice.append(view)
            center.move(1.5*size, 0)

    def addDiceButtons(self, center, width, height):
        center.move(-3*width,0)
        for i in range(1,6):
            label = "Die {0}".format(i)
            b = Button(self.win, center, width, height, label)
            self.buttons.append(b)
            center.move(1.5*width, 0)

    def setMoney(self, amt):
        self.money.setText("${}".format(amt))

    def showResult(self, msg, score):
        if score > 0:
            text = "{0}! you win ${1}".format(msg,score)
        else:
            text = "you rolled {0}".format(msg)
        self.msg.setText(text)

    def setDice(self, values):
        for i in range(5):
            self.dice[i].setValue(values[i])

    def wantToPlay(self):
        while True:
            
            ans = self.choose(["Roll Dice", "Quit", "Help"])
            self.msg.setText("")
            if ans == "Help":
                self.help()
            else:
                break
        return ans == "Roll Dice"
    
    def chooseDice(self):
        # choices is a list of the indexes of teh selected dice
        choices = []            # no dice choosen yet
        while True:
            # wait for user to click a valid button
            b = self.choose(["Die 1", "Die 2", "Die 3", "Die 4", "Die 5",
                             "Roll Dice", "Score", "Help"])

            if b[0] == "D":         # User Clicked a die button
                i = int(b[4]) - 1   # Translate label to die index
                if i in choices:    # Currently selected, unselect it
                    choices.remove(i)
                    self.dice[i].setColor("black")
                else:               # Currentely deselected, select it
                    choices.append(i)
                    self.dice[i].setColor("gray")
            else:                   # User clicked roll or score
                for d in self.dice: # Revert appearance of all dice
                    d.setColor("black")
                if b == "Score":    # Score clicked, ignore choices
                    return []
                elif b == "Help":
                    self.help()
                elif choices !=[]:  # Don't accept roll unless some
                    return choices  #   dice are actually selected
        
    def close(self):
        self.win.close()

    def choose(self, choices):
        buttons = self.buttons

        # activate choice buttons, deactivate others
        for b in buttons:
            if b.getLabel() in choices:
                b.activate()
            else:
                b.deactivate()

        # get mouse clicks until an active button is clicked
        while True:
            p = self.win.getMouse()
            for b in buttons:
                if b.clicked(p):
                    return b.getLabel() # function exit here.

    def setValue(self, value):
        # Turn all the pips off
        self.value = value
        for pip in self.pips:
            pip.setFill(self.background)

        # Turn the appropriate pips back on
        for i in self.onTable[value]:
            self.pips[i].setFill(self.forground)

    def showIntro(self):
        self.intro = Text(Point(300,200), "Lets Play Some Poker with Dice!!")
        self.intro.draw(self.win)

    def choosePlay(self):
        letsPlay = Button(self.win, Point(300,100), 100, 60, "Lets Play")
        letsPlay.activate()
        while True:
            p = self.win.getMouse()
            if letsPlay.clicked(p):
                break
        self.intro.undraw()
        letsPlay.undraw()

    def help(self):
        helpWin = GraphWin("help", 400, 200)
        helpWin.setBackground("blue1")
        helpmsg = Text(Point(200,100), "hand     \t   pay\n\
--------------------- \n\
Two Pairs       \t $5 \n\
Three of a Kind \t $8 \n\
Full House      \t $12\n\
Four of a Kind  \t $15\n\
Straight        \t $20\n\
Five of a Kind  \t $30 ")
                      
        helpmsg.draw(helpWin)

    def showHighScore(self):
        highscores = open("high_score.txt", "r")
        high_score = highscores.readlines()
        y = 170
        scores = []
        scorText = Text(Point(300,y-30), "High Score name")
        scorText.draw(self.win)
        for line in high_score:
            s = Text(Point(300,y), line).draw(self.win)
            scores.append(s)
            y = y + 18
        highscores.close()
        cbut = Button(self.win, Point(300, 100), 400, 40, "Start Game")
        cbut.activate()
        while True:
            p = self.win.getMouse()
            if cbut.clicked(p):
                scorText.undraw()
                cbut.undraw()
                for obj in scores:
                    obj.undraw()
                break
          
    def askUsername(self):
        nameWin = GraphWin("player name", 300, 200)
        name = Entry(Point(150,100),10)
        name.draw(nameWin)
        okbut = Button(nameWin, Point(150, 150), 30, 40, "OK")
        okbut.activate()
        while True:
            p = nameWin.getMouse()
            if okbut.clicked(p):
                break
        player = name.getText()
        nameWin.close()
        return player

    def updateScore(self, money):
        highscores = open("high_score.txt", "r")
        high_score = highscores.readlines()
        i = 0
        for line in high_score:
            
            if money > int(line.split("\t")[0]):
                name = self.askUsername()
                
                high_score.insert(i,"{}\t{}\n".format(money,name))
                high_score.pop(10)
                highscores = open("high_score.txt", "w")
                for line in high_score:
                    print(line, file = highscores, end = "")
                highscores.close()
                break
            i = i + 1

                    
