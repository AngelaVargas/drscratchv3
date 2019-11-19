
import json
import zipfile


class DuplicateScripts():

   """Analyzer of duplicate scripts in projects sb3, the new version Scratch 3.0"""

   def __init__(self):

     self.total_duplicate = 0
     self.blocks_dicc = {}
     self.total_blocks = []
     self.list_duplicate = []
     self.blocks_dup = {}
     #self.list_duplicate_string = []


   """Only takes into account scripts with more than 5 blocks"""
   def analyze(self, filename):

     zip_file = zipfile.ZipFile(filename, "r")
     json_project = json.loads(zip_file.open("project.json").read())
  
     scripts_set = {}

     for key, value in json_project.iteritems():
       if key == "targets":
         for dicc in value:
           sprite = dicc["name"]
           self.blocks_dicc = {}
           scripts_set[sprite] = []

           for blocks, blocks_value in dicc["blocks"].iteritems():
               # for blocks, blocks_value in dicc_value.iteritems():
                 if type(blocks_value) is dict:
                   self.blocks_dicc[blocks] = blocks_value
                   self.total_blocks.append(blocks_value)

           for key_block in self.blocks_dicc:
               block = self.blocks_dicc[key_block]

               if block["topLevel"] == True:
                  block_list = []
                  block_list.append(str(block["opcode"]))
                  next = block["next"]
                  aux_next = []
                  self.search_next(next, block_list, key_block, aux_next)
                  print block_list

                  blocks_tuple = tuple(block_list)
                  #Only scripts with more than 5 blocks
                  if len(block_list) >= 5:
                    scripts_set[sprite].append(blocks_tuple)

                  for sprite_key, sprite_value in scripts_set.iteritems():
                     if sprite_key != sprite:
                         if blocks_tuple in sprite_value:
                            if block_list not in self.list_duplicate:
                                self.list_duplicate.append(block_list)
                                self.total_duplicate += 1


     #Find the number of duplicates
     for repeat_block in self.list_duplicate:
        sprites_dup = []

        for key, value in scripts_set.iteritems():
            if tuple(repeat_block) in value:
               sprites_dup.append(str(key))

        sprites_dup = ", ".join(sprites_dup)
        self.blocks_dup[sprites_dup] = repeat_block



   def search_next(self, next, block_list, key_block, aux_next):
       if next == None:
           try:
              # Maybe is a loop block
              next = self.blocks_dicc[key_block]["inputs"]["SUBSTACK"][1]
              if next == None:
                  block_list.append("finish_end")
                  return
              # try:
              #     else_block = self.blocks_dicc[key_block]["inputs"]["SUBSTACK2"][1]
              # except:
              #     else_block = None
           except:
              if aux_next:      #Check if there is an aux_next saved
                next = aux_next[-1]
                aux_next.pop(-1)
                block_list.append("finish_end")
              else:
                next = None
                return
       else:
            # Maybe is a loop block
            if "SUBSTACK" in self.blocks_dicc[key_block]["inputs"]:
                loop_block = self.blocks_dicc[key_block]["inputs"]["SUBSTACK"][1]
                #Check if is a loop block but EMPTY
                if loop_block != None:
                    aux_next.append(next)          #Add the real next until the end of the loop
                    next = loop_block



       block = self.blocks_dicc[next]
       block_list.append(str(block["opcode"]))
       key_block = next
       next = block["next"]
       self.search_next(next, block_list, key_block, aux_next)



   """Output the duplicate scripts detected."""
   def finalize(self):

     result = ("%d duplicate scripts found" % self.total_duplicate)
     result += "\n"
     result += str(self.blocks_dup)

     return result



def main(filename):
    """The entrypoint for the 'duplicateScripts' extension"""

 
    duplicate = DuplicateScripts()
    duplicate.analyze(filename)
    return duplicate.finalize()


