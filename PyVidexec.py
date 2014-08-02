#!/usr/bin/env python
# -*- coding: utf-8 -*-
# terminal based Media Organisator
# Author: Martin Jung
# Date: 2011

# Imports
import imdb  # aptitude install python-imdbpy
import sqlite3 # aptitude install python-sqlite
import os, sys, getopt, fnmatch


# Video Datatype Endings
ext = ['*.avi','*.mkv']
extB = map(lambda x:x.upper(),ext)

# VideoPlayer Executable
player = 'vlc'



class PyVidexec():
	def __init__(self):
		self.ia = imdb.IMDb('http', uri='http://www.imdb.de/') # by default access the web.
	#Db-Creating or printing Information
	def dbTest(self):
		if os.path.exists('localvid.db'):
			self.con = sqlite3.connect('localvid.db')
			self.cursor = self.con.cursor()
			#info = self.cursor.fetchall()
			#for i in info:
			#	print "Id: " + str(i[0]) + "  path: " + i[1] + "  name: " + i[2] + "   year " + i[3]
		else:
			create = raw_input('No Database found. Wanna create one? (y|n)')
			if create == 'y':
				self.dbCreate()
				print "#########################"
				print "Start again"
			else:
				print "You have to create a Database to work with. ...Exiting..."
				sys.exit(0)
			
	#Database Creating
	def dbCreate(self):
		self.con = sqlite3.connect('localvid.db')
		self.cursor = self.con.cursor()
		table = "CREATE TABLE Pyvid(id INTEGER PRIMARY KEY, path TEXT, name TEXT, year TEXT)"
		self.cursor.execute(table)
		# Reading all Files in
		for root, dirnames, filenames in os.walk(os.getcwd()):
			s = os.path.basename(root)
			r = self.ia.search_movie(s)  #Searches imdb for the Movie
			if len(r) > 1:
				print "Multiple Results for " + s
			elif len(r) == 1:
				up = r[0]
				y = up['year']    #Retrieves the release year
				self.ia.update(up) # Updates all Data for the given Movie
				print up.summary() # Gives out the Data
				for i in ext:
					m = fnmatch.filter(filenames, i)
					for j in m:
						if len(m)==1:
							f = str((os.path.join(root, m[0])))
						elif len(m)==2:
							f = str((os.path.join(root, m[0]),os.path.join(root, m[1])))
						elif len(m) >2:
							print "To many Video-Files"
						if self.cursor.execute('INSERT INTO Pyvid VALUES (null, ?, ?, ?)',(f, s, y)):
							print "Sucessfully added " + s + " to the database"
						break
					break
				for i in extB:
					m = fnmatch.filter(filenames, i)
					for j in m:
						if len(m)==1:
							f = str((os.path.join(root, m[0])))
						elif len(m)==2:
							f = str((os.path.join(root, m[0]),os.path.join(root, m[1])))
						elif len(m) >2:
							print "To many Video-Files"
						if self.cursor.execute('INSERT INTO Pyvid VALUES (null, ?, ?, ?)',(f, s, y)):
							print "Sucessfully added " + s + " to the database"
						break
					break
		self.con.commit()
		self.con.close()
	
	# Lists all Entrys with a (non)given Term
	def dbList(self,term):
		self.con = sqlite3.connect('localvid.db')
		self.cursor = self.con.cursor()
		if term == 'all':
			self.cursor.execute("SELECT * FROM Pyvid") 
			info = self.cursor.fetchall()
			for i in info:
				print "Id: " + str(i[0]) + "\n  path: " + i[1] + "\n  name: " + i[2] + "\n  year " + i[3]
		elif term == 'year':
			self.cursor.execute("SELECT id, name, year FROM Pyvid") 
			info = self.cursor.fetchall()
			for i in info:
				print "Id: " + str(i[0]) + "   name: " + i[1] + " ("+str(i[2])+")"
		elif term == 'name':
			self.cursor.execute("SELECT id, name FROM Pyvid") 
			info = self.cursor.fetchall()
			for i in info:
				print "Id: " + str(i[0]) + "   name: " + i[1]

	# Watches the Movie with a given Database-ID
	def dbWatch(self,id):
		self.con = sqlite3.connect('localvid.db')
		self.cursor = self.con.cursor()
		self.cursor.execute("SELECT path FROM Pyvid WHERE id=?",id)
		path = self.cursor.fetchall()
		path = str(path[0][0])
		if ',' in path:
			x,y = path.split(',')
			if sys.platform == 'linux2':
				x = x.replace(" ", "\ ")
				y = y.replace(" ", "\ ")
			z = x[2:-1] + " " + y[3:-2]
		else:
			z = x[2:-2]	
			if sys.platform == 'linux2':
				z = z.replace(" ", "\ ")
		p = player + " " + z
		os.system(p) # play the file(s)
	
	# Deletes the Database and creates a new one
	def dbRem(self):
		db = 'localvid.db'
		os.remove(db)
		self.dbCreate()
		
	#Starting Procedure
	def start(self):
		#Curent Script-Path os.path.realpath(__file__)
		#Database-Test
		self.dbTest()
		try:
			if len(sys.argv[1:]) < 1:
				self.help()
			optlist, list = getopt.getopt(sys.argv[1:],':ahruwls:')
		except getopt.GetoptError: 
			self.help()
		for opt in optlist:
			if opt[0] == '-a':
				self.about()
			if opt[0] == '-h':
				self.help()
			if opt[0] == '-r':
				self.dbRem()
			if opt[0] == '-u':
				pass
			if opt[0] == '-w':
				if len(list) > 0:
					self.dbWatch(list[0])
				else:
					print "No ID given. Search for your Movie first."
			if opt[0] == '-l':
				if len(list) >0:
					self.dbList(list[0])
				else:
					self.dbList('all')
			if opt[0] == '-s':
				pass
		
	# Prints About-Information
	def about(self):
		print "PyVidexec.py by Martin Jung"
		print "###########################"
		print "This is a very customized little Mediaorganizer-Script for Videofiles\n"
		print "it reads through all sub-folders, saves information about videofiles with a little help of imdb"
		print "and is able to start a mediaplayer (default=vlc) directly.\n"
		print "###########################\n"
		sys.exit(0)
	
	# Prints the help		
	def help(self):
		print "PyVidexec [-a] [-h] [-r] [-u] [-w] [-l] [-s]\n"
		h = {}
		h["-a"] = "Displays Information about the Programm and the Author"
		h["-h"] = "Shows this help"
		h["-r"] = "Deletes all Content in the Database and read through all Folders again"
		h["-u"] = "Updates the database"
		h["-w"] = "watches a Movie with a given Id"
		h["-l"] = "List all files with a specific term"
		h["-s"] = "Performs a search through the database"
		for k in h.keys():
			print(str(k) + "    " + str(h[k]))
		sys.exit(0)
		


if __name__ == '__main__':	
	app = PyVidexec()
	app.start()
