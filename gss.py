import argparse
import urllib
from BeautifulSoup import BeautifulSoup
import random
parser = argparse.ArgumentParser(description='Add Key.')
parser.add_argument('key',type=str)
arguments = parser.parse_args()
lastfm_key2 = 'f30074d1365071a86b89594c8d583658'
lastfm_key = arguments.key

artistList = []
url = urllib.urlopen("http://ws.audioscrobbler.com/2.0/?method=artist.getSimilar&artist=kate+nash&api_key=" + lastfm_key)
string_url = url.read()
url.close()
soup = BeautifulSoup(string_url)
print "soup made"
for tag in soup.findAll("name"):
	if tag(text=True):
		artistList.append(tag.text.replace('&amp;','&'))

randomIndex = random.randint(0,len(artistList)-1)
randomArtist = artistList[randomIndex]
print randomArtist
