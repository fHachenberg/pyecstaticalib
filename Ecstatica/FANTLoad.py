# coding: utf-8

#Created on 08.03.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

import struct
import itertools
import os

from . import Sound
from . import Code
from . import Event
from . import MapArea
from . import SectorSection
from . import Camera
from . import Fixpoint

from .Event import NextSceneEvent

def readNames(fileobj):    
    names = []
        
    char = fileobj.read(1)
    #if the first char is 0 right away, the list of strings is empty!
    while ord(char) != 0:
        count = 0
        strbuffer = b""
        while ord(char) != 0:
            #if ord(char) < 32:
            #    char = '_'         
            strbuffer += char
            char = fileobj.read(1)                             
            count += 1
            if count >= 50:
                raise Exception("Name too long:")
        
        string = str(strbuffer)
        #we remove whitespaces after the name
        if count >= 2:
            string = string.rstrip(' ')
        
        #TODO(correctness) I'm not certain I reproduced the string 
        #transformation at 2B49A correctly
        
        #add the new name to the db
        names.append(string)
        
        char = fileobj.read(1)
    
    return names
    
def readEvent(fileobj):
    '''
    Reads an event object from file
    '''
    
    evttype = struct.unpack(">h", fileobj.read(2))[0]
    index = struct.unpack(">h", fileobj.read(2))[0]
    value1 = struct.unpack(">h", fileobj.read(2))[0]
    value2 = struct.unpack(">h", fileobj.read(2))[0]
    value3 = struct.unpack(">h", fileobj.read(2))[0]
    #There's a special case: ev_NEXT_SCENE
    #This Event is directly followed by at least 25 bytes of data which are used to initialize
    #a struc_19 object of the scene object
    #We simply read in the data and attach it to the Event
    if evttype == Event.ev_NEXT_SCENE:        
        #the additional data block is present only when index != 0
        if index != 0:            
            #read in data
            #The special data sections ends with a 0 byte
            #We have to read in data until we reach that, thgouh -after 24 bytes - we're not storing anymore what we read in
            uk_data = b""
            char = fileobj.read(1)
            length = 0
            while ord(char) != 0:
                if length >= 24:
                    break
                uk_data += char
                char = fileobj.read(1)
            while ord(char) != 0:
                print("exceeding char in NEXT_SCENE-Event:", ord(char))
                char = fileobj.read(1)
            #print "read attachment of length", len(uk_data)
        else: 
            uk_data = b""
                     
        return NextSceneEvent(index, value1, value2, value3, uk_data)
    else:                        
        return Event.Event(index, evttype, value1, value2, value3)

def readSound(fileobj, indextable, fileversion):
    '''
    Reads a single sound object from file
    '''
    
    file_index = struct.unpack("<h", fileobj.read(2))[0]
    #print "sound index", file_index
    if file_index < 0:
        raise Exception("negative sound index. Dunno what to do :(")
    else:
        index = indextable[file_index]
    
    #IMPORTANT: In the original loading code, flag 1 is automatically set like this:
    #flags = 1 | struct.unpack("<H", fileobj.read(2))[0]  
    #(flag 1 propably means "loaded"?)
    #I don't do this here, because THIS loading code has the meaning to represent the content of the file    
    #I have changed h to H here, because i think in such a packed-data value you cannot use a sign...    
    flags = struct.unpack("<H", fileobj.read(2))[0]
    unknown1 = struct.unpack("<h", fileobj.read(2))[0]
    length = struct.unpack("<i", fileobj.read(4))[0]
    if fileversion >= 27:
        unknown = struct.unpack("<h", fileobj.read(2))[0]
    else:
        unknown = 100
    
    data = fileobj.read(length)
    
    return Sound.Sound(index, length, unknown, unknown1, data, flags)

def readMapArea(fileobj, indextable, fileversion):
        file_index = struct.unpack("<h", fileobj.read(2))[0]
        if file_index < 0:
            raise Exception("negative maparea index. Dunno what to do :(")
        else:
            index = indextable[file_index]
        
        numvalues = struct.unpack("<h", fileobj.read(2))[0]
        numvalues = min(10, numvalues) #see 2CBD9
        values = []
        for i in range(numvalues):
            values.append(struct.unpack("<h", fileobj.read(2))[0])
        
        maparea = MapArea.MapArea(index, values)
        return maparea
        
