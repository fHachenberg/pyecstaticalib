# coding: utf-8

#Created on 12.02.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

import re
import struct
import functools
import xml.parsers.expat

from . import Sound
from . import Code
from . import Camera
from . import Event
from . import SectorSection
from .Event import createEventFromTextData, ev_NO_EVENT
from .Code import createCodeFromText
from .FantFile import FANTFile
from . import MapArea

from . import XmlSave
from . import FANTSave

class XmlLoadError(Exception):
    def __init__(self, str):
        Exception.__init__(self, str)

class XmlHandler(object):
    def __init__(self, context):
        self.context = context
    
    def handleEnterElement(self, tag, atts):
        raise StandardError("not implemented")
    
    def handleLeaveElement(self, tag):
        raise StandardError("not implemented")
    
    def handleText(self, text):
        raise StandardError("not implemented")
    
    def CDataStart(self):
        pass
    
    def CDataStop(self):
        pass
    
class GenericXmlSingularTagHandler(XmlHandler):
    '''
    Used to parse an empty-tag value like
    <foo attrib="haha" />
    '''
    def __init__(self, context, tag, attrs, resultobj):
        XmlHandler.__init__(self, context)
        self.tag = tag
        self.attrs = attrs
        self.propname = tag
        self.resultobj = resultobj                
    
    def handleEnterElement(self, tag, atts):
        raise StandardError("No subtags allowed within empty-tag value")        
    
    def handleLeaveElement(self, tag):
        assert tag == self.tag
        self._createValue()
        self.context.popHandler(self)
        
    def handleText(self, text):
        raise StandardError("No data allowed within empty-tag value")  
    
class GenericXmlValueHandler(XmlHandler):
    '''
    Used to parse a single value
    <bla> ewrfgaswfef </bla>
    Subtags are NOT allowed!
    
    Does NOT implement the evaluation of text data, which has to be implemented by derived classes!
    '''
    def __init__(self, context, tag, attrs, resultobj, only_cdata=False):
        XmlHandler.__init__(self, context)
        self.tag = tag
        self.propname = tag
        self.resultobj = resultobj
        self.text = ""
        self.only_cdata = only_cdata #if set, only text within CDATA-section is collected
        self.incdata = False
        
    def handleEnterElement(self, tag, atts):
        raise StandardError("No subtags allowed in simple value definition")        
    
    def handleLeaveElement(self, tag):
        assert tag == self.tag
        self._createValue()
        self.context.popHandler(self)
        
    def handleText(self, text):
        if self.only_cdata:
            if self.incdata:
                self.text += text
        else:
            self.text += text            
        
    def CDataStart(self):
        self.incdata = True
    
    def CDataStop(self):
        self.incdata = False
    
'''
The reason for these classes is: There are cases where we want to get just a simple
string from xml. In those cases, we could just write the read string into the python
object. But in other cases, we want to create a python list from a sequence a,b,c,d,e,...
or something like that. 
'''
    
class _addInteger(GenericXmlValueHandler):
    def __init__(self, context, tag, attrs, resultobj):
        GenericXmlValueHandler.__init__(self, context, tag, attrs, resultobj)
    
    def _createValue(self):
        try:
            int(self.text)
        except:
            print("**********************************", self.tag)
        self.resultobj.__setattr__(self.propname, int(self.text))
        
class _addFloat(GenericXmlValueHandler):
    def __init__(self, context, tag, attrs, resultobj):
        GenericXmlValueHandler.__init__(self, context, tag, attrs, resultobj)
    
    def _createValue(self):
        self.resultobj.__setattr__(self.propname, float(self.text))

class _addString(GenericXmlValueHandler):
    def __init__(self, context, tag, attrs, resultobj):
        GenericXmlValueHandler.__init__(self, context, tag, attrs, resultobj)
    
    def _createValue(self):
        self.resultobj.__setattr__(self.propname, self.text.strip())
        
class _addCDATA(GenericXmlValueHandler):
    def __init__(self, context, tag, attrs, resultobj):
        GenericXmlValueHandler.__init__(self, context, tag, attrs, resultobj, True)
    
    def _createValue(self):
        self.resultobj.__setattr__(self.propname, self.text)
        
class _addStringList(GenericXmlValueHandler):
    def __init__(self, context, tag, attrs, resultobj):
        GenericXmlValueHandler.__init__(self, context, tag, attrs, resultobj)
    
    def _createValue(self):
        self.resultobj.__setattr__(self.propname, self.text.split(","))
        
