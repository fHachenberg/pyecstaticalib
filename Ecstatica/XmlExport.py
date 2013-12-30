# coding: utf-8

#Created on 08.02.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

from . import Event
import itertools

def encodeIndex(idx, idx_type, xmldoc):
    index_tag = xmldoc.createElement('Index')
    index_tag.setAttribute("Type", idx_type)
    index_value = xmldoc.createTextNode(str(idx))
    index_tag.appendChild(index_value)
    
    return index_tag

def encodeEvent(event, xmldoc):
    assert event.event_type in Event.avaible_eventtypes
    
    event_tag = xmldoc.createElement('Event')
    event_tag.setAttribute('Type', Event.event_names[event.event_type])
    
    index_tag = xmldoc.createElement('Index')
    if event.event_type in Event.have_actoridx:
        index_tag.setAttribute('type', "Actor")
    elif event.event_type in Event.have_partidx:
        index_tag.setAttribute('type', "Part")
    elif event.event_type in Event.have_triangleidx:
        index_tag.setAttribute('type', "Triangle")
    elif event.event_type in Event.have_sceneidx:
        index_tag.setAttribute('type', "Scene")
    #else:
        #Wenn nicht bekannt ist, welche Art von Index es
        #ist, ist es dennoch immer noch ein Index, nur eben
        #ohne Attribut
    index_value = xmldoc.createTextNode(str(event.index))
    index_tag.appendChild(index_value)
    event_tag.appendChild(index_tag)
        
    event_tag.appendChild(encodeValue("Value1", event.value1, xmldoc))    
    event_tag.appendChild(encodeValue("Value2", event.value2, xmldoc))    
    event_tag.appendChild(encodeValue("Value3", event.value3, xmldoc))
    
    #if this is a ev_NEXT_SCENE-Event, we also have to attach the special data block
    if event.event_type == Event.ev_NEXT_SCENE:
        specialdata_tag = encodeData("ExtraData", event.uk_data, xmldoc)
        event_tag.appendChild(specialdata_tag)
    
    return event_tag

import tempfile

def createDataFile(tagname, data, xmldoc):
    '''
    This puts the data string into a separate file and creates
    a reference to it, which is returned
    '''
    datafile = tempfile.NamedTemporaryFile(delete=False)
    datafile.write(data)
    datafile.close()
    
    ref_tag = xmldoc.createElement(tagname)
    ref_tag.setAttribute("Filename", datafile.name)
    return ref_tag

def encodeCode(code, xmldoc):
    code_tag = xmldoc.createElement('Code')

    code_tag.appendChild(encodeIndex(code.index, "Code", xmldoc))
    code_tag.appendChild(encodeData('Sourcecode', "\n".join(code.slang), xmldoc))
    if "RepeatScene \"tria45_r\"" in code.slang:
        print(code.slang)
    code_tag.appendChild(encodeValue('Tokenlist', ",".join(map(lambda a: str(a), code.tokens)), xmldoc))
    
    return code_tag

def encodeVector3(vector, xmldoc):
    assert len(vector) == 3
    
    vector_tag = xmldoc.createElement('Vector3')
    vector_value = xmldoc.createTextNode(",".join(map(lambda x: str(x), vector)))
    vector_tag.appendChild(vector_value)
    
    return vector_tag    

def encodeCamera(camera, xmldoc):
    camera_tag = xmldoc.createElement('Camera')
    
    position_tag = xmldoc.createElement('Position')
    position_value = encodeVector3(camera.position, xmldoc)
    position_tag.appendChild(position_value)
    camera_tag.appendChild(position_tag)
    
    angles_tag = xmldoc.createElement('Angles')
    angles_value = encodeVector3(camera.angles, xmldoc)
    angles_tag.appendChild(angles_value)
    camera_tag.appendChild(angles_tag)
        
    f_value = encodeValue("F", camera.f, xmldoc)
    camera_tag.appendChild(f_value)
    
    return camera_tag

def encodeData(dataname, text, xmldoc):
    '''
    Uses XML CDATA-Section to directly encode data
    '''
    value_tag = xmldoc.createElement(dataname)
    cdata_node = xmldoc.createCDATASection(text)
    value_tag.appendChild(cdata_node)
    return value_tag

def encodeValue(valuename, value, xmldoc):
    value_tag = xmldoc.createElement(valuename)
    value_value = xmldoc.createTextNode(str(value))
    value_tag.appendChild(value_value)
    return value_tag

