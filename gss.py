import urllib
from BeautifulSoup import BeautifulSoup
import random

artistList = []
url = urllib.urlopen("http://ws.audioscrobbler.com/2.0/?method=artist.getSimilar&artist=kate+nash&api_key=f30074d1365071a86b89594c8d583658")
string_url = url.read()
url.close()
soup = BeautifulSoup(string_url)
print "soup made"
for tag in soup.findAll("name"):
	if tag(text=True):
		artistList.append(tag.text.replace('&amp;','&'))

randomIndex = random.randint(0,len(artistList)-1)
print artistList[randomIndex]
