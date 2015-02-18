
##########################################
#
# Author: Wojtek Swiderski
# 
# Main file for tornado server
# Application for uploading and listening to music
#
# Last Update: February 17th, 2015
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
import time
import json
import bson

# 1st party imports
import modules as Modules
import external as External
import file as File

# Required to choose port on which the server runs
from tornado.options import define, options

# Default runs on port 8000
define('port', default = 8000, help = 'run on given port', type = int)

# Constants
CUSTOM_ERROR_MESSAGE = 'MAIN.PY ERROR MESSAGE: '

# Application class for the Tornado server
class Application(tornado.web.Application):
	def __init__(self):
		conn = pymongo.Connection('localhost',  27017)
		self.db = conn['muzit']
		handlers = [
			(r'/', TopHandler),
			(r'/upload', UploadHandler),
			(r'/top', TopHandler),
			(r'/new', NewHandler),
			(r'/vote', VoteHandler)
		]
		settings = dict(
			template_path = os.path.join(os.path.dirname(__file__), 'templates'),
			static_path = os.path.join(os.path.dirname(__file__), 'static'),
			ui_modules = {
				'SongEntry': Modules.SongEntryModule,
				'TitleEntry': Modules.TitleEntryModule
			},
			cookie_secret = 'wwaApJxeTnmzwC5vFjkWsPfYhPjKyUyNio8YwLZj81o=',
			xsrf_cookies = True,
			debug = True
		)
		tornado.web.Application.__init__(self, handlers, **settings)

# Class for the upload page request handler
class UploadHandler(tornado.web.RequestHandler):
	def get(self):
		self.xsrf_token
		self.render(
			'upload.html',
			browserTitle = 'Muzit',
			errors = [],
			icon = 'cloud-upload',
			state = 2
		)

	def post(self):
		errors = []
		song = None
		fileData = self.request.files
		submitter = self.get_argument('submitter', '')
		songName = self.get_argument('songName', '')
		captchaRes = self.get_argument('g-recaptcha-response', '')

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
				icon = 'cloud-upload',
				state = 2
			)
		else:

			status = {
				'icon': 'check-circle',
				'color': 'green',
				'message': 'Successfully uploaded '
			}

			filePath = File.saveMusicFile(song['body'], song['filename'], song['content_type'])

			if filePath == 'file.error':
				status['icon'] = 'minus-circle'
				status['color'] = 'red'
				status['message'] = 'Failure uploading '

			else:
				if songName == '':
					songName = song['filename'][:-4]

				songObj = {
					'songName': songName,
					'userName': submitter,
					'time': time.time(),
					'filePath': filePath,
					'rating': 0
				}

				songs = self.application.db.songs
				songs.insert(songObj)

			self.render(
				'uploadStatus.html',
				browserTitle = 'Muzit',
				message = status['message'] + songName,
				name = submitter,
				icon = 'cloud-upload',
				status = status,
				state = 2
			)

# Class for the top page request handler
class TopHandler(tornado.web.RequestHandler):
	def get(self):
		self.xsrf_token
		songs = self.application.db.songs.find().sort('rating', pymongo.DESCENDING)
		voteList = self.get_secure_cookie('voteList')
		voteList = json.loads(voteList) if voteList else dict()
		self.render(
			'main.html',
			browserTitle = 'Muzit',
			titleEntry = 'Top',
			icon = 'trophy',
			songs = songs,
			voteList = voteList,
			state = 0
		)

# Class for the new AJAX request handler
class NewHandler(tornado.web.RequestHandler):
	def get(self):
		self.xsrf_token
		songs = self.application.db.songs.find().sort('time', pymongo.DESCENDING)
		voteList = self.get_secure_cookie('voteList')
		voteList = json.loads(voteList) if voteList else dict()
		self.render(
			'main.html',
			browserTitle = 'Muzit',
			titleEntry = 'New',
			icon = 'star',
			songs = songs,
			voteList = voteList,
			state = 1
		)

# Class for voting, keeping track of who has voted using secure cookies
class VoteHandler(tornado.web.RequestHandler):
	def post(self):
		voteList = self.get_secure_cookie('voteList')
		voteList = json.loads(voteList) if voteList else dict()
		userID = self.get_argument('userID', '')
		type = self.get_argument('type', '')
		song = self.application.db.songs.find_one({'_id': bson.ObjectId(userID)})
		if not song:
			logging.error(CUSTOM_ERROR_MESSAGE + 'Could not find song')
		if not voteList.get(userID):
			voteList[userID] = 1 if type == 'up' else -1
			song['rating'] = song['rating'] + 1 if type == 'up' else song['rating'] - 1
		elif voteList[userID] == 1 and type == 'down':
			voteList[userID] = -1
			song['rating'] = song['rating'] - 2
		elif voteList[userID] == -1 and type == 'up':
			voteList[userID] = 1
			song['rating'] = song['rating'] + 2
		print song['rating']
		self.set_secure_cookie('voteList', json.dumps(voteList))
		self.application.db.songs.save(song)
		self.write(str(song['rating']))

# If file was ran from command line, do the following
if __name__ == '__main__':

	# Parses command line for port
	tornado.options.parse_command_line();

	# Creates app, setting handlers and default paths
	httpServer = tornado.httpserver.HTTPServer(Application())
	httpServer.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()