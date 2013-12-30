# coding: utf-8

#Created on 19.02.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

import struct
import itertools
import codecs

from . import Fixpoint
from . import Event
from .Event import ev_NO_EVENT
from . import FantFile 

from . import FANTLoad


def fantifyNameList(namelist):    
    stringlist = b""
    for name in namelist:        
        stringlist += bytes(name, 'utf-8')
        stringlist += struct.pack('b', 0)
    stringlist += struct.pack('b', 0)
    return stringlist

def fantifyEventList(eventlist):
    '''    
    '''
    #by default, we always construct a terminal event and attach it to the list
    #but if the last event in the given list is already a NO_EVENT-event, we omit our own
    attach_terminal_event = True
    
    eventliststr = b""
    for event in eventlist:
        eventliststr += struct.pack(">hhhhh", event.event_type, event.index, event.value1, event.value2, event.value3)
        if event.event_type == Event.ev_NEXT_SCENE and event.index != 0: #special case! We have to attach data
            #eventliststr += struct.pack(">" + "".join(itertools.repeat("b", len(event.uk_data))), event.uk_data)
            eventliststr += event.uk_data.encode("ascii")
            eventliststr += struct.pack("b", 0)
        elif event.event_type == Event.ev_NO_EVENT:
            assert event == eventlist[-1] #make sure this is the last event in the list!
            attach_terminal_event = False
            
    if attach_terminal_event:
        #we append a ZERO-event to mark the end of the event list    
        
        #In the original ECSTATICA data files, I found that the NO-EVENT-Events have actually specific values for value1, value2, value3
        #I use these values here
        #Except in one case: When the list of events is completele empty. So we do this differentiation here too...
        if len(eventlist) > 0:
            eventliststr += struct.pack('>HhHHH', ev_NO_EVENT, 0, 0x160a, 0x004d, 0xd0f7)
        else:
            eventliststr += struct.pack(">hhhhh", Event.ev_NO_EVENT, 0, 0, 0, 0)
    return eventliststr

def fantifyCode(code):
    codestr = b""
    
    codestr += struct.pack(">h", code.index)
    
    for token in code.tokens:    
        codestr += struct.pack(">h", token)
    codestr += struct.pack(">h", 0)
    
    #TODO: I'm not satisfied with the current state here
    #I have to use an ascii encoder in order to connect the byte string for the code object
    #with the human-readable Sourcecode, which could come as unicode string!
    #but I'm sure there's a more elegant way to do this encoding!
    encoder = codecs.getencoder('ascii')
    
    codestr += struct.pack(">h", len(code.slang))
    for line in code.slang:
        encodedstr, unknownnumber = encoder(line)      
        codestr += encodedstr
        codestr += struct.pack("b", 0)
        
    return codestr

def fantifyCodeList(codelist):
    #we first provide the total number of entries in the following list of code instances
    codeliststr = struct.pack(">h", len(codelist))        
    for code in codelist:
        codeliststr += fantifyCode(code)
        
    return codeliststr

def fantifySectorSection(section):
    
    secstr = b""
    #2CA4F    
    print(section.prio)
    secstr += struct.pack("B", section.prio)
    secstr += struct.pack("b", section.section) 
    secstr += struct.pack("B", section.cam_idx)     
    secstr += struct.pack("B", section.ymax)
    secstr += struct.pack("b", section.unknown1)
    secstr += struct.pack("b", 4) #dummy byte for alignment, value 4 is taken from official ecstatica files
    
    deccodeidx = section.codeidx_plus_one - 1
    combivalue = section.flags |  deccodeidx 
    #print hex(combivalue)
    secstr += struct.pack(">H", combivalue)
    secstr += struct.pack(">H", 0xff3f) #dummy word for alignment, value 0xff3f is taken from official ecstatica files
        
    return secstr

def fantifySectorSectionList(seclist):
    secliststr = b""
        
    #we write out the total number of items in the following sequence of sector sections
    secliststr += struct.pack(">i", len(seclist))    
    print("number of sectorsections=", len(seclist))
    for sec in seclist:
        secliststr += fantifySectorSection(sec)
        
    return secliststr

def fantifyCamera(camera):
    camstr = b""
        
    #camstr += struct.pack("<h", Fixpoint.tofixpoint(camera.position[0], 14))
    #camstr += struct.pack("<h", Fixpoint.tofixpoint(camera.position[1], 14))
    #camstr += struct.pack("<h", Fixpoint.tofixpoint(camera.position[2], 14))
    #camstr += struct.pack("<h", Fixpoint.radtofpangle(camera.angles[0]))
    #camstr += struct.pack("<h", Fixpoint.radtofpangle(camera.angles[1]))
    #camstr += struct.pack("<h", Fixpoint.radtofpangle(camera.angles[2]))
    #camstr += struct.pack("<h", Fixpoint.tofixpoint(camera.f, 14))
    camstr += struct.pack("<h", camera.position[0])
    camstr += struct.pack("<h", camera.position[1])
    camstr += struct.pack("<h", camera.position[2])
    camstr += struct.pack("<h", camera.angles[0])
    camstr += struct.pack("<h", camera.angles[1])
    camstr += struct.pack("<h", camera.angles[2])
    camstr += struct.pack("<h", camera.f)
    
    return camstr

