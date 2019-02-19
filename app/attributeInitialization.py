
import json
import zipfile


class AttributeInitialization():

    """
    Plugin that checks if modified attributes are properly initialized.

    """   

    BLOCKMAPPING = {
        'costume': frozenset([('looks_switchbackdropto', 'absolute'),
                              ('looks_nextbackdrop', 'relative'),
                              ('looks_switchcostumeto', 'absolute'),
                              ('looks_nextcostume', 'relative')]),
        'orientation': frozenset([('motion_turnright', 'relative'),
                                  ('motion_turnleft', 'relative'),
                                  ('motion_pointindirection', 'absolute'),
                                  ('motion_pointtowards_menu', 'relative')]),
        'position': frozenset([('motion_movesteps', 'relative'),
                               ('motion_gotoxy', 'absolute'),                            
                               ('motion_goto', 'relative'),
                               ('motion_glidesecstoxy', 'relative'),
                               ('motion_glideto', 'relative'),
                               ('motion_changexby', 'relative'),
                               ('motion_setx', 'absolute'),
                               ('motion_changeyby', 'relative'),
                               ('motion_sety', 'absolute')]),
        'size': frozenset([('looks_changesizeby', 'relative'),
                           ('looks_setsizeto', 'absolute')]),
        'visibility': frozenset([('looks_hide', 'absolute'),
                                 ('looks_show', 'absolute')])
                  }


    def __init__(self):

      self.total_default = 0
      self.list_default = []
      self.attributes = ['costume', 'orientation', 'position', 'size', 'visibility']

      
   
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
             blocks_set = dicc["blocks"]
             block_list = self.iter_blocks(blocks_set)
             for name in block_list:
                for attribute in self.attributes:
                   if (name, 'absolute') in self.BLOCKMAPPING[attribute]:
                     print (name, 'absolute')
                   elif (name, 'relative') in self.BLOCKMAPPING[attribute]:
                     print (name, 'relative')
                   else:
                     print name



    def iter_blocks(self, blocks_set):

       block_list = []

       for _, block_value in blocks_set.iteritems():
          if block_value['opcode'] == 'event_whenflagclicked':
             next_block = block_value["next"]
             
             for block_id, block in blocks_set.iteritems():
                if block_id == next_block:
                   block_list.append(str(block['opcode']))
                   next_block = block['next']


       return block_list
                  


def main(filename):
    """The entrypoint for the 'attributeInitialization' extension"""

    attinit = AttributeInitialization()
    attinit.analyze(filename)
    return attinit.finalize()



