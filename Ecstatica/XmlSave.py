# coding: utf-8

#Created on 11.02.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

from . import Event
from . import XmlExport
from .XmlExport import encodeName, encodeEvent, encodeCode

from xml.dom.minidom import getDOMImplementation

import struct
import itertools
from .Game import NamesDB
from . import FANTLoad

def exportStack(stack, outputfilename):
    
    #creating a DOM tree representing ALL FANT files generally requires too much memory
    #so what we do is the following. We manually create the opening <FANT_stack> and closing </FANT_stack> tags
    #and then fill one FANT-element, write it into the file and remove it from the DOM again
    
    impl = getDOMImplementation()
    xmldoc = impl.createDocument(None, "FANT_stack", None)
    
    f = open(outputfilename, "wb")
    f.write(b"<?xml version=\"1.0\" ?>\n<FANT_stack>")    
        
    i = 0
    for fantfile in stack:
        filelement = xmldoc.createElement("FANT")
        fantdoc = XmlExport.FantXmlDocument("export", xmldoc, filelement)
        xmldoc.documentElement.appendChild(filelement)
        createXml(fantfile, fantdoc)
        i = i + 1        
        print("writing", str(i) + "th FANT file into XML")
        f.write(filelement.toprettyxml().encode("utf-8"))
        #removeing the created DOM element
        xmldoc.documentElement.removeChild(filelement)
        del filelement
        
    f.write(b"</FANT_stack>")    
    f.close()
        
def createXml(fantfile, doc):
    '''
    doc has to be a valid FANT file object
    '''
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
    for nametype, namelist in lists:        
        doc.startNameSection(nametype)
        for name in namelist:
            #print name, [ ord(a) for a in name ]
            doc.addName(nametype, name)
        doc.endNameSection(nametype)
    
    eventlists = [
                  ("Action", fantfile.actionevents),
                  ("Actor", fantfile.actorevents),
                  ("Scene", fantfile.sceneevents)                      
                  ]
        
    for eventgroup, eventlist in eventlists:
        doc.startEventSection(eventgroup)
        for event in eventlist:                
            doc.addEvent(eventgroup, event)
        doc.endEventSection(eventgroup)
        
    doc.startCodeSection()    
    for code in fantfile.codes:        
        doc.addCode(code)
    doc.endCodeSection()
    
    doc.startEventSection("Repertoire")
    for event in fantfile.repertoireevents:
        doc.addEvent("Repertoire", event)
    doc.endEventSection("Repertoire")            
            
    doc.startSoundSection()
    for sound in fantfile.sounds:
        doc.addSound(sound)
    doc.endSoundSection()        
    
    doc.setSectormap(fantfile.sectormap)
    
    doc.startSectorSectionList()
    for section in fantfile.sectorsections:
        doc.addSectorSection(section)
    doc.endSectorSectionList()
        
    doc.startCamerasList()
    for camera in fantfile.cameras:
        doc.addCamera(camera)
    doc.endCamerasList()
    
    doc.startMapAreaSection()
    for maparea in fantfile.mapareas:
        doc.addMapArea(maparea)
    doc.endMapAreaSection()
   
def exportXml(fantfile):
    impl = getDOMImplementation()
    xmldoc = impl.createDocument(None, "FANT", None)
    fantdoc = XmlExport.FantXmlDocument("export", xmldoc, xmldoc.documentElement)
    createXml(fantfile, fantdoc)
    return xmldoc.toprettyxml()
    
import unittest       

class Test(unittest.TestCase):

    def testNoMagicString(self):
        f = open("test/no_fant_file", "rb")
        #self.assertRaises(IOError, FantFile.FantFile, f) 
        
    def testXmlOutput(self):
        doc = FANTLoad.FANTFileLoader(open("test/ecstatic.fan", "rb"))
        print(doc.fantfile)
        f = open("/tmp/fant.xml", "wb") 
        f.write(exportXml(doc.fantfile).encode('utf-8'))        
        f.close()
                            
if __name__ == "__main__":
    doc = XmlSave("test/ecstatic.fan") 
    print(doc.exportXml())  
