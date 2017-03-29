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
Filter on scans
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

'''
merge peaks 
'''
def mergePeaksOnFilterline(scans):
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
        mergedPeaks[filterLine][0].extend(zmass)
        mergedPeaks[filterLine][1].extend(abunds)
        mergedPeaks[filterLine][2].extend(resols)
    
    return mergedPeaks

'''
generate bins
'''
def generateBins_decimalPlaces(peakData, decimal_places = 4):
    log.debug('generateBins_decimalPlaces, decimal_places %d',  decimal_places)
    masses = peakData[0]
    abunds = peakData[1]
    resols = peakData[2]
    log.debug('generateBins_decimalPlaces, peak count %d', len(masses))
    
    halfWidth= (10**-decimal_places)/2
    bins_low = [ round(mass-halfWidth,decimal_places) for mass in masses]
    bins_high = [ round(mass+halfWidth,decimal_places) for mass in masses] 
    
    peakData = zip(*zip(peakData[0], peakData[1], peakData[2], bins_low, bins_high))
    return peakData

def generateBins_resolution(peakData, decimal_places = 4):
    log.debug('generateBins_resolution, decimal_places %d',  decimal_places)
    masses = peakData[0]
    abunds = peakData[1]
    resols = peakData[2]
    log.debug('generateBins_resolution, peak count %d', len(masses))
    
    bins_high = [mass + ((mass/resol)/2) for mass, resol in zip(masses,resols)] 
    bins_low =  [mass - ((mass/resol)/2) for mass, resol in zip(masses,resols)]
    # rounding to make bins larger
    bins_low = [round(low,decimal_places ) for low in bins_low]
    bins_high = [round(low,decimal_places ) for low in bins_high]
    
    peakData = zip(*zip(peakData[0], peakData[1], peakData[2], bins_low, bins_high))
    return peakData

def generateBins_theoreticalResolution(peakData, decimal_places = 4):
    log.debug('generateBins_theoreticalResolution, decimal_places %d',  decimal_places)
    masses = peakData[0]
    abunds = peakData[1]
    resols = peakData[2]
    log.debug('generateBins_theoreticalResolution, peak count %d', len(masses))
    
    log.info('curve fitting to generate theoreticalResolution')
    from scipy.optimize import curve_fit
    def func(x, a, b):
        return  a*(x**-b)
    
    sort_mass = sorted(zip(masses, resols))
    
    select_masses, select_resols = zip(*sort_mass)
    log.debug('Selecting only middle of distribution, as per Kai S.')
    side_len = len(select_masses) / 15
    popt, pconv = curve_fit(func, select_masses[side_len:-side_len], select_resols[side_len:-side_len])
        
    theoResols = [func(mass, *popt) for mass in masses]
    
    bins_high = [mass + ((mass/resol)/2) for mass, resol in zip(masses,theoResols)] 
    bins_low =  [mass - ((mass/resol)/2) for mass, resol in zip(masses,theoResols)]
    # rounding to make bins larger
    bins_low = [round(low,decimal_places ) for low in bins_low]
    bins_high = [round(low,decimal_places ) for low in bins_high]
    
    peakData = zip(*zip(peakData[0], peakData[1], peakData[2], bins_low, bins_high))
    return peakData

'''
aggregate bins
'''
def aggregateBinData(peakData):
    log.debug('aggregateBinData, count')
    masses = peakData[0]
    abunds = peakData[1]
    resols = peakData[2]
    bins_low = peakData[3]
    bins_high = peakData[4] 
    log.debug('generateBins_theoreticalResolution, peak count %d', len(masses))


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
    
    #Note: mergePeaksOnFilterline_withRandom to generate testing data
    filterLines = mergePeaksOnFilterline(scans)
    
    ''' create bins for peaks
    #filterlines_withBins = {k: generateBins_decimalPlaces(v) for k, v in filterLines.iteritems()}
    #filterlines_withBins = {k: generateBins_resolution(v) for k, v in filterLines.iteritems()}
    '''
    filterlines_withBins = {k: generateBins_theoreticalResolution(v) for k, v in filterLines.iteritems()}
    
    binData = {k: aggregateBinData(v) for k, v in filterlines_withBins.iteritems()}
    
    log.debug('finish %f',  time.clock())
    