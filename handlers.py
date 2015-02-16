##########################################
#
# Author: Wojtek Swiderski
# 
# File containing all handlers required for the application
# Application for uploading and listening to music
#
# Last Update: February 16th, 2015
#
##########################################

# Required Tornado import
import tornado.web

# Class for the main page request handler
class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('main.html', browser_title = "Muzit")

# Class for the upload AJAX request handler
class UploadHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('upload.html')

# Class for the top AJAX request handler
class TopHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('upload.html')

# Class for the new AJAX request handler
class NewHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('upload.html')