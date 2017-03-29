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

if __name__ == '__main__':
    log.addHandler(logging.StreamHandler()) # log to console
    log.setLevel(logging.DEBUG)
    
    log.debug('Start %f', time.clock())
    if len(sys.argv) == 1:
        print("A filename must be provided")
        raise SystemExit
    
    scans = ThermoRawfile2Scans(" ".join(sys.argv[1:]))
    
    log.debug('finish %f',  time.clock())
    