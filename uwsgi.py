import cherrypy
from from sma.archiver import ArchiveServer

from sma.config import PATH_IMAGES, SERVER_PORT,SERVER_IMAGES, SERVER_CSS

# Starting things up
if __name__ == '__main__':
	conf = {
		'/'+PATH_IMAGES: {'tools.staticdir.on': True, 'tools.staticdir.dir': SERVER_IMAGES},
		'/css': {'tools.staticdir.on': True, 'tools.staticdir.dir': SERVER_CSS},		
	}
	cherrypy.config.update({
		'tools.sessions.on': True,
		'server.socket_port': SERVER_PORT,
	})
	app = cherrypy.tree.mount(ArchiveServer(), '/')
	# for Facebook authentication
	cherrypy.quickstart(app,config=conf)