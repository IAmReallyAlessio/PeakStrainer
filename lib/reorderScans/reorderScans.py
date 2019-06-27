'''
Created on 03.05.2017

@author: mirandaa
'''
from .reorderScansUI_batch import MyFrame1
import wx
import xml.etree.ElementTree as ET
import os
import re
import copy
import re

def main(folderpath = None):
    app = wx.App(False)
    frame = MyFrame(None, folderpath)
    frame.Show(True)
    app.MainLoop()
    
def getScanHeaders(files):
    filterlines = []
    for f in files:
        with open(f,'r') as file:
            matches = re.findall(' filterLine="(.*?)" ', file.read())
            filterlines.extend(matches)
    return list(set(filterlines))
    
def getMZXMLFiles(folderPath):
    result = []
    for file in os.listdir(folderPath):
        if file.lower().endswith(".mzxml"):
            result.append(os.path.join(folderPath, file))
    return result


def getSourceList(folderPath):
    sourceList = []
    
    files = getMZXMLFiles(folderPath)
    scans = getScanHeaders(files)
    
    select = set()
    containsMS = False
    containsPos = False
    containsNeg = False
    for scan in scans:
        if not containsMS and ' ms ' in scan: containsMS = True 
        if not containsPos and ' + ' in scan: containsPos = True
        if not containsNeg and ' - ' in scan: containsNeg = True
        
        m = re.search(r'@(.*?) ', scan)
        if m:
            select.add(m.group(1))
    
    #----
    if containsMS:
        if containsNeg: sourceList.append(' ms , - ') # notice comma I split on comma
        if containsPos: sourceList.append(' ms , + ')
        
    for e in select:
        if containsNeg: sourceList.append(e+', - ')
        if containsPos: sourceList.append(e+', + ')
    
    
    return sourceList


def saveFile(filePath, targetOrder, includeSims=False):
       #     TODO:handle different namespaces of mzxml 
    namespaces = {'xmlns': 'http://sashimi.sourceforge.net/schema_revision/mzXML_3.0'}
    ET.register_namespace('', 'http://sashimi.sourceforge.net/schema_revision/mzXML_3.0')
    tree = ET.parse(filePath)
 
    msRunElement = tree.find('.//xmlns:msRun', namespaces)
    scanElems = msRunElement.findall('.//xmlns:scan', namespaces)
    filterlines = [scan.attrib['filterLine'] for scan in scanElems]
    
    _, sortedScanElems = list(zip(*sorted(zip(filterlines,scanElems ))))
    
    for scan in scanElems:
        msRunElement.remove(scan)
    
    
    counter = 0
    for selectionLine in targetOrder:
        type = selectionLine.split(',')[0]
        mode = selectionLine.split(',')[1]
        for scan in sortedScanElems:
            scanLine = scan.attrib['filterLine']
            if includeSims == False and ' sim ' in scanLine.lower(): continue
            if type in scanLine and mode in scanLine:
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
        idx = self.m_listBox1.GetSelection()
        self.model.target.append(self.m_listBox1.GetItems()[idx])
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
        saveFiles(self.m_dirPicker1.GetPath(), self.model.target, self.m_checkBox1.GetValue())
        self.m_dirPicker1.SetPath('')
        self.directoryUpdated(None)
        wx.MessageBox('Process complete', 'Info', 
            wx.OK | wx.ICON_INFORMATION)
#         raise SystemExit
        

if __name__ == '__main__':
    main()
    
    
    
    