from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from sklearn import ensemble, preprocessing
import pandas as pd
from matplotlib import style
style.use("ggplot")

from sklearn import cross_validation
from sklearn.cluster import MiniBatchKMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn import svm
from sklearn import linear_model

FEATURES =  [
  	'_Sizemm','_Age','_Gender','_Latitude','_Quant. Loc','Change','Concern'
]

def Build_Data_Set():
  data_df = pd.DataFrame.from_csv("clinical.csv")

  data_df = data_df.reindex(np.random.permutation(data_df.index))
  
  X = np.array(data_df[FEATURES].values)

  y = ( data_df["_NewType_030415"].values.tolist()  )

  X = preprocessing.scale(X)

  return X,y

def Analysis():
  test_size = 900
  X, y = Build_Data_Set()
  print(len(X))

  clf = RandomForestClassifier(n_estimators = 30)
  clf.fit(X[:-test_size],y[:-test_size]) # train data

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



  print("correct_count=%s"%float(correct_count))
  print("test_size=%s"%float(test_size))
  # on OS X with 64-bit python 2.7.6 had to add float(), otherwise result was zero:
  print("Accuracy:", (float(correct_count) / float(test_size)) * 100.00)
  print("Precision:", (float(tp)/(float(tp)+float(fp)))*100)
  print("Recall:", (float(tp)/(float(tp)+float(fn)))*100)
# test shuffling data:
# def Randomizing():
#   df = pd.DataFrame({"D1":range(5), "D2":range(5)})
#   print(df)
#   df2 = df.reindex(np.random.permutation(df.index))
#   print(df2)

# Randomizing()

Analysis()