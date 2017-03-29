#!/bin/env python2.7
# encoding: utf-8
'''
Created on 29.03.2017
msBinFilter is a tool to reduce the size of an MS spectra
@author: mirandaa
'''
import sys
import os
import time
import logging
log = logging.getLogger(os.path.basename(__file__))
from lib import MSFileReader

__version__ = "17.03.29.0"

def ThermoRawfile2Scans(file_path):
    # NOTE: for testing use ThermoRawfile2Scans_sample instead
    log.info('file: %s', file_path)
    rawfile = MSFileReader.ThermoRawfile(file_path)
    
    start = rawfile.FirstSpectrumNumber
    end = rawfile.GetLastSpectrumNumber()
 
    MSrawscans = []
    for scanNum in range(start, end+1):
        peak_datas = rawfile.GetLabelData(scanNum)[0]
        filterLine = rawfile.GetFilterForScanNum(scanNum)
        retTime =  rawfile.RTFromScanNum(scanNum)*60
        row = (scanNum, filterLine, peak_datas, retTime)
        MSrawscans.append(row)
    
    log.info('Scan Count is %d', len(MSrawscans))
    #Note: to reshape into lists use 
    #scanNum, filterLine, peak_datas, retTime = zip(*MSrawscans)
    
    #Note: to get list of mass use 
    # peak_data = peak_datas[0]
    # peak_data.mass
    
    return MSrawscans

'''
Start Filtering out scans
'''


def filterScanBy_retentionTime(scans, lowSeconds=0.5, highSeconds=float("inf")):
    log.info('filterScanBy_retentionTime %f to %f', lowSeconds, highSeconds)
    
    for row in scans:
        scanNum, filterLine, peak_datas, retTime = row 
        if retTime >+ lowSeconds and  retTime <= highSeconds:
            yield row
    

def filterScanBy_filterline(scans, subtext = ' ms ', keep=False):
    log.info('filterScanBy_filterline %s filter keep: %s', subtext, keep)
    
    for row in scans:
        scanNum, filterLine, peak_datas, retTime = row 
        if keep:
            if (subtext in filterLine):
                yield row
        else: #not keep
            if (subtext not in filterLine):
                yield row

def filterScanBy_samples(scans, step_size = 10):
    log.info('filterScanBy_samples step_size %d', step_size)
    
    for idx, row in enumerate(scans):
        if idx %  step_size == 0:
            yield row


if __name__ == '__main__':
    log.addHandler(logging.StreamHandler()) # log to console
    log.setLevel(logging.DEBUG)
    
    log.debug('Start %f', time.clock())
    if len(sys.argv) == 1:
        print("A filename must be provided")
        raise SystemExit
    
    scans = ThermoRawfile2Scans(" ".join(sys.argv[1:]))
    
    ''' filtering by scan
    scans = filterScanBy_retentionTime(scans)
    
    scans = filterScanBy_filterline(scans)
    
    scans = filterScanBy_samples(scans, step_size = 3)
    '''
    
    
    
    log.debug('finish %f',  time.clock())
    