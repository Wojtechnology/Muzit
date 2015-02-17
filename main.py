
##########################################
#
# Author: Wojtek Swiderski
# 
# Main file for tornado server
# Application for uploading and listening to music
#
# Last Update: February 16th, 2015
#
##########################################

# 3rd party imports
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
import os.path
import pymongo
import logging

# 1st party imports
import modules as Modules
import external as External

# Required to choose port on which the server runs
from tornado.options import define, options

# Default runs on port 8000
define('port', default = 8000, help = 'run on given port', type = int)

# Constants
CUSTOM_ERROR_MESSAGE = 'CUSTOM ERROR MESSAGE: '

# Application class for the Tornado server
class Application(tornado.web.Application):
	def __init__(self):
		conn = pymongo.Connection('localhost',  27017)
		self.db = conn['muzit']
		handlers = [
			(r'/', IndexHandler),
			(r'/upload', UploadHandler),
			(r'/top', TopHandler),
			(r'/new', NewHandler)
		]
		settings = dict(
			template_path = os.path.join(os.path.dirname(__file__), 'templates'),
			static_path = os.path.join(os.path.dirname(__file__), 'static'),
			ui_modules = {
				'SongEntry': Modules.SongEntryModule,
				'TitleEntry': Modules.TitleEntryModule
			},
			debug = True
		)
		tornado.web.Application.__init__(self, handlers, **settings)

# Class for the main page request handler which redirects to top
class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.redirect('/top')

# Class for the upload page request handler
class UploadHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			'upload.html',
			browserTitle = 'Muzit',
			errors = [],
			state = 2
		)

	def post(self):
		errors = []
		song = None
		fileData = self.request.files
		submitter = self.get_argument('submitter')
		songName = self.get_argument('songName')
		captchaRes = self.get_argument('g-recaptcha-response')

		if len(fileData) > 0:
			song = self.request.files['songFile'][0]
			if song['content_type'] != 'audio/mp3':
				logging.error(CUSTOM_ERROR_MESSAGE + 'Wrong file type')
				errors.append('Wrong file type')
		else:
			logging.error(CUSTOM_ERROR_MESSAGE + 'File not given')
			errors.append('File missing')

		if submitter == '':
			logging.error(CUSTOM_ERROR_MESSAGE + 'Name not given')
			errors.append('Username missing')

		if not External.correctCaptcha(captchaRes):
			logging.error(CUSTOM_ERROR_MESSAGE + 'Captcha error')
			errors.append('You are a robot')

		if len(errors) > 0:
			self.render(
				'upload.html',
				browserTitle = 'Muzit',
				errors = errors,
				state = 2
			)
		else:
			message = 'Successfully uploaded '
			if not songName == '':
				message = message + songName
			else:
				message = message + song['filename']
			self.render(
				'uploadThanks.html',
				browserTitle = 'Muzit',
				message = message,
				name = submitter,
				state = 2
			)

# Class for the top page request handler
class TopHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			'main.html',
			browserTitle = 'Muzit',
			titleEntry = 'Top',
			state = 0
		)

# Class for the new AJAX request handler
class NewHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			'main.html',
			browserTitle = 'Muzit',
			titleEntry = 'New',
			state = 1
		)

# If file was ran from command line, do the following
if __name__ == '__main__':

	# Parses command line for port
	tornado.options.parse_command_line();

	# Creates app, setting handlers and default paths
	httpServer = tornado.httpserver.HTTPServer(Application())
	httpServer.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()