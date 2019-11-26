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
      self.control_blocks = ["control_wait", "control_repeat", "control_if", "control_if_else", "control_wait_until",
                             "control_repeat_until"]
      self.blocks_dicc = {}
      self.total_blocks = {}



    """Run and return the results form the DeadCode plugin."""
    def analyze(self, filename):

      zip_file = zipfile.ZipFile(filename, "r")
      json_project = json.loads(zip_file.open("project.json").read())

      self.save_blocks(json_project)

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
                control_block = any(block["opcode"] == control for control in self.control_blocks)
                list = []

                if block["parent"] == None and block["next"] == None:
                    # DEAD BLOCK: NO PARENTS AND CHILDREN
                    list, _ = self.check_loop_block(block, list)
                    blocks_list.append(list)

                elif block["topLevel"] == True and block["next"] != None and not event_variable:
                    # DEAD STRUCTURE: NO HAT BLOCKS
                    list, is_loop = self.check_loop_block(block,list)
                    blocks_list.append(list)

                elif block["parent"] != None and control_block:
                    # DEAD BLOCKS INSIDE AN STRUCTURE: EMPTY BLOCKS

                    # 1. WITH NO CONDITIONS
                    empty_list = self.check_empty_conditions(block)
                    if empty_list:
                        blocks_list.append(empty_list)

                    # 2. WITH NO BLOCKS INSIDE
                    if loop_block and not empty_list:
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

                elif block["opcode"] == "event_whenbroadcastreceived":
                    # BLOCKS WAITING FOR A MESSAGE THAT IS NOT SENT
                    broadcast_list = self.check_message(block)
                    if broadcast_list:
                        blocks_list.append(broadcast_list)

                else:
                    #Normal block
                    pass

            if blocks_list:
              sprites[sprite] = blocks_list
              self.dead_code_instances += 1

      return sprites


    #___ SAVE ALL THE BLOCKS TOGETHER___#
    def save_blocks(self, file):

        for blocks_dicc in file["targets"]:
            for key, value in blocks_dicc["blocks"].iteritems():
                if type(value) is dict:
                   self.total_blocks[key] = value


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
                    list, loop = self.check_loop_block(self.blocks_dicc[block["next"]], list)

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


    def check_empty_conditions(self, block):
        empty_list = []

        if block["opcode"] == "control_wait":
            condition = block["inputs"]["DURATION"][1][1]
            if not condition:
                empty_list.append(block["opcode"])
        elif block["opcode"] == "control_repeat":
            condition = block["inputs"]["TIMES"][1][1]
            if not condition:
                empty_list, _ = self.check_loop_block(block, empty_list)
        elif block["opcode"] == "control_wait_until":
            if not block["inputs"]:
                empty_list.append(block["opcode"])
        else:
            try:
                condition = block["inputs"]["CONDITION"][1]
                if condition == None:
                    empty_list, _ = self.check_loop_block(block, empty_list)
            except:
                empty_list, _ = self.check_loop_block(block, empty_list)

        return empty_list




    def check_message(self, block):

        find_message = False
        broadcast_list = []
        message = block["fields"]["BROADCAST_OPTION"][0]
        broadcast_id = block["fields"]["BROADCAST_OPTION"][1]

        for broad_key in self.total_blocks:
            broad_block = self.total_blocks[broad_key]
            if broad_block["opcode"] == "event_broadcastandwait" or broad_block["opcode"] == "event_broadcast":
                if broad_block["inputs"]["BROADCAST_INPUT"][1][2] == broadcast_id:
                    find_message = True

        if not find_message:
            name_block = block["opcode"] + "_" + message
            broadcast_list.append(name_block)

        return broadcast_list



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


