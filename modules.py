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
import datetime
import json

# Template for the song entry module
class SongEntryModule(tornado.web.UIModule):
	def render(self, song, voteList):
		when = ''
		now = time.time()

		if time.time() - song['time'] > 86400:
			when = datetime.datetime.fromtimestamp(int(song['time'])).strftime('%Y-%m-%d')
		elif time.time() - song['time'] > 3600:
			when = str(int(round((time.time() - song['time']) / 3600))) + ' hours ago'
		elif time.time() - song['time'] > 60:
			when = str(int(round((time.time() - song['time']) / 60))) + ' minutes ago'
		else:
			when = str(int(round(time.time() - song['time']))) + ' seconds ago'

		userID = str(song['_id'])
		preVote = voteList[userID] if voteList.get(userID) else 0

		return self.render_string('modules/songEntry.html', song = song, time = when, userID = userID, preVote = preVote)

# Template for the title entry module
class TitleEntryModule(tornado.web.UIModule):
	def render(self, icon, title):
		return self.render_string('modules/titleEntry.html', title = title, icon = icon)