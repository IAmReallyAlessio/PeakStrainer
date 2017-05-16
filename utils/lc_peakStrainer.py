'''
Created on 16.05.2017

@author: mirandaa
'''

from peakStrainer import ThermoRawfile2Scans, preliminaryFilter
from utils.peakStrainer_util import decode_mzXML_Peaks, encodePeaks, setLogger
from collections import OrderedDict
import xml.etree.ElementTree as ET
import copy, os

import logging
log = logging.getLogger(os.path.basename(__file__))

def main():
    setLogger()
    fileName = r'C:\apps\eclipseRCP\workspace\PeakStrainer\resources\qc3_01.raw'
    step=3
    
    scans = ThermoRawfile2Scans(fileName)
    print 'og scans '+str(len(scans))
    ms_scans = [scan for scan in scans if ' ms ' in scan[1]]
    print 'ms scans '+str(len(ms_scans))
    
    scansData = OrderedDict()
    for idx, scan in enumerate(ms_scans):
        if idx+step >len(ms_scans): break 
        
#         if idx % step == 0  :
#             mergeM, mergeI = decode_mzXML_Peaks(ms_scans[idx][2])
        mergeM, mergeI = map(list,ms_scans[idx][2][0:2])
     
        thisM1, thisI1 = ms_scans[idx+1][2][0:2] 
        thisM2, thisI2 = ms_scans[idx+2][2][0:2]
         
        mergeM.extend(thisM1)  
        mergeI.extend(thisI1)
         
        mergeM.extend(thisM2)  
        mergeI.extend(thisI2)
         
        print 'Merged group '+str(idx) +' has '+str(len(mergeM))
        peakdata = (mergeM, mergeI)  
         
        newpeakData = preliminaryFilter(peakdata, minCount = 1)
         
        #scanNum, filterline, retTime
        scanHead = (scan[0], scan[1], scan[3])
        if newpeakData:
            print 'filered Merged group '+str(idx) +' has '+str(len(newpeakData[0]))
             
        else:
            print 'filered Merged group '+str(idx) +' has no peaks '+ str(scanHead)
            newpeakData = ([],[])
             
        log.debug(('analitics',)+scanHead+(len(peakdata[0]),len(newpeakData[0])))
        print 'Scan Head '+str(scanHead)
        scansData[scanHead] = newpeakData
        
    print 'writing mzxml'
    write2templateMzXML(fileName[:-4]+'.mzxml', scansData)
    print 'done'
         
def write2templateMzXML(newfilename, scanPeaks):
    namespaces = {'xmlns': 'http://sashimi.sourceforge.net/schema_revision/mzXML_3.0'}
    ET.register_namespace('', 'http://sashimi.sourceforge.net/schema_revision/mzXML_3.0')
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    tree = ET.parse(scriptPath+'\\template.mzXML')
    
    msRunElement = tree.find('.//xmlns:msRun', namespaces)
    scanTemplete = msRunElement.find('.//xmlns:scan', namespaces)
    
    
    for idx, scan in enumerate(scanPeaks):
        scanNum, filterline, retTime = scan
        (masses, intens) = scanPeaks[scan]
        newScan = copy.deepcopy(scanTemplete)
        newScan.attrib['filterLine'] = filterline
        newScan.attrib['peaksCount'] = str(len(masses))
        newScan.attrib['num']=str(scanNum)
        newScan.attrib['retentionTime']='PT'+str(retTime)+'s' 
        
        msLevel = 1 if ' ms ' in filterline else 2
        if msLevel == 1:
            newScan.remove(newScan.find('.//xmlns:precursorMz', namespaces))
        else:
            precursorMz = newScan.find('.//xmlns:precursorMz', namespaces)
            precursorMz.attrib['activationMethod'] = scan.split()[6][7:10]
            precursorMz.text = scan.split()[6][:6]

        newScan.attrib['msLevel'] = str(msLevel)
        newScan.attrib['polarity'] = '-' if ' - ' in scan else '+'
        newScan.attrib['retentionTime'] = 'PT{}S'.format(0.0+idx)
        
        encodedPeaks = encodePeaks(masses, intens)
        newScan.find('.//xmlns:peaks', namespaces).text = encodedPeaks
        msRunElement.append(newScan)
    
    msRunElement.remove(scanTemplete)
    
    tree.write(newfilename, encoding='ISO-8859-1', xml_declaration=True)        
              
    
if __name__ == '__main__':
    main()