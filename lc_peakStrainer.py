#!/bin/env python2.7
# encoding: utf-8
'''
Created on 29.03.2017
lc_PeakStrainer is a tool to reduce the size of lc MS spectra,
usage: lc_peakStrainer spectra_file.raw
@author: mirandaa
'''
import sys
import os
import time
import logging
import csv
from utils.peakStrainer_util import write2templateMzXML, generatePsudoMGF
import itertools
import math
from collections import namedtuple
log = logging.getLogger(os.path.basename(__file__))
from lib import MSFileReader
import numpy as np
import pandas as pd

__version__ = "17.07.03.0"
            
#@profile for line_profiler 2.0, see https://psteinb.github.io/hpc-in-a-day/
def main(file, validate =False):
    log.setLevel(logging.DEBUG)
    if log.level == logging.DEBUG:log.addHandler(logging.StreamHandler()) # log to console
    if log.level == logging.DEBUG:logging.basicConfig(filename='lcpeakStrainer.log',filemode='w')
    
    log.debug('Start %f', time.clock())
    
    filename = file #" ".join(sys.argv[1:])
    scansDF, peaksDF = ThermoRawfile2DataFrames(filename)
    
    lastMS = None
    secondLastMS = None
    thirdLastMS = None
#     TODO use recusrion because this is silly
    tmpMSList = []
    tmpMSList2 = []
    tmpMSList3 = []
    
    for row in scansDF.itertuples():
        if ' ms ' in row.filterLine:
            tmpMSList.append(None)
            tmpMSList2.append(None)
            tmpMSList3.append(None)
            thirdLastMS = secondLastMS 
            secondLastMS = lastMS
            lastMS = row.scanNum
             
        else:
            tmpMSList.append(lastMS)
            tmpMSList2.append(secondLastMS)
            tmpMSList3.append(thirdLastMS)
            
            
    scansDF['LastMS'] = tmpMSList
    scansDF['LastMS2'] = tmpMSList2
    scansDF['LastMS3'] = tmpMSList3
    
    scansDF['targetPeak'] = scansDF.filterLine.str.extract(' ms2 (.*)@')
    
    ms2TriggerPeaks = scansDF[~scansDF.targetPeak.isnull()]
 
    trigerPeaksList=[]
    trigerPeaksList2=[]
    trigerPeaksList3=[]
    twoOfThreePass = []
    minDistance = 0.01
    ms2ScanNum = []
    for row in ms2TriggerPeaks.itertuples():
    # find the peak in the scan
        targetPeak = float(row.targetPeak)
        peaks1 =  peaksDF.loc[row.LastMS]
        peaks2 =  peaksDF.loc[row.LastMS2]
        peaks3 =  peaksDF.loc[row.LastMS3]
        
        peaks1['toTarget'] = peaks1.mass - targetPeak
        peaks1['toTarget'] = peaks1['toTarget'].abs()
        min = peaks1['toTarget'].min()  
        closest = peaks1[peaks1['toTarget'] == min]

        peaks2['toTarget'] = peaks2.mass - targetPeak
        peaks2['toTarget'] = peaks2['toTarget'].abs()
        min2 = peaks2['toTarget'].min()  
        closest2 = peaks2[peaks2['toTarget'] == min2]
                
        peaks3['toTarget'] = peaks3.mass - targetPeak
        peaks3['toTarget'] = peaks3['toTarget'].abs()
        min3 = peaks3['toTarget'].min()  
        closest3 = peaks3[peaks3['toTarget'] == min3]
        
        trigerPeaksList.append(closest)
        trigerPeaksList2.append(closest2)
        trigerPeaksList3.append(closest3)
        count = 0
        if min < minDistance : count += 1
        if min2 < minDistance : count += 1
        if min3 < minDistance : count += 1
        
        twoOfThreePass.append(count >= 2)
        ms2ScanNum.append(row.scanNum)
        print str(row.scanNum) +' pass '+ str(count >= 2)
    
    trigerPeaks = pd.concat(trigerPeaksList)
    trigerPeaks2 = pd.concat(trigerPeaksList2)
    trigerPeaks3 = pd.concat(trigerPeaksList3)
    #are these in the filtered results?
    trigerPeaks['twoOfTree']=twoOfThreePass
    trigerPeaks['ms2ScanNum']=ms2ScanNum
    trigerPeaks['toTarget2'] = trigerPeaks2['toTarget'].tolist()
    trigerPeaks['secondMS'] = trigerPeaks2.index.tolist()
    
    trigerPeaks['toTarget3'] = trigerPeaks3['toTarget'].tolist()
    trigerPeaks['thirdMS'] = trigerPeaks3.index.tolist()
    
    if log.level == logging.DEBUG: scansDF.to_csv('msScans.csv') 
    
    #generate allscans and selectscans
    allScans = {}
    selectScans = {}
    unselectedScan ={}
    for row in trigerPeaks.itertuples():
        scanN = row.ms2ScanNum
        filterLine = scansDF.loc[scanN].filterLine
        charge  = int(row.charge)
        masses = peaksDF.loc[scanN]['mass'].tolist()
        intens = peaksDF.loc[scanN]['intensity'].tolist()
        
        if not isinstance(masses, list):
            masses = [masses] # because if there is one element its not a list
        if not isinstance(intens, list): 
            intens = [intens] 
        
        
        header  = '{} {} {}'.format(scanN, filterLine, charge)
        allScans[header] = masses,intens
        if row.twoOfTree : selectScans[header] = (masses,intens)
        else: unselectedScan[header] = (masses,intens)
        
    
    generatePsudoMGF(filename[:-4]+ '-og.mgf', allScans)
    generatePsudoMGF(filename[:-4]+ '-s.mgf', selectScans)
    generatePsudoMGF(filename[:-4]+ '-us.mgf', unselectedScan)
    
    return



    # uniq filterlines
    uniqFilterlines = scansDF.filterLine.unique()
    
    batchSize = 3 # scans
    log.info('size off scan groups {}'.format(batchSize))
    maxDuration = 10 # seconds
    log.info('max time between scans to be grouped {}'.format(maxDuration))
    maxGap = 0.001 # max distance between peak to still be the same
    log.info('max distance between peaks before thes are counted as same {}'.format(maxGap))
    
    filteredmass = []
    filteredintensity = []
    filtered_scans = {}
    for uniqFilterline in uniqFilterlines:
        # scans with uniq filterline
        filterline1DF = scansDF[scansDF.filterLine == uniqFilterline]
        
        for scanTuple in filterline1DF.itertuples():
        
            base = filterline1DF.loc[scanTuple.Index] 
            
            batch = filterline1DF[(filterline1DF.retTime < base.retTime + maxDuration) & (filterline1DF.scanNum >= base.scanNum) ].head(batchSize)
            
            scanPeaks = None
            if validate:
                for idx, scan in batch.iterrows():
                    scanPeaks = peaksDF.loc[scan.scanNum]
                    if scanPeaks.mass.diff(1).min() < maxGap:
                        log.error('peaks are too close in single scan {}, make maxGap larger!'.format(scan.scanNum))
                        log.error('code does not filter for uniq peaks, so these peaks in one scan will binIdx as two, distance {} '.format(scanPeaks.mass.diff(1).min()))
            
            batchPeaks = batch.join(peaksDF)
            batchPeaks.sort_values(by='mass', inplace=True)
            

            batchPeaks['gap'] = batchPeaks.mass.diff(1)# gives difference between current rown and previos
            
            batchPeaks['isSmallGap'] = batchPeaks['gap'] < maxGap
            
            bins = []
            binIdx = 0
            for isSmallGap in batchPeaks.isSmallGap:
                if isSmallGap: # its the same group
                    bins.append(binIdx)
                else:
                    binIdx += 1
                    bins.append(binIdx)
                
            batchPeaks['bin'] = bins
            batchPeaks['freq'] = batchPeaks.groupby('bin')['bin'].transform('count')     
            filtered = batchPeaks[(batchPeaks.freq != 1) & (batchPeaks.scanNum == batch.scanNum.median())] #dont keep all the peaks from all the scans, only the ones from the center scan
            # this will sacrifice the first and last scan but it avoids duplicate peaks in filtered scans,
            # first scan is not trusted anyway, because its first and things not really setup
            
            log.info('filtered {} of {}'.format(filtered.__len__(), batchPeaks.__len__()))
            
            if not filtered.empty : # dont add empties
                header = filtered.filterLine.unique()[0] + batchPeaks.scanNum.unique().tolist().__str__().replace(',', ';')
                filtered_scans[header]= (filtered.mass, filtered.intensity)
                if ' ms ' in header:
                    filteredmass.extend(filtered.mass)
                    filteredintensity.extend(filtered.intensity)
                    print filtered.filterLine.unique()[0]
                
             
        #---end scans
    #----end filterlines


    newfilename = filename[:-4]+ '-f.mzxml'
    log.info('Writing results to %s', newfilename)
    write2templateMzXML(newfilename, filtered_scans)

    generatePsudoMGF(filename[:-4]+ '-f.mgf', filtered_scans)
     
    log.debug('finish %f',  time.clock())
     
    return    
    
    

