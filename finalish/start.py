import logging
import os
import sys

from flask import Flask, request
from extract import extract_phone_image_features

# app = Flask(__name__)

# app.logger.addHandler(logging.StreamHandler(sys.stdout))
# app.logger.setLevel(logging.ERROR)

# # heee
# @app.route('/')
# def hello():
#   return 'Hello World!'

# @app.route('/data')
# def get_image_classification():
#   img_url = request.args.get('img_url')
#   messages = classify_image_url(str(img_url))
#   print 'Success'
#   return ','.join(messages) 

# if __name__ == '__main__':
#   app.run(debug=True)

# from standardize import imageMask
# print imageMask("test2.jpg","test2.tif")

mode = "production" #"training"
if mode=="production"
@app.route('/imagePost')
def classify():
	img = request.args.get('img')
	res = extract_phone_image_features(img,age,gender,location,quantloc,concern)
