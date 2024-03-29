#!/usr/bin/env python

from json import dumps as to_json, loads as from_json
import logging

from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2



# This is for monitoring purposes only
class HealthHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('200')



# Base handler data
class BaseHandler(webapp2.RequestHandler):
	# Setup request parameters
	def initialize(self, *args, **kwargs):
		value = super(BaseHandler, self).initialize(*args, **kwargs)
		self.params = from_json(self.request.body)
		return value

    def options(self, *args, **kwargs):
        self.response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        self.response.headers['Access-Control-Allow-Origin' ] = '*'
        self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        self.response.headers['Cache-Control'] = 'no-cache'
        self.response.out.write('')

	# Send response JSON object
	def respond(self, data):
		self.response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
		self.response.headers['Access-Control-Allow-Origin' ] = '*'
		self.response.headers['Cache-Control'] = 'no-cache'
		self.response.headers['Content-Type' ] = 'application/json'
		self.response.out.write( to_json(data, separators=(',',':')) )

# Models
class User(ndb.Model):
	username = ndb.StringProperty()
	push_token = ndb.StringProperty()

class Game(ndb.Model):
	username = ndb.StringProperty()
	score = ndb.IntegerProperty()
	duration = ndb.IntegerProperty()
	bubbles = ndb.IntegerProperty()
	bombs = ndb.IntegerProperty()
	freezes = ndb.IntegerProperty()
	lifes = ndb.IntegerProperty()

	def serialize(self):
		return { 'username' : self.username, 'score': self.score }

# APIs
class GetAllGames(BaseHandler):
	def post(self):
		games = Game.query().order(-Game.score)
		data = [game.serialize() for game in games]
		self.respond(data)

class GetUserGames(BaseHandler):
	def post(self):
		games = Game.query(Game.username == self.params['username']).order(-Game.score)
		data = [game.serialize() for game in games]
		self.respond(data)

class CreateGame(BaseHandler):
	def post(self):
		game = Game()
		game.username = self.params['username']
		game.score = self.params['score']
		game.duration = self.params['duration']
		game.bubbles = self.params['bubbles']
		game.bombs = self.params['bombs']
		game.freezes = self.params['freezes']
		game.lifes = self.params['lifes']
		game.put()
		self.respond({})

# Router

app = webapp2.WSGIApplication([
	(r'/health', HealthHandler),
	(r'/games', GetUserGames),
	(r'/game/create', CreateGame),
	(r'/allgames', GetAllGames),
], debug=False)
