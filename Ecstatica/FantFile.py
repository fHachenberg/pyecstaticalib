# coding: utf-8
from __future__ import absolute_import

#Created on 18.10.2011

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.
    
#from .Game import NamesDB
from .Game import NamesDB

class FANTFile(object):
    def __setcodes(self, codes):
        self._codes = codes
        
    def __getcodes(self):
        return self._codes
    
    codes = property(__getcodes, __setcodes)
    
    def _initIndexArrays(self):
        '''
        This routine initializes the index arrays using a for each type predefined number of
        objects
        see 2A1A3 
        '''        
        
        self.partnameidxs = range(203)
        self.trinameidxs = range(30)
        self.pointnameidxs = range(50)
        self.actornameidxs = range(500)
        self.actionnameidxs = range(1000)
        self.scenenameidxs = range(1000)
        self.codenameidxs = range(1500)
        self.repertnameidxs = range(150)
        self.soundnameidxs = range(500)
        self.mapareanameidxs = range(100)
    
    def __init__(self):
        self.parts = []
        self.actors = []
        self.actions = []
        self.scenes = []
        self.points = []
        self.triangles = []
        self.repertoires = []
        
        self.mapareas = []
        self.codes = []
        self.sounds = []
        self.cameras = []
        self.sectorsections = []
        
        self.sectormap = None
        
        self.actorevents = []
        self.actionevents = []
        self.sceneevents = []
        self.repertoireevents = []
        
        self.partnames = NamesDB("Part")
        self.actornames = NamesDB("Actor")
        self.actionnames = NamesDB("Action")
        self.scenenames = NamesDB("Scene")
        self.pointnames = NamesDB("Point")
        self.trianglenames = NamesDB("Triangle")
        self.codenames = NamesDB("Code")
        self.repertoirenames = NamesDB("Repertoire")
        self.soundnames = NamesDB("Sound")
        self.mapareanames = NamesDB("MapArea")
        
        self.partnameidxs = []
        self.actornameidxs = []         
        self.actionnameidxs = []
        self.scenenameidxs = []                
        self.pointnameidxs = []            
        self.trinameidxs = []                
        self.codenameidxs = []                 
        self.repertnameidxs = []                
        self.soundnameidxs = []                
        self.mapareanameidxs = []
        
    def getNameList(self, nametype):
        if nametype == "Part":
            return self.partnames
        elif nametype == "Actor":
            return self.actornames
        elif nametype == "Action":
            return self.actionnames
        elif nametype == "Scene":
            return self.scenenames
        elif nametype == "Point":
            return self.pointnames
        elif nametype == "Triangle":
            return self.trianglenames
        elif nametype == "Code":
            return self.codenames
        elif nametype == "Repertoire":
            return self.repertoirenames
        elif nametype == "Sound":
            return self.soundnames
        elif nametype == "MapArea":
            return self.mapareanames
        else:
            raise StandardError("Unknown name type")
        
    def getAllNameLists(self):
        return {    "Part":         self.partnames,
                    "Actor":        self.actornames,
                    "Action":       self.actionnames,
                    "Scene":        self.scenenames,
                    "Point":        self.pointnames,
                    "Triangle":     self.trianglenames,
                    "Code":         self.codenames,
                    "Repertoire":   self.repertoirenames,
                    "Sound":        self.soundnames,
                    "MapArea":      self.mapareanames
                }
        
    def setNameList(self, nametype, namelist):
        if nametype == "Part":
            self.partnames = namelist
        elif nametype == "Actor":
            self.actornames = namelist
        elif nametype == "Action":
            self.actionnames = namelist
        elif nametype == "Scene":
            self.scenenames = namelist
        elif nametype == "Point":
            self.pointnames = namelist
        elif nametype == "Triangle":
            self.trianglenames = namelist
        elif nametype == "Code":
            self.codenames = namelist
        elif nametype == "Repertoire":
            self.repertoirenames = namelist
        elif nametype == "Sound":
            self.soundnames = namelist
        elif nametype == "MapArea":
            self.mapareanames = namelist
        else:
            raise StandardError("Unknown name type")
            
    def setNameIdxList(self, nametype, nameidxlist):
        if nametype == "Part":
            self.partnameidxs = nameidxlist
        elif nametype == "Actor":
            self.actornameidxs = nameidxlist
        elif nametype == "Action":
            self.actionnameidxs = nameidxlist
        elif nametype == "Scene":
            self.scenenameidxs = nameidxlist
        elif nametype == "Point":
            self.pointnameidxs = nameidxlist
        elif nametype == "Triangle":
            self.trianglenames = nameidxlist
        elif nametype == "Code":
            self.codenameidxs = nameidxlist
        elif nametype == "Repertoire":
            self.repertoirenames = nameidxlist
        elif nametype == "Sound":
            self.soundnameidxs = nameidxlist
        elif nametype == "MapArea":
            self.mapareanameidxs = nameidxlist
        else:
            raise StandardError("Unknown name type")
        
    def getNameIdxList(self, nametype):
        if nametype == "Part":
            return self.partnameidxs
        elif nametype == "Actor":
            return self.actornameidxs
        elif nametype == "Action":
            return self.actionnameidxs
        elif nametype == "Scene":
            return self.scenenameidxs
        elif nametype == "Point":
            return self.pointnameidxs
        elif nametype == "Triangle":
            return self.trianglenames
        elif nametype == "Code":
            return self.codenameidxs
        elif nametype == "Repertoire":
            return self.repertoirenames
        elif nametype == "Sound":
            return self.soundnameidxs
        elif nametype == "MapArea":
            return self.mapareanameidxs
        else:
            raise StandardError("Unknown name type")
        
    def __str__(self):
        
        st = "FANT file:\n"
        st+= "Name-Arrays\n"
        st+= "Type\t\tNumber of Names\n"
        st+= "Part\t\t" + str(len(self.partnameidxs)) + "\n"
        st+= "Actor\t\t" + str(len(self.actornameidxs)) + "\n"
        st+= "Action\t\t" + str(len(self.actionnameidxs)) + "\n"
        st+= "Scene\t\t" + str(len(self.scenenameidxs)) + "\n"        
        st+= "Point\t\t" + str(len(self.pointnameidxs)) + "\n"   
        st+= "Triangle\t" + str(len(self.trinameidxs)) + "\n"       
        st+= "Code\t\t" + str(len(self.codenameidxs)) + "\n"             
        st+= "Repertoire\t" + str(len(self.repertnameidxs)) + "\n"          
        st+= "Sound\t\t" + str(len(self.soundnameidxs)) + "\n"        
        st+= "MapArea\t\t" + str(len(self.mapareanameidxs)) + "\n"
        st+= "\n"
        st+= "Objects\n"
        st+= "Type\t\tNumber of Data Entries\n"
        st+= "Part\t\t" + str(len(self.parts)) + "\n"
        st+= "Actor\t\t" + str(len(self.actors)) + "\n"
        st+= "Action\t\t" + str(len(self.actions)) + "\n"
        st+= "Scene\t\t" + str(len(self.scenes)) + "\n"        
        st+= "Point\t\t" + str(len(self.points)) + "\n"   
        st+= "Triangle\t" + str(len(self.triangles)) + "\n"       
        st+= "Code\t\t" + str(len(self.codes)) + "\n"             
        st+= "Repertoire\t" + str(len(self.repertoires)) + "\n"          
        st+= "Sound\t\t" + str(len(self.sounds)) + "\n"        
        st+= "MapArea\t\t" + str(len(self.mapareas)) + "\n"
        return st        