def readCode(fileobj, indextable, fileversion):
        file_index = struct.unpack(">h", fileobj.read(2))[0]
        if file_index >= len(indextable):
            print(file_index, "in", len(indextable))
        index = indextable[file_index]
        if index < 0:
            raise Exception("negative code index. Dunno what to do :(")        
        
        tokenlist=[]
        token = struct.unpack(">h", fileobj.read(2))[0]
        while token != 0:
            tokenlist.append(token)
            strlen = Code.tokenIsString(token)
            if strlen > 0: #this is a string
                string = fileobj.read(2*(strlen/2))
                #print string
                tokenlist.append(string)
            token = struct.unpack(">h", fileobj.read(2))[0]
        
        numlines = struct.unpack(">h", fileobj.read(2))[0]
        lines = []
        for j in range(numlines):
            linestr = b""
            char = fileobj.read(1)
            while ord(char) != 0:
                linestr += char
                char = fileobj.read(1)
            linestr = str(linestr)
            linestr.replace("NOT present", "CheckActor") #seems to be a measure to grant downward compatibility
            lines.append(str(linestr))
                
        code = Code.Code(index, lines, tokenlist)
        
        return code
    
def readSectorSection(fileobj, indextable, fileversion):        
    #2CA4F
    prio = struct.unpack("B", fileobj.read(1))[0]
    y_uk = prio
    section = struct.unpack("b", fileobj.read(1))[0] 
    cam_idx = struct.unpack("B", fileobj.read(1))[0]     
    ymax = struct.unpack("B", fileobj.read(1))[0]
    unknown1 = struct.unpack("b", fileobj.read(1))[0]
    if fileversion >= 21:
        fileobj.read(1) #alignment
     
    #I have changed h to H here, because i think in such a packed-data value you cannot use a sign...
    combivalue = struct.unpack(">H", fileobj.read(2))[0]
    fileindex = combivalue & 0x3fff #extract lower 14 bits containing code idx
    codeidx = fileindex #self.codenameidxs[fileindex]
    inccodeidx = codeidx + 1 #+1 is a convention
    
    flags = combivalue & 0xC000 #extract upper 2 bits
    
    if fileversion >= 10:
        fileobj.read(2) #alignment
        
    return SectorSection.SectorSection(prio, section, unknown1, cam_idx, y_uk, ymax, inccodeidx, flags)
    
def readCamera(fileobj, indextable, fileversion):
    x = struct.unpack("<h", fileobj.read(2))[0]
    y = struct.unpack("<h", fileobj.read(2))[0]
    z = struct.unpack("<h", fileobj.read(2))[0]
    ax = struct.unpack("<h", fileobj.read(2))[0]
    ay = struct.unpack("<h", fileobj.read(2))[0]
    az = struct.unpack("<h", fileobj.read(2))[0]
    f = struct.unpack("<h", fileobj.read(2))[0]
    #x = Fixpoint.tofloat(struct.unpack("<h", fileobj.read(2))[0])
    #y = Fixpoint.tofloat(struct.unpack("<h", fileobj.read(2))[0])
    #z = Fixpoint.tofloat(struct.unpack("<h", fileobj.read(2))[0])
    #ax = Fixpoint.fpangletorad(struct.unpack("<h", fileobj.read(2))[0])
    #ay = Fixpoint.fpangletorad(struct.unpack("<h", fileobj.read(2))[0])
    #az = Fixpoint.fpangletorad(struct.unpack("<h", fileobj.read(2))[0])
    #f = Fixpoint.fpangletorad(struct.unpack("<h", fileobj.read(2))[0])    
    return Camera.Camera((x,y,z), (ax, ay, az), f)


from . import FantFile    

