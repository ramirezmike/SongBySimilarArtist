import urllib
from BeautifulSoup import BeautifulSoup

url = urllib.urlopen("http://ws.audioscrobbler.com/2.0/?method=artist.getSimilar&artist=kate+nash&api_key=f30074d1365071a86b89594c8d583658")
string_url = url.read()
url.close()
soup = BeautifulSoup(string_url)
print "soup made"
print soup
for tag in soup.findAll("name"):
	if tag(text=True):
		print tag.text.replace('&amp;','&')
