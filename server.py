import cherrypy

# connect to a database


def contents(filename):
	f = open(filename)
	contents = f.read()
	f.close()
	return contents

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
	def search(self):
		thing = contents('app/search.html')
		return thing

cherrypy.quickstart(Root(), "", "app.conf")