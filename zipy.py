#! /usr/bin/python
# quick and dirty zip
# by Martin Jung

#Import everything necessary
import os, time, zipfile, glob

#The Extensions
ext = []

def main():
	#Starting the Program
	folder = os.getcwd()
	allfiles = os.listdir(folder)
	leng = int(len(allfiles))

	time.sleep(1)
	print str(leng)+" Files in the current Directory"
	size = foldersize(folder)
	print "Foldersize = %0.1f MB" % (size/(1024*1024.0))
	extension()
	while 1:
		more = raw_input("Do you want to add another extension ? (y|n)\n")
		if more == "y":
			extension()
		else:
			break
	fin_string = ' '.join(ext)
	print "Starting Zipping everything which ends with "+fin_string+"\n\n"
	zipper(folder, ext)
	
	print "\nFinished Zipping"
	time.sleep(1)
	x = raw_input("Do you want to delete the Source Files ?  (y|n)\n")
	if x == "y":
		clean(folder, ext)
	size_new = foldersize(folder)
	print "New Foldersize = %0.1f MB\n" % (size_new/(1024*1024.0))

def extension():
	x = raw_input("Enter a extension to zip everything in the current folder:")
	ext.append(x)
	return ext

def foldersize(folder):
	size = 0
	for (path, dirs, files) in os.walk(folder):
		for file in files:
			filename = os.path.join(path, file)
			size += os.path.getsize(filename)
	return size

def zipper(path, ext):
	#zip function
	for i in ext:
		for name in glob.glob(path+'/*.'+i):
			print "zipping "+ name
			file = zipfile.ZipFile(name+".zip", "w")
			file.write(name, os.path.basename(name), zipfile.ZIP_DEFLATED)
			file.close()
		
def clean(path, ext):
	#clean function
	for i in ext:
		for name in glob.glob(path+'/*.'+i):
			os.remove(name)

if __name__ == "__main__" :
	main()
	print "-----------------------"
	print "Thank you 4 using Zipy"
