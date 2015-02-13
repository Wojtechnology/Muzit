##########################################
#
# Author: Wojtek Swiderski
# 
# File containing all modules required for the application
# Application for uploading and listening to music
#
# Last Update: February 13th, 2015
#
##########################################

# Required Tornado import
import tornado.web

# Template for the song entry module
class SongEntryModule(tornado.web.UIModule):
	def render(self):
		return self.render_string('modules/songEntry.html')