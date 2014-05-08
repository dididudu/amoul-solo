#!/usr/bin/env python
#
# AMOUL SOLO PROJECT
#

__author__ = 'Didier Dulac'

import webapp2

from actions import BaseRequestHandler

class MainPage(BaseRequestHandler):
  def get(self):
    template_values = {
      }
    self.generate('index.html', template_values)

application = webapp2.WSGIApplication([
  ('/', MainPage)
], debug=True)
