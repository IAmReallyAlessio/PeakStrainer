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
from timeit import itertools
from msBinFilter_util import encodePeaks
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
merge peaks and coarse grained filtering 
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


def preliminaryFilter(peakData, decimal_places = 2, minCount = 2, minRepetitionRate = 0.5):
    log.debug('preliminaryFilter rounding to decimal_places %d, minCount = %d, minRepetitionRate %f',  decimal_places, minCount, minRepetitionRate)
    masses = peakData[0]
    log.debug('initial peak count %d',len(masses))
    
    roundeds = [round(mass, decimal_places) for mass in masses]
    bins = dict()
    for rounded in roundeds:
        bins[rounded] = bins.get(rounded, 0) + 1
    
    log.debug('Prelimianry groups count %d', len(bins))
    minCount_bin = {bin:count for bin,count in bins.iteritems() if count >+ minCount}
    log.debug('groups with minCount %d: %d', minCount,len(minCount_bin))
    minCount_bin_max = float(max(minCount_bin.values()))
    minRepetitionRate_bin = {bin:count for bin,count in minCount_bin.iteritems() if (count/minCount_bin_max) > minRepetitionRate }
    log.debug('groups with minRepetitionRate %f: %d', minRepetitionRate,len(minRepetitionRate_bin))
    
    preFilterPass = [rounded in minRepetitionRate_bin.keys() for rounded in roundeds]
    compressedPeakData = list(itertools.compress(zip(*peakData), preFilterPass))
    compressedPeakData = zip(*compressedPeakData)
    log.debug('final peak count %d',len(compressedPeakData))
    return compressedPeakData    


def preliminaryReductionFilter(peakData, reduction = 0.10, minPeaks = 10):
    peak_count = len(peakData[0])
    goal = int(peak_count * reduction)
    log.debug('preliminaryReductionFilter will reduce peak count to max %d and min %d',  goal, minPeaks)
        
    decimal_places = 2
    minCount = 2
    minRepetitionRate = 0.5
    toggle = False
    while (peak_count > goal):
        if toggle: decimal_places += 1 
        else: minRepetitionRate +=0.1
        peakData = preliminaryFilter(peakData, decimal_places, minCount, minRepetitionRate)
        peak_count = len(peakData[0])
    
    return peakData
    
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
    
    log.info('function a*(x**-b) uses values: mass, %f, %f ', popt[0], popt[1])
        
    theoResols = [func(mass, *popt) for mass in masses]
    
    bins_high = [mass + ((mass/resol)/2) for mass, resol in zip(masses,theoResols)] 
    bins_low =  [mass - ((mass/resol)/2) for mass, resol in zip(masses,theoResols)]
    # rounding to make bins larger
    bins_low = [round(low,decimal_places ) for low in bins_low]
    bins_high = [round(low,decimal_places ) for low in bins_high]
    
    peakData = zip(*zip(peakData[0], peakData[1], peakData[2], bins_low, bins_high))
    return peakData

'''
sort each mass in a bin
'''
def sortMassIn_FirstBin(peakData):
    log.debug('sortMassIn_FirstBin, no sorting , just the first bins that matches')
    masses = peakData[0]
    abunds = peakData[1]
    resols = peakData[2]
    bins_low = peakData[3]
    bins_high = peakData[4]
    
    uniqBins = set(zip(bins_low,bins_high))
    log.debug('Mass count %d, available bins %d', len(masses), len(uniqBins))
    if (len(masses) * len(uniqBins) > 1000000):
        log.warn('this operation may take a long time, use sortMassIn_sortWindow instead')
        return sortMassIn_sortWindow(peakData, len(uniqBins)/100)
    bins = []
    for mass in masses:
        for bin_low, bin_high in uniqBins:
            if mass >= bin_low and mass <= bin_high:
                bins.append((bin_low,bin_high))
                break
    
    if(len(bins) != len(masses)):
        log.error('There was a problem setting masses in bins, please verify bins where created correctly')
    
    peakData = zip(*zip(peakData[0], peakData[1], peakData[2], peakData[3], peakData[4], bins))
    return peakData


def sortPeaksByBinWidth(peakData):
    bin_width = [bin_high - bin_low for bin_low, bin_high in zip(peakData[3], peakData[4])]
    sorted_peakdata_plus = zip(*sorted(zip(bin_width, *peakData)))
    sorted_peakdata = sorted_peakdata_plus[1:]
    return sorted_peakdata

