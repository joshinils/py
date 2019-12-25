from turtle import Turtle, Screen
import random
import copy
import math
import time

# to make pylint happy:
t = Turtle()
s = Screen()

def init():
    t.speed(0)
    t.color('white', 'yellow')
    s.bgcolor('black')
    t.hideturtle()
    t.pu()
    t.setpos(0,0)
    s.tracer(0,0)
    s.colormode(255)
init()

def drawRing(pos, color = 'white', fillColor = s.bgcolor(), str = '', r=25):
    t.pu()
    t.setpos(*pos)
    t.pd()
    t.dot(r, color )
    t.dot(r * .8, fillColor)
    if len(str) > 0:
        fontSize = 12
        t.pu()
        t.sety(t.ycor()-fontSize*1.5/2)
        t.setx(t.xcor()+1) # this offset unfortunately somewhat depends on the fontSize
        t.pd()

        """
        todo: this one, right here!!!
        why does writing "a lot"
        all of a sudden mean i get to "see" and observe the t as it is writing?
        havent i set the tracer(n) to 0?
        """
#        t.write(str, False, 'center', ('times New Roman', fontSize, 'normal') )
        """
        i just dont understand why inserting the above line makes it flicker so damn much
        """
    t.pu()

def drawLine(start, end):
    t.pu()
    t.setpos(*start)
    t.pd()
    t.setpos(*end)
    t.pu()

class PointList(list):
    def __init__(self): pass
    def travelLength(self) -> float:
        sum = 0
        for i, val in enumerate(self[:-1]):
            sum += math.sqrt( (val[0] - self[i+1][0]) ** 2 + 
                              (val[1] - self[i+1][1]) ** 2   )
        return sum

class tsm:
    def __init__(self, nPoints = 10, moveEnds = True):
        self.nPoints = nPoints
        self.pointList = PointList()
        self.moveEnds = moveEnds

        w = s.window_width()
        h = s.window_height()
        d = min(w * .1, h * .1)
        w -= d
        h -= d
        for _ in range(self.nPoints):
            self.pointList.append([int(random.random() * w - w/2), int(random.random() * h - h/2)])

    def draw(self):
        t.clear()
        for i, val in enumerate(self.pointList[:-1]):
            drawLine(val, self.pointList[i+1])
        
        for i, p in enumerate(self.pointList):
            color = (255 - round( 255 * i/len(self.pointList) ), 
                           round( 255 * i/len(self.pointList) ), 
                     0 )
            if i == 0 or i == len(self.pointList)-1:
                fillColor = color
            else:
                fillColor = s.bgcolor()
            drawRing(p, color, fillColor, str(i))
        s.update()
    
    def iterate(self, maxIt=50):
        while maxIt > 0:
            maxIt -= 1

            id1=0; id2=0
            if self.moveEnds:
                id1 = random.randrange(self.nPoints)
                id2 = random.randrange(self.nPoints)
            else:
                id1 = random.randrange(1, self.nPoints-1)
                id2 = random.randrange(1, self.nPoints-1)

            pl2 = copy.deepcopy(self.pointList)
            pl2[id1], pl2[id2] = pl2[id2], pl2[id1]
            if pl2.travelLength() < self.pointList.travelLength():
                self.pointList = pl2
                return


TSM = tsm(50, moveEnds = False)
for i in range(5000):
    TSM.draw()
    TSM.iterate(100)
TSM.draw()
print('done')
s.mainloop()



