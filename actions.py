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
      j = self.request.get('j')
      m = self.request.get('m')
      a = self.request.get('a')
      v = self.request.get('v')
      t = self.request.get('t')
      logging.info('Adding %s/%s%s %s %s' % (j,m,a,v,t))
      jj = int(j)
      mm = int(m)
      aa = int(a)
      d = datetime.date(aa,mm,jj)
      vv = int(v)
      mes = Mesure(jour=d,annee=aa,type=t,valeur=vv)
      mes.put()
    except:
      logging.error('There was an error adding mesure')
    logging.debug('Finish mesure adding')
    self.redirect('/mesures?a=%s#table' % a)

class AddTagToExpression(webapp2.RequestHandler):
  def get(self):
    logging.info('Start adding tag to expression request')

    tag = None
    try:
      i = int(self.request.get('t'))
      tag = Tag.get(db.Key.from_path('Tag', i))
    except:
      tag = None

    if tag:
      expression = None
      try:
        i = int(self.request.get('id'))
        expression = Expression.get(db.Key.from_path('Expression', i))
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

    self.redirect('/expression/%s' % i)

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

class ComputeMesures(BaseRequestHandler):
  def get(self):
    mesures = []

    t = self.request.get('t')
    title = 'mesures'

    try:
      mesures = Mesure.gql("WHERE type = :1 ORDER BY jour", t)
      if t == 'E':
        val = 65996
      else:
        val = 13331
      j = datetime.date(2011,12,24)
      for mes in mesures:
        mes.conso = mes.valeur - val
        delta = mes.jour - j
        mes.nb_jours = delta.days
        mes.put()
        val = mes.valeur
        j = mes.jour
      title = 'Mesures'
    except:
      logging.error('There was an error retreiving mesures from the datastore')

    template_values = {
      'title': title,
      'annee': 2013,
      'type': t,
      'mesures': mesures
      }

    self.generate('mesures.html', template_values)

class ListMesures(BaseRequestHandler):
  def get(self):
    mesures = []

    t = self.request.get('t')
    a = self.request.get('a')
    annee = int(a)
    title = 'mesures'

    try:
      mesures = Mesure.gql("WHERE annee = :1 AND type = :2 ORDER BY jour", annee, t)
      title = 'Mesures'
    except:
      logging.error('There was an error retreiving mesures from the datastore')

    template_values = {
      'title': title,
      'type': t,
      'annee': annee,
      'mesures': mesures
      }

    self.generate('mesures.html', template_values)

class ViewExpression(BaseRequestHandler):
  def get(self, arg):
    title = 'Expression introuvable'
    ex = None
    tags = []

    # Get and displays the expression informations
    try:
      i = int(arg)
      ex = Expression.get(db.Key.from_path('Expression', i))
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
