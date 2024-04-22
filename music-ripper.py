#!/usr/bin/python3

"""
Music Ripper
Version 0.1 Beta
By Brandon Hammond

A tool for stealing music from YouTube
"""

import os
import sys
import flask
from lib import song_ripper
from lib import album_ripper
from lib import sanitize_inputs

# Create the Flask application and define routes
app = flask.Flask(__name__)

@app.route("/")
def index():
	""" Index page with HTML download form

	Arguments:
	None
	"""

	return flask.render_template("index.html")

@app.route("/api/endpoints/rip-song", methods=["POST"])
def endpoint_rip_song():
	""" API endpoint for downloading songs

	Arguments:
	None
	"""

	# Get the form data from Flask and sanitize
	sanitizer = sanitize_inputs.Sanitizer(os.getcwd())
	dl_request_data = {
		"video_url": flask.request.form["video_url"],
		"file_name": flask.request.form["filename"],
		"title": flask.request.form["title"],
		"artist": flask.request.form["artist"],
		"genre": flask.request.form["genre"],
		"year": flask.request.form["year"]
	}
	dl_request_data = sanitizer.handle_defaults_song(dl_request_data)

	# Format the data for the song ripper
	song = {
		"video_url": dl_request_data["video_url"],
		"directory": os.getcwd(),
		"file_name": dl_request_data["file_name"],
		"full_path": None,
		"thumbnail": None,
		"title": dl_request_data["title"],
		"artist": dl_request_data["artist"],
		"genre": None,
		"release_year": None
	}

	# Create a new song ripper
	ripper = song_ripper.SongRipper(song)
	dl_status = ripper.begin(script_mode=False)

	# Return a response
	return dl_status

@app.route("/api/endpoint/rip-album", methods=["POST"])
def endpoint_rip_album():
	""" API endpoint for downloading albums

	Arguments:
	None
	"""

	return "<h1>Music Ripper Beta Version (0.1)</h1><br /><p>Feature not implemented yet!<p>"



