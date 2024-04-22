#!/usr/bin/python3

import os
import sys
import re
from pytube import YouTube

class Sanitizer(object):
	def __init__(self, outdir):
		self.outdir = outdir
		
	def handle_defaults_song(self, dl_request_data):
		yt = YouTube(dl_request_data["video_url"])

		if dl_request_data["title"] == "title":
			dl_request_data["title"] = yt.title
		if dl_request_data["artist"] == "artist":
			dl_request_data["artist"] = yt.author
		if dl_request_data["genre"] == "genre":
			dl_request_data["genre"] = None
		if dl_request_data["year"] == "year":
			dl_request_data["year"] = None
		if dl_request_data["file_name"] == "filename":
			if "-" in dl_request_data["title"]:
				s = dl_request_data["title"].split(" - ")
				x = re.sub("[\(\[].*?[\)\]]", "", s[1])
				sanitized_title = x.strip()
				file_name = "{}.mp3".format(sanitized_title)
				dl_request_data["file_name"] = file_name

			else:
				x = re.sub("[\(\[].*?[\)\]]", "", dl_request_data["title"])
				sanitized_title = x.strip()
				file_name = "{}.mp3".format(sanitized_title)
				dl_request_data["file_name"] = file_name

		return dl_request_data
