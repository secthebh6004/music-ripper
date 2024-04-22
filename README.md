# Music Ripper
## Version 0.1 Beta
A tool for stealing music from YouTube based off the Song Ripper and Album Ripper scripts. Runs as a Flask web application accessible 
via web browser. Currently still in beta, so not all functionality has been implemented yet. 

### Usage
**Web Application**
To start the Music Ripper webapp, you can use the following command:
`$ python3 -m flask --app music-ripper run`

**Song Ripper Script**
The Song Ripper script is stored in `lib/song_ripper.py`. For script usage:
`$ python3 lib/song_ripper.py -h`

**Album Ripper Script**
Likewise, the Album Ripper script can be found at `lib/album_ripper.py`. For usage:
`$ python3 lib/album_ripper.py -h`

