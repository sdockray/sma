import cherrypy
from sma.server import ArchiveServer

def application(environ, start_response):
  app = cherrypy.tree.mount(ArchiveServer(), '/')
  return cherrypy.tree(environ, start_response)
