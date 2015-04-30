# -*- coding: utf-8 -*-
import string
import os
import glob

import markdown2
import cherrypy

from sma.files import load_txt
from sma.config import PATH_IMAGES
from sma.auth import FBAuth
from sma.archiver import FB

# for groups, or a post within a group
def obj_path(id, sub_id=None):
	if sub_id:
		return os.path.join("archives", id, "posts", "%s.md" % sub_id)
	else:
		return os.path.join("archives", id, "archive.md")

# for archived links
def link_path(link_id):
	return os.path.join("archives", "web", "%s.md" % link_id)

# get a group name
def obj_title(id, default="Social Media Archive"):
	t = load_txt(subdir=id, filename="title.txt")
	return t if t else default

# loads a metadata file and converts to html
def load(path):
	if os.path.exists(path):
		with open(path, 'r') as f:
			return markdown2.markdown(f.read())
	else:
		return "Page not found."

# searches a group
def search(id, query):
	found = []
	search_path = os.path.join("archives", id, "posts","*.md")
	for file in glob.glob(search_path):
		with open(file) as f:
			contents = f.read()
		if query in contents:
			post_id = os.path.splitext(os.path.split(file)[1])[0]
			try:
				found.append(load(obj_path(id, post_id)))
			except:
				found.append(post_id)
				pass
	return "\n\n---\n\n".join(found)

# markup for a search form
def search_form(id):
	return """
<form method='get' action='/group/%s/search'>
<input value="" name="post_id" size='75'/>
<input type='submit' value='Search' />
</form>
---
	""" % id

# spits out the final html
def html(html, title="Social Media Archive", inject=""):
	return """
	<html>
		<head>
			<title>%s</title>
			<link rel="stylesheet" type="text/css" href="/css/style.css" media="screen" />
		</head>
		<body>
			%s
			%s
		</body>
	</html>
	""" % (title, inject, html)

# 
class ArchiveServer(object):
	@cherrypy.expose
	def default(self, attr="abc"):
		return "Page not found!"

	@cherrypy.expose
	def index(self):
		with open('README.md', 'r') as f:
			return html(markdown2.markdown(f.read()))

	# Viewing groups and posts (within groups)
	@cherrypy.expose
	def group(self, id, post=None, post_id=None):
		if post and post_id and post=='post':
			return html(load(obj_path(id, post_id)), title=obj_title(id))
		elif post and post_id and post=='search':
			html(search(id, post_id))
		else:
			return html(load(obj_path(id)), title=obj_title(id), inject=search_form(id))
			#return "group ",id

	# Viewing groups and posts (within groups)
	@cherrypy.expose
	def post(self, id):
		return html(load(obj_path(id)), title=obj_title(id))

	# Viewing cached links
	@cherrypy.expose
	def link(self, id):
		return html(load(link_path(id)))

	# Facebook importing
	@cherrypy.expose
	def fb(self, action='access_token', value=None):
		if not action=='access_token' and not 'access_token' in cherrypy.session:
			raise cherrypy.HTTPRedirect(cherrypy.request.base + '/fb/access_token')
		# Manually enter an access token
		if action=='access_token':
			if value:
				cherrypy.session['access_token'] = value
				raise cherrypy.HTTPRedirect(cherrypy.request.base + '/fb/list')
			# otherwise a form
			content = """
Step 1: Get an access token
---------------------------
To make an archive, you need to get an "access token" from this page:
[https://developers.facebook.com/tools/explorer/](https://developers.facebook.com/tools/explorer/)

1. Click on **Get Token** and choose **Get Access Token**
2. Make sure **user_status**, **user_groups**, and **user_posts** are checked 
3. Click the **Get Access Token** button
4. Copy and paste it into the form below!
5. Hit submit and wait (a few minutes) for data to load 
<form method='get' action='/fb/access_token'>
<input value="" name="value" size='75'/>
<input type='submit' value='Submit' />
</form>
			"""
		elif action=='list':
			fb = FB(cherrypy.session['access_token'])
			fb.load_groups()
			fb.load_posts()
			content = fb.markdownify()
		elif action=='archive_group':
			fb = FB(cherrypy.session['access_token'])
			fb.archive_group(value)
			content = """
Step 2: Archiving group
-----------------------
Your group has been archived and can be seen [here](/group/%s) but now I'd like to grab images and page content from all the links.
It will take a pretty long time depending on how many links your group has shared. [Click here to start and check back later](/fb/build_group/%s)
			""" % (value,value)
		elif action=='archive_post':
			fb = FB(cherrypy.session['access_token'])
			fb.archive_post(value)
			content = """
Step 2: Archiving post
----------------------
Your post has been archived and can be seen [here](/post/%s)
			""" % value
		elif action=='build_group':
			fb = FB(cherrypy.session['access_token'])
			fb.rebuild_group(value, do_snaps=True)
			content = """
Step 3: You're done!
--------------------
You can now see the archive [here](/group/%s)
			""" % value
		return html(markdown2.markdown(content))


# Starting things up
if __name__ == '__main__':
	conf = {
		'/'+PATH_IMAGES: {'tools.staticdir.on': True, 'tools.staticdir.dir': '/Users/dddd/Documents/dev/social-archives/archives'},
		'/css': {'tools.staticdir.on': True, 'tools.staticdir.dir': '/Users/dddd/Documents/dev/social-archives/css'},		
	}
	cherrypy.config.update({
		'tools.sessions.on': True
	})
	app = cherrypy.tree.mount(ArchiveServer(), '/')
	# for Facebook authentication
	fb_auth = cherrypy.tree.mount(FBAuth(), '/auth/fb/')
	cherrypy.quickstart(app,config=conf)