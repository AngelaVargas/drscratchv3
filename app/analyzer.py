#Analyzer of projects sb3, the new version Scratch 3.0

import json
from collections import Counter
import sys
import zipfile



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
                if type(blocks_value) is dict:
                  self.total_blocks.append(blocks_value)
  
   for block in self.total_blocks:
     for key, value in block.iteritems():
       if key == "opcode":
          self.blocks_dicc[value] += 1




  """Run and return the results of Mastery. """
  def analyze(self):
      
     self.logic() 
     self.flow_control()
     self.synchronization()
     self.abstraction()
     self.data_representation()
     self.user_interactivity()
     self.parallelization()
     



  """Output the overall programming competence"""
  def finalize(self, filename):
   result = ""

   result += filename 
   result += '\n'

   result += json.dumps(self.mastery_dicc)
   result += '\n'
   
   total = 0
   for i in self.mastery_dicc.items():
     total += i[1]
   result += ("Total mastery points: %d/21\n" % total)
   
   average =  float (total) / 7
   result += ("Average mastery points: %.2f/3\n" % average)

   if average > 2:
    result += "Overall programming competence: Proficiency"
   elif average > 1:
    result += "Overall programming competence: Developing"
   else:
    result += "Overall programming competence: Basic"

   return result



  """Assign the Logic skill result"""
  def logic(self):

   operations = {'operator_and', 'operator_or', 'operator_not'}
   score = 0
  
   for operation in operations:
     if self.blocks_dicc[operation]:
        score = 3
        self.mastery_dicc['Logic'] = score
        return
  
   if self.blocks_dicc['control_if_else']:
     score = 2
   elif self.blocks_dicc['control_if']:
     score = 1
  
   self.mastery_dicc['Logic'] = score



  """Assign the Flow Control skill result"""     
  def flow_control(self):

   score = 0
  
   if self.blocks_dicc['control_repeat_until']:
     score = 3
   elif (self.blocks_dicc['control_repeat'] or self.blocks_dicc['control_forever']):
     score = 2
   else:
     for block in self.total_blocks:
       for key, value in block.iteritems():
         if key == "next" and value != None:
            score = 1
            break
       
     
   self.mastery_dicc['FlowControl'] = score




  """Assign the Syncronization skill result"""
  def synchronization(self):
    
   score = 0
   
   if (self.blocks_dicc['control_wait_until'] or
       self.blocks_dicc['event_whenbackdropswitchesto'] or
       self.blocks_dicc['event_broadcastandwait']):
            score = 3
   elif (self.blocks_dicc['event_broadcast'] or 
         self.blocks_dicc['event_whenbroadcastreceived'] or
         self.blocks_dicc['control_stop']):
            score = 2
   elif self.blocks_dicc['control_wait']:
            score = 1
  
   self.mastery_dicc['Synchronization'] = score



  """Assign the Abstraction skill result"""
  def abstraction(self):
        
   score = 0
        
   if self.blocks_dicc['control_start_as_clone']:
            score = 3
   elif self.blocks_dicc['procedures_definition']:
            score = 2
   else:
      count = 0
      for block in self.total_blocks:
        for key, value in block.iteritems():
          if key == "parent" and value == None:
            count += 1
      if count > 1 :
         score = 1

   self.mastery_dicc['Abstraction'] = score



  """Assign the Data representation skill result"""
  def data_representation(self):
        
   score = 0
  
   modifiers = {'motion_movesteps', 'motion_gotoxy', 'motion_glidesecstoxy', 'motion_setx', 'motion_sety', 
               'motion_changexby', 'motion_changeyby', 'motion_pointindirection', 'motion_pointtowards',
               'motion_turnright', 'motion_turnleft', 'motion_goto', 
               'looks_changesizeby', 'looks_setsizeto', 'looks_switchcostumeto', 'looks_nextcostume', 
               'looks_changeeffectby', 'looks_seteffectto', 'looks_show', 'looks_hide', 'looks_switchbackdropto', 
               'looks_nextbackdrop'}

   lists = {'data_lengthoflist', 'data_showlist', 'data_insertatlist', 'data_deleteoflist', 'data_addtolist',
           'data_replaceitemoflist', 'data_listcontainsitem', 'data_hidelist', 'data_itemoflist'}
        
   for item in lists:
    if self.blocks_dicc[item]:
       score = 3
       self.mastery_dicc['DataRepresentation'] = score
       return
  
   if self.blocks_dicc['data_changevariableby'] or self.blocks_dicc['data_setvariableto']:
     score = 2
   else:
    for modifier in modifiers:
       if self.blocks_dicc[modifier]:
          score = 1


   self.mastery_dicc['DataRepresentation'] = score



  """Assign the User Interactivity skill result"""
  def user_interactivity(self):
   score = 0
       
   proficiency = {'videoSensing_videoToggle', 'videoSensing_videoOn', 'videoSensing_whenMotionGreaterThan',
                  'videoSensing_setVideoTransparency', 'sensing_loudness'}
        
   developing = {'event_whenkeypressed', 'event_whenthisspriteclicked', 'sensing_mousedown', 'sensing_keypressed',
                 'sensing_askandwait', 'sensing_answer'}

   for item in proficiency:
      if self.blocks_dicc[item]:
          self.mastery_dicc['UserInteractivity'] = 3
          return
   for item in developing:
      if self.blocks_dicc[item]:
          self.mastery_dicc['UserInteractivity'] = 2
          return
   if self.blocks_dicc['motion_goto_menu']:
      if self.check_mouse() == 1:
          self.mastery_dicc['UserInteractivity'] = 2
          return
   if self.blocks_dicc['sensing_touchingobjectmenu']:
      if self.check_mouse() == 1:
          self.mastery_dicc['UserInteractivity'] = 2
          return
   if self.blocks_dicc['event_whenflagclicked']:
       score = 1
    
   self.mastery_dicc['UserInteractivity'] = score


  """Check whether there is a block 'go to mouse' or 'touching mouse-pointer?' """
  def check_mouse(self):

   for block in self.total_blocks:
     for key, value in block.iteritems():
       if key == 'fields':
         for mouse_key, mouse_val in value.iteritems():
           if (mouse_key == 'TO' or mouse_key =='TOUCHINGOBJECTMENU') and mouse_val[0] == '_mouse_':
                 return 1

   return 0



  """Assign the Parallelization skill result"""
  def parallelization (self):
       
   score = 0
   keys = [] 
   messages = []
   backdrops = []
   multimedia = []
   dict_parall = {}
 
   dict_parall = self.parallelization_dict()


   if self.blocks_dicc['event_whenbroadcastreceived'] > 1:            # 2 Scripts start on the same received message
     if dict_parall['BROADCAST_OPTION']:
          new_message = dict_parall['BROADCAST_OPTION']
          if new_message in messages:
              score = 3
              self.mastery_dicc['Parallelization'] = score
              return
          else:
              messages.append(new_message)

   if self.blocks_dicc['event_whenbackdropswitchesto'] > 1:           # 2 Scripts start on the same backdrop change
      if dict_parall['BACKDROP']:
          new_backdrop = dict_parall['BACKDROP']
          if new_backdrop in backdrops:
              score = 3
              self.mastery_dicc['Parallelization'] = score
              return
          else:
              backdrops.append(new_backdrop)

   if self.blocks_dicc['event_whengreaterthan'] > 1:                  # 2 Scripts start on the same multimedia (audio, timer) event
      if dict_parall['WHENGREATERTHANMENU']:
         new_multi = dict_parall['WHENGREATERTHANMENU']
         if new_multi in multimedia:
              score = 3
              self.mastery_dicc['Parallelization'] = score
              return
         else:
              multimedia.append(new_multi)

   if self.blocks_dicc['videoSensing_whenMotionGreaterThan'] > 1:     # 2 Scripts start on the same multimedia (video) event
        score = 3
        self.mastery_dicc['Parallelization'] = score
        return
 
   if self.blocks_dicc['event_whenkeypressed'] > 1:                   # 2 Scripts start on the same key pressed
     if dict_parall['KEY_OPTION']:
          new_key = dict_parall['KEY_OPTION']
          if new_key in keys:
              score = 2
          else:
              keys.append(new_key)  
                              
   if self.blocks_dicc['event_whenthisspriteclicked'] > 1:           # Sprite with 2 scripts on clicked
     score = 2
  
   if self.blocks_dicc['event_whenflagclicked'] > 1 and score == 0:  # 2 scripts on green flag
     score = 1
  

   self.mastery_dicc['Parallelization'] = score



  def parallelization_dict(self):
   dicc = {}

   for block in self.total_blocks:
     for key, value in block.iteritems():
         if key == 'fields':
           for key_pressed, val_pressed in value.iteritems():  
              dicc[key_pressed] = val_pressed   

   return dicc



def main(filename):
    """The entrypoint for the `Mastery` extension"""

    mastery = Mastery()
    mastery.process(filename)
    mastery.analyze()
    return mastery.finalize(filename)