class FANTFileLoader(object):
    '''
    This is a as-simple-as-possible implementation for creating a XML file from a FANT file
    It works similiar to FANTFile, except it does simply forward als data to the XML document instead of interpreting it...
    '''   

    def __init__(self, fileobj, save_terminal_events=True):
        '''
        Constructor
        '''                    
        
        self.fantfile = FantFile.FANTFile()
        
        #see _readevent for a brief description
        self.save_terminal_events = save_terminal_events
        self.fantfile.eventlists_contain_terminal_event = self.save_terminal_events
        
        self.fileobj = fileobj
        self.autoskip = 1
        
        #the object to which all loaded data is passed        
        
        self.state = "open"            
                
        magicstring = self.fileobj.read(4)
        print(magicstring)
        if magicstring != b"FANT":
            raise IOError("This is not a FANT file")
        
        self.fileversion = struct.unpack(">h", self.fileobj.read(2))[0]     
        #print "fileversion=", self.fileversion
        if self.fileversion < 26:
            self.skip_transtables = 0
        else:
            self.skip_transtables = struct.unpack(">h", self.fileobj.read(2))[0]
        self.fantfile.skip_transtables = self.skip_transtables #hack?
               
        if self.fileversion >= 23:
            self.unknownstr = self.fileobj.read(26)
            
        if self.fileversion >= 15 and self.fileversion <= 17:
            self.aCodeIndices = range(1500)
            if self.autoskip == 0:
                print("Bad File Version")
                return
            
        #print "after header", hex(self.fileobj.tell())
            
        self.state = "header_loaded"
        
        if self.skip_transtables == 0:                        
            self.fantfile.partnameidxs = self.fantfile.partnames.addNames(readNames(self.fileobj))            
            self.fantfile.actornameidxs = self.fantfile.actornames.addNames(readNames(self.fileobj))
            self.fantfile.actionnameidxs = self.fantfile.actionnames.addNames(readNames(self.fileobj))
            self.fantfile.scenenameidxs = self.fantfile.scenenames.addNames(readNames(self.fileobj))
            
            if self.fileversion >= 2:
                self.fantfile.pointnameidxs = self.fantfile.pointnames.addNames(readNames(self.fileobj))            
                self.fantfile.trinameidxs = self.fantfile.trianglenames.addNames(readNames(self.fileobj))                
                
            if self.fileversion >= 6:
                self.fantfile.codenameidxs = self.fantfile.codenames.addNames(readNames(self.fileobj))                
            
            if self.fileversion >= 12:
                self.fantfile.repertnameidxs = self.fantfile.repertoirenames.addNames(readNames(self.fileobj))                
                
            if self.fileversion >= 16:
                self.fantfile.soundnameidxs = self.fantfile.soundnames.addNames(readNames(self.fileobj))                
                
            if self.fileversion >= 20:
                self.fantfile.mapareanameidxs = self.fantfile.mapareanames.addNames(readNames(self.fileobj))
                                            
        else:
            self.fantfile._initIndexArrays()                    
            
        if self.fileversion >= 4:  
            #print "before action events", hex(self.fileobj.tell())       
            self._readActionEvents()
            #print "before actor events", hex(self.fileobj.tell())
            self._readActorEvents()
        else:
            raise Exception("Not implemented")      
    
        #print "before scene events", hex(self.fileobj.tell())
        self._readSceneScriptEvents()            
       
        if self.fileversion > 6:
            #print "before codes", hex(self.fileobj.tell())
            self._readCodes()

        if self.fileversion > 13:
            #print "before repert events", hex(self.fileobj.tell())
            self._readRepertoireEvents()
            
        if self.fileversion > 16:
            #print "before sounds", hex(self.fileobj.tell())
            self._readSounds()
            
        if self.fileversion > 9:
            self.skip_field = struct.unpack(">h", self.fileobj.read(2))[0]
            if self.skip_field != 0:
                self._readSectorData()
                self._readCameras()
                self._readMapAreas()
        if self.autoskip == 0:
            pass
            #Geometrie Transformation für alle Actors
            #2BE12
            #Initialisierung für Actors-Positionen
            #raise StandardError("Not implemented")
        
        #TODO
        #Alle Actions müssen Flag 1 löschen (Zählung beginnt bei 0)
        
        self.state = "loaded"
    
    def _readSounds(self):
        '''
        reads all sounds from file
        '''
        more = struct.unpack("b", self.fileobj.read(1))[0]
        #print "more-flag=", more
        i = 0
        #print "before sound", hex(self.fileobj.tell())
        while more != 0:
            sound = readSound(self.fileobj, self.fantfile.soundnameidxs, self.fileversion)
            self.fantfile.sounds.append(sound)            
            more = struct.unpack("b", self.fileobj.read(1))[0]
            i+=1
            
    def _readMapAreas(self):
        '''
        reads all mapareas from the file
        '''
        more = struct.unpack("b", self.fileobj.read(1))[0]
        while more != 0:
            maparea = readMapArea(self.fileobj, self.fantfile.mapareanameidxs, self.fileversion)
            self.fantfile.mapareas.append(maparea)                   
            more = struct.unpack("b", self.fileobj.read(1))[0]
            
    def _readCodes(self):
        numcodes = struct.unpack(">h", self.fileobj.read(2))[0]
        for i in range(numcodes):            
            code = readCode(self.fileobj, self.fantfile.codenameidxs, self.fileversion)
            self.fantfile.codes.append(code)            
    
    def _readSectorData(self):
        '''
        Loads a 128x128 array of indices into the sector sections array from the file
        '''        
        filedta = self.fileobj.read(128*128*2)
        self.fantfile.sectormap = struct.unpack("<" + "".join(itertools.repeat("h", 128*128)), filedta)
        
        #k = open("/tmp/data", "wb")
        #k.write(filedta)
        #k.close()
        
        numitems = struct.unpack(">i", self.fileobj.read(4))[0]
        print("Number of sector section entries found in FANT file:", numitems)
        assert numitems < 30000                        
        
        for i in range(numitems):
            section = readSectorSection(self.fileobj, None, self.fileversion)
            self.fantfile.sectorsections.append(section)            
    
    def _readCameras(self):
        '''
        Reads all camera configs from the file
        '''
        numconfigs = struct.unpack("<h", self.fileobj.read(2))[0]
        for i in range(numconfigs):
            camera = readCamera(self.fileobj, None, self.fileversion)
            self.fantfile.cameras.append(camera)                
    
    def _readevent(self):
        event = readEvent(self.fileobj)
        while event.event_type != Event.ev_NO_EVENT:        
            yield event
            event = readEvent(self.fileobj)
        #if we are in debug mode, we output the final event as well
        #because we are aiming to recreate the FANT file later up to the last bit
        #Those terminating events are undefined except for their event type id ev_NO_EVENT
        #In the original FANT files, those terminating events are not all zero but have
        #specific values. Maybe those are just uninitialized values - in any case, we save
        #their state to write them later... 
        if self.save_terminal_events:
            yield event
                    
    def _readRepertoireEvents(self):
        for event in self._readevent():
            self.fantfile.repertoireevents.append(event)
    
    def _readActionEvents(self):                
        for event in self._readevent():
            self.fantfile.actionevents.append(event)
    
    def _readActorEvents(self):
        for event in self._readevent():
            self.fantfile.actorevents.append(event)
                    
    def _readSceneScriptEvents(self):
        for event in self._readevent():                        
            self.fantfile.sceneevents.append(event)
        
