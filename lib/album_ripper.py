#!/usr/bin/python3

"""
Album Ripper
v0.2
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
from pytube import YouTube, Playlist

class AlbumRipper(object):
  def __init__(self, album):
    self.album = album
    
  def _fetch_song(self, song):
    yt = YouTube(song["video_url"])
    audio_stream = yt.streams.filter(only_audio=True).first()
    raw_audio_file = audio_stream.download()
    
    convert_command = """ffmpeg -hide_banner -loglevel error -i "{0}" "{1}" """.format(raw_audio_file, song["file_name"])
    subprocess.check_output(convert_command, shell=True)
    os.remove(raw_audio_file)
    
    open_mp3_file = eyed3.load(song["file_name"])
    open_mp3_file.initTag(version=(2, 3, 0))
    if self.album["thumbnail"] != None:
      with open(thumbnail_file, "rb") as tf:
        raw_thumb = tf.read()
      open_mp3_file.tag.images.set(3, raw_thumb, "image/jpeg", "cover")
    open_mp3_file.tag.title = song["title"]
    open_mp3_file.tag.artist = self.album["artist"]
    open_mp3_file.tag.album = self.album["name"]
    open_mp3_file.tag.genre = self.album["genre"]
    open_mp3_file.tag.track_num = song["track_no"]
    format_year = eyed3.core.Date(int(self.album["release_year"]))
    open_mp3_file.tag.recording_date = format_year
    open_mp3_file.tag.save()
  
  def begin(self):
    os.chdir(self.album["directory"])
    os.system("clear")
    print("##### Album Ripper #####")
    print("----------")
    print("[I] Beginning rip of album: {}".format(self.album["name"]))
    print("\t[i] Artist: {0} | Genre: {1} | Year: {2}".format(self.album["artist"], self.album["genre"], self.album["release_year"]))
    print("\t[i] Track Count: {}".format(len(self.album["songs"])))
    print("\t[i] Album Directory: {}".format(self.album["directory"]))
    print("----------")
    
    tl = []
    for song in self.album["songs"]:
      print(">Starting download thread for song: {}".format(song["title"]))
      new_thread = threading.Thread(target=self._fetch_song, args=(song,))
      tl.append(new_thread)
    for thread in tl:
      thread.start()
    for thread in tl:
      thread.join()
      
    print("----------")
    print("[!!!] Done!")
  
def main(outdir, playlist_url):
  """ Prompt for user input and initialize download
  
  Arguments:
    outdir - Directory to output to
    playlist_url - URL to YouTube Playlist
  """
  pl = Playlist(playlist_url)
  
  os.system("clear")
  print("##### Album Ripper #####")
  print("----------")
  print("[I] Preparing to rip album from YouTube Playlist: {}".format(pl.title))
  print("\t[i] Playlist URL: {}".format(playlist_url))
  print("----------")
  print("(Please provide album metadata. Leave blank to auto-populate.)")
  album_name = input("\t[?] Album Name: ") or pl.title
  album_artist = input("\t[?] Artist: ") or pl.owner
  album_genre = input("\t[?] Genre: ") or None
  album_year = input("\t[?] Year: ") or None
  album_thumbnail = input("\t[?] Thumbnail File: ") or None
   
  album_dir = os.path.join(outdir, album_name)
  os.mkdir(album_dir)

  album = {
    "source_playlist_url": playlist_url,
    "directory": album_dir,
    "thumbnail": album_thumbnail,
    "name": album_name,
    "artist": album_artist,
    "genre": album_genre,
    "release_year": album_year,
    "songs": []
  }
  
  tn = 1
  for url in pl.video_urls:
    yt = YouTube(url)
    if " - " in yt.title:
      s = yt.title.split(" - ")
      x = re.sub("[\(\[].*?[\)\]]", "", s[1])
      song_title = x.strip()
      song_file_name = "{0}. {1}.mp3".format(tn, song_title)
    
    else:
      x = re.sub("[\(\[].*?[\)\]]", "", yt.title)
      song_title = x.strip()
      song_file_name = "{0}. - {1}.mp3".format(track_num, song_title)
      
    song = {
      "video_url": url,
      "file_name": song_file_name,
      "track_no": tn,
      "title": song_title
    }
    album["songs"].append(song)
    
    tn = tn + 1
    
  ripper = AlbumRipper(album)
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
      print("\talbum_ripper.py [-h] [-o OUTDIR] PLAYLIST_URL")
      exit(0)
      
    elif opt in ("-o", "--outdir"):
      outdir = arg
      
    elif opt in ("-u", "--url"):
      playlist_url = arg
    
  main(outdir, playlist_url)
