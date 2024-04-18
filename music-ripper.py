#!/usr/bin/python3

"""
Music Ripper

A tool for stealing music from YouTube
"""

import os
import sys
import flask
from lib import rip_song
from lib import rip_album

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
    
    dl_request_data = {
        "video_url": flask.request.form["video_url"],
        "filetype": flask.request.form["filetype"],
        "filename": flask.request.form["filename"],
        "metadata": {
            "title": flask.request.form["title"],
            "artist": flask.request.form["artist"],
        }
    }

    api_response = rip_song.download(dl_request_data)
    return api_response

@app.route("/api/endpoint/rip-album", methods=["POST"])
def endpoint_rip_album():
    """ API endpoint for downloading albums
    
    Arguments:
        None
    """

    dl_request_data = {
        "playlist_url": flask.request.form["playlist_url"],
        "filetype": flask.request.form["filetype"],
        "filename": flask.request.form["filename"],
        "metadata": {
            "title": flask.request.form["title"],
            "artist": flask.request.form["artist"],
        }
    }

    api_response = rip_album.download(dl_request_data)
    return api_response
    
