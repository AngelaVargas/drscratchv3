import json
from collections import Counter
import sys
import zipfile


# /home/angela/Escritorio/drScratch/drScratch/uploads/346.sb3


class Mastery: 

  """Analyzer of projects sb3, the new version Scratch 3.0"""

  def __init__(self):

    self.mastery_dicc = {}		#New dict to save punctuation
    self.total_blocks = [] #List with blocks
    self.blocks_dicc = Counter()		#Dict with blocks



  """Start the analysis."""
  def process(self,filename):
        

   zip_file = zipfile.ZipFile(filename, "r")
   json_project = json.loads(zip_file.open("project.json").read())
  
   for key, value in json_project.iteritems():
     if key == "targets":
       for dicc in value:
          for dicc_key, dicc_value in dicc.iteritems():
            if dicc_key == "blocks":
              for blocks, blocks_value in dicc_value.iteritems():
                self.total_blocks.append(blocks_value)
  
   for block in self.total_blocks:
     for key, value in block.iteritems():
       if key == "opcode":
          self.blocks_dicc[value] += 1




def main(filename):
    """The entrypoint for the `Mastery` extension"""

    mastery = Mastery()
    mastery.process(filename)
    mastery.analyze()
    return mastery.finalize(filename)



