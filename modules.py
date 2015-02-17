##########################################
#
# Author: Wojtek Swiderski
# 
# File containing all modules required for the application
# Application for uploading and listening to music
#
# Last Update: February 17th, 2015
#
##########################################

# 3rd party imports
import tornado.web

# Template for the song entry module
class SongEntryModule(tornado.web.UIModule):
	def render(self):
		return self.render_string('modules/songEntry.html')

# Template for the title entry module
class TitleEntryModule(tornado.web.UIModule):
	def render(self, icon, title):
		return self.render_string('modules/titleEntry.html', title = title, icon = icon)