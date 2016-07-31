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

class Grille(Objet):
  valeurs = db.StringProperty();
  niveau = db.IntegerProperty()
  solution = db.StringProperty();

  def raz(self):
    valeurs = "000000000000000000000000000000000000000000000000000000000000000000000000000000000";
    solution = "";

  def pretty(self):
    ret = "";
    if self.valeurs:
      for i,c in enumerate(self.valeurs):
        if (i+1) % 9 == 0:
          ret = ret+c+"<br/>";
        else:
          ret = ret+c;
    return ret

  def get_tableau(self):
    ret = "<table class=\"sudoku\"><tbody><tr>";
    if self.valeurs:
      for i,c in enumerate(self.valeurs):
        td = "";
        tr = "";
        content = "";

        if c == '0':
          td = " onClick=\"selectionne('d"+str(i)+"')\"";
          content = "<i>&nbsp;</i>";
        else:
          content = "<b>"+c+"</b>";

        if i % 3 == 2:
          td = td+" class=\"sudoku\"";

        if i == 17:
          tr = " class=\"sudoku\"";
        elif i == 44:
          tr = " class=\"sudoku\"";
        elif i == 71:
          tr = " class=\"sudoku\"";

        if (i+1) % 9 == 0:
          ret = ret+"<td id=\"d"+str(i)+"\""+td+">"+content+"</td></tr><tr"+tr+">";
        else:
          ret = ret+"<td id=\"d"+str(i)+"\""+td+">"+content+"</td>";

    ret = ret + "</tr></tbody></table>";
    return ret

  def get_formulaire_creation(self):
    form ="<form action=\"/addEssai\" method=\"post\">";
    form = form + "<input type=\"hidden\" name=\"grille\" value=\""+str(self.key().id())+"\"/>";
    for i,c in enumerate(self.valeurs):
      form = form + "<input type=\"hidden\" name=\"v"+str(i)+"\" value=\""+c+"\"/>";
    form = form + "<input class=\"submit\" type=\"submit\" value=\"Enregistrer cet essai\"/>";
    form = form + "</form><br/>";
    return form;

  def get_tableau_solution(self):
    ret = "<table class=\"sudoku\"><tbody><tr>";

    if self.solution:
      for i,c in enumerate(self.solution):
        td = "";
        tr = "";

        if i % 3 == 2:
          td = " class=\"sudoku\""

        if i == 17:
          tr = " class=\"sudoku\""
        elif i == 44:
          tr = " class=\"sudoku\""
        elif i == 71:
          tr = " class=\"sudoku\""

        if (i+1) % 9 == 0:
          if self.valeurs[i] == '0':
            ret = ret + "<td"+td+"><i>"+c+"</i></td></tr><tr"+tr+">";
          else:
            ret = ret + "<td"+td+"><b>"+c+"</b></td></tr><tr"+tr+">";
        else:
          if self.valeurs[i] == '0':
            ret = ret + "<td"+td+"><i>"+c+"</i></td>";
          else:
            ret = ret + "<td"+td+"><b>"+c+"</b></td>";

    ret = ret + "</tr></tbody></table>";
    return ret

class Essai(Objet):
  valeurs = db.StringProperty();
  grille = db.ReferenceProperty(Grille, collection_name='essais')

  def get_formulaire_update(self):
    form ="<form action=\"/updateEssai\" method=\"post\">";
    form = form + "<input type=\"hidden\" name=\"essai\" value=\""+str(self.key().id())+"\"/>";
    for i,c in enumerate(self.valeurs):
      form = form + "<input type=\"hidden\" name=\"v"+str(i)+"\" value=\""+c+"\"/>";
    form = form + "<input class=\"submit\" type=\"submit\" value=\"Enregistrer l'&eacute;tat de cet essai\"/>";
    form = form + "</form><br/>";
    return form;

  def get_tableau(self):
    ret = "<table class=\"sudoku\"><tbody><tr>";
    if self.valeurs:
      for i,c in enumerate(self.valeurs):
        td = "";
        tr = "";
        content = "";

        if c == '0':
          td = " onClick=\"selectionne('d"+str(i)+"')\"";
          content = "<i>&nbsp;</i>";
        else:
          content = "<b>"+c+"</b>";

        if i % 3 == 2:
          td = td+" class=\"sudoku\"";

        if i == 17:
          tr = " class=\"sudoku\"";
        elif i == 44:
          tr = " class=\"sudoku\"";
        elif i == 71:
          tr = " class=\"sudoku\"";

        if (i+1) % 9 == 0:
          ret = ret+"<td id=\"d"+str(i)+"\""+td+">"+content+"</td></tr><tr"+tr+">";
        else:
          ret = ret+"<td id=\"d"+str(i)+"\""+td+">"+content+"</td>";

    ret = ret + "</tr></tbody></table>";
    return ret

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
