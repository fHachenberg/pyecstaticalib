# coding: utf-8

#Created on 10.03.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

class debugopen(object):
    def __init__(self, filename, openmode, reffile):
        self.fileobj = open(filename, openmode)
        self.reffile = open(reffile, "rb")
        
    def write(self, str):
        refstr = self.reffile.read(len(str))
        assert str == refstr
