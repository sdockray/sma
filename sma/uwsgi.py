import cherrypy
from sma.server import ArchiveServer

from sma.config import PATH_IMAGES, SERVER_PORT, SERVER_CSS, SERVER_IMAGES

def application(environ, start_response):
	conf = {
		'/'+PATH_IMAGES: {'tools.staticdir.on': True, 'tools.staticdir.dir': SERVER_IMAGES},
		'/css': {'tools.staticdir.on': True, 'tools.staticdir.dir': SERVER_CSS},		
	}
	cherrypy.config.update({
		'tools.sessions.on': True,
		'server.socket_port': SERVER_PORT
	})
  app = cherrypy.tree.mount(ArchiveServer(), '/', config=conf)
  return cherrypy.tree(environ, start_response)
