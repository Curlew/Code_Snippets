#! /usr/bin/env python
# quick and dirty zip for dirs
# by Martin Jung

#Import
import os
import time
import zipfile

def main():
	folder = os.getcwd()
	alldirs = os.listdir(folder)
	leng = int(len(alldirs))
	
	time.sleep(0.5)
	print str(leng-1)+" Dirs in the current Directory"
	time.sleep(0.5)
	#Zipping
	for entry in alldirs:
		#os.path.isdir(entry) or e
		if entry == 'zipy-dir.py' or entry[0] == '.':
			pass
		else:
			print "zipping dir : "+ entry
			file = zipfile.ZipFile(entry+".zip","w")
			cfolder = os.chdir(entry)
			try:
				allfiles = os.listdir(os.getcwd())
				check = 1
			except TypeError:
				check = 0
			if check == 1:
				for i in allfiles:
					if os.path.isfile(i):
						file.write(os.path.abspath(i), os.path.basename(i), zipfile.ZIP_DEFLATED)
					elif os.path.isdir(i):
						afolder = os.chdir(i)
						try:
							allfiles2 = os.listdir(os.getcwd())
							check2 = 1
						except TypeError:
							check2 = 0
						if check2 == 1:
							for i in allfiles:
								if os.path.isfile(i):
									file.write(os.path.abspath(i), os.path.basename(i), zipfile.ZIP_DEFLATED)	
								elif os.path.isdir(i):
									print 'Too many Directories !'
									return
			file.close()
			os.chdir(folder)
			#Cleaning
#			if check:
#				os.chdir(entry)
#				for i in os.listdir(os.getcwd()):
#					os.remove(i)				
#			os.chdir(folder)
#			os.removedirs(entry)

if __name__ == "__main__" :
	print "In the current Directory should be no files, right ?"
	if raw_input('Yes or No ? | Answer : ') == 'Yes' or 'yes':
		main()
		print "-----------------------"
		print "Thank you 4 using Zipy-Dir"	