def ThermoRawfile2DataFrames(file_path, head = None):
    # NOTE: for testing use ThermoRawfile2Scans_sample instead
    log.info('file: %s', file_path)
    rawfile = MSFileReader.ThermoRawfile(file_path)
    
    start = rawfile.FirstSpectrumNumber
    end = rawfile.GetLastSpectrumNumber() if head == None else head
 
    MSrawscansDF = pd.DataFrame(index = np.arange(start, end+1),columns=['scanNum', 'filterLine', 'retTime', 'chargeState', 'isolationMass'])
    peak_datasDF_list =[]
    startTime = time.time()
    for scanNum in np.arange(start, end+1):
        filterLine = rawfile.GetFilterForScanNum(scanNum)
        peak_datas = rawfile.GetLabelData(scanNum)[0]
        retTime =  rawfile.RTFromScanNum(scanNum)*60
        chargeState= rawfile.GetTrailerExtraForScanNum(scanNum)['Charge State']
        isolationMass = rawfile.GetPrecursorInfoFromScanNum(scanNum).isolationMass if  rawfile.GetPrecursorInfoFromScanNum(scanNum) is not None else 0.0# or monoIsoMass
        row = [scanNum, filterLine, retTime, chargeState, isolationMass]
        MSrawscansDF.loc[scanNum] = row
        peak_datasT = zip(*peak_datas)
        peak_datasDF = pd.DataFrame(peak_datasT, index = [scanNum]*len(peak_datasT), columns=['mass', 'intensity', 'resolution', 'baseline', 'noise', 'charge'])
        peak_datasDF_list.append(peak_datasDF)
    MSPeakDatasDF=pd.concat(peak_datasDF_list) # concat is expensive so just once
    log.info('File Read time %f s', time.time()-startTime)
    log.info('Scan Count is %d', len(MSrawscansDF))
    
    return MSrawscansDF, MSPeakDatasDF


