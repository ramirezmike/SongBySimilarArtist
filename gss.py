import argparse
import urllib
from BeautifulSoup import BeautifulSoup
import random
import json
import pexpect
import time

argParser = argparse.ArgumentParser(description='Add Key.')
argParser.add_argument('key',type=str)
arguments = argParser.parse_args()
passedArtist = arguments.key.replace(' ','+')
print passedArtist
lastfm_key = "f30074d1365071a86b89594c8d583658" 
artistList = []

def createArtistList(artist,key):
	alist = []
	print "LastFM Opening"
	url = urllib.urlopen("http://ws.audioscrobbler.com/2.0/?method=artist.getSimilar&artist=" + artist + "&api_key=" + key)
	print "LastFM Opened"
	string_url = url.read()
	soup = BeautifulSoup(string_url)
	print "Soup Made"
	for tag in soup.findAll("name"):
		if tag(text=True):
			alist.append(tag.text.replace('&amp;','&'))
	return alist

def randomArtistFromList(alist):
	randomIndexForArtistList = random.randint(0,len(alist)-1)
	randomArtist = alist[randomIndexForArtistList]
	randomArtist = randomArtist.replace(' ','+')
	return randomArtist

def URLForRandomSongByArtist(artist):
	print "TinySong Opening"
	tinysongurl = urllib.urlopen("http://tinysong.com/s/" + artist + "?format=json&limit=1&key=59f18b16a371c3d6090205c642fdf0f5").read()
	print "TinySong Opened"
	parsed_tinysongurl = json.loads(tinysongurl) 
	print parsed_tinysongurl
	pickedSong_url = parsed_tinysongurl[0]['Url']
	print pickedSong_url
	return pickedSong_url


browserController = pexpect.spawn('/usr/bin/irb')
browserController.expect('>>')
print 'Browser Controller Initiated'
browserController.sendline('require "watir-webdriver"')  
browserController.expect('>>')
browserController.sendline('browser = Watir::Browser.new :ff')  
browserController.expect('>>')
browserController.sendline('browser.goto "' + URLForRandomSongByArtist(randomArtistFromList(createArtistList(passedArtist,lastfm_key)))+ '"')  
browserController.expect('>>')
time.sleep(20)
browserController.sendline('browser.execute_script("javascript:window.Grooveshark.addSongsByID(21104374,false);")')
print "First Javascript Insertion"
time.sleep(10)
browserController.expect('>>')
browserController.sendline('browser.execute_script("javascript:window.Grooveshark.addSongsByID(21104374,false);")')
browserController.expect('>>')
print "Second Javascript Insertion"
time.sleep(10)
browserController.sendline('browser.execute_script("javascript:window.Grooveshark.addSongsByID(21104374,false);")')
browserController.expect('>>')
print "Third Javascript Insertion"
time.sleep(10)
browserController.sendline('browser.execute_script("javascript:window.Grooveshark.addSongsByID(21104374,false);")')
browserController.expect('>>')
print "Fourth Javascript Insertion"
