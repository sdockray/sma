# adapted from https://raw.githubusercontent.com/njurgens/cherrypy-facebook-oauth-seed/master/app/auth.py
import cherrypy
import time

from sma import utils
from sma.config import OAUTH_FB_CLIENT_ID, OAUTH_FB_CLIENT_SECRET

__all__ = []

class FBAuth(object):

    def __init__(self):
        # ideal read client_id from config
        self.client_id = OAUTH_FB_CLIENT_ID
        self.client_secret = OAUTH_FB_CLIENT_SECRET

        # ideally read urls from config
        self.auth_uri = 'https://facebook.com/dialog/oauth/'
        self.access_token_uri = 'https://graph.facebook.com/oauth/access_token'

        # where to redirect to after login
        self.redirect_uri = '/auth/fb/success'
        self.access_token_redirect_uri = '/auth/fb/access_token'

        # facebook user profile
        self.user_profile_uri = 'https://graph.facebook.com/me'

    @cherrypy.expose
    def index(self):
        # already logged in
        if 'login' in cherrypy.session:
            raise cherrypy.HTTPRedirect(cherrypy.base)

        # generate a secret to verify OAuth responses
        cherrypy.session['auth_secret'] = utils.gen_secret()

        # make OAuth request
        args = {
                'client_id': self.client_id,
                'redirect_uri': cherrypy.request.base + self.redirect_uri,
                'state': cherrypy.session['auth_secret']
        }
        raise cherrypy.HTTPRedirect(utils.encode_uri(self.auth_uri, args))


    @cherrypy.expose
    def success(self, code=None, access_token=None, expires=None, state=None):
        # we didn't ask for authorization
        if not 'auth_secret' in cherrypy.session:
            raise cherrypy.HTTPError(401)

        # incorrect response params
        if not code or not state:
            raise cherrypy.HTTPError(401)

        # forged request secret
        if state != cherrypy.session['auth_secret']:
            raise cherrypy.HTTPError(401)

        # remove the secret
        del cherrypy.session['auth_secret']

        cherrypy.session['auth_code'] = code

        # retrieve OAuth access token
        args = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'redirect_uri': cherrypy.request.base + self.redirect_uri,
                'code': code,
        }
        response = utils.get_request(self.access_token_uri, args, 'query')

        # verify access token response
        if not 'access_token' in response or not 'expires' in response:
            raise cherrypy.HTTPError(500)

        access_token = response['access_token'][0]
        expires = response['expires'][0]

        cherrypy.session['access_token'] = access_token
        cherrypy.session['access_token_expires'] = time.time() + float(expires)

        # retrieve user's credentials
        args = {
                'access_token': access_token
        }
        user_profile = utils.get_request(self.user_profile_uri, args)

        # verify we received an id for the user
        if 'id' not in user_profile:
            raise cherrypy.HTTPError(500)

        # user is now logged in
        cherrypy.session['profile'] = user_profile
        cherrypy.session['login'] = True

        raise cherrypy.HTTPRedirect(cherrypy.request.base + '/fb')

    @cherrypy.expose
    def profile(self):
        if not 'login' in cherrypy.session:
            raise cherrypy.HTTPRedirect(cherrypy.request.base + '/auth/fb')
        return str(cherrypy.session['profile'])

    @cherrypy.expose
    def logout(self):
        cherrypy.lib.sessions.expire()
        raise cherrypy.HTTPRedirect(cherrypy.request.base + '/')


