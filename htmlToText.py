#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  htmlToText.py
#  
#  Copyright 2020 jacks <jacks@DESKTOP-MINUT5T>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

##### Turn .html files into files i can actually use lmfao #####
import codecs
import os
import re
from Simplify import *

##### INITIALIZE FOLDERS AND FILES #####
sourceName = (r'{}source'.format(os.path.dirname(__file__)))
outputName = (r'{}output'.format(os.path.dirname(__file__)))
#sourceName = r'D:\jacks\Documents\seazer\testSongs'
logName = (r'{}logs\htmllog.txt'.format(os.path.dirname(__file__)))
trashLogName = (r'{}logs\htmltrashlog.txt'.format(os.path.dirname(__file__)))

#clean dump folder (outputName)
if len(os.listdir(outputName)) > 0:
    for f in os.listdir(outputName):
        try:
            os.remove(outputName + '\\' + f)
        except:
            with open(trashLogName, 'a', encoding='utf-8') as newTrashLog:
                newTrashLog.write('Error removing ' + f)

#clean log (logName)
with open(logName, 'w') as newLog:
    pass
#clean trash log (trashLogName)
with open(trashLogName, 'w', encoding='utf-8') as newTrashLog:
    pass

#find all files under current directory
pathList = [os.path.join(dirpath,filename) for dirpath, _, filenames\
 in os.walk('source') for filename in filenames if filename.endswith('.html')]

#log the names and number of files to parse
with open(logName, 'a') as newLog:
    newLog.write('This is the pathlist: ' + str(len(pathList)) + ' items.\n\n')
    newLog.write(str(pathList))
    newLog.write('\n\nThis is what was created:\n')

#feed pathList
def songLister(directories):
    masterList = []
    
    songNumber = -1
    for HTMLS in range(len(pathList)):
        htmls = pathList[HTMLS]
        #ignore tracklists and "extra content" htmls
        if 'Tracklist' in htmls or 'Track_List' in htmls or 'Audio' in htmls\
        or 'Interview' in htmls:
            with open(trashLogName, 'a', encoding='utf-8') as newTrashLog:
                newTrashLog.write(htmls)
                
        #it is time..... for cleaning up this raw HTML shit
        else:
            songNumber = songNumber + 1
##### CREATE RAW TEXT #####
            with codecs.open(htmls, 'r', 'utf-8') as f:
                test = f.read()
##### CLEAN UP RAW TEXT #####
            #im so ass at formal languages
            #removes parts inside <these>, basically takes out HTML
            test = re.sub('<[^>]+>', '', test)
            #removes parts that just go ;;;+
            test = re.sub(';;+', '', test)
##### CREATE LINES ######
            testArray = []
            testArray = test.split('\n')
##### CLEAN UP LINES #####
            #set up an array of indexes to remove from testArray later
            delLater = []
            #dictionary of Unicode things ive seen in these files and
            #what to replace them with
            repStr = ['&nbsp','\xa0','&quot;','&ldquo;','&rdquo;','&rsquo;','&amp;' ]
            wthStr = [''     ,' '   ,'"'     ,'\''     ,'\''     ,'\''       ,'&'    ]
            #replace repStr with wthStr in lines
            for a in range(len(testArray)):
                testArray[a] = testArray[a].strip()
                for i in range(len(repStr)):
                    testArray[a] = testArray[a].replace(repStr[i], wthStr[i])
                    testArray[a] = re.sub(';;+', '', testArray[a])
##### DELETE MEANINGLESS LINES ######
                #note empty or placeholder lines for later deletion
                delEqual = ['', ';', '-', '-;', ' ']
                delHas = ['---', 'Repeat']
                for d in delEqual:
                    if testArray[a] == d:
                        delLater.append(a)
                for d in delHas:
                    if d in testArray[a]:
                        delLater.append(a)
                        
            #this is the later deletion
            countDel = 0
            for d in delLater:
                del testArray[d - countDel]
                countDel = countDel + 1
