from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from sklearn import ensemble, preprocessing
import pandas as pd
from matplotlib import style
style.use("ggplot")
import pickle
import cPickle

from sklearn import cross_validation
from sklearn.cluster import MiniBatchKMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn import svm
from sklearn import linear_model

FEATURES =  [
  	'ssim','border_gof','age','gender','location','quantloc','concern',
]

def Build_Data_Set():
  data_df = pd.DataFrame.from_csv("compiled.csv")

  # data_df = data_df.reindex(np.random.permutation(data_df.index))
  
  X = np.array(data_df[FEATURES].values)

  y = ( data_df["cancerous"].values.tolist()  )

  X = preprocessing.scale(X)

  return X,y

def Analysis():
  test_size = 800
  X, y = Build_Data_Set()
  # print(len(X))

  clf = RandomForestClassifier(n_estimators = 30)
  clf.fit(X[:-test_size],y[:-test_size]) # train data
  print clf.predict_proba(X[850])
  print clf.predict(X[850])[0]
  print y[850]
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



  print("correct_count=%s"%float(correct_count))
  print("test_size=%s"%float(test_size))
  # on OS X with 64-bit python 2.7.6 had to add float(), otherwise result was zero:
  print("Accuracy:", (float(correct_count) / float(test_size)) * 100.00)
  print("Precision:", (float(tp)/(float(tp)+float(fp)))*100)
  print("Recall:", (float(tp)/(float(tp)+float(fn)))*100)
  scores = cross_validation.cross_val_score(clf, X, y, cv = 5)
  with open('test2.pk1', 'wb') as clf_file:
    cPickle.dump(clf, clf_file)
# test shuffling data:
# def Randomizing():
#   df = pd.DataFrame({"D1":range(5), "D2":range(5)})
#   print(df)
#   df2 = df.reindex(np.random.permutation(df.index))
#   print(df2)

# Randomizing()

Analysis()