def ThermoRawfile2Scans_csv(scans, filename='ThermoRawfile2DataFrame.csv'):
    with open(filename, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(('scanNum', 'filterLine', 'retTime', 'charge state','row', 'isolationMass'))
        for scan in scans:
            (scanNum, filterLine, peak_datas, retTime, chargeState, isolationMass) = scan
#             for row in zip(*peak_datas):
#                 line = (scanNum, filterLine, retTime, chargeState, isolationMass) + row
            writer.writerow((scanNum, filterLine, retTime, chargeState, isolationMass))

'''
Filter on scans
'''
                
def filterScanBy_first(scans, n = 1):
    log.info('filterScanBy_first %d scans', n)
    
    return scans[n:]
    
def filterScanBy_retentionTime(scans, lowSeconds=0.5, highSeconds=float("inf")):
    log.info('filterScanBy_retentionTime %f to %f', lowSeconds, highSeconds)
    result = []
    for row in scans:
        scanNum, filterLine, peak_datas, retTime , chargeState, isolationMass = row 
        if retTime >+ lowSeconds and  retTime <= highSeconds:
            result.append(row)
    return result
    

def filterScanBy_filterline(scans, subtext = ' ms ', keep=False):
    log.info('filterScanBy_filterline %s filter keep: %s', subtext, keep)
    result=[]
    for row in scans:
        scanNum, filterLine, peak_datas, retTime , chargeState, isolationMass= row 
        if keep:
            if (subtext in filterLine):
                result.append(row)
        else: #not keep
            if (subtext not in filterLine):
                result.append(row)
    return result

def filterScanBy_samples(scans, step_size = 10):
    log.info('filterScanBy_samples step_size %d', step_size)
    result = []
    for idx, row in enumerate(scans):
        if idx %  step_size == 0:
            result.append(row)
    return result

'''
merge peaks and coarse grained filtering 
'''
def mergePeaksOnFilterline(scans):
    log.info('Merging %d scans' , len(scans))
    
    def strCombine(filterLine, chargeState):
        return str(filterLine)+' '+'{0:.0f}'.format(chargeState)
    
    filterLines = set([strCombine(filterLine, chargeState) for scanNo, filterLine, peakData, retTime , chargeState, isolationMass in scans])
    log.info('found %d uniqe filterlines', len(filterLines))
    
    # create dict
    mergedPeaks = {}
    for filterLine in filterLines:
        mergedPeaks[filterLine]=([],[],[])
        
#     populate dict
    for scanNo, filterLineOG, peakData, retTime , chargeState, isolationMass in scans:
        (zmass, abunds, resols, baseline , noise, charge) = peakData
        filterLine = strCombine(filterLineOG, chargeState)
        mergedPeaks[filterLine][0].extend(zmass)
        mergedPeaks[filterLine][1].extend(abunds)
        mergedPeaks[filterLine][2].extend(resols)
    
    return mergedPeaks

def filterlinePeaks_csv(mergedPeaks, filename = 'filterlinePeaks.csv'):
    with open(filename, "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(('Scan','Row data'))
            for scan in mergedPeaks:
                peak_data = mergedPeaks[scan]
                for row in zip(*peak_data):
                    line = (scan,) + row
                    writer.writerow(line)

def preliminaryFilter(peakData, decimal_places = 2, minCount = 2, minRepetitionRate = 0.0):
    log.debug('preliminaryFilter rounding to decimal_places %d, minCount = %d, minRepetitionRate %f',  decimal_places, minCount, minRepetitionRate)
    masses = peakData[0]
    log.debug('initial peak count %d',len(masses))
    
    halfdec = (10 ** -decimal_places)/2
    
    # bins plus round up and round down to catch the edge cases of close to top or close to bottom of bin
    # eg  123.104 round = 123.10 up=123.11 down= 123.10
    #     123.106 round = 123.11 up=123.11 down= 123.10
    #     by counting the bins from round up and down we get a bin count
    #     123.10 : 3 and 123.11 : 3 
    # for peaks with no adjacent bins the peak count is 2
    
    rounddown = [round(mass-halfdec, decimal_places) for mass in masses]
    roundeds = [round(mass, decimal_places) for mass in masses]
    roundup = [round(mass+halfdec, decimal_places) for mass in masses]
    
    bins = dict()
    for rounded in roundeds:
        bins[rounded] = bins.get(rounded, 0) + 1
    
    for rounded in roundup:
        bins[rounded] = bins.get(rounded, 0) + 1
    
    for rounded in rounddown:
        bins[rounded] = bins.get(rounded, 0) + 1
    
    log.debug('Prelimianry groups count %d', len(bins))
    minCount_bin = {bin:(count/3)+1 for bin,count in bins.iteritems() if (count/3)+1 > minCount}
    log.debug('groups with minCount %d: %d', minCount,len(minCount_bin))
    minCount_bin_max = float(max(minCount_bin.values())) if len(minCount_bin) is not 0 else 0 
    minRepetitionRate_bin = {bin:count for bin,count in minCount_bin.iteritems() if (count/minCount_bin_max) > minRepetitionRate }
    sorted_minRepetitionRate_bin = minRepetitionRate_bin.keys()
    sorted_minRepetitionRate_bin.sort()
    np_minRepetitionRate_bin = np.array(sorted_minRepetitionRate_bin)
    np_roundeds = np.array(roundeds)
    log.debug('groups with minRepetitionRate %f: %d', minRepetitionRate,len(minRepetitionRate_bin))
    
    
#     -------------------
    start = time.time()     
#     preFilterPass = [rounded in sorted_minRepetitionRate_bin for rounded in roundeds] # this is the bottle neck
    preFilterPass = np.in1d(np_roundeds, np_minRepetitionRate_bin)
    for e in preFilterPass:
        if e is True:
            print  preFilterPass
    
    log.debug(time.time()-start)
#     -------------------

    
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
    
    peakData = (peakData[0], peakData[1], peakData[2], bins_low, bins_high)
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
    halfWidth= (10**-decimal_places)/2
    bins_low = [round(mass-halfWidth,decimal_places ) for mass in bins_low]
    bins_high = [round(mass+halfWidth,decimal_places ) for mass in bins_high]
    
    peakData = (peakData[0], peakData[1], peakData[2], bins_low, bins_high)
    return peakData

def peakWidth_at_hight(abunds, highth = 0.95):
    ''' Note:
    for future implementation
    assuming that the peak has a gausian curve,
    and that the resols is full width at half maximum, fwhm
    and given the equation in wikipedia for fwhm
    
    the formula for the full width at an abritary height between [0,1]
    
    is width = 2 * sqrt(abund**2 * log(hight) / (-4*log(2))) 
    
    '''
    def widthAtHight(fwhm , normHight ):
        return 2 * math.sqrt(fwhm**2 * math.log(normHight) / (-4*math.log(2)))
    
    return [widthAtHight(abund, highth) for abund in abunds]
    
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
    
    sort_mass = sorted(zip(abunds, masses, resols))#filter on intensity
        # 5408000.0, 2096000.0
    select_abunds, select_masses, select_resols = zip(*sort_mass)
    log.debug('Selecting only 90% highest intensity, as per Kai S.')
    side_len = len(select_masses) / 10
    popt, pconv = curve_fit(func, select_masses[side_len:], select_resols[side_len:])
    
    log.info('function a*(x**-b) uses values: mass, %f, %f ', popt[0], popt[1])
        
    theoResols = [func(mass, *popt) for mass in masses]
    
    bins_high = [mass + ((mass/resol)/2) for mass, resol in zip(masses,theoResols)] 
    bins_low =  [mass - ((mass/resol)/2) for mass, resol in zip(masses,theoResols)]
     # rounding to make bins larger
    halfWidth= (10**-decimal_places)/2
    bins_low = [round(mass-halfWidth,decimal_places ) for mass in bins_low]
    bins_high = [round(mass+halfWidth,decimal_places ) for mass in bins_high]
    
    
    peakData = (peakData[0], peakData[1], peakData[2], bins_low, bins_high)
    return peakData

def generateBins_resolutionPowerFunc(peakData, a = 1.0, minus_b = 1.0, decimal_places = 4):
    log.debug('generateBins_resolutionPowerFunc, mass +- res_func, res_func = a*(mass**-b), a= %f, b = %f',a, minus_b  )
    masses = peakData[0]
    log.debug('generateBins_resolutionPowerFunc, peak count %d', len(masses))
    
    def func(x, a, b):
        return  a*(x**-b)
    
    popt = (a, minus_b) 
    
    log.info('function a*(x**-b) uses values: mass, %f, %f ', popt[0], popt[1])
        
    theoResols = [func(mass, *popt) for mass in masses]
    
    bins_high = [mass + ((mass/resol)/2) for mass, resol in zip(masses,theoResols)] 
    bins_low =  [mass - ((mass/resol)/2) for mass, resol in zip(masses,theoResols)]
     # rounding to make bins larger
    halfWidth= (10**-decimal_places)/2
    bins_low = [round(mass-halfWidth,decimal_places ) for mass in bins_low]
    bins_high = [round(mass+halfWidth,decimal_places ) for mass in bins_high]
    
    
    peakData = (peakData[0], peakData[1], peakData[2], bins_low, bins_high)
    return peakData

def generateBins_theoreticalIntensity(peakData, decimal_places = 4):
    log.debug('generateBins_theoreticalIntensity, decimal_places %d',  decimal_places)
    masses = peakData[0]
    abunds = peakData[1]
    resols = peakData[2]
    log.debug('generateBins_theoreticalResolution, peak count %d', len(masses))
    
    log.info('curve fitting to generate theoreticalResolution')
    from scipy.optimize import curve_fit
    def func(x, a, b):
        return  a*(x**-b)
    
    sort_mass = sorted(zip(masses, abunds))
    
    select_masses, select_resols = zip(*sort_mass)
    log.debug('Selecting only middle of distribution, as per Kai S.')
    side_len = len(select_masses) / 15
    popt, pconv = curve_fit(func, select_masses[side_len:-side_len], select_resols[side_len:-side_len])
    
    log.info('function a*(x**-b) uses values: mass, %f, %f ', popt[0], popt[1])
        
    theoResols = [func(mass, *popt) for mass in masses]
    
    bins_high = [mass + ((mass/resol)/2) for mass, resol in zip(masses,theoResols)] 
    bins_low =  [mass - ((mass/resol)/2) for mass, resol in zip(masses,theoResols)]
     # rounding to make bins larger
    halfWidth= (10**-decimal_places)/2
    bins_low = [round(mass-halfWidth,decimal_places ) for mass in bins_low]
    bins_high = [round(mass+halfWidth,decimal_places ) for mass in bins_high]
    
    
    peakData = (peakData[0], peakData[1], peakData[2], bins_low, bins_high)
    return peakData

def alterBins_mergeOverlap(peakData):
    log.debug('alterBins_mergeOverlap')
    
    
    sortedPeakData = zip(*sorted(zip(*peakData)))
    masses =    list(sortedPeakData[0])
    abunds =    list(sortedPeakData[1])
    resols =    list(sortedPeakData[2])
    bins_low =  list(sortedPeakData[3])
    bins_high = list(sortedPeakData[4])
    
    while True: #bubble check
        changeCount = 0
        for idx, _ in enumerate(bins_high):
            if idx >= len(bins_high)-1 : continue 
            low = bins_low[idx]
            high = bins_high[idx]
            nextLow = bins_low[idx+1]
            nexthigh = bins_high[idx+1]
            
            if low== nextLow and high == nexthigh : continue # already updated
                        
            if high > nextLow:
                newHigh = max(nexthigh, high)
                newLow = min(nextLow, low)
                
                bins_high[idx] = newHigh
                bins_high[idx+1] = newHigh
                bins_low[idx] = newLow
                bins_low[idx+1] = newLow
                    
                changeCount += 1
        log.debug('merged %d pairs of bins', changeCount)
        if changeCount == 0 : break
                
    peakData = (masses, abunds, resols, bins_low, bins_high)
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
        log.debug('this operation may take a long time, use sortMassIn_sortWindow instead')
        return sortMassIn_sortWindow(peakData,len(uniqBins)/100)
    bins = []
    for mass in masses:
        inbin =False
        for bin_low, bin_high in uniqBins:
            if mass >= bin_low and mass <= bin_high:
                bins.append((bin_low,bin_high))
                inbin = True
                break
        if not inbin:
            print 'error'
            
    
    if(len(bins) != len(masses)):
        log.error('There was a problem setting masses in bins, please verify bins where created correctly')
        raise RuntimeError('There was a problem setting masses in bins, please verify bins where created correctly')
    
    peakData = (peakData[0], peakData[1], peakData[2], peakData[3], peakData[4], bins)
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
        log.debug('this operation may take a long time, use sortMassIn_sortNarrowWindow instead')
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
    
    peakData = (peakData[0], peakData[1], peakData[2], peakData[3], peakData[4], bins)
    return peakData

def sortMassIn_sortWindow(peakData, window = 200):
    if window > 200 : window = 200  
    log.debug('sortMassIn_sortWindow, window size %d', window)
    
    peakData_sorted = zip(*sorted(zip(*peakData)))
    
    masses = peakData_sorted[0]
    abunds = peakData_sorted[1]
    resols = peakData_sorted[2]
    bins_low = peakData_sorted[3]
    bins_high = peakData_sorted[4]
    
    tryAgain =True
    
    while tryAgain:
        tryAgain = False
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
                log.error('the mass at index %d did not find a bin, window size %d', idx, window)
                window = window * 2
                log.error('change window size to %d', window)
                tryAgain =True
                break
    
    if(len(bins) != len(masses)):
        log.error('There was a problem setting masses in bins, please verify bins where created correctly, and window size')
    
    peakData = (peakData[0], peakData[1], peakData[2], peakData[3], peakData[4], bins)
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
    
    peakData = (peakData_sorted[0], peakData_sorted[1], peakData_sorted[2], peakData_sorted[3], peakData[4], bins)
    return peakData

'''
aggregate bins
'''
def aggregateBinData(peakData):
    log.debug('aggregateBinData count %d, count, sumZmass, sumAbund', len(peakData))
    masses = peakData[0]
    abunds = peakData[1]
    resols = peakData[2]
    bins_low = peakData[3]
    bins_high = peakData[4] 
    bins = peakData[5]
    binsData = dict()
    
    newRow = 0,0.0,0.0 #  count, sumZmass, sumAbund
    for mass, abund, resol, bin_low, bin_high, bin in zip(*peakData):
        count, sumZmass, sumAbund = binsData.get(bin, newRow) 
        count +=1
        sumZmass += mass
        sumAbund += abund
        binsData[bin] = count, sumZmass, sumAbund 

    log.debug('bin count %d ', len(binsData))
    return binsData

def filterlineBins_csv(filterlineBins, filename = 'filterlineBins.csv'):
    with open(filename, "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(('filterline','binLow', 'binH','row data'))
            for filterline in filterlineBins:
                binsdata = filterlineBins[filterline]
                for bin in binsdata:
                    row = binsdata[bin]
                    line = (filterline,)+ bin + row
                    writer.writerow(line)
                   

def getMaxCount(binData, disregardBottom = 0.10):
    maxCount = 0
    maxAbunds = 0
    for bin in binData:
        count, sumZmass, sumAbund = binData[bin]
        if maxAbunds < (sumAbund / count):
            maxAbunds = sumAbund / count
    
    abundsCutoff = maxAbunds * disregardBottom
    log.debug('bins with average intensity lower than %f are not evaluated to establish min repetition rate', abundsCutoff)
    for bin in binData:
        count, sumZmass, sumAbund = binData[bin]
        if (sumAbund / count) < abundsCutoff: continue  # dont consider the
        if maxCount < count:
            maxCount = count
    
    log.debug('Max peak count is %d, for bins with average abundance above %f ', maxCount, abundsCutoff)
    return maxCount

def filterBins(binData, minRepetitionRate = 0.70, decimal_places = 4, disregardBottom= 0.10):
    decimal = (10 ** -decimal_places)
    log.debug('filterBins count %d ,minRepetitionRate %f, decimal places %d, %f, desrigarding bottom %f percent',len(binData),minRepetitionRate, decimal_places, decimal, disregardBottom)
    if disregardBottom >= 1 : raise RuntimeError('disregardBottom can not be more than 1')
    maxCount = getMaxCount(binData, disregardBottom)
    
    bintable = [(k + binData[k]) for k in binData]
    sortedBintable = sorted(bintable)
    #TODO this code is fishy , refactor
    binData_filtered = {}
#     for bin in binData:
    for idx, row in enumerate(sortedBintable):
        bin = row[0:2]
        (count, sumZmass, sumAbund) = row[2:]
        if count >= (maxCount * minRepetitionRate):
            binData_filtered[bin]=(count, sumZmass, sumAbund)
        
        if idx+1 >= len(sortedBintable): continue
            
        nextrow = sortedBintable[idx+1]  
        # test edge cases
        if abs(nextrow[0]-row[1])<decimal : # row highbin is adjecent nextrow lowbin
            if  row[2]+nextrow[2]>= (maxCount * minRepetitionRate):
                binData_filtered[bin]=(count, sumZmass, sumAbund)
                binData_filtered[nextrow[0:2]]=nextrow[2:]

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

def bins2Peaks(binsData, peakData):
    log.debug('bins2Peaks get all the peaks with given bin, into simple list pair, mass and intentisty')
    bins_filtered = binsData.keys()
    masses = peakData[0]
    abunds = peakData[1]
    resols = peakData[2]
    bins_low = peakData[3]
    bins_high = peakData[4] 
    bins = peakData[5]
    
    filteredRowdata = [(row[0], row[1]) for row in zip(*peakData) if row[5] in bins_filtered]
    result = zip(*filteredRowdata)
    return result
    


if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        print("A filename must be provided")
        raise SystemExit
    
    filename = " ".join(sys.argv[1:])
    
    for file in sys.argv[1:]:
        main(file)