#!/usr/bin/env python

import sys
from PIL import Image
import random

def file_input():
	argc = len(sys.argv)
	if argc == 4:
		global secret, shareA, shareB, width, height
		secret = Image.open(sys.argv[1]).convert('1')
		shareA = Image.open(sys.argv[2]).convert('1')
		shareB = Image.open(sys.argv[3]).convert('1')
		width = secret.width
		height = secret.height
		return True
	else:
		print 'usage: vss.py <secret> <shareA> <shareB>'
		return False

def vss():
	global pixelsA, pixelsB
	shadowA = Image.new('1', (width, height))
	shadowB = Image.new('1', (width, height))
	pixelsA = shadowA.load()
	pixelsB = shadowB.load()
	for i in range(0, width - 1, 2):
		for j in range(0, height - 1, 2):
			temp = pix_plan(secret.getpixel((i, j)), shareA.getpixel((i, j)), shareB.getpixel((i, j)))
			draw(temp[0], temp[1], i, j)
	shadowA.save('shadowA.bmp')
	shadowB.save('shadowB.bmp')

def pix_plan(s, a, b):
	white_gridA = []
	black_gridA = [0, 1, 2, 3]
	white_gridB = []
	if a == 255:
		#random 2 white in range 0~3
		do_random(white_gridA, black_gridA, True)
		do_random(white_gridA, black_gridA, True)
	elif a == 0:
		#random 1 white in range 0~3
		do_random(white_gridA, black_gridA, True)
	if s == 255:
		if a == 255:
			#random 1 white with a's 2 white grids
			do_random(white_gridB, white_gridA, False)
			if b == 255:
				#random 1 white with a's 2 black grids
				do_random(white_gridB, black_gridA, False)
		elif a == 0:
			white_gridB = white_gridA[:]
			if b == 255:
				#random 1 white with a's 3 black grids
				do_random(white_gridB, black_gridA, False)
	elif s == 0:
		if a == 255:
			if b == 255:
				white_gridB = black_gridA[:]
			elif b == 0:
				#random 1 white with a's 2 black grids
				do_random(white_gridB, black_gridA, False)
		elif a == 0:
			if b == 255:
				#random 2 white with a's 3 black grids
				do_random(white_gridB, black_gridA, True)
				do_random(white_gridB, black_gridA, False)
			elif b == 0:
				#random 1 white with a's 3 black grids
				do_random(white_gridB, black_gridA, False)
	return [white_gridA, white_gridB]

def do_random(l1, l2, flag):
	temp = random.choice(l2)
	if flag == True:
		l2.remove(temp)
	l1.extend([temp])

def draw(l1, l2, x, y):
	for i in range(len(l1)):
		q = l1[i] / 2
		r = l1[i] % 2
		pixelsA[x + q, y + r] = 255
	for i in range(len(l2)):
		q = l2[i] / 2
		r = l2[i] % 2
		pixelsB[x + q, y + r] = 255

if __name__ == "__main__":
    if file_input() == False:
		sys.exit()
	#temp = temp.resize((secret.width/2, secret.height/2), Image.BILINEAR)
	vss()
