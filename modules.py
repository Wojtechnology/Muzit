##########################################
#
# Author: Wojtek Swiderski
# 
# File containing all modules required for the application
# Application for uploading and listening to music
#
# Last Update: February 16th, 2015
#
##########################################

# Required Tornado import
import tornado.web

# Template for the song entry module
class SongEntryModule(tornado.web.UIModule):
	def render(self):
		return self.render_string('modules/songEntry.html')

# Template for the title entry module
class TitleEntryModule(tornado.web.UIModule):
	def render(self, title):
		return self.render_string('modules/titleEntry.html', title = title)