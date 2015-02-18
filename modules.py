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
import time

# Template for the song entry module
class SongEntryModule(tornado.web.UIModule):
	def render(self, song):
		when = ''
		now = time.time()

		if time.time() - song['time'] > 86400:
			when = time.asctime(time.localtime(song['time']))
		elif time.time() - song['time'] > 3600:
			when = str(int(round((time.time() - song['time']) / 3600))) + ' hours ago'
		elif time.time() - song['time'] > 60:
			when = str(int(round((time.time() - song['time']) / 60))) + ' minutes ago'
		else:
			when = str(int(round(time.time() - song['time']))) + ' seconds ago'

		self.userID = str(song['_id'])

		return self.render_string('modules/songEntry.html', song = song, time = when, userID = self.userID)

# Template for the title entry module
class TitleEntryModule(tornado.web.UIModule):
	def render(self, icon, title):
		return self.render_string('modules/titleEntry.html', title = title, icon = icon)