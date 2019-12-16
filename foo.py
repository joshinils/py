from PIL import Image
import numpy as np
from os import listdir
from os import mkdir
from os import path
from os.path import isfile, join
import time
from shutil import copyfile

mypath = '/home/nils/kamera/20191210cp/'
diffpath = mypath + 'diffs/'

if not path.exists(diffpath):
    mkdir(diffpath)

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

onlyfiles.sort()
print('opening ', len(onlyfiles), ' images')
images = list( zip([Image.open(mypath + i) for i in onlyfiles], onlyfiles) )

# make list of lists, instead of list of tuples
images = [list(i) for i in images]
for i,j in zip(images, onlyfiles):
	i.append(False) # if it shall be saved afterward, to be set

#pre-process images
w,h = images[0][0].size
s = 4
w //= s
h //= s
for imList in images:
	# scale images down
 	imList[0] = imList[0].resize( (w, h) ) 

	#TODO normalize images before comparison
	

#detect level of differences
print('detecting differences')
for index, imList in enumerate(images):
	if index == len(images)-1:
		break
	print('comparing image ', index, ' of ', len(images), end=' ')
	buf1 = np.asfarray(imList[0])
	buf2 = np.asfarray(images[index+1][0])

	buf3 = abs(buf1 - buf2)

	p = [0,0,0];
	for k in range(h):
		for j in range(w):
			p += buf3[k][j]
	p /= w*h
	p = (p[0]+ p[1] + p[2]) / 3
	print(' diff=', p, end='\r')

	doSave = bool((p >= 6))
	imList[2] |= doSave # save this
	images[index+1][2] = doSave # save next

# count different images
diffs = 0
for imList in images:
	if imList[2]:
		diffs += 1

# save images
print('saving ', diffs, 'images')
for imList in images:
	if imList[2]:
		copyfile(mypath + imList[1], diffpath + imList[1])
		#imList[0].save(diffpath + imList[1])
print('savng done')

















