def sortMassIn_NarrowestBin(peakData):
    log.debug('sortMassIn_NarrowestBin')
    masses = peakData[0]
    abunds = peakData[1]
    resols = peakData[2]
    bins_low = peakData[3]
    bins_high = peakData[4]
    
    uniqBins = set(zip(bins_low,bins_high))
    log.debug('Mass count %d, available bins %d', len(masses), len(uniqBins))
    if (len(masses) * len(uniqBins) > 1000000):
        log.warn('this operation may take a long time, use sortMassIn_sortNarrowWindow instead')
        return sortMassIn_sortNarrowWindow(peakData, len(uniqBins)/100)
    
    
    sorted_peakdata = sortPeaksByBinWidth(peakData) 
    
    masses = sorted_peakdata[0]
    abunds = sorted_peakdata[1]
    resols = sorted_peakdata[2]
    bins_low = sorted_peakdata[3]
    bins_high = sorted_peakdata[4]
    
    bins = []
    for mass in masses:
        for bin_low, bin_high in uniqBins:
            if mass >= bin_low and mass <= bin_high:
                bins.append((bin_low,bin_high))
                break
    
    if(len(bins) != len(masses)):
        log.error('There was a problem setting masses in bins, please verify bins where created correctly')
    
    peakData = zip(*zip(peakData[0], peakData[1], peakData[2], peakData[3], peakData[4], bins))
    return peakData

def sortMassIn_sortWindow(peakData, window = 200):
    log.debug('sortMassIn_sortWindow, window size %d', window)
    
    peakData_sorted = zip(*sorted(zip(*peakData)))
    
    masses = peakData_sorted[0]
    abunds = peakData_sorted[1]
    resols = peakData_sorted[2]
    bins_low = peakData_sorted[3]
    bins_high = peakData_sorted[4]
    
    bins = []
    for idx, mass in enumerate(masses):
        found = False
        lowidx = 0 if idx < (window / 2) else idx - (window / 2)
        highidx = window + lowidx
        if idx % window == 0: log.debug('at %d of %d', idx, len(masses))
        for bin_low, bin_high in zip(bins_low[lowidx:highidx], bins_high[lowidx:highidx]):
            if mass >= bin_low and mass <= bin_high:
                found = True
                bins.append((bin_low,bin_high))
                break
        if not found:
            log.error('the mass at index %d did not find a bin', idx)
    
    if(len(bins) != len(masses)):
        log.error('There was a problem setting masses in bins, please verify bins where created correctly')
    
    peakData = zip(*zip(peakData[0], peakData[1], peakData[2], peakData[3], peakData[4], bins))
    return peakData

def sortMassIn_sortNarrowWindow(peakData, window = 200):
    log.debug('sortMassIn_sortNarrowWindow, window size %d', window)
    
    peakData_sorted = zip(*sorted(zip(*peakData)))
    
    masses = peakData_sorted[0]
    abunds = peakData_sorted[1]
    resols = peakData_sorted[2]
    bins_low = peakData_sorted[3]
    bins_high = peakData_sorted[4]
    
    bins = []
    for idx, mass in enumerate(masses):
        found = False
        lowidx = 0 if idx < (window / 2) else idx - (window / 2)
        highidx = window + lowidx
        
        #--
        bin_width = [bin_high - bin_low for bin_low, bin_high in zip(peakData_sorted[3][lowidx:highidx], peakData_sorted[4][lowidx:highidx])]
        sorted_peakdata_plus = zip(*sorted(zip(bin_width, peakData_sorted[0][lowidx:highidx],
                                               peakData_sorted[1][lowidx:highidx],
                                               peakData_sorted[2][lowidx:highidx],
                                               peakData_sorted[3][lowidx:highidx],
                                               peakData_sorted[4][lowidx:highidx])))
        sorted_peakdata = sorted_peakdata_plus[1:]
        #--
        
        if idx % window == 0: log.debug('at %d of %d', idx, len(masses))
        for bin_low, bin_high in zip(sorted_peakdata[3], sorted_peakdata[4]):
            if mass >= bin_low and mass <= bin_high:
                found = True
                bins.append((bin_low,bin_high))
                break
        if not found:
            log.error('the mass at index %d did not find a bin', idx)
    
    if(len(bins) != len(masses)):
        log.error('There was a problem setting masses in bins, please verify bins where created correctly')
    
    peakData = zip(*zip(peakData_sorted[0], peakData_sorted[1], peakData_sorted[2], peakData_sorted[3], peakData[4], bins))
    return peakData

