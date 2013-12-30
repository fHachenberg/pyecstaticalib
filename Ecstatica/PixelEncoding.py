# coding: utf-8

#Created on 05.06.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

def decodePixels(data):
    '''
    according to 35008
    '''
    maxlen = 128000

    bytedata = bytearray(data)
    out = bytearray()
    pos = 0
    lastcolor = int(0)
    while pos < len(bytedata) and len(out) < maxlen:
        #we test whether the lowest bit is set
        typeval = (bytedata[pos] & 0x03)         
        runlength = bytedata[pos] >> 2
        pos += 1
        if runlength == 0:
            return out
        if typeval == 0:
            #relative color values
            #each byte contains up to 2 relative pixel values
            #if runlength is an odd number, for the last of these packed bytes only the lower 4 bits are used
            while runlength > 0:                
                first = bytedata[pos] & 0x0f                                
                second = bytedata[pos] >> 4
                pos += 1 #we move the input pointer forward independent of wether we will use the upper 4 bits
                #lower 4 bits
                if first & 0x08 != 0:#if bit #4 is set, the value is negative                 
                    first |= 0xf0                
                lastcolor += first
                if lastcolor < 0:
                    lastcolor = lastcolor + 256
                if lastcolor > 255:
                    lastcolor = lastcolor - 256
                out.append(lastcolor)
                runlength -= 1                
                if runlength == 0:
                    break
                #upper 4 bits
                if second & 0x08 != 0: #if bit #4 is set, the value is negative
                    #print(second, second | 0xf0)
                    second |= 0xf0
                lastcolor += second
                if lastcolor < 0:
                    lastcolor = lastcolor + 256
                if lastcolor > 255:
                    lastcolor = lastcolor - 256
                out.append(lastcolor)
                runlength -= 1                    
        elif typeval == 2:
            #direct transfer of pixel values
            for i in range(runlength):
                lastcolor = bytedata[pos]
                out.append(lastcolor)
                pos += 1
        else:
            #run-length times the following pixel value
            lastcolor = bytedata[pos]
            for i in range(runlength):
                out.append(lastcolor)
            pos += 1                            
        
    return out

def decodePixelsWords(data):
    '''
    decodes depth data (2-byte-wide entries, as opposed to the color data with 1-byte-wide entries)
    
    according to 35065
    '''
    maxlen = 128000

    bytedata = bytearray(data)
    out = []
    pos = 0
    lastcolor = int(0)
    while pos < len(bytedata) and len(out) < maxlen:
        #we test whether the lowest bit is set
        typeval = (bytedata[pos] & 0x03)         
        runlength = bytedata[pos] >> 2
        pos += 1
        if runlength == 0:
            return out
        if typeval == 0:
            #relative color values
            #each byte contains up to 2 relative pixel values
            #if runlength is an odd number, for the last of these packed bytes only the lower 4 bits are used
            while runlength > 0:                
                first = (bytedata[pos] & 0x0f)                                 
                second = (bytedata[pos] >> 4) 
                pos += 1 #we move the input pointer forward independent of wether we will use the upper 4 bits
                
                #lower 4 bits
                if first & 0x08 != 0:#if bit #4 is set, the value is negative                 
                    first |= 0xfff0                
                lastcolor += first << 2
                lastcolor &= 0xffff
                out.append(lastcolor)
                runlength -= 1                
                if runlength == 0:
                    break
                
                #upper 4 bits
                if second & 0x08 != 0: #if bit #4 is set, the value is negative                    
                    second |= 0xfff0
                lastcolor += second << 2
                lastcolor &= 0xffff
                out.append(lastcolor)
                runlength -= 1     
        elif typeval == 1:
            for i in range(runlength):
                value = bytedata[pos]    
                if value & 0x80: #negative?
                    value |= 0xff00
                pos += 1
                lastcolor += value << 2
                lastcolor &= 0xffff
                out.append(lastcolor)
        elif typeval == 2:
            #direct transfer of pixel values
            for i in range(runlength):
                lastcolor = ((bytedata[pos] + (bytedata[pos+1] << 8)) << 2) & 0xffff
                out.append(lastcolor)
                pos += 2
        elif typeval == 3:
            #run-length times the following pixel value
            lastcolor = ((bytedata[pos] + (bytedata[pos+1] << 8)) << 2) & 0xffff            
            for i in range(runlength):
                out.append(lastcolor)
            pos += 2
        
    return out

  
        
import unittest
import struct
import itertools

class TestView(unittest.TestCase):
    def test_decodepixels(self):
        #we have to load data for testing
        viewfileobj = open("test/views/0002.raw", "rb")
        
        typemark = viewfileobj.read(2)
        len_a = struct.unpack("<i", viewfileobj.read(4))[0]        
        len_b = struct.unpack("<i", viewfileobj.read(4))[0]
        print(len_a, len_b)
                
        structstr = "".join(itertools.repeat("B", len_a))
        packed_pixeldata_a = struct.unpack(structstr, viewfileobj.read(len_a))
        decodePixels(packed_pixeldata_a)

        structstr = "".join(itertools.repeat("B", len_b))
        packed_depthdata = struct.unpack(structstr, viewfileobj.read(len_b))
        decodePixelsWords(packed_depthdata)
        