class _addDataFileRef(GenericXmlSingularTagHandler):
    def __init__(self, context, tag, attrs, resultobj):
        GenericXmlSingularTagHandler.__init__(self, context, tag, attrs, resultobj)
    
    def _createValue(self):
        f = open(self.attrs['Filename'], "rb")
        data = f.read()
        self.resultobj.__setattr__(self.propname, data)
        
class _addIntegerList(GenericXmlValueHandler):
    '''
    @param fixedsize: If given >0, an exception is thrown if the list size does not match!
    '''
    def __init__(self, context, tag, attrs, resultobj, fixedsize=None):
        self.fixedsize = fixedsize
        GenericXmlValueHandler.__init__(self, context, tag, attrs, resultobj)
    
    def _createValue(self):
        intlist = [ int(a) for a in self.text.split(',') if a.strip() != ""]
        if self.fixedsize != None:
            if len(intlist) != self.fixedsize:
                raise XmlLoadError("invalid integer list size: " + str(len(intlist)) + " < " + str(self.fixedsize)) 
        self.resultobj.__setattr__(self.propname, intlist)
    
class _addVector3(XmlHandler):    
    def __init__(self, context, tag, attrs, resultobj):
        XmlHandler.__init__(self, context)
        self.tag = tag
        self.propname = tag
        self.resultobj = resultobj
        self.text = ""
        
    def handleEnterElement(self, tag, atts):
        assert tag == "Vector3" or tag == self.tag
    
    def handleLeaveElement(self, tag):
        if tag == self.tag:
            self.context.popHandler(self)
            self.resultobj.__setattr__(self.propname, tuple( float(a) for a in self.text.split(','))) #TODO:read in Fixed-Point-Value
    
    def handleText(self, text):
        self.text += text
        
class GenericXmlDataHandler(XmlHandler):
    '''
    Used to parse a tag containing a finite number of special sub-tags, not a list or something like that
    <bla>
        <a> fsfesf </a>
        <b> sfsf </b>
    </bla>
    '''
    def __init__(self, context, tag, attrs, property_mapping, allow_top_value=False):        
        XmlHandler.__init__(self, context)
        
        self.tag = tag
        self.property_mapping = property_mapping
        
    def handleEnterElement(self, tag, atts):
        assert tag in self.property_mapping.keys()
        self.context.pushHandler(self.property_mapping[tag](self.context, tag, atts, self))
    
    def handleLeaveElement(self, tag):
        assert tag == self.tag
        
        self.context.popHandler(self)
                    
    def handleText(self, text):
        assert text.strip() == ""
    
class GenericXmlClassHandler(XmlHandler):
    '''
    Used to parse the XML representation of a specific object, like an Event or a Code
    Is used together with GenericXmlClassListHandler
    
    @param classtag: The tag for which this handler was entered. This is normally one specific tag but we provide means to communicate the explizit tag name
    @param attrs: The attributes of the opening tag which caused entering this handler 
    '''
    def __init__(self, context, classtag, attrs, property_mapping, object_list):
        XmlHandler.__init__(self, context)
        
        self.property_mapping = property_mapping
        self.classtag = classtag                
        
        self.object_list = object_list
    
    def _createInstance(self):
        '''
        Has to be overloaded by all derived types
        '''
        raise StandardError("No creation routine implemented")
            
    def handleEnterElement(self, tag, atts):
        if not tag in self.property_mapping.keys():
            print("unexptected tag", tag, "in handler", type(self))
        assert tag in self.property_mapping.keys()
        
        self.context.pushHandler(self.property_mapping[tag](self.context, tag, atts, self))
    
    def handleLeaveElement(self, tag):
        assert tag == self.classtag
                
        self.object_list.append(self._createInstance())
        self.context.popHandler(self)                
    
    def handleText(self, text):        
        assert text.strip() == ''
        
class GenericXmlClassListHandler(XmlHandler):
    '''
    Used to parse lists of objects 
    <blubs>
        <blub> ... </blub>
        <blub> ... </blub>
        <blub> ... </blub>
        <blub> ... </blub>
        <blub> ... </blub>
        <blub> ... </blub>
    </blubs>
    '''    
    def __init__(self, context, listtag, typeattribs, ListElementClass):
        XmlHandler.__init__(self, context)
        
        self.listtag = listtag        
        self.typeattribs = typeattribs
        self.ListElementClass = ListElementClass
        self.classtag = self.ListElementClass.tagname
                            
        self.object_list = []
        
    def handleEnterElement(self, tag, atts):        
        if tag != self.listtag and tag != self.classtag:
            print("Unerwartetes tag", tag, "for handler", type(self))
        assert (tag == self.listtag or tag == self.classtag)
        
        if tag == self.classtag:
            handler = self.ListElementClass(self.context, self.classtag, atts, self.object_list)            
            self.context.pushHandler(handler)
    
    def handleLeaveElement(self, tag):
        assert tag == self.listtag or tag == self.classtag
        
        if tag == self.listtag:
            self._setList()
            self.context.popHandler(self)
    
    def handleText(self, text):
        if text.strip() == '':
            return
        raise StandardError("No text expected in list tag. Found:" + text)
    
