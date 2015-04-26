import os

import requests

from selenium import webdriver
from readability.readability import Document
from summary import Summary
import html2text

from . import files


# Gets summary
def summary(url):
	summ = Summary(url)
	summ.extract()
	return (summ.title, summ.description, summ.image.url)


# Grabs things from the internet and saves them
def all(url):
	image(url)
	content(url)
	screenshot(url)


# Download image
def image(url, force=False):
	if force or not os.path.exists(files.get_image_path(url)):
		response = requests.get(url, stream=True)
		path = files.save_image(response, url)
		del response
		return path
	else:
		return files.get_image_path(url)

# requests a url and converts content to markdown
def content(url, force=False):
	if force or not os.path.exists(files.get_content_path(url)):
		try:
			response = requests.get(url, timeout=10)
			c = "this is an archive. [go to %s](%s)\n\n" % (url,url)
			c = "%s---\n\n" % c
			if response.ok:
				c = "%s### %s\n" % (c, Document(response.content).short_title())
				c = "%s%s" % (c, html2text.html2text(Document(response.content).summary()))
			else:
				c = "%sFor one reason or another, this document couldn't be archived." % c
			files.save_content(c, url)
		except:
			print "Failed to make markdown from: ", url

def screenshot(url, force=False):
	path = files.screenshot_path(url)
	if not os.path.exists(path):
		driver = webdriver.PhantomJS()
		driver.set_window_size(1024, 768)
		driver.get(url)
		driver.save_screenshot(path)
		files.square_crop(path)
	files.thumbnail(path)
	return path
	#print "Screenshot saved to: ",filepath