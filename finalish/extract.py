import border
import color
import pickle
import cv2
import numpy as np
import os
import assymmetry
import sys
import standardize
import pandas as pd
from skimage import io
from learn import AnalysisSpec
from sklearn import cross_validation
from sklearn.cluster import MiniBatchKMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
from sklearn.externals import joblib
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn import svm
def extract_phone_image_features(imgorig,age,gender,location,quantloc,concern):
	img = cv2.imread(imgorig)
	height, width, channels = img.shape
	mh = height/2 
	mw = width/2
	img = img[(mh-300):(mh+300),(mw-300):(mw+300)]
	# cv2.imshow('lel',img)
	x, y, _ = img.shape
	image = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
  	image = image.reshape((image.shape[0] * image.shape[1], 3))
  	clt = MiniBatchKMeans(n_clusters = 3)
  	labels = clt.fit_predict(image)
  	quant = clt.cluster_centers_.astype("uint8")[labels]
  	quant = quant.reshape((x, y, 3))
  	image = image.reshape((x, y, 3))
  	quant = cv2.cvtColor(quant, cv2.COLOR_LAB2BGR)
  	image = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)
  	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  	symmetry_ssim = assymmetry.get_symmetry_ssim(image)
  	symmetry_mse = assymmetry.get_symmetry_mse(image)
  #symmetry_mse = 0
  	border_gof = border.get_gof(gray)
    #print border_gof
    #border_gof = 0
  	color_contrast = color.color_contrast(image)
  	current_vec = [(symmetry_mse/1000),
  	symmetry_ssim,
  	(border_gof/10),
  	color_contrast,
  	age,
  	gender,
  	location,
  	quantloc,
  	concern]
  	# clf2 = pickle.load(open('final.pk1', 'rb'))
  	# print clf2
  	# print imgorig
  	return AnalysisSpec(current_vec)
  	# prediction = clf2.predict(np.array(current_vec))[0]
  	# print prediction
  	# print current_vec
  	# print clf2.predict_proba(current_vec)
  	# return clf2.predict_proba(current_vec), prediction
# image_list = []

# imgpath = '../hairremove/'
# img_list = [x[0] for x in os.walk(imgpath)]
# each_file = os.listdir(imgpath)
# for x in each_file:
# 	if x.find("Inpaint") != -1:
# 		image_list.append(x)
# for index in range(len(image_list)):
# 	x = image_list[index]
# 	print x
	# extract_phone_image_features(imgpath+x,58,2,1,5,2)
#extract_phone_image_features("anton.png",18,2,1,5,2)

# def extract_image_features(imgorig,mask):
#   img = cv2.imread(imgorig)
#   # x, y, _ = img.shape

#   # if x > 1000 or y > 1000:
#   #   continue # hack to avoid large images
#   # image2,original2 = standardize.imageMask(img,masker)
#   img = standardize.imageMask(imgorig,mask) 
#   x, y, _ = img.shape

#   image = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
#   image = image.reshape((image.shape[0] * image.shape[1], 3))
#   clt = MiniBatchKMeans(n_clusters = 3)
#   labels = clt.fit_predict(image)
#   quant = clt.cluster_centers_.astype("uint8")[labels]
#   quant = quant.reshape((x, y, 3))
#   image = image.reshape((x, y, 3))
#   quant = cv2.cvtColor(quant, cv2.COLOR_LAB2BGR)
#   image = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)
#   gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#   # cv2.imshow('eh',img)
#     # gray = cv2.imread(img_filename,0)
#     # img = cv2.resize(img, (300, 300)) 
#     # gray = cv2.resize(gray, (300, 300))

#   #print img_filename
#   symmetry_ssim = assymmetry.get_symmetry_ssim(image)
#   symmetry_mse = assymmetry.get_symmetry_mse(image)
#   #symmetry_mse = 0
#   border_gof = border.get_gof(gray)
#     #print border_gof
#     #border_gof = 0
#   color_contrast = color.color_contrast(image)
#   healthdata_df = pd.DataFrame.from_csv("clinical.csv")
#   row = healthdata_df[(healthdata_df.index==imgorig)]
#   # age = int(row["_Age"])
#   # gender = int(row["_Gender"])
#   # location = row["_Latitude"]
#   # quantloc = row["_Quant. Loc"]
#   # concern =  row["Concern"]
#   # cancerous = row["_NewType_030415"]
#   current_vec = [symmetry_mse, symmetry_ssim, border_gof, color_contrast]
#   df = pd.DataFrame(columns = [
#  		'symmetry',
#  		'ssim',
#  		'border_gof',
#  		'color_contrast',
#  		'age',
#  		'gender',
#  		'location',
#  		'quantloc',
#  		'concern',
#  		'cancerous'
# 	])
#   df = df.append({
#   		'symmetry':symmetry_mse,
#   		'ssim':symmetry_ssim,
#   		'border_gof':border_gof,
#   		'color_contrast':color_contrast,
#   		'age':age,
#   		'gender':gender,
#   		'location':location,
#   		'quantloc':quantloc,
#   		'concern':concern,
#   		'cancerous':cancerous
#   	},
#   	ignore_index=True)

#   with open('test2.csv','a') as f:
#   	df.to_csv(f, header=False)
#   return current_vec
# image_list = []
# mask_list = []
# imgpath = '../hairremove/'
# maskpath = '../masks/'
# img_list = [x[0] for x in os.walk(imgpath)]
# each_file = os.listdir(imgpath)
# for x in each_file:
# 	if x.find("Inpaint") != -1:
# 		image_list.append(x)
# 		y = x.replace('Inpaint','mask')
# 		mask_list.append(y)
# count = 0
# for index in range(len(image_list)):
# 	x = image_list[index]
# 	y = mask_list[index].replace('mask','Inpaint')
# 	if y == x:
# 		y = mask_list[index]
# 		extract_image_features(imgpath+x,maskpath+y)
# 		print "finished " + x
# 		count += 1
# 	else:
# 		print "fail " + x + " " + y
# print count
