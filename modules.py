##########################################
#
# Author: Wojtek Swiderski
# 
# Main file for tornado server
# Application for uploading and listening to music
#
# Last Update: February 13th, 2015
#
##########################################

# Required Tornado import
import tornado.web

class SongEntryModule(tornado.web.UIModule):
	def render(self):
		return self.render_string('modules/songEntry.html')