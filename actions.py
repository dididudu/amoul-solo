#!/usr/bin/env python
#
# AMOUL SOLO PROJECT
#

__author__ = 'Didier Dulac'

import datetime
import logging
import os
import webapp2

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from models import Expression
from models import Tag
from models import Mesure

# Set to true if we want to have our webapp print stack traces, etc
_DEBUG = True

class BaseRequestHandler(webapp2.RequestHandler):
  def generate(self, template_name, template_values={}):
    values = {
      'request': self.request,
      'user': users.GetCurrentUser(),
      'admin': users.IsCurrentUserAdmin(),
      'login_url': users.CreateLoginURL(self.request.uri),
      'logout_url': users.CreateLogoutURL('http://' + self.request.host + '/'),
      'debug': self.request.get('deb'),
      'application_name': 'Amoul Solo'
    }
    values.update(template_values)
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, os.path.join('templates', template_name))
    self.response.out.write(template.render(path, values, debug=_DEBUG))

class AddExpression(webapp2.RequestHandler):
  def post(self):
    logging.debug('Start expression adding request')

    f = self.request.get('francais')
    w = self.request.get('wolof')
    exp = Expression(francais=f,wolof=w)

    user = users.GetCurrentUser()
    if user:
      logging.info('Expression %s added by user %s' % (f, user.nickname()))
      exp.created_by = user
      exp.updated_by = user
    else:
      logging.info('Expression %s added by anonymous user' % f)

    try:
      exp.put()
    except:
      logging.error('There was an error adding expression %s' % f)

    logging.debug('Finish Expression adding')
    self.redirect('/expressions')

class AddTag(webapp2.RequestHandler):
  def post(self):
    logging.debug('Start tag adding request')

    n = self.request.get('nom')
    tag = Tag(nom=n)

    user = users.GetCurrentUser()
    if user:
      logging.info('Tag %s added by user %s' % (n, user.nickname()))
      tag.created_by = user
      tag.updated_by = user
    else:
      logging.info('Tag %s added by anonymous user' % n)

    try:
      tag.put()
    except:
      logging.error('There was an error adding tag %s' % n)

    logging.debug('Finish tag adding')
    self.redirect('/tags')

class AddMesure(webapp2.RequestHandler):
  def post(self):
    logging.debug('Start mesure adding request')
    try:
      m = self.request.get('m')
      t = self.request.get('t')
      logging.info('Adding %s' % m)
      j = datetime.date.today()
      a = j.year
      v = int(tab[1])
      mes = Mesure(jour=j,annee=a,type=t,valeur=v)
      mes.put()
    except:
      logging.error('There was an error adding mesure')
    logging.debug('Finish mesure adding')
    self.redirect('/mesures')

class AddTagToExpression(webapp2.RequestHandler):
  def get(self):
    logging.info('Start adding tag to expression request')

    tag = None
    try:
      id = int(self.request.get('t'))
      tag = Tag.get(db.Key.from_path('Tag', id))
    except:
      tag = None

    if tag:
      expression = None
      try:
        id = int(self.request.get('id'))
        expression = Expression.get(db.Key.from_path('Expression', id))
      except:
        expression = None

      if expression:
        if tag.key() not in expression.tags:
          expression.tags.append(tag.key())
          expression.put()
          logging.info('Finish tag adding')
        else:
          expression.tags.remove(tag.key())
          expression.put()
          logging.info('Tag already added')
      else:
        logging.info('Expression not found so no tag adding')
    else:
      logging.info('Tag not found so no tag adding')

    self.redirect('/expression/%s' % id)

class ListExpressions(BaseRequestHandler):
  def get(self):
    expressions = []
    title = 'Expressions'
    try:
      expressions = Expression.gql("ORDER BY francais")
      title = 'Expressions'
    except:
      logging.error('There was an error retreiving expressions from the datastore')

    template_values = {
      'title': title,
      'expressions': expressions,
      }

    self.generate('expressions.html', template_values)

class ListTags(BaseRequestHandler):
  def get(self):
    tags = []
    title = 'Tags'
    try:
      tags = Tag.gql("ORDER BY nom")
      title = 'Tags'
    except:
      logging.error('There was an error retreiving tags from the datastore')

    template_values = {
      'title': title,
      'tags': tags,
      }

    self.generate('tags.html', template_values)

class ListMesures(BaseRequestHandler):
  def get(self):
    mesures = []
    title = 'mesures'
    try:
      mesures = Mesure.gql("ORDER BY jour")
      title = 'Mesures'
    except:
      logging.error('There was an error retreiving mesures from the datastore')

    template_values = {
      'title': title,
      'mesures': mesures,
      }

    self.generate('mesures.html', template_values)

class ViewExpression(BaseRequestHandler):
  def get(self, arg):
    title = 'Expression introuvable'
    ex = None
    tags = []

    # Get and displays the expression informations
    try:
      id = int(arg)
      ex = Expression.get(db.Key.from_path('Expression', id))
      tags = Tag.gql("ORDER BY nom")
    except:
      ex = None
      logging.error('There was an error retreiving expression and its informations from the datastore')

    if not ex:
      self.error(403)
      return
    else:
      title = "Expression"

    template_values = {
      'title': title,
      'expression': ex,
      'tags': tags
      }

    self.generate('expression.html', template_values)
