from __future__ import division
import numpy as np
#import matplotlib.pyplot as plt
from sklearn import ensemble, preprocessing
import pandas as pd
#from matplotlib import style
#style.use("ggplot")
import pickle
import cPickle

from sklearn import cross_validation
from sklearn.cluster import MiniBatchKMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn import svm
from sklearn.externals import joblib
from sklearn import linear_model

total = 0
nc_color_sum = []
nc_mse_sum = []
nc_ssim_sum = []
nc_border_sum = []
nc_age = []
nc_gender = []
nc_location = []
nc_quantloc = []
nc_concern = []

cancerous_color_sum = []
cancerous_mse_sum = []
cancerous_ssim_sum= []
cancerous_border_sum = []
cancerous_age = []
cancerous_gender = []
cancerous_location = []
cancerous_quantloc = []
cancerous_concern = []

FEATURES =  ['sym','ssim','border_gof', 'color_contrast', 'age','gender','location','quantloc','concern']
def Build_Data_Set():
  data_df = pd.DataFrame.from_csv("compiledfinal.csv")

  # data_df = data_df.reindex(np.random.permutation(data_df.index))
  X = np.array(data_df[FEATURES].values)
  y = ( data_df["cancerous"].values.tolist()  )

  X = preprocessing.scale(X)

  return X,y
def cancerousdata():
  return map(np.mean,(cancerous_mse_sum,cancerous_ssim_sum,cancerous_border_sum,cancerous_color_sum,cancerous_age,cancerous_gender,cancerous_location,cancerous_quantloc,cancerous_concern))
def ncdata():
  return map(np.mean,(nc_mse_sum,nc_ssim_sum,nc_border_sum,nc_color_sum,nc_age,nc_gender,nc_location,nc_quantloc,nc_concern))
def find_means():
  data_df = pd.DataFrame.from_csv("compiledfinal.csv")
  X = np.array(data_df[FEATURES].values)
  y = (data_df["cancerous"].values.tolist())
  # X = preprocessing.scale(X)
  for i in range(1, (len(X))):

    if y[i] == 1:
      cancerous_mse_sum.append(X[i][0])
      cancerous_ssim_sum.append(X[i][1])
      cancerous_border_sum.append(X[i][2])
      cancerous_color_sum.append(X[i][3])
      cancerous_age.append(X[i][4])
      cancerous_gender.append(X[i][5])
      cancerous_location.append(X[i][6])
      cancerous_quantloc.append(X[i][7])
      cancerous_concern.append(X[i][8])
    if y[i] == 0:
      nc_mse_sum.append(X[i][0])
      nc_ssim_sum.append(X[i][1])
      nc_border_sum.append(X[i][2])
      nc_color_sum.append(X[i][3])
      nc_age.append(X[i][4])
      nc_gender.append(X[i][5])
      nc_location.append(X[i][6])
      nc_quantloc.append(X[i][7])
      nc_concern.append(X[i][8])
  
  malig_avg = cancerousdata()
  nc_avg = ncdata()

  with open('malignant_averages.txt', 'w') as malig_file:
    for s in malig_avg:
      malig_file.write(str(s) + '\n')
  with open('benign_averages.txt', 'w') as benign_file:
    for s in nc_avg:
      benign_file.write(str(s) + '\n')
# find_means()
def Analysis():
  test_size = 800
  X, y = Build_Data_Set()
  # print(len(X))

  clf = RandomForestClassifier(n_estimators = 30)
  clf.fit(X[:-test_size],y[:-test_size]) # train data
  # print clf.predict_proba(X[3])
  # print clf.predict(X[3])[0]
  # print y[3]
  correct_count = 0
  correct_count = 0
  tp = 0
  fn = 0
  fp = 0
  for x in range(1, test_size+1):
    if clf.predict(X[-x])[0] == y[-x]:
      correct_count += 1
      if clf.predict(X[-x])[0] == 1:
      	tp += 1
    if (clf.predict(X[-x])[0] != y[-x]) and (clf.predict(X[-x])[0] == 0):
    	fn += 1
    if (clf.predict(X[-x])[0] != y[-x]) and (clf.predict(X[-x])[0] == 1):
    	fp += 1



  # print("correct_count=%s"%float(correct_count))
  # print("test_size=%s"%float(test_size))
  # #on OS X with 64-bit python 2.7.6 had to add float(), otherwise result was zero:
  # print("Accuracy:", (float(correct_count) / float(test_size)) * 100.00)
  # print("Precision:", (float(tp)/(float(tp)+float(fp)))*100)
  # print("Recall:", (float(tp)/(float(tp)+float(fn)))*100)
  # scores = cross_validation.cross_val_score(clf, X, y, cv = 5)
  # joblib.dump(clf,'final.pk1')
  # with open('final.pk1', 'wb') as clf_file:
  #   cPickle.dump(clf, clf_file)

def AnalysisSpec(vector):
  test_size = 800
  X , y = Build_Data_Set()
  clf = svm.SVC(probability=True)
  clf.fit(X[:-test_size],y[:-test_size])
  malig_avgs = []
  benign_avgs = []

  with open('malignant_averages.txt', 'r') as malig_file:
    malignant_avgs = [float(line.rstrip('\n')) for line in malig_file]
  with open('benign_averages.txt', 'r') as benign_file:
    benign_avgs = [float(line.rstrip('\n')) for line in benign_file]
  support_count = 0

  if clf.predict(vector)[0] == 1:
    for i in range(0,8):
      if vector[i] < malignant_avgs[i]:
        support_count += 1
  if clf.predict(vector)[0] == 0:
    for j in range(0,8):
      if vector[j] < benign_avgs[j]:
        support_count += 1
  if support_count > 3:
    finalVector = clf.predict(vector)[0]
  if support_count <= 3:
    if (clf.predict(vector)[0] == 1):
      finalVector = 0
    else: 
      finalVector = 0
  # print support_count

  test =  clf.predict_proba(vector)
  # print clf.predict(vector)[0]
  test2 = np.append(clf.predict_proba(vector),finalVector)
  return test2
  # return finalVector,clf.predict_proba(vector)

# test shuffling data:
# def Randomizing():
#   df = pd.DataFrame({"D1":range(5), "D2":range(5)})
#   print(df)
#   df2 = df.reindex(np.random.permutation(df.index))
#   print(df2)

# Randomizing()

# Analysis()
