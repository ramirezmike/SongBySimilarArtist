import argparse
import urllib
from BeautifulSoup import BeautifulSoup
import random
import json
import pexpect
import time
import re

argParser = argparse.ArgumentParser(description='Add Key.')
argParser.add_argument('key',type=str)
arguments = argParser.parse_args()
passedArtist = arguments.key.replace(' ','+')
lastfm_key = "&api_key=f30074d1365071a86b89594c8d583658" 
tinysong_key = "59f18b16a371c3d6090205c642fdf0f5"
lastFMUrl = 'http://ws.audioscrobbler.com/2.0/?method=artist.getSimilar&artist='
regex = '[Nn][Ii][Cc][Kk][Ee][Ll][Bb][Aa][Cc][Kk]'
ADD_SONG_TIMER = 5
MAX_SONG_ADD_TIME = 120
TIMER_INCREASE = 5

def jsonObjectCount(obj):
	count = 0
	for x in obj:
		count += 1
	return count

def createArtistList(artist,key):
	alist = []
	url = urllib.urlopen(lastFMUrl + artist + key)
	print "LastFM Opened"
	string_url = url.read()
	soup = BeautifulSoup(string_url)
	for tag in soup.findAll("name"):
		if tag(text=True):
			alist.append(tag.text.replace('&amp;','&'))
	alist.append(artist)
	print "Number of Artists added to List: %s"% len(alist)
	for name in alist:
		match = re.findall(regex,name)
		if (match):
			alist.remove('Nickelback')
			print "Nickelback removed"
	return alist

def randomArtistFromList(alist):
	randomIndexForArtistList = random.randint(0,len(alist)-1)
	randomArtist = alist[randomIndexForArtistList]
	randomArtist = randomArtist.replace(' ','+')
	return randomArtist

def IdForRandomSongByArtist(artist):
	print "TinySong Opening"
	try:
	    tinysongurl = urllib.urlopen("http://tinysong.com/s/" + str(artist).encode('utf-8') + "?format=json&limit=32&key=" + tinysong_key).read()
	except:
	    print "[Incompatible Encoding in URL]"
	    return '0'
	print "TinySong Opened"
	parsed_tinysongurl = json.loads(tinysongurl) 
	numberOfSongs = jsonObjectCount(parsed_tinysongurl)
	if (numberOfSongs == 0):
		return '0'
	randomIndexForSong = random.randint(0,numberOfSongs-1)
	print "Number of Songs:",
	print numberOfSongs
	pickedSong_id = parsed_tinysongurl[randomIndexForSong]['SongID']
	print str(pickedSong_id) + " Artist: ",
	try:
	    print str(parsed_tinysongurl[randomIndexForSong]['ArtistName']).encode('utf-8'),
	except:
	    print "[Incompatible Encoding]",
	print " Song: ",
	try:
	    print str(parsed_tinysongurl[randomIndexForSong]['SongName']).encode('utf-8')
	except:
	    print "[Incompatible Encoding]"
	print "This is the song ID:",
	print pickedSong_id
	return pickedSong_id


def setupBrowserController():
	controller = pexpect.spawn('/usr/bin/irb')
	controller.expect('>>')
	print 'Browser Controller Initiated'
	controller.sendline('require "watir-webdriver"')  
	controller.expect('>>')
	controller.sendline('browser = Watir::Browser.new :chrome')  
	controller.expect('>>')
	return controller

def javaCallAddNewRandomSong(controller,idNumber,songNumber):
	if (songNumber == 1):
#		scriptSetup(controller,idNumber)
		scriptSetup(controller,idNumber)
		return
	time.sleep(ADD_SONG_TIMER)
	idNumber = str(idNumber)
#	controller.sendline('browser.execute_script("javascript:window.Grooveshark.addSongsByID(%s,false);")'% idNumber)
#	controller.expect('>>')
#	time.sleep(5)
	controller.sendline('browser.execute_script("javascript:window.Grooveshark.addSongsByID([%s],false);")'% idNumber)
	controller.expect('>>')
	print controller.before
	return

def scriptSetup(controller,idNumber):
	setupPlaylistCall = 'browser.execute_script("javascript:window.Grooveshark.addSongsByID([' + str(idNumber) + '],true);")'
	print "Setting up script.." 
	time.sleep(ADD_SONG_TIMER)
	controller.sendline(setupPlaylistCall)
	controller.expect('>>')
	print controller.before
	return

def increaseWaitTime(time):
	if (time < MAX_SONG_ADD_TIME):
		time += TIMER_INCREASE 
	return time

artistList = createArtistList(passedArtist,lastfm_key)
browserController = setupBrowserController()
browserController.sendline('browser.goto "http://www.grooveshark.com"')  
browserController.expect('>>',120)

loop = 1
while (loop>0):
	idNumber = IdForRandomSongByArtist(randomArtistFromList(artistList))
	javaCallAddNewRandomSong(browserController,idNumber,loop)
	ADD_SONG_TIMER = increaseWaitTime(ADD_SONG_TIMER)
	loop += 1
