import argparse
import urllib
from BeautifulSoup import BeautifulSoup
import random
import json
parser = argparse.ArgumentParser(description='Add Key.')
parser.add_argument('key',type=str)
arguments = parser.parse_args()
lastfm_key = arguments.key

artistList = []
url = urllib.urlopen("http://ws.audioscrobbler.com/2.0/?method=artist.getSimilar&artist=kate+nash&api_key=" + lastfm_key)
string_url = url.read()
soup = BeautifulSoup(string_url)
print "soup made"
for tag in soup.findAll("name"):
	if tag(text=True):
		artistList.append(tag.text.replace('&amp;','&'))

randomIndex = random.randint(0,len(artistList)-1)
randomArtist = artistList[randomIndex]
randomArtist = randomArtist.replace(' ','+')
tinysongurl = urllib.urlopen("http://tinysong.com/s/" + randomArtist + "?format=json&limit=1&key=59f18b16a371c3d6090205c642fdf0f5").read()
print tinysongurl
parsed_tinysongurl = json.loads(tinysongurl) 
pickedSong_url = parsed_tinysongurl[0]['Url']
print pickedSong_url
