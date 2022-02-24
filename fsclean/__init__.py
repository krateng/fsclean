import os
import re
import string
import hashlib
import yaml
import datetime

import emoji
import unidecode

from doreah.io import col
from doreah.control import mainfunction



nowstr = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

customreplace = {
	"ä":"ae",
	"ü":"ue",
	"ö":"oe",
	"Ä":"AE",
	"Ü":"UE",
	"Ö":"OE"
}

# LEVELS
# 1 - Remove Emojis, because they are a crime against God
# 2 - ASCIIfy, transliterate different alphabets etc
# 3 - Remove whitespaces
# 4 - Lower Case everything
#

def cleanf(name,level):
	name = " ".join(name.split())
	name = "".join(customreplace[char] if char in customreplace else char for char in name)
	if level == 1:
		# get rid of emojis, automatically included in asciifying
		name = emoji.get_emoji_regexp().sub('',name)
		name = " ".join(name.split())
	if level > 1:
		# asciify
		name = unidecode.unidecode(name)
		name = name.replace("/","-")
		# replace all whitespaces with normal one (and collapse multiple into one)
		name = " ".join(name.split())
	if level > 2:
		name = name.replace(" ","_")
	if level > 3:
		name = name.lower()

	name = name.strip()
	assert name != ""
	return name


@mainfunction({},flags=["dryrun","save_log"],shield=True)
def main(rootpath,level=3,dryrun=False,save_log=False):
	found,changed,skipped = 0,0,0
	renamed = []
	for root, dirs, files in os.walk(rootpath,topdown=False):
		for f in files+dirs:
			found += 1
			fc = cleanf(f,level=level)
			oldname = os.path.join(root,f)
			newname = os.path.join(root,fc)
			if fc != f:
				print(col["red"](oldname))
				print(col["green"](newname))

				if os.path.exists(newname):
					print(newname,"already exists!")
					skipped += 1
					try:
						for f in [oldname,newname]:
							sha256_hash = hashlib.sha256()
							with open(f,"rb") as fd:
								for byte_block in iter(lambda: fd.read(4096),b""):
									sha256_hash.update(byte_block)
							print("Hash: " + sha256_hash.hexdigest())
					except:
						pass
				else:
					changed += 1
					if not dryrun: os.rename(oldname,newname)
					renamed.append({"original":oldname,"new":newname})

	if dryrun: print(changed,"offending files found. No files have been renamed.")
	else: print("Renamed",changed,"of",found,"files, skipped",skipped)
	if save_log:
		with open("rename_" + nowstr + ".yml","w") as log:
			yaml.dump(renamed,log)


def cleandir(root,path=[],printeddepth=0):
	abspath = os.path.join(root,*path)
	try:
		nodes = os.listdir(abspath)
	except:
		print("Cannot access",abspath)
		return False
	files = [n for n in nodes if os.path.isfile(os.path.join(abspath,n))]
	subdirs = [n for n in nodes if os.path.isdir(os.path.join(abspath,n))]

	changed = False
	for d in subdirs:
		changed = cleandir(root,path=path+[d],printeddepth=printeddepth) or changed
		if changed: printeddepth = len(path)

	for f in files:
		fc = cleanf(f,level=level)
		if (not changed) and fc != f:
			changed = True
			while printeddepth<len(path):
				print(indent(printeddepth),path[printeddepth])
				printeddepth += 1
		if fc != f:
			print(indent(printeddepth),"-",col["red"](f))
			print(indent(printeddepth)," ",col["green"](fc))
	#print(abspath)

	return changed


def indent(n):
	return n * "   "
