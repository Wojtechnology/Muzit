
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

# Required Tornado imports
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop

# Import for pymongo
import pymongo 

# Self written Tornado imports
import modules as Modules
import handlers as Handlers

# Required to set paths for templates and static files
import os.path

# Required to choose port on which the server runs
from tornado.options import define, options

# Default runs on port 8000
define('port', default = 8000, help = 'run on given port', type = int)

# Application class for the Tornado server
class Application(tornado.web.Application):
	def __init__(self):
		conn = pymongo.Connection('localhost',  27017)
		self.db = conn['muzit']
		handlers = [
			(r'/', Handlers.IndexHandler),
			(r'/upload', Handlers.UploadHandler)
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

# If file was ran from command line, do the following
if __name__ == '__main__':

	# Parses command line for port
	tornado.options.parse_command_line();

	# Creates app, setting handlers and default paths
	httpServer = tornado.httpserver.HTTPServer(Application())
	httpServer.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()