def encodeSectorSection(section, xmldoc):
    sector_tag = xmldoc.createElement('SectorSection')
    
    sector_tag.appendChild(encodeValue('Priority', section.prio, xmldoc))
    sector_tag.appendChild(encodeValue('Section', section.section, xmldoc))
    sector_tag.appendChild(encodeValue('Unknown1', section.unknown1, xmldoc))
    sector_tag.appendChild(encodeValue('CameraIndex', section.cam_idx, xmldoc))
    sector_tag.appendChild(encodeValue('Y_Unknown', section.y_uk, xmldoc))
    sector_tag.appendChild(encodeValue('YMax', section.ymax, xmldoc))
    sector_tag.appendChild(encodeIndex(section.codeidx_plus_one, "Code", xmldoc))
    sector_tag.appendChild(encodeValue('Flags', section.flags, xmldoc))
    
    return sector_tag

def encodeMapArea(maparea, xmldoc):
    area_tag = xmldoc.createElement('MapArea')
    
    area_tag.appendChild(encodeIndex(maparea.index, "MapArea", xmldoc))
    #values_tag = xmldoc.createElement('Values')
    values_tag = encodeValue("Values", ",".join(map(lambda a: str(a), maparea.values)), xmldoc)
    #for value in maparea.values:
    #    values_tag.appendChild(encodeValue("Value", value, xmldoc))
    area_tag.appendChild(values_tag)
    
    return area_tag

def encodeSound(sound, xmldoc):
    sound_tag = xmldoc.createElement('Sound')
    
    index_tag = encodeValue("Index", sound.index, xmldoc)    
    sound_tag.appendChild(index_tag)
    
    flags_tag = encodeValue("Flags", sound.flags, xmldoc)
    sound_tag.appendChild(flags_tag)
    
    length_tag = encodeValue("Length", sound.length, xmldoc)
    sound_tag.appendChild(length_tag)
    
    unknown_tag = encodeValue("Unknown", sound.unknown, xmldoc)
    sound_tag.appendChild(unknown_tag)
    
    unknown1_tag = encodeValue("Unknown1", sound.unknown1, xmldoc)    
    sound_tag.appendChild(unknown1_tag)
    
    #data_tag = encodeData("Data", sound.data, xmldoc)
    data_tag = createDataFile("Data", sound.data, xmldoc)    
    sound_tag.appendChild(data_tag)
    
    return sound_tag

def encodeName(nametype, name, xmldoc):
    #What am I doing here?
    #XML does strangely forbid to use most of the characters in the range 0-32
    #and Python does not escape those, so I do this myself here... :(
    def replbadchars(a):
        if ord(a) <= 0x20:
            return '&#' + str(ord(a)) + ';'
        else:
            return a
    name_tag = xmldoc.createElement('Name')
    name_tag.setAttribute('Type', nametype)
    name_value = xmldoc.createTextNode("".join(map(replbadchars,name)))
    name_tag.appendChild(name_value)
    
    return name_tag

def encodeSectormap(sectormap, xmldoc):
    name_tag = xmldoc.createElement('Sectormap')
    if sectormap != None:
        name_value = xmldoc.createTextNode(",".join(map(lambda a: str(a), sectormap)))
        name_tag.appendChild(name_value)
    
    return name_tag