def loadFANTFile(filename):
    fileobj = open(filename, "rb")
    loader = FANTFileLoader(fileobj)
    return loader.fantfile
            
def loadFANTStack(filename):
    fantfiles = []
    
    fileobj = open(filename, "rb")
    
    while True:
        if __debug__:
            print("LOADING NEXT FANT FILE from offset", fileobj.tell())
        loader = FANTFileLoader(fileobj)
        fantfiles.append(loader.fantfile)        
        
        #we check the next character
        #if there's another FANT file attached, this char then
        #has to be "F". 
        #(to not be an error, we ought to have read in at least ONE FANT file)
        testchar = fileobj.read(1)
        if testchar == b"": #no more characters present, end of file
            break        
        if testchar != b"F": #does NOT look like beginning of another FANT file
            print("Warning: Found junk data after last FANT file in stack")
            break
        #restore file pointer
        fileobj.seek(-1, os.SEEK_CUR)
    
    return fantfiles
     
import unittest
        
class TestFANTFileLoader(unittest.TestCase):
    def testLoader(self):
        doc = FANTFileLoader(open("test/ecstatic.fan", "rb"))
        print(list(doc.fantfile.partnames))

if __name__ == "__main__":
    f = open("test/ecstatic.fan", "rb") 
    print(FantFile(f, 0))