class StackHandler(XmlHandler):
    def __init__(self, context):
        XmlHandler.__init__(self, context)
        
    def handleEnterElement(self, tag, attrs):
        assert tag == "FANT" or tag == "FANT_stack"
        if tag == "FANT":
            self.context.pushHandler(TopHandler(self.context))
            
    def handleLeaveElement(self, tag):
        pass
            
    def handleText(self, text):
        if text.strip() == "":
            return
        raise StandardError("Unexpected text \"" + text + "\"" )
    
class TopHandler(XmlHandler):
    def __init__(self, context):
        XmlHandler.__init__(self, context)        
        
        self.nametypes = ["Part", "Actor", "Action", "Scene", "Point", "Triangle", "Repertoire", "Code", "MapArea", "Sound"]
        self.eventlisttypes = ["Action", "Actor", "Scene", "Repertoire"]
        self.eventtypes =   { 
                            'Actor'     : map(lambda evtidx: Event.event_names[evtidx], Event.ActorEvents),
                            'Action'    : map(lambda evtidx: Event.event_names[evtidx], Event.ActionEvents),
                            'Scene'     : map(lambda evtidx: Event.event_names[evtidx], Event.SceneEvents),
                            'Repertoire': map(lambda evtidx: Event.event_names[evtidx], Event.RepertoireEvents)
                            }
                        
        self.context.newFANTFile()
    
    def handleEnterElement(self, tag, attrs):#         
        #print tag               
        if tag == 'Header':
            self.context.pushHandler(HeaderHandler(self.context))
            return
        elif tag == "Names":
            assert 'Type' in attrs.keys()
            #print attrs['Type']
            assert attrs['Type'] in self.nametypes
            self.context.pushHandler(NameHandler(attrs['Type'], self.context))
            return
        elif tag == "Events":
            assert 'Type' in attrs.keys()
            assert attrs['Type'] in self.eventlisttypes
            self.context.pushHandler(EventListHandler(self.context, attrs['Type'], self.eventtypes[attrs['Type']]))
            return
        elif tag == "Codes":
            self.context.pushHandler(CodeListHandler(self.context))
            return
        elif tag == "Sounds":
            self.context.pushHandler(SoundListHandler(self.context))
            return
        elif tag == "Sectormap":
            self.context.pushHandler(SectormapHandler(self.context))
            return
        elif tag == "SectorSections":
            self.context.pushHandler(SectorSectionListHandler(self.context))
            return
        elif tag == "Cameras":
            self.context.pushHandler(CameraListHandler(self.context))
            return
        elif tag == "MapAreas":
            self.context.pushHandler(MapAreaListHandler(self.context))
            return

        assert False
    
    def handleLeaveElement(self, tag):         
        assert tag == "FANT"
        self.context.popHandler(self)
    
    def handleText(self, text):
        if text.strip() == "":
            return
        raise StandardError("Unexpected text \"" + text + "\"" )
    
# ---------------------------------------------------------------------------------------------
    
class CodeHandler(GenericXmlClassHandler):
    tagname = 'Code'
    
    def _createInstance(self):
        #print self.Sourcecode
        #we have to pass a list of lines to the Code 
        return Code.Code(self.Index, self.Sourcecode.split("\n"), self.Tokenlist)
    
    def __init__(self, context, tag, attrs, codelist):
        '''        
        '''
        assert tag == CodeHandler.tagname #just make sure we were called for the correct tag
        propmap = {"Index":_addInteger, "Sourcecode":_addCDATA, "Tokenlist": _addIntegerList}
        GenericXmlClassHandler.__init__(self, context, "Code", attrs, propmap, codelist)
    
class CodeListHandler(GenericXmlClassListHandler):
    def _setList(self):        
        self.context.fantfile.codes = self.object_list        
            
    def __init__(self, context):        
        GenericXmlClassListHandler.__init__(self, context, 'Codes', None, CodeHandler)
        
