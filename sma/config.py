from ConfigParser import SafeConfigParser

import os

config = SafeConfigParser({
	'base_dir':'archives',
	'link_dir':'web',
	'screenshots_dir':'screenshots',
	'images_dir':'images',
	'images_path':'images', # static image directory for web server, eg /images
	})
config.read('config.ini')

DIR_BASE = config.get('dirs', 'base_dir')
DIR_LINKS = config.get('dirs', 'links_dir')
DIR_SCREENSHOTS = config.get('dirs', 'screenshots_dir')
DIR_IMAGES = config.get('dirs', 'images_dir')

PATH_IMAGES = config.get('web', 'images_path')

OAUTH_FB_CLIENT_ID = config.get('OAuth', 'fb_client_id')
OAUTH_FB_CLIENT_SECRET = config.get('OAuth', 'fb_client_secret')

SERVER_PORT = config.get('server', 'server_port')
SERVER_IMAGES = config.get('server', 'images_dir')
SERVER_CSS = config.get('server', 'css_dir')
SERVER_SESSIONS = config.get('server', 'sessions_dir')


#https://developers.facebook.com/tools/explorer/145634995501895/?method=GET&path=me%2Fgroups&version=v2.3&
ACCESS_TOKEN = "CAACEdEose0cBACyfbZBpKZCtw4GLaGLhLADd6hs4ylkNhKkgL6OFs6ZCwZB7PCmphJUaZB31j1mRrVovhhaOerT4mJP187cxYw1JtFfTZB4H5pDEZBFaZBPAuGB1ye7b6KLA1dsu15gbYCZBF8P6nXABLZCmRYuf5OtuQEh48KezwOl2PR0XUcHI42dAGbFf0jsbXww7Ipcmj5q73d9vwCwHfQ"
group_id = '1463661227181475'
post_id = '10152476878391236_10153011857856236'
post_id = '10152476878391236_10153011861626236'