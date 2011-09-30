#!/usr/bin/python
import oauth2 as oauth
import urlparse, time, webbrowser
from twisted.internet import reactor, protocol, ssl
from twisted.web import http

CONSUMER_KEY='CHANGEME'
CONSUMER_SECRET='CHANGEME'
CONSUMER=oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)

ACCESS_TOKEN_FILE = 'OAUTH_ACCESS_TOKEN'

TWITTER_REQUEST_TOKEN_URL = 'http://twitter.com/oauth/request_token'
TWITTER_ACCESS_TOKEN_URL = 'http://twitter.com/oauth/access_token'
TWITTER_AUTHORIZE_URL = 'http://twitter.com/oauth/authorize'
TWITTER_STREAM_API_HOST = 'stream.twitter.com'
TWITTER_STREAM_API_PATH = '/1/statuses/sample.json'

class TwitterStreamer(http.HTTPClient):
    def connectionMade(self):
        self.sendCommand('GET', self.factory.url)
        self.sendHeader('Host', self.factory.host)
        self.sendHeader('User-Agent', self.factory.agent)
        self.sendHeader('Authorization', self.factory.oauth_header)
        self.endHeaders()
  
    def handleStatus(self, version, status, message):
        if status != '200':
            self.factory.tweetError(ValueError("bad status"))
  
    def lineReceived(self, line):
        self.factory.tweetReceived(line)

    def connectionLost(self, reason):
        self.factory.tweetError(reason)

class TwitterStreamerFactory(protocol.ClientFactory):
      protocol = TwitterStreamer
  
      def __init__(self, oauth_header):
          self.url = TWITTER_STREAM_API_PATH
          self.agent='Twisted/TwitterStreamer'
          self.host = TWITTER_STREAM_API_HOST
          self.oauth_header = oauth_header
  
      def clientConnectionFailed(self, _, reason):
          self.tweetError(reason)
  
      def tweetReceived(self, tweet):
        print tweet
  
      def tweetError(self, error):
        print error

def save_access_token(key, secret):
    with open(ACCESS_TOKEN_FILE, 'w') as f:
        f.write("ACCESS_KEY=%s\n" % key)
        f.write("ACCESS_SECRET=%s\n" % secret)

def load_access_token():
    with open(ACCESS_TOKEN_FILE) as f:
        lines = f.readlines()

    str_key=lines[0].strip().split('=')[1]
    str_secret=lines[1].strip().split('=')[1]
    return oauth.Token(key=str_key, secret=str_secret)

def fetch_access_token():
    client = oauth.Client(CONSUMER)

    # Step 1: Get a request token.
    resp, content = client.request(TWITTER_REQUEST_TOKEN_URL, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])
    request_token = dict(urlparse.parse_qsl(content))
    print "Request Token:"
    print "     oauth_token        = %s" % request_token['oauth_token']
    print "     oauth_token_secret = %s" % request_token['oauth_token_secret']

    # Step 2: User must authorize application.
    auth_url = "%s?oauth_token=%s" % (TWITTER_AUTHORIZE_URL, request_token['oauth_token'])
    webbrowser.open_new_tab(auth_url)
    print "Go to the following link in your browser:"
    print auth_url
    pin = raw_input('What is the PIN? ')
    token = oauth.Token(request_token['oauth_token'],request_token['oauth_token_secret'])
    token.set_verifier(pin)

    # Step 3: Get access token.
    client = oauth.Client(CONSUMER, token)
    resp, content = client.request(TWITTER_ACCESS_TOKEN_URL, "POST")
    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])
    access_token = dict(urlparse.parse_qsl(content))
    print "Access Token:"
    print "     oauth_token        = %s" % request_token['oauth_token']
    print "     oauth_token_secret = %s" % request_token['oauth_token_secret']
    return (access_token['oauth_token'], access_token['oauth_token_secret'])

def build_authorization_header(access_token):
    url = "https://%s%s" % (TWITTER_STREAM_API_HOST, TWITTER_STREAM_API_PATH)
    params = {
        'oauth_version': "1.0",
        'oauth_nonce': oauth.generate_nonce(),
        'oauth_timestamp': int(time.time()),
        'oauth_token': access_token.key,
        'oauth_consumer_key': CONSUMER.key
    }

    # Sign the request.
    req = oauth.Request(method="GET", url=url, parameters=params)
    req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), CONSUMER, access_token)

    # Grab the Authorization header
    header = req.to_header()['Authorization'].encode('utf-8')
    print "Authorization header:"
    print "     header = %s" % header
    return header

if __name__ == '__main__':
    # Check if we have saved an access token before.
    try:
        f = open(ACCESS_TOKEN_FILE)
    except IOError:
        # No saved access token. Do the 3-legged OAuth dance and fetch one.
        (access_token_key, access_token_secret) = fetch_access_token()
        # Save the access token for next time.
        save_access_token(access_token_key, access_token_secret)

    # Load access token from disk.
    access_token = load_access_token()

    # Build Authorization header from the access_token.
    auth_header = build_authorization_header(access_token)

    # Twitter stream using the Authorization header.
    twsf = TwitterStreamerFactory(auth_header)
    reactor.connectSSL(TWITTER_STREAM_API_HOST, 443, twsf, ssl.ClientContextFactory())
    reactor.run()