class FantXmlDocument(object):
    def __init__(self, name, doc, element):
        '''
        doc is the DOM document object to fill
        element is the DOM element object to attach the XML content of the FANT file to
        '''
        self.name = name
        
        self.stateidx = 0 #Init                

        self.xmldoc = doc
        
        self.stateidx = 0
        #The order of data in the FANT files is represented in this list,
        #as well as in the lists of substates for events and names!
        self.statelist =    [  
                                "init", 
                                "header",
                                "names",
                                "events",
                                "codes",
                                "repertoire_events",                                
                                "sounds",
                                "sectordata",
                                "cameras",
                                "mapareas",
                                "loaded"
                            ]
        
        self.sectordata_stateidx = None
        self.sectordata_statelist = [
                                    "sectormap",
                                    "sections"
                                    ]
        
        self.names_stateidx = None
        self.names_statelist = [     
                                "Part",
                                "Actor",
                                "Action",
                                "Scene",
                                "Point",
                                "Triangle",
                                "Code",
                                "Repertoire",
                                "Sound",
                                "MapArea"
                            ]
        
        self.events_stateidx = None
        self.events_statelist =  [   
                                 "Action",
                                 "Actor",
                                 "Scene",
                                 ]            
        
        self.current_element = None                    
        self.top_element = element
        
        self.nextState() #Header
        
        header_tag = self.xmldoc.createElement("Header")
        self.top_element.appendChild(header_tag)
        
        version_tag = self.xmldoc.createElement("Version")
        version_value = self.xmldoc.createTextNode("30")
        version_tag.appendChild(version_value)
        header_tag.appendChild(version_tag)            
        
        self.nextState() #Names        
        
    def nextState(self):
        '''
        This is the central routine to switch states.
        Why don't we just use self.stateidx += 1 for changing the state?
        There are currently 2 states having sub states: names and events. Upon entering the state, the
        sub state management has to be initialized and upon leaving them, substate management has to be reset
        Also we have tried to minimize and centralize references to the actual order of states, so it is easier
        and less error-prone to change this order. This is achieved by putting all implicit information about
        state order and state entering/leaving-characteristics into this routine so no other routine has to deal
        with those details!
        '''
        
        #from the last valid state, it is not allowed to call this routine!
        assert self.stateidx < len(self.statelist)-1
        if self.stateidx == len(self.statelist)-2:
            self.stateidx += 1
            return            
            
        if self.statelist[self.stateidx] == "names":
            #to change to the next name section, we simply increase the names_stateidx by one
            #until we reach the end of the list
            if self.names_stateidx < len(self.names_statelist)-1:
                self.names_stateidx += 1
                return
            else:
                self.names_stateidx = None
                self.stateidx += 1                            
        elif self.statelist[self.stateidx] == "events":
            #to change to the next event section, we simply increase the events_stateidx by one
            #until we reach the end of the list
            if self.events_stateidx < len(self.events_statelist)-1:
                self.events_stateidx += 1
                return
            else:
                self.events_stateidx = None
                self.stateidx += 1
        elif self.statelist[self.stateidx] == "sectordata":
            if self.sectordata_stateidx < len(self.sectordata_statelist)-1:
                self.sectordata_stateidx += 1
                return
            else:
                self.sectordata_stateidx = None
                self.stateidx += 1
        else: #apart from the above exceptions, a statechange can be simply introduced by increasing the state idx            
            self.stateidx += 1        
            
        #we have now already increased the state idx and for the cases where we have not (events, names) we have left the function,
        #therefore we are now checking for the _NEW_ state!
        #if the _NEW_ state is "names" or "events" we have to initialize the respective state's sub-idx
            
        if self.statelist[self.stateidx] == "events":
            self.events_stateidx = 0
        elif self.statelist[self.stateidx] == "names":
            self.names_stateidx = 0
        elif self.statelist[self.stateidx] == "sectordata":
            self.sectordata_stateidx = 0
        
    #---------------------------------------
        
    def startEventSection(self, event_type):
        '''
        Starts one of the event sections. There are a couple of these, see events_statelist
        '''
        #We have to make an exception for repertoire events, because they appear after
        #the codes in the FANT file, separated from the other event lists (actions, actors, sceneactions)
        assert self.statelist[self.stateidx] == "events" or self.statelist[self.stateidx] == "repertoire_events"      
        if self.events_stateidx != None:  
            assert self.events_statelist[self.events_stateidx] == event_type
        else:
            self.statelist[self.stateidx] == "repertoire_events"            
        
        events_tag = self.xmldoc.createElement("Events")
        events_tag.setAttribute("Type", event_type)
        self.current_element = events_tag
        self.top_element.appendChild(events_tag)
    
    def addEvent(self, event_type, event):
        '''
        Adds an event to the current event section
        '''                
        assert self.statelist[self.stateidx] == "events" or self.statelist[self.stateidx] == "repertoire_events"
        #assert event_xml.tagName == "Event"
        event_xml = encodeEvent(event, self.xmldoc)        
        self.current_element.appendChild(event_xml)
    
    def endEventSection(self, event_type):
        '''
        Ends the current event section and moves forward to the next (sub)state
        '''
        assert self.statelist[self.stateidx] == "events" or self.statelist[self.stateidx] == "repertoire_events"
        if self.events_stateidx != None:
            assert self.events_statelist[self.events_stateidx] == event_type        
        self.nextState()
            
    #---------------------------------------
        
    def setSectormap(self, sectormap):
        assert self.statelist[self.stateidx] == "sectordata"
        assert self.sectordata_statelist[self.sectordata_stateidx] == "sectormap"
            
        #we base this on the following paradigma:
        #When the Sectormap-Tag is existing in the XML structure, is has to contain a list of integers of size 16384
        #So if there's no Sectormap, the Sectormap-Tag has to be ommitted!                    
        if sectormap != None:
            sectormap_xml = encodeSectormap(sectormap, self.xmldoc)
            assert sectormap_xml.tagName == "Sectormap"
            self.top_element.appendChild(sectormap_xml)
        
        self.nextState()
        
    def skipSectormap(self):
        '''
        Omit the heightmap
        '''
        assert self.statelist[self.stateidx] == "sectordata"
        assert self.sectordata_statelist[self.sectordata_stateidx] == "heightmap"
        
        self.nextState()
    
    #---------------------------------------
    
    def startSectorSectionList(self):
        assert self.statelist[self.stateidx] == "sectordata"
        assert self.sectordata_statelist[self.sectordata_stateidx] == "sections"
        
        sectors_tag = self.xmldoc.createElement("SectorSections")
        self.current_element = sectors_tag
        self.top_element.appendChild(sectors_tag)
    
    def addSectorSection(self, section):
        assert self.statelist[self.stateidx] == "sectordata"
        assert self.sectordata_statelist[self.sectordata_stateidx] == "sections"
        
        section_xml = encodeSectorSection(section, self.xmldoc)        
        assert section_xml.tagName == "SectorSection"        
        self.current_element.appendChild(section_xml)
    
    def endSectorSectionList(self):
        assert self.statelist[self.stateidx] == "sectordata"
        assert self.sectordata_statelist[self.sectordata_stateidx] == "sections"
        
        self.nextState()
        
    #---------------------------------------
    
    def startCamerasList(self):
        assert self.statelist[self.stateidx] == "cameras"
        
        cameras_tag = self.xmldoc.createElement("Cameras")        
        self.current_element = cameras_tag
        self.top_element.appendChild(cameras_tag)
    
    def addCamera(self, camera):
        camera_xml = encodeCamera(camera, self.xmldoc)
        assert self.statelist[self.stateidx] == "cameras"
        self.current_element.appendChild(camera_xml)
    
    def endCamerasList(self):
        assert self.statelist[self.stateidx] == "cameras"
        self.nextState()
    
    #---------------------------------------
    
    def startCodeSection(self):
        assert self.statelist[self.stateidx] == "codes"
        
        codes_tag = self.xmldoc.createElement("Codes")        
        self.current_element = codes_tag
        self.top_element.appendChild(codes_tag)
    
    def addCode(self, code):
        code_xml = encodeCode(code, self.xmldoc)
        assert self.statelist[self.stateidx] == "codes"
        self.current_element.appendChild(code_xml)
    
    def endCodeSection(self):
        assert self.statelist[self.stateidx] == "codes"
        self.nextState()
    
    #---------------------------------------
    
    def startSoundSection(self):
        assert self.statelist[self.stateidx] == "sounds"
        
        sounds_tag = self.xmldoc.createElement("Sounds")        
        self.current_element = sounds_tag
        self.top_element.appendChild(sounds_tag)
    
    def addSound(self, sound):
        sound_xml = encodeSound(sound, self.xmldoc)
        assert self.statelist[self.stateidx] == "sounds"
        self.current_element.appendChild(sound_xml)
    
    def endSoundSection(self):
        assert self.statelist[self.stateidx] == "sounds"
        self.nextState()
    
    #---------------------------------------
    
    def startMapAreaSection(self):
        assert self.statelist[self.stateidx] == "mapareas"
        
        mapareas_tag = self.xmldoc.createElement("MapAreas")        
        self.current_element = mapareas_tag
        self.top_element.appendChild(mapareas_tag)
    
    def addMapArea(self, maparea):
        maparea_xml = encodeMapArea(maparea, self.xmldoc)
        assert self.statelist[self.stateidx] == "mapareas"
        self.current_element.appendChild(maparea_xml)
    
    def endMapAreaSection(self):
        assert self.statelist[self.stateidx] == "mapareas"
        self.nextState()
    
    #---------------------------------------
    
    def startNameSection(self, nametype):
        assert self.statelist[self.stateidx] == "names"
        
        names_tag = self.xmldoc.createElement("Names")
        names_tag.setAttribute("Type", nametype)
        self.current_element = names_tag
        self.top_element.appendChild(names_tag)
    
    def addName(self, nametype, name):
        name_xml = encodeName(nametype, name, self.xmldoc)
        assert self.statelist[self.stateidx] == "names"
        self.current_element.appendChild(name_xml)
    
    def endNameSection(self, nametype):
        assert self.statelist[self.stateidx] == "names"
        self.nextState()
    
    
    
