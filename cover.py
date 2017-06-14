#!/usr/bin/env python

import sys
from PIL import Image

def img_load():
	if len(sys.argv) == 3:
		global imgA, imgB, secret
		imgA = Image.open(sys.argv[1])
		imgB = Image.open(sys.argv[2])
		secret = Image.new('1', (imgA.width, imgA.height))
		return True
	else:
		print 'usage: vss.py <shadowA> <shadowB>'
		return False

def img_cover():
	A_pixels = imgA.load()
	B_pixels = imgB.load()
	S_pixels = secret.load()

	for i in range(imgA.width):
		for j in range(imgA.height):
			if A_pixels[i, j] == 255 and B_pixels[i, j] == 255:
				S_pixels[i, j] = 255

	secret.save('secret.bmp')

if __name__ == "__main__":
	if img_load() == False:
		sys.exit()
	img_cover()
