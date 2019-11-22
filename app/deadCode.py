import json
import zipfile

import logging

logger = logging.getLogger(__name__)


class DeadCode():

    """Plugin that indicates unreachable code in Scratch files."""

    def __init__(self):

      self.dead_code_instances = 0
      self.event_variables = ["event_whenbroadcastreceived", "event_whenflagclicked", "event_whengreaterthan", "event_whenkeypressed",
                              "event_whenthisspriteclicked", "event_whenbackdropswitchesto", "event_whenstageclicked",
                              "control_start_as_clone", "procedures_definition"]
      self.loop_blocks = ["control_repeat", "control_forever", "control_if", "control_if_else", "control_repeat_until"]
      self.blocks_dicc = {}
      self.recurs_blocks = []



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
                   if blocks_value["opcode"] != "procedures_prototype":
                        self.blocks_dicc[blocks] = blocks_value

            for key_block in self.blocks_dicc:
                block = self.blocks_dicc[key_block]
                event_variable = any(block["opcode"] == event for event in self.event_variables)
                loop_block = any(block["opcode"] == loop for loop in self.loop_blocks)
                list = []

                if block["parent"] == None and block["next"] == None:
                    # DEAD BLOCK: NO PARENTS AND CHILDREN
                    list, _ = self.check_loop_block(block, list)
                    blocks_list.append(list)

                elif block["topLevel"] == True and block["next"] != None and not event_variable:
                    # DEAD STRUCTURE: NO HAT BLOCKS
                    list, is_loop = self.check_loop_block(block,list)
                    # if is_loop:
                        # next = block["next"]
                        # block = self.blocks_dicc[next]
                        # try:
                        #     l_block = block["inputs"]["SUBSTACK"][1]
                        #     list, _ = self.check_loop_block(self.blocks_dicc[l_block], list)
                        # except:
                        #     pass

                        # Check if it's an if_else block
                        # try:
                        #     l2_block = block["inputs"]["SUBSTACK2"][1]
                        #     list.append("control_else")
                        #     list, _ = self.check_loop_block(self.blocks_dicc[l2_block], list)
                        #     list.append("finish_end")
                        # except:
                        #     pass

                        # list.append("finish_end")

                        # try:
                        #     next = self.blocks_dicc[block]["next"]
                        #     list = self.search_next(next, list)
                        # except:
                        #     pass

                    blocks_list.append(list)

                elif block["parent"] != None and loop_block:
                    # DEAD BLOCKS INSIDE AN STRUCTURE: EMPTY BLOCKS
                    list, is_loop = self.check_loop_block(block, list)
                    if list and not is_loop:
                        #Add the parent
                        parent = block["parent"]
                        parent_block = self.blocks_dicc[parent]
                        list.insert(0, parent_block["opcode"])
                        if any(parent_block["opcode"] == loop for loop in self.loop_blocks):
                            #The parent it's also a control block
                            list.append("finish_end")
                        blocks_list.append(list)
                else:
                    #Normal block
                    pass

            if blocks_list:
              sprites[sprite] = blocks_list
              self.dead_code_instances += 1

      return sprites



    def check_loop_block(self, block, list):
        loop_block = any(block["opcode"] == loop for loop in self.loop_blocks)
        normal_loop = True
        is_loop = False

        if loop_block:
            is_loop = True
            try:
                next_in_loop = block["inputs"]["SUBSTACK"][1]
                list.append(block["opcode"])
                if next_in_loop:
                    list, _ = self.check_loop_block(self.blocks_dicc[next_in_loop], list)
                else:
                    normal_loop = False
            except:
                normal_loop = False
                list.append(block["opcode"])

            self.check_if_else(block,list)
            list.append("finish_end")
            if normal_loop:
                if block["next"] != None:
                    list,_ = self.check_loop_block(self.blocks_dicc[block["next"]], list)
                    list = self.search_next(self.blocks_dicc[block["next"]]["next"], list)

        else:
            list.append(block["opcode"])
            try:
                list, _ = self.check_loop_block(self.blocks_dicc[block["next"]], list)
            except:
                list = self.search_next(block["next"], list)

        return list, is_loop



    def search_next(self, next, list):

        if next:
            #Update
            next_block = self.blocks_dicc[next]
            list.append(next_block["opcode"])
            next = next_block['next']
            self.search_next(next, list)

        return list



    def check_if_else(self, block, list):
        if block["opcode"] == "control_if_else":
            list.append("control_else")
            try:
                else_block = block["inputs"]["SUBSTACK2"][1]
                next_block = self.blocks_dicc[else_block]
                loop_list, _ = self.check_loop_block(next_block, list)
            except:
                return
        else:
            return




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


