##########################################
#
# Author: Wojtek Swiderski
# 
# File containing file management functions for the server
# Application for uploading and listening to music
#
# Last Update: February 17th, 2015
#
##########################################

# 3rd party imports
import logging
import os.path
import string

# Constants
CUSTOM_ERROR_MESSAGE = 'FILE.PY ERROR MESSAGE: '
MUSIC_PATH = 'static/music/'

# Function to save music files on server
def saveMusicFile(data, fileName, type):
	if type == 'audio/mp3':
		counter = 0
		for char in '!@#$':
			fileName = fileName.replace(char, '')
		songName = fileName[:-4]
		while os.path.isfile(MUSIC_PATH + fileName):
			fileName = songName + unicode(counter) + fileName[-4:]
			counter = counter + 1
		musicFile = open(MUSIC_PATH + fileName, 'w')
		musicFile.write(data)
		musicFile.close()
		return fileName

	else:
		logging.error(CUSTOM_ERROR_MESSAGE + 'Did not recognize file type')
		return 'file.error'