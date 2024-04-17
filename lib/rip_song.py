# lib/rip_song.py
# Download and convert/tag songs from a YouTube video

import os
import sys
import threading
import subprocess
import pytube
import eyed3

class SongRipper(object):
	def __init__(self, dl_request_data):
		# Check for default values
		if dl_request_data["filetype"] == "filetype" or dl_request_data["filename"] == "filename":
			dl_request_data["filetype"] = "mp3"
			dl_request_data["filename"] = None
			
		self.dl_request_data = dl_request_data
		
def download(dl_request_data):
	""" Handle download requests from the webapp or API and return
	a JSON response
	
	Arguments:
		dl_request_data - dict - Contains the video URL and file/tag info
	"""
	
	# Create a new SongRipper
	ripper = SongRipper(dl_request_data)
