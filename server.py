#!/bin/python


import cherrypy
import dataset
import md5

def connect():
#	db = dataset.connect('sqlite:///:memory:')
	db = dataset.connect('sqlite:///data.db')
	table = db['users']
	return table

def contents(filename):
	f = open(filename)
	contents = f.read()
	f.close()
	return contents

def clarify(kwargs):
	out = "You gave me: <br>"
	for key in kwargs:
		out += key + " = " + str(kwargs[key]) + "<br>"

	return out
	
def inject_navbar(inp):
	nav = contents("app/navbar.html")
	return inp.replace("{NAVBAR}", nav)
	  
class Root(object):
	def index(self):
		return inject_navbar(contents('app/index.html'))
	index.exposed = True
	
	@cherrypy.expose
	def signup(self, *args, **kwargs):
		# connect to a database
		table = connect()
		username = kwargs["username"]
		password = kwargs["password"]
		if password != kwargs["confirm"]:
			return "passwords don't match"
			
		# hash password
		m = md5.new()
		m.update(password)
		hashed = m.hexdigest()
		if table.find_one(username=username):
			return "user already exists"
		
		# insert the user into the database
		table.insert(dict(username=username, password=hashed))
		
		return "User " + username + " created successsfully!"
	
	@cherrypy.expose
	def create(self):
		return contents('app/create.html')
	
	@cherrypy.expose
	def update(self, *args, **kwargs):
		return clarify(kwargs)
	
	@cherrypy.expose
	def search(self, *args, **kwargs):
		return clarify(kwargs)
	#		if cherrypy.request.method == "POST":
#			if "desire" in kwargs:
#				pass
#			if "experience" in kwargs:
#				pass
#			if "genre" in kwargs:
#				pass
#			if "topic" in kwargs:
#				pass
#			return kwargs

cherrypy.quickstart(Root(), "", "app.conf")