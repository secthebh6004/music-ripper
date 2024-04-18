# lib/rip_song.py
# Download and convert/tag songs from a YouTube video

import os
import sys
import threading
import subprocess
from pytube import YouTube

class SongRipper(object):
	def __init__(self, dl_request_data):
		# Check for default values
		if dl_request_data["filetype"] == "filetype" or dl_request_data["filename"] == "filename":
			dl_request_data["filetype"] = "mp3"
			dl_request_data["filename"] = None
			
		self.dl_request_data = dl_request_data
		
	def download(self):
		yt = YouTube(self.dl_request_data["video_url"])
		dl_path = os.getcwd()
		
		# Fetch tag data if defaults used
		if self.dl_request_data["metadata"]["title"] == "title" or self.dl_request_data["metadata"]["artist"] == "artist":
			self.dl_request_data["metadata"]["title"] = yt.title
			self.dl_request_data["metadata"]["artist"] = None
			
		audio_stream = yt.streams.filter(only_audio = True).first()
		
		if self.dl_request_data["filename"] != None:
			file_dl = audio_stream.download(output_path = self.dl_request_data["filename"])
			
		else:
			file_dl = audio_stream.download()
		
		api_response = "<p>{}</p>".format(file_dl)
		return api_response
		
def download(dl_request_data):
	""" Handle download requests from the webapp or API and return
	a JSON response
	
	Arguments:
		dl_request_data - dict - Contains the video URL and file/tag info
	"""
	
	# Create a new SongRipper
	ripper = SongRipper(dl_request_data)
	api_response = ripper.download()
	return api_response
