from PIL import Image
import numpy as np
from os import listdir
from os.path import isfile, join
import time

a=range(1,4)
b=range(4,7)
c=range(7,10)

L=list(zip(a,b))

print(L)

L = [list(i) for i in L]

print(L)
print()


[i.append(j) for i,j in zip(L,c)]

print(L)

