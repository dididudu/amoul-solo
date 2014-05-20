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