# ---------------------------------------------------------------------------------------------        
        
class SoundHandler(GenericXmlClassHandler):
    tagname = 'Sound'
    
    def _createInstance(self):
        return Sound.Sound(self.Index, self.Length, self.Unknown, self.Unknown1, self.Data, self.Flags)
    
    def __init__(self, context, tag, attrs, codelist):
        '''        
        '''
        assert tag == SoundHandler.tagname #just make sure we were called for the correct tag
        propmap = {"Index":_addInteger, "Flags":_addInteger, "Length":_addInteger, "Unknown": _addInteger, "Unknown1": _addInteger, "Data": _addDataFileRef}
        GenericXmlClassHandler.__init__(self, context, SoundHandler.tagname, attrs, propmap, codelist)
    
class SoundListHandler(GenericXmlClassListHandler):
    def _setList(self):
        self.context.fantfile.sounds = self.object_list
            
    def __init__(self, context):        
        GenericXmlClassListHandler.__init__(self, context, 'Sounds', None, SoundHandler)
        
# ---------------------------------------------------------------------------------------------        
        
class SectorSectionHandler(GenericXmlClassHandler):
    tagname = 'SectorSection'
    
    def _createInstance(self):
        return SectorSection.SectorSection(self.Priority, self.Section, self.Unknown1, self.CameraIndex, self.Y_Unknown, self.YMax, self.Index, self.Flags)
    
    def __init__(self, context, tag, attrs, seclist):
        '''        
        '''
        assert tag == SectorSectionHandler.tagname #just make sure we were called for the correct tag
        propmap = {"Priority": _addInteger, 
                   "Section": _addInteger, 
                   "Unknown1": _addInteger, 
                   "CameraIndex": _addInteger,
                   "Y_Unknown": _addInteger, 
                   "YMax": _addInteger, 
                   "Index": _addInteger, 
                   "Flags": _addInteger}
        GenericXmlClassHandler.__init__(self, context, SectorSectionHandler.tagname, attrs, propmap, seclist)
    
class SectorSectionListHandler(GenericXmlClassListHandler):
    def _setList(self):
        print("number of sectorsections in XML data:", len(self.object_list))
        self.context.fantfile.sectorsections = self.object_list
            
    def __init__(self, context):        
        GenericXmlClassListHandler.__init__(self, context, 'SectorSections', None, SectorSectionHandler)
      
# ---------------------------------------------------------------------------------------------

class CameraHandler(GenericXmlClassHandler):
    tagname = 'Camera'
    
    def _createInstance(self):
        return Camera.Camera(self.Position, self.Angles, self.F)
    
    def __init__(self, context, tag, attrs, camlist):
        '''        
        '''
        assert tag == CameraHandler.tagname #just make sure we were called for the correct tag
        propmap = {"Position":_addVector3, "Angles":_addVector3, "F":_addInteger} #TODO:read in Fixed-Point-Value 
        GenericXmlClassHandler.__init__(self, context, CameraHandler.tagname, attrs, propmap, camlist)
        
        self.F = 1.0
    
class CameraListHandler(GenericXmlClassListHandler):
    def _setList(self):
        self.context.fantfile.cameras = self.object_list
            
    def __init__(self, context):        
        GenericXmlClassListHandler.__init__(self, context, 'Cameras', None, CameraHandler)
      
# ---------------------------------------------------------------------------------------------

class MapAreaHandler(GenericXmlClassHandler):
    tagname = 'MapArea'
    
    def _createInstance(self):
        return MapArea.MapArea(self.Index, self.Values)
    
    def __init__(self, context, tag, attrs, maparealist):
        '''        
        '''
        assert tag == MapAreaHandler.tagname #just make sure we were called for the correct tag
        propmap = {"Index":_addInteger, "Values":_addIntegerList}
        GenericXmlClassHandler.__init__(self, context, MapAreaHandler.tagname, attrs, propmap, maparealist)
        
        self.F = 1.0
    
class MapAreaListHandler(GenericXmlClassListHandler):
    def _setList(self):
        self.context.fantfile.mapareas = self.object_list
            
    def __init__(self, context):     
        GenericXmlClassListHandler.__init__(self, context, 'MapAreas', None, MapAreaHandler)
      
# ---------------------------------------------------------------------------------------------

class SectormapHandler(_addIntegerList):
    def __init__(self, context):
        _addIntegerList.__init__(self, context, "Sectormap", {}, context.fantfile, 16384)
        self.propname = "sectormap"
        
