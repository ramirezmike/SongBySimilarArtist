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
lastfm_key = "f30074d1365071a86b89594c8d583658" 

def jsonObjectCount(obj):
	count = 0
	for x in obj:
		count += 1
	return count

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
	alist.append(artist)
	print "Number of Artists added to List: %s"% len(alist)
	return alist

def randomArtistFromList(alist):
	randomIndexForArtistList = random.randint(0,len(alist)-1)
	randomArtist = alist[randomIndexForArtistList]
	randomArtist = randomArtist.replace(' ','+')
	return randomArtist

def IdForRandomSongByArtist(artist):
	print "TinySong Opening"
	tinysongurl = urllib.urlopen("http://tinysong.com/s/" + artist + "?format=json&limit=32&key=59f18b16a371c3d6090205c642fdf0f5").read()
	print "TinySong Opened"
	parsed_tinysongurl = json.loads(tinysongurl) 
	numberOfSongs = jsonObjectCount(parsed_tinysongurl)
	randomIndexForSong = random.randint(0,numberOfSongs-1)
	print "Number of Songs:",
	print numberOfSongs
	pickedSong_id = parsed_tinysongurl[randomIndexForSong]['SongID']
	print str(pickedSong_id) + " Artist: ",
	print str(parsed_tinysongurl[randomIndexForSong]['ArtistName']),
	print " Song: ",
	print str(parsed_tinysongurl[randomIndexForSong]['SongName'])
	print "This is the song ID:",
	print pickedSong_id
	return pickedSong_id


def setupBrowserController():
	controller = pexpect.spawn('/usr/bin/irb')
	controller.expect('>>')
	print 'Browser Controller Initiated'
	controller.sendline('require "watir-webdriver"')  
	controller.expect('>>')
	controller.sendline('browser = Watir::Browser.new :ff')  
	controller.expect('>>')
	return controller

def javaCallAddNewRandomSong(controller,idNumber,songNumber):
	if (songNumber == 1):
		scriptSetup(controller,idNumber)
		scriptSetup(controller,idNumber)
		return
	time.sleep(10)
	idNumber = str(idNumber)
	controller.sendline('browser.execute_script("javascript:window.Grooveshark.addSongsByID(%s,false);")'% idNumber)
	controller.expect('>>')
	time.sleep(5)
	controller.sendline('browser.execute_script("javascript:window.Grooveshark.addSongsByID(%s,false);")'% idNumber)
	controller.expect('>>')
	print controller.before
	return

def scriptSetup(controller,idNumber):
	test = 'browser.execute_script("javascript:window.Grooveshark.addSongsByID(' + str(idNumber) + ',true);")'
	print "Setting up script.." 
	time.sleep(20)
	controller.sendline(test)
	controller.expect('>>')
	print controller.before
	return

artistList = createArtistList(passedArtist,lastfm_key)
browserController = setupBrowserController()
browserController.sendline('browser.goto "http://www.grooveshark.com"')  
browserController.expect('>>',120)

loop = 1
while (loop>0):
	idNumber = IdForRandomSongByArtist(randomArtistFromList(artistList))
	javaCallAddNewRandomSong(browserController,idNumber,loop)
	loop += 1
