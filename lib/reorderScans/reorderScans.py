'''
Created on 03.05.2017

@author: mirandaa
'''
from reorderScansUI_batch import MyFrame1
import wx
import xml.etree.ElementTree as ET
import os
import re

def main(folderpath = None):
    app = wx.App(False)
    frame = MyFrame(None, folderpath)
    frame.Show(True)
    app.MainLoop()
    
def getScanHeaders(filePath):
        #     TODO:handle different namespaces of mzxml 
    namespaces = {'xmlns': 'http://sashimi.sourceforge.net/schema_revision/mzXML_3.0'}
    ET.register_namespace('', 'http://sashimi.sourceforge.net/schema_revision/mzXML_3.0')
    tree = ET.parse(filePath)
 
    scanElems = tree.findall('.//xmlns:scan', namespaces)
    
    scans = []
    for scan in scanElems:
#             scanNo = int(scan.attrib['num'])
#         scanNo = scan.attrib['num'].zfill(5)
#  scan number ges confused with other values so its not good
# maybe add zerowidth space to solve '\u200b'
        filterLine = scan.attrib['filterLine']
        scans.append(filterLine)

    return scans
    
def getMZXMLFiles(folderPath):
    result = []
    for file in os.listdir(folderPath):
        if file.lower().endswith(".mzxml"):
            result.append(os.path.join(folderPath, file))
    
    return result 


def getSourceList(folderPath):
    sourceList = []
    sourceList.append(' ms , - ') # notice comma I split on comma
    sourceList.append(' ms , + ') 
    
    files = getMZXMLFiles(folderPath)
    first = files[0]
    scans = getScanHeaders(first)
    
    select = set()
    for scan in scans:
        m = re.search(r'@(.*?) ', scan)
        if m:
            select.add(m.group(1))
    
    for e in select:
        sourceList.append(e+', - ')
        sourceList.append(e+', + ')
    
    
    return sourceList


def saveFile(filePath, targetOrder):
       #     TODO:handle different namespaces of mzxml 
    namespaces = {'xmlns': 'http://sashimi.sourceforge.net/schema_revision/mzXML_3.0'}
    ET.register_namespace('', 'http://sashimi.sourceforge.net/schema_revision/mzXML_3.0')
    tree = ET.parse(filePath)
 
    msRunElement = tree.find('.//xmlns:msRun', namespaces)
    scanElems = msRunElement.findall('.//xmlns:scan', namespaces)
    
    for scan in scanElems:
        msRunElement.remove(scan)
    
    for selectionLine in targetOrder:
        type = selectionLine.split(',')[0]
        mode = selectionLine.split(',')[1]
        for scan in scanElems:
            scanLine = scan.attrib['filterLine']
            if type in scanLine and mode in scanLine:
                msRunElement.append(scan)

    dir,file = os.path.split(filePath)
    
    if not os.path.exists(dir+'\\organized'):
        os.makedirs(dir+'\\organized')
    newfilename = dir+'\\organized\\'+file
    tree.write(newfilename, encoding='ISO-8859-1', xml_declaration=True)


def saveFiles(path, targetOrder):
    files =  getMZXMLFiles(path)
    
    for file in files:
        saveFile(file, targetOrder)
        

class MyModel(object):
    def __init__(self):
        self.source = []
        self.target = []
        


class MyFrame(MyFrame1):
    def __init__(self, parent, folderpath = None):
        super(MyFrame, self).__init__(parent)
        self.model = MyModel()
        if folderpath is not None: 
            self.m_dirPicker1.SetPath(folderpath)
            self.directoryUpdated(None)
        
    def directoryUpdated( self, event ):
        self.model.source = getSourceList(self.m_dirPicker1.GetPath())
        self.m_listBox1.Set(self.model.source)
        self.model.target = []
        self.m_listBox2.Set(self.model.target)
        
    
    def addToTargetList( self, event ):
        idx = self.m_listBox1.GetSelection()
        self.model.target.append(self.m_listBox1.GetItems()[idx])
        self.m_listBox2.Set(self.model.target)
    
    def removeFromTargetList( self, event ):
#         idx = self.m_listBox2.GetSelection() only remove last
        self.model.target.pop()
        self.m_listBox2.Set(self.model.target)
        
    
    def finish( self, event ):
        saveFiles(self.m_dirPicker1.GetPath(), self.model.target)
        raise SystemExit

        

if __name__ == '__main__':
    main()
    
    
    
    