# ---------------------------------------------------------------------------------------------

class HeaderHandler(GenericXmlDataHandler):
    def __init__(self, context):
        propmap = {"Version":_addInteger}
        
        GenericXmlDataHandler.__init__(self, context, 'Header', {}, propmap)
        
# ---------------------------------------------------------------------------------------------
    
class EventHandler(GenericXmlClassHandler): 
    tagname = 'Event'
          
    def _createInstance(self):
        if self.event_type == Event.ev_NEXT_SCENE:
            #in this case we create a special event class
            return Event.NextSceneEvent(self.Index, self.Value1, self.Value2, self.Value3, self.ExtraData)
        else:
            return Event.Event(self.Index, self.event_type, self.Value1, self.Value2, self.Value3)
            
    def __init__(self, context, tag, attrs, objlist):
        assert tag == EventHandler.tagname #just make sure we were called for the correct tag
        assert "Type" in attrs.keys()
        
        self.event_type = Event.EventTypeName[attrs['Type']].typeid
        
        mapping =   {
                        "Index":_addInteger,
                        "Value1":_addInteger,
                        "Value2":_addInteger,
                        "Value3":_addInteger,
                        "ExtraData":_addCDATA
                    }
        GenericXmlClassHandler.__init__(self, context, EventHandler.tagname, attrs, mapping, objlist)
        
class EventListHandler(GenericXmlClassListHandler):
    def _setList(self):
        '''
        This routine grabs the generic "object list" and puts it - depending on the eventlist type -
        into the right spot in the context!
        '''
        if self.eventlisttype == "Scene":
            self.context.fantfile.sceneevents = self.object_list
        elif self.eventlisttype == "Actor":
            self.context.fantfile.actorevents = self.object_list
        elif self.eventlisttype == "Action":
            self.context.fantfile.actionevents = self.object_list
        elif self.eventlisttype == "Repertoire":
            self.context.fantfile.repertoireevents = self.object_list
        else:
            raise StandardError("Unknown Event list type")
            
    def __init__(self, context, eventlisttype, eventtypes):        
        GenericXmlClassListHandler.__init__(self, context, 'Events', eventtypes, EventHandler)
        self.eventlisttype = eventlisttype
        
# ---------------------------------------------------------------------------------------------
    
class NameHandler(XmlHandler):
    '''
    Handles a list of Names AS WELL AS THE SURROUNDING TAG
    '''
    def setList(self):
        if self.nametype == "Actor":
            self.context.fantfile.actornameidxs = self.context.fantfile.actornames.addNames(self.namelist)
        elif self.nametype == "Action":
            #print self.namelist
            self.context.fantfile.actionameidxs = self.context.fantfile.actionnames.addNames(self.namelist)
        elif self.nametype == "Part":
            self.context.fantfile.partnameidxs = self.context.fantfile.partnames.addNames(self.namelist)
        elif self.nametype == "Scene":
            self.context.fantfile.scenenameidxs = self.context.fantfile.scenenames.addNames(self.namelist)
        elif self.nametype == "Repertoire":
            self.context.fantfile.repertnameidxs = self.context.fantfile.repertoirenames.addNames(self.namelist)
        elif self.nametype == "MapArea":
            self.context.fantfile.mapareanameidxs = self.context.fantfile.mapareanames.addNames(self.namelist)
        elif self.nametype == "Point":
            self.context.fantfile.pointnameidxs = self.context.fantfile.pointnames.addNames(self.namelist)
        elif self.nametype == "Triangle":
            self.context.fantfile.trinameidxs = self.context.fantfile.trianglenames.addNames(self.namelist)
        elif self.nametype == "Code":
            self.context.fantfile.codenameidxs = self.context.fantfile.codenames.addNames(self.namelist)
        elif self.nametype == "Sound":
            self.context.fantfile.soundnameidxs = self.context.fantfile.soundnames.addNames(self.namelist)
        else:
            raise StandardError("Unknown name type " + self.nametype)
    
    def __init__(self, nametype, context):
        XmlHandler.__init__(self, context)
        
        self.nametype = nametype
        self.inlist = False #whether we are in the names list or not
        self.inname = False #whether we are in a name tag or not
        
        self.namelist = []
             
    def handleEnterElement(self, tag, attrs):
        #print attrs
        assert tag == "Names" or tag == "Name"
        assert attrs["Type"] == self.nametype
        
        if tag == "Names":
            self.inlist = True
        elif tag == "Name":
            self.inname = True
    
    def handleLeaveElement(self, tag):
        assert tag == "Names" or tag == "Name"
        
        if tag == "Names":
            self.setList()
            self.context.popHandler(self)
            self.context = None
        elif tag == "Name":
            self.inname = False
    
    def handleText(self, text):
        if text.strip() == "":
            if self.inname == False:
                return
        assert self.inname == True
        #see XmlExport.encodeName
        #XML forbids most characters in range 0-32
        #unfortunately Python does not escape them nor unescape them, so I do this manually here
        #(actually the ampersand in the escape sequence is escaped by python)    
        #print text        
        self.namelist.append(re.sub('&#([0-9]+);', lambda x: struct.pack('b', int(x.group(1))).decode("utf-8"), text.strip()))
        #print re.sub('&#([0-9]+);', lambda x: struct.pack('b', int(x)), text)
        
