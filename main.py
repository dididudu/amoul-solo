#!/usr/bin/env python
#
# AMOUL SOLO PROJECT
#

__author__ = 'Didier Dulac'

import webapp2

from actions import BaseRequestHandler
from actions import AddExpression
from actions import AddTag
from actions import ListExpressions
from actions import ListTags

class MainPage(BaseRequestHandler):
  def get(self):
    template_values = {
      }
    self.generate('index.html', template_values)

class AboutPage(BaseRequestHandler):
  def get(self):
    template_values = {
      }
    self.generate('about.html', template_values)

class ContactsPage(BaseRequestHandler):
  def get(self):
    template_values = {
      }
    self.generate('contacts.html', template_values)

application = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/about', AboutPage),
  ('/contacts', ContactsPage),
  ('/addExpression', AddExpression),
  ('/addTag', AddTag),
  ('/expressions', ListExpressions),
  ('/tags', ListTags)
], debug=True)
