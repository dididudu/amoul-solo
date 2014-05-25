#!/usr/bin/env python
#
# AMOUL SOLO PROJECT
#

__author__ = 'Didier Dulac'

import datetime
import logging

from google.appengine.ext import db

class Objet(db.Model):
  created_by = db.UserProperty()
  created = db.DateTimeProperty(auto_now_add=True)
  updated_by = db.UserProperty()
  updated = db.DateTimeProperty(auto_now=True)

class Tag(Objet):
  nom = db.StringProperty()

  def expressions(self):
    return Expression.gql("WHERE tags = :1", self.key())

class Expression(Objet):
  francais = db.StringProperty()
  wolof = db.StringProperty()
  tags = db.ListProperty(db.Key)

  def mes_tags(self):
    return Tag.get(self.tags)
