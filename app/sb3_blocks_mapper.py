
import json


class BlocksMapper():

    def __init__(self):

        self.categories = ["motion", "looks", "sound", "data", "event", "control", "operator", "sensing", "procedures",
                           "videoSensing", "pen", "music", "text2speech", "translate", "makeymakey"]

    def analyze(self, block):
        category = block.split("_")[0]
        block_name = block.split("_")[1]

        if len(block.split("_")) > 2:
            block_name = block.split("_")[1] + "_" + block.split("_")[2]

        if category == "motion":
           result = self.motion_mapper(block_name)
        elif category == "looks":
           result = self.look_mapper(block_name)
        elif category == "sound":
           result = self.sound_mapper(block_name)
        elif category == "event":
           result = self.event_mapper(block_name)
        elif category == "control":
           result = self.control_mapper(block_name)
        elif category == "sensing":
           result = self.sensing_mapper(block_name)
        elif category == "operator":
           result = self.operator_mapper(block_name)
        elif category == "data":
           result = self.data_mapper(block_name)
        elif category == "procedures":
           result = self.procedures_mapper(block_name)
        elif category == "music":
           result = self.music_mapper(block_name)
        else:
           result = block_name

        return result


    #___MOTION CATEGORY___#

    def motion_mapper(self, block_name):
        if block_name == "movesteps":
            block_name = "move () steps"
        elif block_name == "turnright":
            block_name = "turn cw () degrees"
        elif block_name == "turnleft":
            block_name = "turn ccw () degrees"
        elif block_name == "goto":
            block_name = "go to ( v)"
        elif block_name == "gotoxy":
            block_name = "go to x: () y: ()"
        elif block_name == "glideto":
            block_name = "glide () secs to x: () y: ()"
        elif block_name == "glidesecstoxy":
            block_name = "glide () secs to ( v)"
        elif block_name == "pointindirection":
            block_name = "point in direction ()"
        elif block_name == "pointtowards":
            block_name = "point towards ( v)"
        elif block_name == "changexby":
            block_name = "change x by ()"
        elif block_name == "setx":
            block_name = "set x to ()"
        elif block_name == "changeyby":
            block_name = "change y by ()"
        elif block_name == "sety":
            block_name = "set y to ()"
        elif block_name == "ifonedgebounce":
            block_name = "if on edge, bounce"
        elif block_name == "setrotationstyle":
            block_name = "set rotation style [ v]"
        elif block_name == "xposition":
            block_name = "x position"
        elif block_name == "yposition":
            block_name = "y position"
        else:
            pass

        return block_name


    # ___LOOKS CATEGORY___#

    def look_mapper(self, block_name):
        if block_name == "sayforsecs":
            block_name = "say () for () secs"
        elif block_name == "say":
            block_name = "say ()"
        elif block_name == "thinkforsecs":
            block_name = "think () for () secs"
        elif block_name == "think":
            block_name = "think ()"
        elif block_name == "switchcostumeto":
            block_name = "switch costume to ( v)"
        elif block_name == "nextcostume":
            block_name = "next costume"
        elif block_name == "switchbackdropto":
            block_name = "switch backdrop to ( v)"
        elif block_name == "nextbackdrop":
            block_name = "next backdrop"
        elif block_name == "changesizeby":
            block_name = "change size by ()"
        elif block_name == "setsizeto":
            block_name = "set size to () %"
        elif block_name == "changeeffectby":
            block_name = "change [ v] effect by ()"
        elif block_name == "seteffectto":
            block_name = "set [ v] effect to ()"
        elif block_name == "cleargraphiceffects":
            block_name = "clear graphic effects"
        elif block_name == "gotofrontback":
            block_name = "go to [ v] layer"
        elif block_name == "goforwardbackwardlayers":
            block_name = "go [ v] () layers"
        elif block_name == "costumenumbername":
            block_name = "costume ( v)"
        elif block_name == "backdropnumbername":
            block_name = "backdrop ( v)"
        else:
            pass

        return block_name


    # ___SOUND CATEGORY___#

    def sound_mapper(self, block_name):
        if block_name == "playuntildone":
            block_name = "play sound ( v) until done"
        elif block_name == "play":
            block_name = "start sound ( v)"
        elif block_name == "stopallsounds":
            block_name = "stop all sounds"
        elif block_name == "changeeffectby":
            block_name = "change [pitch v] effect by ()"
        elif block_name == "seteffectto":
            block_name = "set [pitch v] effect to ()"
        elif block_name == "cleareffects":
            block_name = "clear sound effects"
        elif block_name == "changevolumeby":
            block_name = "change volume by ()"
        elif block_name == "setvolumeto":
            block_name = "set volume to () %"

        else:
            pass

        return block_name



    # ___EVENT CATEGORY___#

    def event_mapper(self, block_name):
        if block_name == "whenflagclicked":
            block_name = "when flag clicked"
        elif block_name == "whenkeypressed":
            block_name = "when [ v] key pressed"
        elif block_name == "whenthisspriteclicked":
            block_name = "when this sprite clicked"
        elif block_name == "whenbackdropswitchesto":
            block_name = "when backdrop switches to [ v]"
        elif block_name == "whengreaterthan":
            block_name = "when [ v] > ()"
        elif block_name == "whenbroadcastreceived":
            block_name = "when I receive [ v]"
        elif block_name == "broadcast":
            block_name = "broadcast ( v)"
        elif block_name == "broadcastandwait":
            block_name = "broadcast ( v) and wait"
        elif block_name == "whenstageclicked":
            block_name = "when stage clicked :: hat events"
        else:
            pass

        return block_name



    # ___CONTROL CATEGORY___#

    def control_mapper(self, block_name):
        if block_name == "wait":
            block_name = "wait () secs"
        elif block_name == "repeat":
            block_name = "repeat ()"
        elif block_name == "if":
            block_name = "if <> then"
        elif block_name == "if_else":
            block_name = "if <> then"
        elif block_name == "else":
            block_name = "else"
        elif block_name == "wait_until":
            block_name = "wait until <>"
        elif block_name == "repeat_until":
            block_name = "repeat until <>"
        elif block_name == "stop":
            block_name = "stop [ v]"
        elif block_name == "start_as":
            block_name = "when I start as a clone"
        elif block_name == "create_clone":
            block_name = "create clone of ( v)"
        elif block_name == "delete_this":
            block_name = "delete this clone"

        return block_name




    # ___SENSING CATEGORY___#

    def sensing_mapper(self, block_name):
        if block_name == "touchingobject":
            block_name = "touching ( v)"
        elif block_name == "touchingcolor":
            block_name = "touching color (#F3A533)?"
        elif block_name == "coloristouchingcolor":
            block_name = "color (#988686) is touching (#F3A533)?"
        elif block_name == "distanceto":
            block_name = "distance to ( v)"
        elif block_name == "askandwait":
            block_name = "ask () and wait"
        elif block_name == "keypressed":
            block_name = "key ( v) pressed?"
        elif block_name == "mousedown":
            block_name = "mouse down ?"
        elif block_name == "mousex":
            block_name = "mouse x"
        elif block_name == "mousey":
            block_name = "mouse y"
        elif block_name == "setdragmode":
            block_name = "set drag mode [ v]"
        elif block_name == "resettimer":
            block_name = "reset timer"
        elif block_name == "of":
            block_name = "[ v] of ( v)"
        elif block_name == "current":
            block_name = "current [ v]"
        elif block_name == "dayssince2000":
            block_name = "days since 2000"
        else:
            pass

        return block_name




    # ___OPERATOR CATEGORY___#

    def operator_mapper(self, block_name):
        if block_name == "add":
            block_name = "() + ()"
        elif block_name == "subtract":
            block_name = "() - ()"
        elif block_name == "multiply":
            block_name = "() * ()"
        elif block_name == "divide":
            block_name = "() / ()"
        elif block_name == "random":
            block_name = "pick random () to ()"
        elif block_name == "gt":
            block_name = "() > ()"
        elif block_name == "lt":
            block_name = "() < ()"
        elif block_name == "equals":
            block_name = "() = ()"
        elif block_name == "and":
            block_name = "<> and <>"
        elif block_name == "or":
            block_name = "<> or <>"
        elif block_name == "not":
            block_name = "not <>"
        elif block_name == "join":
            block_name = "join () ()"
        elif block_name == "letter_of":
            block_name = "letter () of ()"
        elif block_name == "length":
            block_name = "length of ()"
        elif block_name == "contains":
            block_name = "() contains () ?"
        elif block_name == "mod":
            block_name = "() mod ()"
        elif block_name == "round":
            block_name = "round ()"
        elif block_name == "mathop":
            block_name = "[abs v] of ()"
        else:
            pass

        return block_name



    # ___DATA CATEGORY___#
    def data_mapper(self, block_name):
        if block_name == "setvariableto":
            block_name = "set [ v] to ()"
        elif block_name == "changevariableby":
            block_name = "change [ v] by ()"
        elif block_name == "showvariable":
            block_name = "show variable [ v]"
        elif block_name == "hidevariable":
            block_name = "hide variable [ v]"
        elif block_name == "addtolist":
            block_name = "add () to [ v]"
        elif block_name == "deleteoflist":
            block_name = "delete () of [ v]"
        elif block_name == "deletealloflist":
            block_name = "delete all of [ v]"
        elif block_name == "insertatlist":
            block_name = "insert () at () of [ v]"
        elif block_name == "replaceitemoflist":
            block_name = "replace item () of [ v] with ()"
        elif block_name == "itemoflist":
            block_name = "item () of [ v]"
        elif block_name == "itemnumoflist":
            block_name = "item # of () in [ v]"
        elif block_name == "lengthoflist":
            block_name = "length of [ v]"
        elif block_name == "listcontainsitem":
            block_name = "[ v] contains ()?"
        elif block_name == "showlist":
            block_name = "show list [ v]"
        elif block_name == "hidelist":
            block_name = "hide list [ v]"
        else:
            pass

        return block_name



    #____PROCEDURES CATEGORY___#
    def procedures_mapper(self, block_name):
        if block_name == "definition":
            block_name = "define my block"
        elif block_name == "call":
            block_name = "my block :: custom"
        else:
            pass

        return block_name



    # ____MUSIC CATEGORY___#
    def music_mapper(self, block_name):
        if block_name == "playDrumForBeats":
            block_name = "play drum ( v) for () beats"
        elif block_name == "restForBeats":
            block_name = "rest for () beats"
        elif block_name == "playNoteForBeats":
            block_name = "play note () for () beats"
        elif block_name == "setInstrument":
            block_name = "set instrument to ( v)"
        elif block_name == "setTempo":
            block_name = "set tempo to ()"
        elif block_name == "changeTempo":
            block_name = "change tempo by ()"
        elif block_name == "getTempo":
            block_name = "tempo"
        else:
            pass

        return block_name


def main(block):
    """The entrypoint for the scratchblocks_v3 mapper"""

    mapper = BlocksMapper()
    return mapper.analyze(block)
    # return mapper.finalize()