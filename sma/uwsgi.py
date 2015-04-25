import cherrypy
from sma.archiver import ArchiveServer

def application(environ, start_response):
  app = cherrypy.tree.mount(ArchiveServer(), '/')
  return cherrypy.tree(environ, start_response)
