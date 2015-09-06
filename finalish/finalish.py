import logging
import os
import sys

from flask import Flask, request
from extract import extract_phone_image_features

from datetime import timedelta
from flask import make_response, request, current_app
from flask import Flask
from functools import update_wrapper
import urllib2
import urllib

def crossdomain(origin=None, methods=None, headers=None,
               max_age=21600, attach_to_all=True,
               automatic_options=True):
   if methods is not None:
       methods = ', '.join(sorted(x.upper() for x in methods))
   if headers is not None and not isinstance(headers, basestring):
       headers = ', '.join(x.upper() for x in headers)
   if not isinstance(origin, basestring):
       origin = ', '.join(origin)
   if isinstance(max_age, timedelta):
       max_age = max_age.total_seconds()

   def get_methods():
       if methods is not None:
           return methods

       options_resp = current_app.make_default_options_response()
       return options_resp.headers['allow']

   def decorator(f):
       def wrapped_function(*args, **kwargs):
           if automatic_options and request.method == 'OPTIONS':
               resp = current_app.make_default_options_response()
           else:
               resp = make_response(f(*args, **kwargs))
           if not attach_to_all and request.method != 'OPTIONS':
               return resp

           h = resp.headers

           h['Access-Control-Allow-Origin'] = origin
           h['Access-Control-Allow-Methods'] = get_methods()
           h['Access-Control-Max-Age'] = str(max_age)
           if headers is not None:
               h['Access-Control-Allow-Headers'] = headers
           return resp

       f.provide_automatic_options = False
       return update_wrapper(wrapped_function, f)
   return decorator


application = Flask(__name__)


todos = {}
@application.route('/')
def hello():
    return "sup bitches"
@application.route('/imagePost')
@crossdomain(origin='*')
def classify():
    img = request.args.get('img')
    age = request.args.get('age')
    gender = request.args.get('gender')
    location = request.args.get('location')
    quantloc = request.args.get('quantloc')
    concern = request.arges.get('concern')
    res = extract_phone_image_features(img,age,gender,location,quantloc,concern)

if __name__ == '__main__':
    application.run(host='0.0.0.0')
