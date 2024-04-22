#!/usr/bin/python3

"""
Song Ripper
v0.1
By Brandon REDACTED

A tool for stealing music from YouTube ;)
"""

import os
import sys
import getopt
import re
import subprocess
import threading
import eyed3
from pytube import YouTube

class SongRipper(object):
	def __init__(self, song):
		self.song = song
		
	def _fetch_song(self):
		yt = YouTube(self.song["video_url"])
		audio_stream = yt.streams.filter(only_audio=True).first()
		raw_audio_file = audio_stream.download()

		convert_command = """ffmpeg -hide_banner -loglevel error -i "{0}" "{1}" """.format(raw_audio_file, self.song["file_name"])
		subprocess.check_output(convert_command, shell=True)
		os.remove(raw_audio_file)

		open_mp3_file = eyed3.load(self.song["file_name"])
		open_mp3_file.initTag(version=(2, 3, 0))
		if self.song["thumbnail"] != None:
			with open(thumbnail_file, "rb") as tf:
				raw_thumb = tf.read()
			open_mp3_file.tag.images.set(3, raw_thumb, "image/jpeg", "cover")
		open_mp3_file.tag.title = self.song["title"]
		open_mp3_file.tag.artist = self.song["artist"]
		if self.song["genre"] != None:
			open_mp3_file.tag.genre = self.song["genre"]
		if self.song["year"] != None:
			format_year = eyed3.core.Date(int(self.song["release_year"]))
			open_mp3_file.tag.recording_date = format_year
		open_mp3_file.tag.save()

	def begin(self, script_mode=True):
		# Change to download directory
		os.chdir(self.song["directory"])

		# If in script mode, show banner
		if script_mode == True:
			os.system("clear")
			print("##### Song Ripper #####")
			print("----------")
			print("[I] Beginning rip of song: {}".format(self.song["title"]))
			print("\t[i] Artist: {0} | Genre: {1} | Year: {2}".format(self.song["artist"], self.song["genre"], self.song["release_year"]))
			print("\t[i] Download Directory: {}".format(self.song["directory"]))
			print("----------")

		new_thread = threading.Thread(target=self._fetch_song)
		new_thread.start()
		new_thread.join()

		dl_status = {
			"status": "Success",
			"downloaded_file_location": os.path.join(self.song["directory"], self.song["file_name"])
		}

		# If in script mode, show banner
		if script_mode == True: 
			print("----------")
			print("[!!!] Done!")

		return dl_status

def main(outdir, playlist_url):
	""" Prompt for user input and initialize download

	Arguments:
	outdir - Directory to output to
	video_url - URL to YouTube video
	"""
	yt = YouTube(video_url)

	os.system("clear")
	print("##### Song Ripper #####")
	print("----------")
	print("[I] Preparing to rip song from YouTube video: {}".format(yt.title))
	print("\t[i] Video URL: {}".format(video_url))
	print("----------")
	print("(Please provide song metadata. Leave blank to auto-populate.)")
	song_title = input("\t[?] Song Title: ") or yt.title
	song_artist = input("\t[?] Artist: ") or yt.owner
	song_genre = input("\t[?] Genre: ") or None
	song_year = input("\t[?] Year: ") or None
	song_thumbnail = input("\t[?] Thumbnail File: ") or None

	if " - " in yt.title:
		s = yt.title.split(" - ")
		x = re.sub("[\(\[].*?[\)\]]", "", s[1])
		song_title = x.strip()
		song_file_name = "{0} - {1}.mp3".format(song_artist, song_title)

	else:
		x = re.sub("[\(\[].*?[\)\]]", "", yt.title)
		song_title = x.strip()
		song_file_name = "{0} - {1}.mp3".format(song_artist, song_title)	

	song = {
		"source_video_url": video_url,
		"directory": outdir,
		"file_name": song_file_name,
		"thumbnail": song_thumbnail,
		"title": song_title,
		"artist": song_artist,
		"genre": song_genre,
		"release_year": song_year
	}

	ripper = SongRipper(song)
	print("(Thank you. Press [ENTER] to continue or Ctrl-C to quit.)")
	input()
	ripper.begin()

# Begin execution
if __name__ == "__main__":
	opts, args = getopt.getopt(sys.argv[1:], "ho:u:", ["help", "outdir=", "url="])

	outdir = os.getcwd()
	playlist_url = None

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print("USAGE:")
			print("\tsong_ripper.py [-h] [-o OUTDIR] video_URL")
			exit(0)

		elif opt in ("-o", "--outdir"):
			outdir = arg

		elif opt in ("-u", "--url"):
			playlist_url = arg

	main(outdir, playlist_url)

