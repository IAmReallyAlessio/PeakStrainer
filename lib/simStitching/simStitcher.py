'''
Created on 24.05.2017

@author: mirandaa
'''
import sys, os
import logging
from collections import namedtuple
import re
from base64 import b64decode
import array
log = logging.getLogger(os.path.basename(__file__))
from utils.peakStrainer_util import getMZXMLEncondedScans, decode_mzXML_Peaks

class Scan(object):
    
    class FilterLine(object):
        def __init__(self, filterline):
            self.filterline = filterline
            self.match = re.match(r'(.*)\[(\d+\.\d*)-(\d+\.\d*)\]', filterline)
        
        def __str__(self):
            return self.filterline
        
        def __repr__(self):
            return self.filterline
        
        def head(self):
            return self.match.group(1)
        def low(self):
            return float(self.match.group(2))
        def high(self):
            return float(self.match.group(3))
        
    
    def __init__(self, scanNo, filterLine, encodedPeaks, retTime = None):
        self.scanNo = scanNo
        self.filterLine = self.FilterLine(filterLine)
        self.encodedPeaks = encodedPeaks
        self.retTime = retTime
        self.masses, self.intens = decode_mzXML_Peaks(self.encodedPeaks)
        self.previous = None
        self.next = None
        
    def __str__(self):
        return 'Scan Num {}, {}, peak Count = {}'.format(self.scanNo,self.filterLine, len(self.masses))
    
    def __repr__(self):
        return '{}; {}; {}; {};'.format(self.scanNo,self.filterLine, self.retTime, self.encodedPeaks)
    
    def decode_mzXML_Peaks(self, encodedPeaks):
        decoded = b64decode(encodedPeaks)
        peaks = array('f',decoded)
    
        if sys.byteorder != 'big':
            peaks.byteswap()
        
        mass = peaks[::2]
        intens = peaks[1::2]
        return mass, intens
    
    
    
        

def simStitcher(filePath = None):
    log.info('getMZXMLEncondedScans from'+ filePath)
    scans_mzxml = getMZXMLEncondedScanRows(filePath)
    log.debug('\n'.join(map(str,scans_mzxml)))
    
    log.info('drop first scan because invalid')
    scans_mzxml = scans_mzxml[1:]
        
    log.info('get Sim scans')
    scans_mzxml_sim= [scan for scan in scans_mzxml if ' sim ' in scan[1].lower()]
    log.debug('\n'.join(map(str,scans_mzxml_sim)))
    
    scans =[Scan(*scan_xml) for scan_xml in scans_mzxml_sim]
    
    log.info('get sorted filterlines')
    scans.sort(key=lambda scan: (scan.filterLine.head(),scan.filterLine.low(),scan.filterLine.high()))
    
    log.debug('\n'.join(map(str,scans)))
    
    scans[0].next = scans[1] #previous is none
    for idx, scan in enumerate(scans[1:-1]):
        scan.previous = scans[idx-1]
        scan.next = scans[idx+1]
    scans[-1].previous = scans[-2] #next is none
    
    
    log.info('finish')
    
def getMZXMLEncondedScanRows(filePath):
    return zip(*getMZXMLEncondedScans(filePath)) 


if __name__ == '__main__':
    if len(sys.argv) > 0:
        simStitcher(sys.argv[1])
    else:
        simStitcher()
    