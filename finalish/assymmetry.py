import numpy as np
import cv2
import sys
from scipy import ndimage
from skimage.measure import structural_similarity as ssim

def makeImageEvenDims(dimensions):
	x,y,_ = dimensions
	if x % 2 == 0 and y % 2 == 0:
		return (x, y)
	if x % 2 == 1 and y % 2 == 1:
		return (x - 1, y - 1)
	elif y % 2 == 1:
		return (x, y - 1)
	else:
		return (x - 1, y)
def divideIntoTwo(img):
	(x, y) = makeImageEvenDims(img.shape)
	top_half = img[0:x, 0:y/2]
	bottom_half = ndimage.rotate(img[0:x, y/2:y], 180)
	top_half = cv2.cvtColor(top_half, cv2.COLOR_BGR2GRAY)
	bottom_half = cv2.cvtColor(bottom_half, cv2.COLOR_BGR2GRAY)
	return (top_half, bottom_half)
def mse(imageA,imageB):
	error = np.sum((imageA.astype("float")-imageB.astype("float")) ** 2)
	error /= float(imageA.shape[0] * imageA.shape[1])
	return error

def get_symmetry_ssim(img):
	(top_half, bottom_half) = divideIntoTwo(img)
	return ssim(top_half, bottom_half)

def get_symmetry_mse(img):
	(top_half, bottom_half) = divideIntoTwo(img)
	return mse(top_half, bottom_half)

if __name__ == '__main__':
	input_filename = sys.argv[1]

	img = cv2.imread(input_filename)
	(x, y) = makeImageEvenDims(img.shape)
	(top_half, bottom_half) = divideIntoTwo(img)

	print get_symmetry_ssim(img)
	print get_symmetry_mse(img)
	cv2.imshow("top half", top_half)
	cv2.imshow("bottom half", bottom_half)
	cv2.waitKey(0)
