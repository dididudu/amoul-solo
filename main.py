#!/usr/bin/env python
#
# AMOUL SOLO PROJECT
#

__author__ = 'Didier Dulac'

import webapp2

from actions import BaseRequestHandler
from actions import AddEssai
from actions import AddExpression
from actions import AddGrille
from actions import AddTag
from actions import AddMesure
from actions import AddTagToExpression
from actions import ComputeMesures
from actions import ListExpressions
from actions import ListGrilles
from actions import ListTags
from actions import ListMesures
from actions import UpgradeGrille
from actions import DowngradeGrille
from actions import DeleteGrille
from actions import ViewExpression
from actions import ViewGrille

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
  ('/addMesure', AddMesure),
  ('/addTagToExpression', AddTagToExpression),
  ('/expressions', ListExpressions),
  ('/expression/([-\w]+)', ViewExpression),
  ('/tags', ListTags),
  ('/addGrille', AddGrille),
  ('/deleteGrille/([-\w]+)', DeleteGrille),
  ('/upgradeGrille/([-\w]+)', UpgradeGrille),
  ('/downgradeGrille/([-\w]+)', DowngradeGrille),
  ('/grilles', ListGrilles),
  ('/grille/([-\w]+)', ViewGrille),
  ('/addEssai', AddEssai),
  ('/mesures', ListMesures),
  ('/computeMesures', ComputeMesures)
], debug=True)
