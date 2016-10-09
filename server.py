import cherrypy

# connect to a database


def contents(filename):
	f = open(filename)
	contents = f.read()
	f.close()
	return contents

def clarify(kwargs):
	out = "You gave me: <br>"
	for key in kwargs:
		print "HELLO HELLO ", key, kwargs[key]
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