# ---------------------------------------------------------------------------------------------
        
class LoadXMLFile(object):
    '''
    This class creates a FANT file from a XML document
    '''    
    
    def pushHandler(self, handler):
        self.handlerstack.append(handler)
        self.parser.StartElementHandler = handler.handleEnterElement
        self.parser.EndElementHandler = handler.handleLeaveElement
        self.parser.CharacterDataHandler = handler.handleText
        self.parser.StartCdataSectionHandler = handler.CDataStart
        self.parser.EndCdataSectionHandler = handler.CDataStop
    
    def popHandler(self, handler):
        assert len(self.handlerstack) > 1
        assert handler == self.handlerstack[-1]
        self.handlerstack = self.handlerstack[:-1]        
        self.parser.StartElementHandler = self.handlerstack[-1].handleEnterElement
        self.parser.EndElementHandler = self.handlerstack[-1].handleLeaveElement
        self.parser.CharacterDataHandler = self.handlerstack[-1].handleText
        self.parser.StartCdataSectionHandler = self.handlerstack[-1].CDataStart
        self.parser.EndCdataSectionHandler = self.handlerstack[-1].CDataStop
        
    def newFANTFile(self):
        '''
        moves on to a new FANT file. Is called by the FANT-tag handler
        '''
        if self.fantfile != None:
            #now we check if there were any names given in the file. If not, we set skip_transtables to True
            #how do we decide that? We get all name lists and check if they all are empty
            if len(list(filter(lambda x: len(x)!=0, self.fantfile.getAllNameLists().values()))) == 0:
                self.fantfile._initIndexArrays()
                self.fantfile.skip_transtables = True
            self.fantfiles.append(self.fantfile)            
                            
        self.fantfile = FANTFile()

    def __init__(self, input_filename):
        '''
        Constructor
        '''
        self.input_filename = input_filename
        
        #the XML interface can handle a stack of FANT files, which are sequentially loaded
        self.fantfile = None #points always on the current FANT file
        self.fantfiles = [] #in the end this list contains all loaded FANT files
        
        self.parser = xml.parsers.expat.ParserCreate()
        self.parser.buffer_text = True
        
        self.handlerstack = []
        
        stackhandler = StackHandler(self)
        self.pushHandler(stackhandler)        
        
    def run(self):
        infile = open(self.input_filename, "rb")
        self.parser.Parse(infile.read())
        infile.close()    
        
        #the following procedure has to be done for the last FANT file as well!
        if self.fantfile != None:              
            self.fantfiles.append(self.fantfile)      
            #now we check if there were any names given in the file. If not, we set skip_transtables to True
            #how do we decide that? We get all name lists and check if they all are empty
            if len(list(filter(lambda x: len(x)!=0, self.fantfile.getAllNameLists().values()))) == 0:
                self.fantfile._initIndexArrays()  
                self.fantfile.skip_transtables = True      
        
def loadStack(filename):
    loader = LoadXMLFile(filename)
    loader.run()
    return loader.fantfiles
    
import unittest

class TestLoadXML(unittest.TestCase):
    def test_load_save_xml(self):
        loader = LoadXMLFile('/tmp/fant.xml')
        loader.run()
        f = open("/tmp/fant_rewritten.xml", "wb")
        f.write(XmlSave.exportXml(loader.fantfile).encode("utf-8"))
        f.close()
    
    def test_load_xml_save_fant(self):
        loader = LoadXMLFile('/tmp/fant.xml')
        loader.run()    
        print(loader.fantfile)
        FANTSave.exportFANT(open("/tmp/rewritten.fant", "wb"), loader.fantfile, False)
