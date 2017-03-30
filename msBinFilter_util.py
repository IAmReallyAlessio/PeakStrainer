'''
Created on 29.03.2017
msBinFilter_util contains functions that are useful but not used
@author: mirandaa
'''
from base64 import b64decode, b64encode
import array
import sys
import os
import logging
import random
log = logging.getLogger(os.path.basename(__file__))
from lib import MSFileReader

def encodePeaks(masses, intens):
    peak_list = []
    for mass, intens in sorted(zip(masses, intens)):
        peak_list.append(mass)
        peak_list.append(intens)
    
    peaks = array('f',peak_list)
    if sys.byteorder != 'big':
        peaks.byteswap()
        
    encoded = b64encode(peaks)
    return encoded
    

def decode_mzXML_Peaks(encodedPeaks):
        '''
        Note zmass and intensity are together
       
        '''
        
        decoded = b64decode(encodedPeaks)
        peaks = array('f',decoded)
    
        if sys.byteorder != 'big':
            peaks.byteswap()
        
        mass = peaks[::2]
        intens = peaks[1::2]
        return mass, intens
    
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

def mergePeaksOnFilterline_withRandom(scans):
    log.info('Merging %d scans' , len(scans))
    
    filterLines = set([filterLine for scanNo, filterLine, peakData, retTime in scans])
    log.info('found %d uniqe filterlines', len(filterLines))
    
    # create dict
    mergedPeaks = {}
    for filterLine in filterLines:
        mergedPeaks[filterLine]=([],[],[])
        
#     populate dict
    for scanNo, filterLine, peakData, retTime in scans:
        (zmass, abunds, resols, baseline , noise, charge) = peakData
        
        logging.warn('Altering content for testing:')
        logging.warn('masses with an odd M/Z will be have random resolution')
    
        for idx, val  in enumerate(zmass):
            massInt  = int(val)
            if massInt % 2 == 1:
                zmass[idx] = massInt + random.random()
                
        mergedPeaks[filterLine][0].extend(zmass)
        mergedPeaks[filterLine][1].extend(abunds)
        mergedPeaks[filterLine][2].extend(resols)
    
    return mergedPeaks

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