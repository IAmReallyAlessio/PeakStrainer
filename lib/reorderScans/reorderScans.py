'''
Created on 03.05.2017

@author: mirandaa
'''
from reorderScansUI_batch import MyFrame1
import wx
import xml.etree.ElementTree as ET
import os
import re
import copy
from collections import OrderedDict

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

def sanitize(scan):
    if "@" in scan:
        m = re.match(r'(.*?)\s(\d*\.\d*)(@.*)\s\[', scan)
        result = m.groups()[0]+' '+m.groups()[2]
    else:
        m = re.match(r'(.*?)\s\[', scan)
        result = m.groups()[0]
   
    return result

def getSourceList(folderPath):
    
    files = getMZXMLFiles(folderPath)
    first = files[0]
    scans = getScanHeaders(first)
    
    sanitizedScans = set([sanitize(scan) for scan in scans])    
    
    return sorted(sanitizedScans)


def saveFile(filePath, targetOrder, includeSims=False): # TODO include sims is deprocated
       #     TODO:handle different namespaces of mzxml 
    namespaces = {'xmlns': 'http://sashimi.sourceforge.net/schema_revision/mzXML_3.0'}
    ET.register_namespace('', 'http://sashimi.sourceforge.net/schema_revision/mzXML_3.0')
    tree = ET.parse(filePath)
 
    msRunElement = tree.find('.//xmlns:msRun', namespaces)
    scanElems = msRunElement.findall('.//xmlns:scan', namespaces)
    filterlines = [scan.attrib['filterLine'] for scan in scanElems]
    
    _, sortedScanElems = zip(*sorted(zip(filterlines,scanElems )))
    
    for scan in scanElems:
        msRunElement.remove(scan)
    
    selected = []
    for selectionLine in targetOrder:
        for scan in sortedScanElems:
            filterLine= scan.attrib['filterLine']
            if sanitize(filterLine) == selectionLine:
               selected.append(scan)

    selectedSet = []
    for e in selected:
        if e not in selectedSet:
            selectedSet.append(e)
    
    counter = 0
    for scan in selectedSet:
        new_scan = copy.deepcopy(scan)
        counter = counter + 1 
        new_scan.attrib['retentionTime'] = 'PT'+str(counter)+'.0S'
        msRunElement.append(new_scan)

    dir,file = os.path.split(filePath)
    
    if not os.path.exists(dir+'\\ordered'):
        os.makedirs(dir+'\\ordered')
    newfilename = dir+'\\ordered\\'+file
    tree.write(newfilename, encoding='ISO-8859-1', xml_declaration=True)


def saveFiles(path, targetOrder, includeSims = False):
    files =  getMZXMLFiles(path)
    
    for file in files:
        saveFile(file, targetOrder,includeSims)
        

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
        if event is None: 
            self.model.source = []
        else:
            self.model.source = getSourceList(self.m_dirPicker1.GetPath())
        self.m_listBox1.Set(self.model.source)
        self.model.target = []
        self.m_listBox2.Set(self.model.target)
        
    def sourceDubleClicked( self, event ):
        idxs = self.m_listBox1.GetSelections()
        for idx in idxs: 
            self.model.target.append(self.m_listBox1.GetItems()[idx])
            self.m_listBox1.Deselect(idx)
        self.m_listBox2.Set(self.model.target)
    
    
    def addToTargetList( self, event ):
        idxs = self.m_listBox1.GetSelections()
        for idx in idxs: 
            self.model.target.append(self.m_listBox1.GetItems()[idx])
            self.m_listBox1.Deselect(idx)
        self.m_listBox2.Set(self.model.target)
    
    def removeFromTargetList( self, event ):
#         idx = self.m_listBox2.GetSelection() only remove last
        self.model.target.pop()
        self.m_listBox2.Set(self.model.target)
        
    
    def finish( self, event ):
        saveFiles(self.m_dirPicker1.GetPath(), self.model.target, self.m_checkBox1.GetValue())
        self.m_dirPicker1.SetPath('')
        self.directoryUpdated(None)
        wx.MessageBox('Process complete', 'Info', 
            wx.OK | wx.ICON_INFORMATION)
#         raise SystemExit
        

if __name__ == '__main__':
    main()
    
    
    
    