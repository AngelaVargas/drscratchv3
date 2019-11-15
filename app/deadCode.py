import json
import zipfile

import logging

logger = logging.getLogger(__name__)


class DeadCode():

    """Plugin that indicates unreachable code in Scratch files."""

    def __init__(self):

      self.dead_code_instances = 0
      self.opcode_argument_reporter = "argument_reporter"
      self.event_variables = ["event_whenbroadcastreceived", "event_whenflagclicked", "event_whengreaterthan", "event_whenkeypressed",
                              "event_whenthisspriteclicked", "event_whenbackdropswitchesto",
                              "control_start_as_clone"]

      #I have to do different
      self.procedures = "procedures_prototype"

      self.loop_blocks = ["control_repeat", "control_forever", "control_if", "control_if_else", "control_repeat_until"]
      self.blocks_dicc = {}


    """Run and return the results form the DeadCode plugin."""
    def analyze(self, filename):

      zip_file = zipfile.ZipFile(filename, "r")
      json_project = json.loads(zip_file.open("project.json").read())

      sprites = {}
      for key, value in json_project.iteritems():
        if key == "targets":
          for dicc in value:
            sprite = dicc["name"]
            #New loop for a new sprite
            blocks_list = []
            self.blocks_dicc = {}

            for blocks, blocks_value in dicc["blocks"].iteritems():
               #Create the list of blocks for this sprite
               if type(blocks_value) is dict:
                   self.blocks_dicc[blocks] = blocks_value

            for key_block in self.blocks_dicc:
                block = self.blocks_dicc[key_block]
                event_variable = any(block["opcode"] == event for event in self.event_variables)
                loop_block = any(block["opcode"] == loop for loop in self.loop_blocks)

                # if not self.opcode_argument_reporter in block["opcode"]:
                if block["opcode"] != "procedures_prototype":
                    if block["parent"] == None and block["next"] == None:
                    #Check if it's a loop_block without parent and next, but with blocks inside
                        if loop_block:
                            try:
                                next = block["inputs"]["SUBSTACK"][1]
                                list = []
                                list = self.search_next(next, block, list)
                                list.append("finish_end")
                                blocks_list.append(list)
                            except:
                                blocks_list.append([block["opcode"], "finish_end"])
                        else:
                             blocks_list.append([block["opcode"]])
                    elif block["topLevel"] == True and block["next"] != None and not event_variable:
                        next = block["next"]
                        list = []
                        list = self.search_next(next, block, list)
                        blocks_list.append(list)
                    elif loop_block:
                        #Check dead loop blocks inside a structure
                        parent = block["parent"]
                        parent_block = self.blocks_dicc[parent]
                        if not block["inputs"]:
                            blocks_list.append([parent_block["opcode"], block["opcode"], "finish_end"])
                        elif "SUBSTACK" not in block["inputs"]:
                            blocks_list.append([parent_block["opcode"], block["opcode"], "finish_end"])
                        else:
                            #Could be normal loop block
                            if block["inputs"]["SUBSTACK"][1] == None:
                                blocks_list.append([parent_block["opcode"], block["opcode"], "finish_end"])
                    else:
                        #Normal block
                        pass

            if blocks_list:
              sprites[sprite] = blocks_list
              self.dead_code_instances += 1

      return sprites

    def search_next(self, next, block, list):
        if next == None:
            list.append(block["opcode"])
        else:
            list.append(block['opcode'])
            #Update
            next_block = self.blocks_dicc[next]
            next = next_block['next']
            self.search_next(next, next_block, list)

        return list



    """Output the number of instances that contained dead code."""
    def finalize(self, dicc_deadCode, filename):
       
      result = ""
      result += filename
      if self.dead_code_instances > 0:
         result += "\n"               
         result += str(dicc_deadCode)

      return result



def main(filename):
    """The entrypoint for the 'deadCode' extension"""

    deadCode = DeadCode()
    result = deadCode.analyze(filename)
    return deadCode.finalize(result, filename)


