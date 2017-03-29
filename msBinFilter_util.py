'''
Created on 29.03.2017
msBinFilter_util contains functions that are useful but not used
@author: mirandaa
'''
from base64 import b64decode
import array
import sys
import os
import logging
log = logging.getLogger(os.path.basename(__file__))
from lib import MSFileReader

def decode_mzXML_Peaks(encodedPeaks):
        '''
        Note zmass and intensity are together
        mass = peaks[::2]
        intens = peaks[1::2]
        '''
        
        decoded = b64decode(encodedPeaks)
        peaks = array('f',decoded)
    
        if sys.byteorder != 'big':
            peaks.byteswap()
        
        return peaks
    
def ThermoRawfile2Scans_sample(file_path):
    log.info('file: %s', file_path)
    rawfile = MSFileReader.ThermoRawfile(file_path)
    
    start = rawfile.FirstSpectrumNumber
    end = rawfile.GetLastSpectrumNumber()
 
    MSrawscans = []
    for scanNum in range(start, end+1):
        if scanNum % 10 == 0 : continue # just take a sample
        rawPeaks = rawfile.GetLabelData(scanNum)[0]
        filterLine = rawfile.GetFilterForScanNum(scanNum)
        if 'ms2' not in filterLine: continue  # to discard the MS1 this is the largest
        retTime =  rawfile.RTFromScanNum(scanNum)*60
        object = (scanNum, filterLine, rawPeaks, retTime)
        MSrawscans.append(object)
    
    logging.info('Scan Count is {}'.format(len(MSrawscans)))
    return MSrawscans

def setLogger(LOG_FILENAME = 'log.log'):
    
    # log to file
    logging.basicConfig(format='%(message)s',
                        filename=LOG_FILENAME,
                        filemode='w',
                        level=logging.DEBUG)
    # log to console
    logging.getLogger().addHandler(logging.StreamHandler())


if __name__ == '__main__':
    pass