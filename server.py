''' '' '' ''
CAC - Coder Artist Connection
Copyright (C) 2016 - Adam Bennani, Philip Donlon, Shuran Li, Mingfang Chang

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
''' '' '' ''

import cherrypy
import dataset
import md5
import datetime

def login(username, password):
	table = connect()
	valid = table.find_one(username=username, password=password)
	print "THE ANSWER", valid
	if valid:
		# set cookie and return
		cherrypy.response.cookie["token"] = username+":"+password
		
		cherrypy.request.cookie["token"] = cherrypy.response.cookie["token"]
		
		# token good for 72 hours
		cherrypy.response.cookie["token"]["max-age"] = datetime.timedelta(hours=72).total_seconds()
		return True
	else:
		return False
	
def notice(text):
	return "<div class='notice'>" + text + "</div>"
	
def is_logged_in():
	# check for the cookie
	if "token" in cherrypy.request.cookie:
		token = cherrypy.request.cookie["token"].value
		delimiter = token.rindex(":")
		username = token[:delimiter]
		password = token[delimiter+1:]
		
		# return successful or not
		return login(username, password)
		
def get_username():
	if "token" in cherrypy.request.cookie:
		token = cherrypy.request.cookie["token"].value
		delimiter = token.rindex(":")
		username = token[:delimiter]
		
		return username
	return None # shouldn't happen

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
	if is_logged_in():
		nav = contents("app/loggedin_navbar.html")
		username = get_username()
		nav = nav.replace("{USERNAME}", username)
	else:
		nav = contents("app/navbar.html")
	return inp.replace("{NAVBAR}", nav)
	  
class Root(object):
	def index(self):
		return inject_navbar(contents('app/index.html'))
	index.exposed = True
	
	@cherrypy.expose
	def login(self, *args, **kwargs):
		table = connect()
		
		username = kwargs["username"]
		password = kwargs["password"]
					
		# hash password
		m = md5.new()
		m.update(password)
		hashed = m.hexdigest()
		
		# try to login
		success = login(username, hashed)
		
		if success:
			return self.index() + notice("Logged in successfully")
		else:
			return self.index() + notice("Error when logging in (invalid user or password?)")
		
	
	@cherrypy.expose
	def signup(self, *args, **kwargs):
		# connect to a database
		table = connect()
		if "username" not in kwargs:
			raise cherrypy.HTTPRedirect("/")
		username = kwargs["username"]
		password = kwargs["password"]
		if password != kwargs["confirm"]:
			return self.index() + notice("passwords don't match")
			
		# hash password
		m = md5.new()
		m.update(password)
		hashed = m.hexdigest()
		if table.find_one(username=username):
			return self.index() + notice("user already exists")
		
		# insert the user into the database
		table.insert(dict(username=username, password=hashed))
		cherrypy.response.cookie["token"] = username+":"+hashed
		
		# token good for 72 hours
		cherrypy.response.cookie["token"]["max-age"] = datetime.timedelta(hours=72).total_seconds()
		
		cherrypy.request.cookie["token"] = cherrypy.response.cookie["token"]

		return self.profile() + notice("User " + username + " created successsfully!")
	
	@cherrypy.expose
	def update(self, *args, **kwargs):
		return clarify(kwargs)
	
	@cherrypy.expose
	def ping(self):
		return str(is_logged_in())
	
	@cherrypy.expose
	def profile(self):
		return inject_navbar(contents('app/profile.html'))
	
	@cherrypy.expose
	def logout(self):
		if "token" not in cherrypy.request.cookie:
			raise cherrypy.HTTPRedirect("/")
		cherrypy.response.cookie["token"] = "delme"
		cherrypy.response.cookie["token"]['expires'] = 0
		del cherrypy.request.cookie["token"]
		return self.index() + notice("Successfully logged out")
	
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