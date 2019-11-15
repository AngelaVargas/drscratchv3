
import json


class BlocksMapper():

    def __init__(self):

        self.categories = ["motion", "looks", "sound", "data", "event", "control", "operator", "sensing", "procedures",
                           "videoSensing", "pen", "music", "text2speech", "translate", "makeymakey"]

    def analyze(self, block):
        category = block.split("_")[0]
        block_name = block.split("_")[1]
        if category == "motion":
           result = self.motion_mapper(block_name)
        elif category == "looks":
           result = self.look_mapper(block_name)
        elif category == "sound":
           result = self.data_mapper(block_name)
        elif category == "event":
           result = self.event_mapper(block_name)
        elif category == "control":
           result = self.control_mapper(block_name)
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
            block_name = block_name
        return block_name


    def look_mapper(self, block_name):
        if block_name == "sayforsecs":
            block_name = "say () for () secs"
        elif block_name == "say":
            block_name = "say ()"
        elif block_name == "thinkforsecs":
            block_name = "think () for () secs"
        elif block_name == "setsizeto":
            block_name = "set size to ()"
        elif block_name == "seteffectto":
            block_name = "set [ v] effect to ()"
        elif block_name == "changesizeby":
            block_name = "change size by ()"
        else:
            block_name = block_name
        return block_name

    def sound_mapper(self, block_name):
        return block_name

    def data_mapper(self, block_name):
        return block_name

    def event_mapper(self, block_name):
        if block_name == "whenflagclicked":
            block_name = "when flag clicked"
        return block_name

    def control_mapper(self, block_name):
        if block_name == "if":
            block_name = "if () then"
        elif block_name == "repeat":
            block_name = "repeat ()"
        elif block_name == "start":
            block_name = "when I start as a clone"
        elif block_name == "stop":
            block_name = "stop [ v]"
        return block_name


def main(block):
    """The entrypoint for the scratchblocks_v3 mapper"""

    mapper = BlocksMapper()
    return mapper.analyze(block)
    # return mapper.finalize()