def fantifyCameraList(camlist):
    camliststr =b""
    
     #we write out the total number of items in the following sequence of cameras
    camliststr += struct.pack("<H", len(camlist))    
    for camera in camlist:
        camliststr += fantifyCamera(camera)
        
    return camliststr    

def fantifySound(sound):
    soundstr = b""
    
    soundstr += struct.pack("<h", sound.index)
    
    #IMPORTANT: see FANTLoad.fantifySound: In the original loading code, flag 1 is
    #automatically set. We don't do this, so in the saving code (here) we don't have to
    #clear the flag!
    combivalue = sound.flags
    soundstr += struct.pack("<H", combivalue)
    
    soundstr += struct.pack("<h", sound.unknown1)                
    soundstr += struct.pack("<i", sound.length)
    soundstr += struct.pack("<h", sound.unknown)        
    
    soundstr += sound.data
    
    return soundstr

def fantifySoundList(sndlist):
    #the output is a sequence of sound-structs, connected by a non-zero byte signaling after each instance, that another
    #instance is following
    if len(sndlist) == 0:
        return struct.pack("b", 0)
    else:    
        return struct.pack("b", 0x53) + struct.pack("b", 0x53).join(map(lambda sound: fantifySound(sound), sndlist)) + struct.pack("b", 0)    

def fantifySectormap(heightmap):
    #print len(heightmap)
    data = struct.pack("<"  + "".join(itertools.repeat("h", 128*128)), *heightmap)
    return data

def fantifyMapArea(maparea):
    mapareastr = b""
    
    mapareastr += struct.pack("<h", maparea.index)
    
    numvalues = min(10, len(maparea.values)) #see 2CBD9
    mapareastr += struct.pack("<h", len(maparea.values))
    
    i = 0
    for value in maparea.values:
        mapareastr += struct.pack("<h", value)
        i += 1
        #FANT file format supports a maximum of 10 values in the map area
        if i >= 10:
            break
    
    return mapareastr

def fantifyMapAreaList(mparealist):
    #the output is a sequence of maparea-structs, connected by a non-zero byte signaling after each maparea instance, that another
    #instance is following
    if len(mparealist) == 0:
        return struct.pack("b", 0)
    else:    #0x4d comes from original ecstatica data files
        return struct.pack("b", 0x4d) + struct.pack("b", 0x4d).join(map(lambda maparea: fantifyMapArea(maparea), mparealist))    

def exportFANT(f, fantfile, skip_transtables=False):
    '''
    @param f: file object, into which the data is written 
    '''
        
    f.write(b'FANT')    
    f.write(struct.pack(">h", 30))
    #if skip_transtables:
    if skip_transtables:
        f.write(struct.pack(">h", 1))
    else:
        f.write(struct.pack(">h", 0))
        
    f.write(b"\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0")
        
    lists = [ 
                ("Part", fantfile.partnames),
                ("Actor", fantfile.actornames),
                ("Action", fantfile.actionnames),
                ("Scene", fantfile.scenenames),
                ("Point", fantfile.pointnames),
                ("Triangle", fantfile.trianglenames),
                ("Code", fantfile.codenames),
                ("Repertoire", fantfile.repertoirenames),
                ("Sound", fantfile.soundnames),
                ("MapArea", fantfile.mapareanames)
            ]
    
    if not skip_transtables:
        for nametype, namedb in lists:
            #print nametype, namedb.names
            f.write(fantifyNameList(namedb.names))

    eventlists = [
                  ("Action", fantfile.actionevents),
                  ("Actor", fantfile.actorevents),
                  ("Scene", fantfile.sceneevents)
                  ]

    for eventgroup, eventlist in eventlists:
        f.write(fantifyEventList(eventlist))    
        #print "after events of type", eventgroup, hex(f.tell())

    f.write(fantifyCodeList(fantfile.codes))
    #print "after codes", hex(f.tell())
    #Repertoire-Events
    f.write(fantifyEventList(fantfile.repertoireevents))
    #print "after repert events", hex(f.tell())     
    f.write(fantifySoundList(fantfile.sounds))
    #print "after sounds", hex(f.tell())
    if fantfile.sectormap != None:
        f.write(struct.pack(">h", 1))#this value specifies, whether sector data follows (1=yes)
        f.write(fantifySectormap(fantfile.sectormap))
        #print "after sector map", hex(f.tell())
        #print hex(f.tell())     
        f.write(fantifySectorSectionList(fantfile.sectorsections))
        #print "after sector section", hex(f.tell())
        #print hex(f.tell())        
        f.write(fantifyCameraList(fantfile.cameras))
        #print hex(f.tell())    
        f.write(fantifyMapAreaList(fantfile.mapareas))
    else:
        f.write(struct.pack(">h", 0))#this value specifies, whether sector data follows (0=no)

def exportFANTStack(filename, fantfiles):
    fileobj = open(filename, "wb")
    for fantfile in fantfiles:
        exportFANT(fileobj, fantfile, fantfile.skip_transtables)
    
    fileobj.close()
    
import unittest

class TestSaveFANT(unittest.TestCase):
    def testsave(self):
        loader = FANTLoad.FANTFileLoader(open("test/ecstatic.fan", "rb"))

        exportFANT(open("/tmp/test_export.fan", "wb"), loader.fantfile)
