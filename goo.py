from turtle import *
from random import *
from copy import *
from math import *

def init():
    speed(0)
    color('white', 'yellow')
    bgcolor('black')
    hideturtle()
    pu()
    setpos(0,0)
init()

def drawRing(pos, r=25):
    pu()
    setpos(*pos)
    pd()
    dot(r, 'white')
    dot(r * .8, bgcolor())
    pu()

def drawLine(start, end):
    pu()
    setpos(*start)
    pd()
    setpos(*end)
    pu()

class PointList(list):
    def __init__(self): pass
    def travelLength(self) -> float:
        sum = 0
        for i, val in enumerate(self[:-1]):
            sum += sqrt( (val[0] - self[i+1][0]) ** 2 + 
                        (val[1] - self[i+1][1]) ** 2   )
        return sum

class tsm:
    def __init__(self):
        self.nPoints = 10
        self.pointList = PointList()

        #s = screensize()
        w = window_width()
        h = window_height()
        d = min(w * .1, h * .1)
        w -= d
        h -= d
        for i in range(self.nPoints):
            self.pointList.append([int(random() * w - w/2), int(random() * h - h/2)])

    def draw(self):
        clear()
        for i, val in enumerate(self.pointList[:-1]):
            drawLine(val, self.pointList[i+1])
        for p in self.pointList:
            drawRing(p)
    
    def iterate(self, maxIt=50):
        while maxIt > 0:
            maxIt -= 1

            id1 = randrange(self.nPoints)
            id2 = randrange(self.nPoints)

            pl2 = deepcopy(self.pointList)
            pl2[id1], pl2[id2] = pl2[id2], pl2[id1]
            if pl2.travelLength() < self.pointList.travelLength():
                self.pointList = pl2
                return


s = tsm()
for i in range(50):
    s.draw()
    s.iterate()
s.draw()

mainloop()



