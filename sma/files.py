import os, re, hashlib, shutil, pickle
from urlparse import urlparse
from PIL import Image

from sma.config import DIR_BASE, DIR_SCREENSHOTS, DIR_IMAGES, DIR_LINKS, PATH_IMAGES

# turn a local path into an absolute url for image thumbnails
def tnurl(path):
	path = tn(path)
	return re.sub('^'+DIR_BASE+'/', '/'+PATH_IMAGES+'/', path)

# turn a url into a local absolute url to the cached markdown version
def lurl(url):
	return "/link/"+hashlib.md5(url).hexdigest()

def screenshot_path(url):
	sd = os.path.join(DIR_BASE, DIR_SCREENSHOTS)
	if not os.path.exists(sd):
		os.makedirs(sd)
	return os.path.join(sd, "%s.png" % hashlib.md5(url).hexdigest())

# pickle an object
def save_obj(obj, subdir, filename):
	if not os.path.exists(os.path.join(DIR_BASE, subdir)):
		os.makedirs(os.path.join(DIR_BASE, subdir))
	path = os.path.join(DIR_BASE, subdir, filename)
	with open(path, 'wb') as f:
		pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
	print "Saved filename to",path

# unpickle n object
def load_obj(subdir, filename):
	if not os.path.exists(os.path.join(DIR_BASE, subdir)):
		os.makedirs(os.path.join(DIR_BASE, subdir))
	path = os.path.join(DIR_BASE, subdir, filename)
	if not os.path.exists(path):
		print "Path doesn't exist: ",path
		return None
	try:
		with open(path, 'rb') as f:
			print "Loading archive from ",path
			d = pickle.load(f)
			return d					
	except:
		print "Couldn't load the archive from file: ",path
	return None

# saves some text
def save_txt(text, subdir=None, filename="archive.md", save_location=None):
	# option to specify a particular location
	if save_location:
		with open(save_location, "w") as f:
			f.write(text.encode('utf-8').strip())
		print "Saved: ",save_location
	elif subdir:
		path = os.path.join(DIR_BASE, subdir)
		if not os.path.exists(path):
			os.makedirs(path)
		with open(os.path.join(path, filename), "w") as f:
			f.write(text.encode('utf-8').strip())
		print "Saved: ",filename

# saves some text
def load_txt(subdir=None, filename="archive.md", path=None):
	# option to specify a particular location
	if subdir and not path:
		path = os.path.join(DIR_BASE, subdir, filename)
	if path and os.path.exists(path):
		with open(path, "r") as f:
			return f.read()


# Gets cached markdown from url
def readable(url):
	path = os.path.join(DIR_BASE, DIR_LINKS, "%s.md" % hashlib.md5(url).hexdigest())
	if os.path.exists(path):
		with open(path, 'r') as f:
			return f.read()
	return ""

#
def get_image_path(url):
	imgd = os.path.join(DIR_BASE, DIR_IMAGES)
	if not os.path.exists(imgd):
		os.makedirs(imgd)
	parsed = urlparse(url)
	filename, file_ext = os.path.splitext(os.path.basename(parsed.path))
	return os.path.join(imgd, "%s%s" %(filename[1:], file_ext))

# saves an image
def save_image(response, url):
	path = get_image_path(url)
	try:
		with open(path, 'wb') as f:
			shutil.copyfileobj(response.raw, f)
		return path
	except:
		print "Failed to save image to ",path
		return None

# 
def get_content_path(url):
	cd = os.path.join(DIR_BASE, DIR_LINKS)
	if not os.path.exists(cd):
		os.makedirs(cd)
	return os.path.join(cd, "%s.md" % hashlib.md5(url).hexdigest())	

# saves content
def save_content(s, url):
	path = get_content_path(url)	
	try:
		with open(path, 'w') as f:
			f.write(s.encode('utf-8').strip())
	except:
		print "Failed to save content to ",path

# makes a square crop of an image and replaces the original image
def square_crop(path):
	if path:
		try:
			img = Image.open(path)
			w, h = img.size
			if h>w:
				img = img.crop((0, 0, w, w))
			img.save(path)
		except:
			print "Failed to crop image: ", path

# returns path to thumbnail (given an image path)
def tn(path):
	if not path:
		return None
	return "%s-tn%s" % (os.path.splitext(path)[0], os.path.splitext(path)[1])

# makes a thumbnail, appending -tn to the filename
def thumbnail(path, dims=(150,150)):
	if path and not os.path.exists(tn(path)):
		try:
			img = Image.open(path)
			if img.size[0]<=dims[0]:
				wpercent = (dims[0] / float(img.size[0]))
 				newh = int((float(img.size[1]) * float(wpercent)))
				img2 = img.resize((dims[0],newh), image.ANTIALIAS)
				img2.save(tn(path))
			else:
				img.thumbnail(dims, Image.ANTIALIAS)
				img.save(tn(path))
		except:
			print "Failed to create thumbnail"