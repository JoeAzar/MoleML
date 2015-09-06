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

# test = extract_phone_image_features("anton.png",18,1,1,1,1)
