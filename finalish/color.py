import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from itertools import combinations
from sklearn.cluster import KMeans


def centroid_histogram(clt):
  # grab the number of different clusters and create a histogram
  # based on the number of pixels assigned to each cluster
  numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
  (hist, _) = np.histogram(clt.labels_, bins = numLabels)
 
  # normalize the histogram, such that it sums to one
  hist = hist.astype("float")
  hist /= hist.sum()
 
  # return the histogram
  return hist

def plot_colors(hist, centroids):
  # initialize the bar chart representing the relative frequency
  # of each of the colors
  bar = np.zeros((50, 300, 3), dtype = "uint8")
  startX = 0
 
  # loop over the percentage of each cluster and the color of
  # each cluster
  for (percent, color) in zip(hist, centroids):
    # plot the relative percentage of each cluster
    endX = startX + (percent * 300)
    cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
      color.astype("uint8").tolist(), -1)
    startX = endX
  
  # return the bar chart
  return bar

def color_contrast(img):
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  img = img.reshape((img.shape[0] * img.shape[1], 3))
  clt = KMeans(n_clusters = 3)
  clt.fit(img)
  color_centroids = [sRGBColor(r, g, b) for (r, g, b) in clt.cluster_centers_]
  color_diff = 0.0

  for (color_a, color_b) in combinations(color_centroids, 2):
    color_a_lab = convert_color(color_a, LabColor);
    color_b_lab = convert_color(color_b, LabColor);
    delta_e = delta_e_cie2000(color_a_lab, color_b_lab)
    color_diff += delta_e

  return float(color_diff/3)

if __name__ == '__main__':
  input_filename = sys.argv[1]

  img = cv2.imread(input_filename)
  #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

  #plt.figure()
  #plt.imshow(img)
  # img = img.reshape((img.shape[0] * img.shape[1], 3))

  # clt = KMeans(n_clusters = 3)
  # clt.fit(img)

  # hist = centroid_histogram(clt)
  # bar = plot_colors(hist, clt.cluster_centers_)

  # color_centroids = [sRGBColor(r, g, b) for (r, g, b) in clt.cluster_centers_]
  # color_diff = 0.0

  # for (color_a, color_b) in combinations(color_centroids, 2):
  #   color_a_lab = convert_color(color_a, LabColor);
  #   color_b_lab = convert_color(color_b, LabColor);
  #   delta_e = delta_e_cie2000(color_a_lab, color_b_lab)
  #   color_diff += delta_e

  print "The avg difference is " + str(color_contrast(img))
  #plt.figure()
  #plt.imshow(bar)
  #plt.show()


