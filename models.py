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

class Mesure(db.Model):
  jour = db.DateProperty()
  annee = db.IntegerProperty()
  valeur = db.IntegerProperty()
  nb_jours = db.IntegerProperty()
  conso = db.IntegerProperty()
  type = db.StringProperty(choices=set(["E", "G"]))

  def get_conso(self):
    ret = 0.0
    if self.nb_jours:
      ret = (self.conso * 1.0) / self.nb_jours
    return ret
