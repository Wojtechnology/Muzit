##########################################
#
# Author: Wojtek Swiderski
# 
# File containing 3rd party API code
# Application for uploading and listening to music
#
# Last Update: February 17th, 2015
#
##########################################

# 3rd party imports
import urllib2
import json

# Constants
RECAPTCHA_SECRET = "6LcyLAITAAAAAJKMoQ84MZr3kb7Tb2ahJPoI1NfS"

# Checks the Google recaptcha
def correctCaptcha(captcha):
	url = 'https://www.google.com/recaptcha/api/siteverify?response=' + captcha + '&secret=' + RECAPTCHA_SECRET
	return json.loads(urllib2.urlopen(url).read())['success']