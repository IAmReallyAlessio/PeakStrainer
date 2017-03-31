'''
Created on 31.03.2017

@author: mirandaa
'''

import argparse
import logging
from msBinFilter import *

def loglevel(v_count):
    if v_count is None: return logging.CRITICAL
    if v_count > 4 : return logging.NOTSET
    return [logging.CRITICAL,logging.ERROR,logging.WARN, logging.INFO,logging.DEBUG][v_count] 

def main():
    parser = argparse.ArgumentParser(description='Combine and filter spectra signals to remove random signals')
    parser.add_argument('filename', metavar='filename', type=str, nargs=1,
                    help='The thermal-raw file')
    
    parser.add_argument('--csv', dest='generateCSV', action='store_true', required=False,
                    help='generate csv report files (default: do not generate)')
    parser.add_argument('--verbose', '-v', action='count', required=False,
                        help='(set the logging level 1-5 (up to -vvvvv)')
    
    scanfiltergroup = parser.add_mutually_exclusive_group()
    scanfiltergroup.add_argument('--filterRetentionTime', '-fr',nargs=2, required=False, 
                        help='filterScanBy_retentionTime: -fr 0.0 10000.0 ;lowSeconds=0.5, highSeconds=float("inf")')
    scanfiltergroup.add_argument('--filterText', '-ft',nargs=2, required=False, 
                        help='filterScanBy_filterline text: -ft ms False ;subtext =  ms , keep=False')
    scanfiltergroup.add_argument('--filterSamples', '-fs',nargs=1, required=False, 
                        help='filterScanBy_samples eg. 1 out of every 10: -fs 10 ;step_size = 10')
    
    prefiltergroup = parser.add_mutually_exclusive_group()
    prefiltergroup.add_argument('--prefilter', '-p',nargs=3, required=False, 
                        help='Default prefilter : -p 2 2 0.5 ;decimal_places=2, minCount=2, minRepetitionRate=0.5')
    prefiltergroup.add_argument('--preliminaryReductionFilter', '-pr',nargs=2, required=False, 
                        help='Reduction settings: -p 0.10 10  reduce to 0.10 of original, minPeaks = 10')
      
    binGenerationgroup = parser.add_mutually_exclusive_group()
    binGenerationgroup.add_argument('--binsDecimal', '-b',nargs=1, required=False, 
                        help='generateBins by decimalPlaces: -b 4  decimal_places = 4')
    binGenerationgroup.add_argument('--binsResolution', '-br',nargs=1, required=False, 
                        help='generateBins by resolution: -br 4  resolutions decimal_places = 4')
    binGenerationgroup.add_argument('--binsTheoResolution', '-bt',nargs=1, required=False, 
                        help='generateBins by theoretical Resolution  -bt 4  resolutions decimal_places = 4')
    
    sortBinsgroup = parser.add_mutually_exclusive_group()
    sortBinsgroup.add_argument('--inFirstBin', '-i', action='store_true', required=False, 
                        help='sortMassIn_FirstBin')
    sortBinsgroup.add_argument('--inWindowBin', '-iw',nargs=1, required=False, 
                        help='sortMassIn_first bin in Window width 200: -iw 200 ;window = 200')
    sortBinsgroup.add_argument('--inNarrowBin', '-in', action='store_true', required=False, 
                        help='sortMassIn_NarrowestBin ')
    
    parser.add_argument('output_path', metavar='output_path', type=str, nargs='?', default='.', 
                    help='Path for the output.mzxml file')

    args = parser.parse_args()
    
    '''
    start application, copy pasta from main in msBinFilter
    '''
    log.setLevel(loglevel(args.verbose))
    if log.level == logging.DEBUG:log.addHandler(logging.StreamHandler()) # log to console
    
    log.debug('Start %f', time.clock())
    
    filename = args.filename[0]
    scans = ThermoRawfile2Scans(filename)
    if args.generateCSV: ThermoRawfile2Scans_csv(scans)
    
    ''' filtering by scan
    scans = filterScanBy_retentionTime(scans)
    scans = filterScanBy_filterline(scans)
    scans = filterScanBy_samples(scans, step_size = 3)
    '''
    
    #Note: mergePeaksOnFilterline_withRandom to generate testing data
    filterLines = mergePeaksOnFilterline(scans)
    if args.generateCSV: filterlinePeaks_csv(filterLines, 'mergePeaksOnFilterline.csv')
    
    preFiltered_filterlines = {k: preliminaryFilter(v) for k, v in filterLines.iteritems()}
    #preFiltered_filterlines = {k: preliminaryReductionFilter(v) for k, v in filterLines.iteritems()}
    if args.generateCSV: filterlinePeaks_csv(preFiltered_filterlines,'preliminaryFilter.csv')    
    
    ''' create bins for peaks
    filterlines_withBins = {k: generateBins_decimalPlaces(v) for k, v in filterLines.iteritems()}
    filterlines_withBins = {k: generateBins_resolution(v) for k, v in filterLines.iteritems()}
    filterlines_withBins = {k: generateBins_theoreticalResolution(v) for k, v in preFiltered_filterlines.iteritems()}
    '''
    filterlines_withBins = {k: generateBins_decimalPlaces(v) for k, v in filterLines.iteritems()}
    if args.generateCSV: filterlinePeaks_csv(filterlines_withBins,'generateBins_decimalPlaces.csv')
    
    ''' put each mass in a bin
    filterlines_inBins = {k: sortMassIn_sortWindow(v) for k, v in filterlines_withBins.iteritems()}
    filterlines_inBins = {k: sortMassIn_FirstBin(v) for k, v in filterlines_withBins.iteritems()}
    filterlines_inBins = {k: sortMassIn_NarrowestBin(v) for k, v in filterlines_withBins.iteritems()}
    '''
    filterlines_inBins = {k: sortMassIn_FirstBin(v) for k, v in filterlines_withBins.iteritems()}
    if args.generateCSV: filterlinePeaks_csv(filterlines_inBins,'sortMassIn_FirstBin.csv')
    
    filterlines_binData = {k: aggregateBinData(v) for k, v in filterlines_inBins.iteritems()}
    if args.generateCSV: filterlineBins_csv(filterlines_binData,'aggregateBinData.csv')
    
    filterlines_filtered = {k: filterBins(v) for k, v in filterlines_binData.iteritems()}
    if args.generateCSV: filterlineBins_csv(filterlines_filtered,'filterBins.csv')
    
    filtered_peaks = {k: formatPeaks(v) for k, v in filterlines_filtered.iteritems()}
    
    newfilename = os.path.abspath(args.output_path) + os.path.basename(filename)[:-4]+ '.mzXML'
    log.info('Writing results to %s', newfilename)
    write2templateMzXML(newfilename, filtered_peaks)
    
    log.debug('finish %f',  time.clock())


if __name__ == '__main__':
    #NOTE: alter the main method in msBinFilter.py instead of setting everything in the command line
    main()