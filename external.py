# 3rd party imports
import urllib2
import json

# Constants
RECAPTCHA_SECRET = "6LcyLAITAAAAAJKMoQ84MZr3kb7Tb2ahJPoI1NfS"

# Checks the Google recaptcha
def correctCaptcha(captcha):
	url = 'https://www.google.com/recaptcha/api/siteverify?response=' + captcha + '&secret=' + RECAPTCHA_SECRET
	return json.loads(urllib2.urlopen(url).read())['success']