'''
aggregate bins
'''
def aggregateBinData(peakData):
    log.debug('aggregateBinData count &d, count, sumZmass, sumAbund', len(peakData))
    masses = peakData[0]
    abunds = peakData[1]
    resols = peakData[2]
    bins_low = peakData[3]
    bins_high = peakData[4] 
    bins = peakData[5]
    bins = dict()
    
    newRow = 0,0.0,0.0 #  count, sumZmass, sumAbund
    for mass, abund, resol, bin_low, bin_high, bin in zip(*peakData):
        count, sumZmass, sumAbund = bins.get(bin, newRow) 
        count +=1
        sumZmass += mass
        sumAbund += abund
        bins[bin] = count, sumZmass, sumAbund 

    log.debug('bin count &d ', len(bins))
    return bins


def filterBins(binData, minRepetitionRate = 0.75):
    log.debug('filterBins count %d ,minRepetitionRate %f',len(binData),minRepetitionRate)
    maxCount = 0
    maxAbunds = 0
    for bin in binData:
        (count, sumZmass, sumAbund) = binData[bin]
        if maxCount < count: maxCount = count
        if maxAbunds <  (sumAbund/count) : maxAbunds = (sumAbund/count)
    
    binData_filtered = {}
    for bin in binData:
        (count, sumZmass, sumAbund) = binData[bin]
        if count >= (maxCount * minRepetitionRate):
            binData_filtered[bin]=(count, sumZmass, sumAbund)
    log.debug('Filter rate %f', len(binData_filtered)/len(binData))
    return binData_filtered
    

def formatPeaks(binData):
    log.debug('formatPeaks into simple list pair, mass and intentisty')
    masses = []
    intens = []
    for bin in binData:
        (count, sumZmass, sumAbund) = binData[bin]
        masses.append(sumZmass/count)
        intens.append(sumAbund/count)
    
    return (masses, intens)


if __name__ == '__main__':
    log.addHandler(logging.StreamHandler()) # log to console
    log.setLevel(logging.DEBUG)
    
    log.debug('Start %f', time.clock())
    if len(sys.argv) == 1:
        print("A filename must be provided")
        raise SystemExit
    
    filename = " ".join(sys.argv[1:])
    scans = ThermoRawfile2Scans(filename)
    
    ''' filtering by scan
    scans = filterScanBy_retentionTime(scans)
    scans = filterScanBy_filterline(scans)
    scans = filterScanBy_samples(scans, step_size = 3)
    '''
    
    #Note: mergePeaksOnFilterline_withRandom to generate testing data
    filterLines = mergePeaksOnFilterline(scans)
     
    preFiltered_filterlines = {k: preliminaryFilter(v) for k, v in filterLines.iteritems()}
    #preFiltered_filterlines = {k: preliminaryReductionFilter(v) for k, v in filterLines.iteritems()}
        
    ''' create bins for peaks
    filterlines_withBins = {k: generateBins_decimalPlaces(v) for k, v in filterLines.iteritems()}
    filterlines_withBins = {k: generateBins_resolution(v) for k, v in filterLines.iteritems()}
    filterlines_withBins = {k: generateBins_theoreticalResolution(v) for k, v in preFiltered_filterlines.iteritems()}
    '''
    filterlines_withBins = {k: generateBins_decimalPlaces(v) for k, v in filterLines.iteritems()}
    
    ''' put each mass in a bin
    filterlines_inBins = {k: sortMassIn_sortWindow(v) for k, v in filterlines_withBins.iteritems()}
    filterlines_inBins = {k: sortMassIn_FirstBin(v) for k, v in filterlines_withBins.iteritems()}
    filterlines_inBins = {k: sortMassIn_NarrowestBin(v) for k, v in filterlines_withBins.iteritems()}
    '''
    filterlines_inBins = {k: sortMassIn_FirstBin(v) for k, v in filterlines_withBins.iteritems()}
    
    filterlines_binData = {k: aggregateBinData(v) for k, v in filterlines_inBins.iteritems()}
    
    filterlines_filtered = {k: filterBins(v) for k, v in filterlines_binData.iteritems()}
    
    filtered_peaks = {k: formatPeaks(v) for k, v in filterlines_filtered.iteritems()}
    
    encoded_peaks = {k: encodePeaks(*v) for k, v in filtered_peaks.iteritems()}
    
    newfilename = filename[:-4]+ '.mzXML'
    writeMzXML(newfilename, filterlines_filtered)
    
    generateCSVreport(scans,filterlines_filtered)
    
    log.debug('finish %f',  time.clock())
    