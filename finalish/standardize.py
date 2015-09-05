import numpy as np
import cv2

def imageMask(image,mask):

	im = cv2.imread(image)
	maskOrig = cv2.imread(mask)
	mask = cv2.imread(mask, cv2.COLOR_BGR2GRAY)
	img = cv2.bitwise_and(im,im, mask=mask)

	ret,thresh = cv2.threshold(mask,127,255,0)
	countours,hierarchy = cv2.findContours(thresh,1,2)
	cnt = countours[0]
	x,y,w,h = cv2.boundingRect(cnt)
	cropped = img[y:y+h,x:x+w]
	original = im[y:y+h,x:x+w]

	return original

# imageMask("test2.jpg","test2.tif")