from PIL import Image
import numpy as np
from os import listdir
from os.path import isfile, join
import time

mypath = '/home/nils/kamera/20191210cp/'
diffpath = '/home/nils/kamera/diffs/'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

onlyfiles.sort()

images = [Image.open(mypath + i) for i in onlyfiles]

w,h = images[0].size
s = 4
w //= s
h //= s

for i in range(len(images)):
	images[i] = images[i].resize( (w, h) )

print(len(images))

diffs = []

for i in range(0, len(images)-1):
	buf1 = np.asfarray(images[i  ])
	buf2 = np.asfarray(images[i+1])

	buf3 = abs(buf1 - buf2)

	m = 0
	for px in buf3:
		for py in px:
			m = max(max(py), m)
	print(m)

	p = [0,0,0];
	for k in range(h):
		for j in range(w):
			p += buf3[k][j]
	p /= w*h
	p = (p[0]+ p[1] + p[2]) / 3
	print(p)

	doSave = (p >= 6)
	if doSave:
		buf3 = np.uint8(buf3)
		diff = Image.fromarray(buf3)
	
		diffs.append( diff )

print(len(diffs))


images = [i.save(diffpath + str(index) + '.jpg')for index, i in enumerate(diffs)]




exit()
image1 = Image.open('bild.jpg')
image2 = Image.open('bild2.jpg')


diff.save('diff.jpg')
