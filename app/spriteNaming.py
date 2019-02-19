
import json
import zipfile


class SpriteNaming():

    """Module that keeps track of how often sprites default 
       
    names (like Sprite1, Sprite2...) are used within a project.
    
    """

    def __init__(self):

      self.total_default = 0
      self.list_default = []
      self.default_names = ["Sprite","Objeto"]

   
    """Output the default sprite names found in the project."""
    def finalize(self):
       result = ""
       
       result += ("%d default sprite names found:\n" % self.total_default)
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
              if dicc_key == "name":
                for default in self.default_names:
                   if default in dicc_value:
                      self.total_default += 1
                      self.list_default.append(dicc_value)



def main(filename):
    """The entrypoint for the 'spriteNaming' extension"""

    naming = SpriteNaming()
    naming.analyze(filename)
    return naming.finalize()




