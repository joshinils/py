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
        print('iterating...', end=' ')
        for idAmount in range( 2, self.nPoints ):
#            print('idAmount', idAmount)
            iters = 0
            while iters < maxIt:
#                print('iters', iters)
                iters += 1

                ids = list(range(self.nPoints))

                if not self.moveEnds:
                    ids.remove(1)
                    ids.remove(max(ids))

                while len(ids) > idAmount:
                    r = random.randrange(len(ids))
                    ids.remove(ids[r])

                ids = list(ids)
                pl2 = copy.deepcopy(self.pointList)
                
                # ringtausch, ohne letzten
                for i, val in enumerate(ids[:-1]):
                    pl2[val], pl2[ids[i+1]] = pl2[ids[i+1]], pl2[val]

                if pl2.travelLength() < self.pointList.travelLength():
                    self.pointList = pl2
                    print(' ...succeeded')
                    return
        print(' ...failed')



TSM = None
nodeAmount = 50

def nodePlus():
    global nodeAmount
    nodeAmount += 1
    start()
s.onkey(nodePlus, 'Up')

def nodeMinus():
    global nodeAmount
    nodeAmount = max(nodeAmount-1, 1)
    start()
s.onkey(nodeMinus, 'Down')

def nodeAmountReset():
    global nodeAmount
    nodeAmount = 5
    start()
s.onkey(nodeAmountReset, 'Left')
s.onkey(nodeAmountReset, 'Right')

def start():
    global TSM
    global nodeAmount
    TSM = tsm(nodeAmount, moveEnds = True)
    TSM.draw()
s.onkey(start, 'Return')

def drawIterate():
    if TSM is None:
        start()
        return
    #for i in range(5000):
#    TSM.draw()
    TSM.iterate(1000)
    TSM.draw()
#    print('foo!')
s.onkey(drawIterate, 'space')

s.listen()
s.mainloop()