##### INDEX SONGS FROM LINES (ENDPOINTS) #####
            #this sets up an array of the indexes of beginnings of individual
            #translations, transciptions, and romanizations
            startArray = []
            for a in range(len(testArray)):
                if 'Translation from' in testArray[a] or 'Translation by' in testArray[a]\
                 or 'As Provided' in testArray[a] or 'Transcribed' in testArray[a]\
                 or 'Translation Notes' in testArray[a] or 'Romanization' in testArray[a]:
                    startArray.append(a)
##### CREATE ARRAY OF SONGS #####
            #while loop to form each "song" and place it in the masterList       
            abc = True
            testOutput = []
            thingsIDontWant = ['Translation Notes', 'Carl Jung', 'Bologna']
            counter = 0
            
            #for readability
            #title  = testArray[startArray[counter] - 1
            #author = testArray[startArray[counter]
            while abc == True:
                thingIsHere = False
                if counter < len(startArray) - 1:
                    #remember testArray is the raw array of all lines
                    #this ignores translation notes, but still counts
                    #them as endpoints
                    thingIsHere = testForThings(thingsIDontWant, [testArray[startArray[counter]], testArray[startArray[counter] - 1]])
                    if thingIsHere == True:
                        counter = counter + 1
                    #this appends to testOutput:
                    #title of song -> until, but not including, title of next song
                    else:
                        testOutput.append(testArray[startArray[counter] - 1 :\
                        startArray[counter + 1] - 1])
                        
                        counter = counter + 1
                else:
                    thingIsHere = testForThings(testArray[startArray[-1]], thingsIDontWant)
                    if thingIsHere == True:
                        pass
                    else:
                        testOutput.append(testArray[startArray[-1]:-1])
                    abc = False
            
            masterList.append(testOutput)
    return masterList

#pass the list with all the lyrics here
def songWriter(masterList):
    for track in masterList:
        for translation in range(len(track)):
            fileAdd = str(simplify(track[translation][0]))
            print(fileAdd)
            #enumerate file name if duplicate file name exists
            fileAdd = enumerateFile(fileAdd, '.txt', outputName)
            print(fileAdd)
            
            #write lines of song to assigned file 'fileAdd'
            with open(outputName + '\\' + fileAdd + '.txt', 'w', encoding='utf-8') as r:
                ending = len(track[translation])
                endingCount = 0
                for line in track[translation]:
                    if endingCount == ending - 1:
                        r.write(line)
                    else:
                        r.write(line + '\n')
                        endingCount = endingCount + 1
                        
            with open(logName, 'a') as newLog:
                newLog.write(fileAdd + '\n')
                
#bold of you to assume i would annotate my program
def testForThings(thingsIDontWant, subjects):
    thingIsHere = False
    for subject in subjects:
        for thing in thingsIDontWant:
            if thing in subject:
                #log it
                with open(trashLogName, 'a', encoding='utf-8') as newTrashLog:
                    trackName = simplify(str(subject))
                    newTrashLog.write\
                    (trackName + '\n' + \
                    subject\
                    + '\n\n')
                #return True if bad thing
                return True
    return thingIsHere
    
#Checks if file exists, enumerates with a suffix if True.
#params: str fileName, str extension, str outputName
#return: str fileAdd
def enumerateFile(fileName, extension, folder = outputName):
    fileAdd = simplify(fileName)
    nfileAdd = ''
    
    #make numbered files if title is taken
    if os.path.exists(folder + '\\' + fileAdd + extension):
        counter = '0'
        #loops until it can't find file with specified name
        while True:
            #add number to fileAdd
            counter = str(int(counter) + 1)
            fileAdd = fileAdd + counter
            print(folder + '\\' + fileAdd + extension)
            if os.path.exists(folder + '\\' + fileAdd + extension) == False:
                return fileAdd
            #rebuild fileAdd without suffix
            else:
                for c in range(len(fileAdd)):
                    if c < len(fileAdd) - len(counter):
                        nfileAdd = nfileAdd + fileAdd[c]
                fileAdd = nfileAdd
                nfileAdd = ''
    else:
        return fileAdd

masterList = songLister(pathList)
print('\n')
songWriter(masterList)
