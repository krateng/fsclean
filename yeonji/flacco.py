#!/usr/bin/env python

import sys
import os
import re

def main():
	if (len(sys.argv) < 3):
		print("You need to specify a number and a title, son!")
		exit()

	try:
		num = int(sys.argv[1])
	except:
		print("That doesn't look like a valid number.")
		exit()

	if (" " in sys.argv[2]):
		title = sys.argv[2]	#if something was given in parantheses, it's probably meant to be the title even if there are more arguemnts
	else:
		title = " ".join(sys.argv[2:])
		
	convert = False

	if (os.path.exists("track" + str(num) + ".cdda.flac")):
		filename = "track" + str(num) + ".cdda.flac"
		numstr = str(num)
	elif (os.path.exists("track0" + str(num) + ".cdda.flac")):
		filename = "track0" + str(num) + ".cdda.flac"
		numstr = "0" + str(num)
	elif (os.path.exists("track00" + str(num) + ".cdda.flac")):
		filename = "track00" + str(num) + ".cdda.flac"
		numstr = "00" + str(num)
		
		
	elif (os.path.exists("track" + str(num) + ".cdda.wav")):
		filename = "track" + str(num) + ".cdda.wav"
		numstr = str(num)
		convert = True
	elif (os.path.exists("track0" + str(num) + ".cdda.wav")):
		filename = "track0" + str(num) + ".cdda.wav"
		numstr = "0" + str(num)
		convert = True
	elif (os.path.exists("track00" + str(num) + ".cdda.wav")):
		filename = "track00" + str(num) + ".cdda.wav"
		numstr = "00" + str(num)
		convert = True
		

		
		
	else:
		print("File could not be found. Are you sure you ripped this with cdparanoia?")
		exit()

	unixtitle = title.replace(" - ","-").replace(" ",".")
	unixtitle = ''.join(c for c in unixtitle if (c.isalpha() or c=="_" or c=="-" or c=="."))
	outputfilename = numstr + "." + unixtitle + ".flac"


	if (convert):
		print("Recoding WAV file...")
		os.system("ffmpeg -i " + filename + " " + outputfilename)
	else:
		os.rename(filename,outputfilename)
		
		
	print("Tagging flac file...")
	os.system("metaflac --set-tag=TITLE='" + title + "' " + outputfilename)

	print("All done!")