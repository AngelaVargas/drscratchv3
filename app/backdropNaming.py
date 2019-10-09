#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import json
import zipfile


class BackdropNaming():

    """Module that keeps track of how often backdrops default 
       
    names (like Backdrop1, Backdrop2...) are used within a project.
    
    """

    def __init__(self):

      self.total_default = 0
      self.list_default = []
      self.default_names = ["backdrop", "fondo", "fons", "atzeko oihala"]

   
    """Output the default backdrop names found in the project."""
    def finalize(self):
       result = ""
       
       result += ("%d default backdrop names found:\n" % self.total_default)
       for name in self.list_default:
            result += name
            result += "\n"

       return result


    """Run and return the results from the SpriteNaming module."""
    def analyze(self, filename):
       
      zip_file = zipfile.ZipFile(filename, "r")
      json_project = json.loads(zip_file.open("project.json").read())

      for key, value in json_project.iteritems():
        if key == "targets":
          for dicc in value:
            for dicc_key, dicc_value in dicc.iteritems():
              if dicc_key == "costumes":
                for backdrop in dicc_value:
                  for name_key, name_value in backdrop.iteritems():
                    if name_key == "name":
                      for default in self.default_names:
                        if default in name_value:
                          self.total_default += 1
                          self.list_default.append(name_value)



def main(filename):
    """The entrypoint for the 'backdropNaming' extension"""

    naming = BackdropNaming()
    naming.analyze(filename)
    return naming.finalize()




