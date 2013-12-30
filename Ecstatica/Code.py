# coding: utf-8

#Created on 18.01.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

import itertools

def tokenIsString(token):
    if token & 0xf000 == 0xe000:
        return token & 0x0fff + 1
    else:
        return -1
    
slang_keyword_dict = {  0x00:"?", 
                        0x01:"?", 
                        0x02:"?", 
                        0x03:"IF", 
                        0x04:"ELSE", 
                        0x05:"ELSEIF", 
                        0x06:"ENDIF", 
                        0x07:"PlayScene", 
                        0x08:"Started", 
                        0x09:"NotStarted", 
                        0x0A:"Finished",
                        0x0B:"NotFinished", 
                        0x0C:"RepeatScene", 
                        0x0D:"AnyKeyPressed", 
                        0x0E:"FacingNorth", 
                        0x0F:"FacingSouth", 
                        0x10:"FacingEast", 
                        0x11:"FacingWest",
                        0x12:"NotPlaying", 
                        0x13:"NoKeyPressed", 
                        0x14:"DrawScene", 
                        0x15:"DrawRoof", 
                        0x16:"InRightHand", 
                        0x17:"InLeftHand", 
                        0x18:"ActivatedBelow", 
                        0x19:"NOT", 
                        0x1A:"CheckActor", 
                        0x1B:"ForceAction", 
                        0x1D:"SceneFlagged", 
                        0x1E:"SetSceneFlag", 
                        0x1F:"ClearSceneFlag", 
                        0x20:"ClearSubtitles", 
                        0x21:"CameraWasOff", 
                        0x22:"RepIs", 
                        0x23:"MakeRep", 
                        0x24:"MapAreaHeight", 
                        0x26:"StopTune", 
                        0x28:"Female", 
                        0x2B:"Key1Pressed", 
                        0x2C:"Key3Pressed", 
                        0x2D:"Key1or3Pressed", 
                        0x2E:"SwapHands", 
                        0x2F:"LeftHandFree", 
                        0x30:"RightHandFree", 
                        0x31:"RenderViews", 
                        0x32:"FadeOutTune", 
                        0x33:"CantBeHit", 
                        0x34:"CanBeHit", 
                        0x35:"HitPointsAbove", 
                        0x36:"MakeHidden", 
                        0x37:"MakeVisible", 
                        0x38:"QuitToDos", 
                        0x39:"RemoveAllGraphic", 
                        0x3A:"MakeDead", 
                        0x3B:"AdjustHitPoints", 
                        0x3C:"CauseGetHit", 
                        0x3D:"SetFullHitPoints", 
                        0x3E:"ExecuteCode", 
                        0x3F:"PartIs", 
                        0x40:"BlockActor", 
                        0x41:"BlockWanderers", 
                        0x42:"BlockAll", 
                        0x43:"SetHitPoints", 
                        0x44:"ForceEscapeKey", 
                        0x45:"SetHitPtX100", 
                        0x46:"SetFullHitPtX100", 
                        0x47:"HitPtsAboveX10", 
                        0x48:"PlayEndScene", 
                        0x49:"ExecuteActorCode" 
                        }

class Code(object):
    def __init__(self, index, slang, tokens):
        self.index = index        
        self.slang = slang
        self.tokens = tokens
        
    def __str__(self):
        stri = "Code " + str(self.index) + "\n"
        if self.slang != None:
            for line in self.slang:
                stri += line + "\n"
        else:
            stri += "Sorry, cannot print token code yet :("
        return stri
    
    def __eq__(self, other):
        if self.index != other.index:
            return False
        if self.tokens != other.tokens:
            return False
        for ourline, theirline in itertools.izip(self.slang, other.slang):
            if ourline.strip() != theirline.strip():
                return False
            
        return True
    
    def __ne__(self, other):
        return not self.__eq__(other)

def printToken(tokenlist):
    i = 0
    while i < len(tokenlist):
        if tokenlist[i] == 0:
            print("NO_TOKEN")
            i+= 1 
        elif tokenlist[i] & 0xf000 == 0xe000:
            length = tokenlist[i] & 0x0fff + 1 
            print("\"" + tokenlist[i+1:i+1+length])
            i += length + 1 
        elif tokenlist[i] & 0xf000 == 0xf000:
            number = tokenlist[i] & 0x0fff
            if number & 0x800 != 0:
                number = number | 0xf000
            print(number)
            i += 1 
        elif tokenlist[i] & 0xf000 == 0:
            index = tokenlist[i] & 0x0fff
            print(slang_keyword_dict[index])
            i += 1
            
def createCodeFromText(index_text, sourcecode_text, tokenlist_text):
    index = int(index_text)
    assert index >= 0
    
    sourcecode = sourcecode_text
    tokenlist = tokenlist_text.split(',')
    
    return Code(index, sourcecode, tokenlist)
