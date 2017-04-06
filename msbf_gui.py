'''
Created on 31.03.2017

@author: mirandaa
'''

import logging
from msBinFilter import *
import configargparse
from lib.mygooey import Gooey, GooeyParser

def loglevel(v_count):
    if v_count is None: return logging.CRITICAL
    if v_count > 4 : return logging.NOTSET
    return [logging.CRITICAL,logging.ERROR,logging.WARN, logging.INFO,logging.DEBUG][v_count] 

@Gooey(program_name="MS Bin Filter",
       dump_build_config=False,   # Dump the JSON Gooey uses to configure itself
       load_build_config=None,    # Loads a JSON Gooey-generated configuration
       default_size=(1080, 1000),
       )
def main():
    parser = GooeyParser(description='MS Bin Filter')
    parser.add_argument('-c', '--my-config', is_config_file=True, help='config file path', widget='FileChooser')
    
    parser.add_argument('filename', metavar='filename', type=str, nargs=1,
                    help='The thermo-raw file',widget='FileChooser')
    
    
    parser.add_argument('--csv', dest='generateCSV', action='store_true', required=False,
                    help='generate csv report files (default: do not generate)')
    parser.add_argument('--verbose', '-v', action='count', required=False, default =1,
                        help='(set the logging level 1-5 (up to -vvvvv)')
    
    scanfiltergroup = parser.add_mutually_exclusive_group()
    scanfiltergroup.add_argument('--filterRetentionTime', '-fr',nargs=2, required=False, 
                        help='filterScanBy_retentionTime: -fr 0.0 10000.0 ;lowSeconds=0.5, highSeconds=float("inf")')
    scanfiltergroup.add_argument('--filterText', '-ft',nargs=2, required=False, 
                        help='filterScanBy_filterline text: -ft ms False ;subtext =  ms , keep=False')
    scanfiltergroup.add_argument('--filterSamples', '-fs',nargs=1, required=False, 
                        help='filterScanBy_samples eg. 1 out of every 10: -fs 10 ;step_size = 10')
    parser.add_argument('--filterArgs', '-fa',nargs='?', required=False, 
                        help='Arguments for the filters ')
    
    prefiltergroup = parser.add_mutually_exclusive_group()
    prefiltergroup.add_argument('--prefilter', '-p',nargs=3, required=False, 
                        help='Default prefilter : -p 2 2 0.5 ;decimal_places=2, minCount=2, minRepetitionRate=0.5')
    prefiltergroup.add_argument('--preliminaryReductionFilter', '-pr',nargs=2, required=False, 
                        help='Reduction settings: -p 0.10 10  reduce to 0.10 of original, minPeaks = 10')
    parser.add_argument('--prefilterArgs', '-pa',nargs='?', required=False, 
                        help='Arguments for the prefilters ')
      
    binGenerationgroup = parser.add_mutually_exclusive_group()
    binGenerationgroup.add_argument('--binsDecimal', '-b',nargs=1, required=False, 
                        help='generateBins by decimalPlaces: -b 4  decimal_places = 4')
    binGenerationgroup.add_argument('--binsResolution', '-br',nargs=1, required=False, 
                        help='generateBins by resolution: -br 4  resolutions decimal_places = 4')
    binGenerationgroup.add_argument('--binsTheoResolution', '-bt',nargs=1, required=False, 
                        help='generateBins by theoretical Resolution  -bt 4  resolutions decimal_places = 4')
    parser.add_argument('--binsArgs', '-ba',nargs='?', required=False, 
                        help='Arguments for the bin creation ')
    
    sortBinsgroup = parser.add_mutually_exclusive_group()
    sortBinsgroup.add_argument('--inFirstBin', '-i', action='store_true', required=False, 
                        help='sortMassIn_FirstBin')
    sortBinsgroup.add_argument('--inWindowBin', '-iw',nargs=1, required=False, 
                        help='sortMassIn_first bin in Window width 200: -iw 200 ;window = 200')
    sortBinsgroup.add_argument('--inNarrowBin', '-in', action='store_true', required=False, 
                        help='sortMassIn_NarrowestBin ')
    parser.add_argument('--sortArgs', '-ia',nargs='?', required=False, 
                        help='Arguments for the sorting in bins')
    
    parser.add_argument('output_path', metavar='output_path', type=str, nargs='?', default='.', 
                    help='Path for the output.mzxml file',widget='DirChooser')

    args = parser.parse_args()
    print(args)
    sys.exit()
        
    '''
    start application, copy pasta from main in msBinFilter
    '''
    log.setLevel(loglevel(args.verbose))
    if log.level == logging.DEBUG:log.addHandler(logging.StreamHandler()) # log to console
    
    log.debug('Start %f', time.clock())
    
    filename = args.filename[0]
    scans = ThermoRawfile2Scans(filename)
    if args.generateCSV: ThermoRawfile2Scans_csv(scans)
    
    ''' filtering by scan '''
    if args.filterRetentionTime: scans = filterScanBy_retentionTime(scans, float(args.filterArgs[0]), 
                                                                   float(args.filterArgs[1]))
    if args.filterText: scans = filterScanBy_filterline(scans, args.filterText[0], args.filterArgs[1]!='False')
    if args.filterSamples: scans = filterScanBy_samples(scans, int(args.filterArgs[0]))
    
    scans = list(scans)
    #Note: mergePeaksOnFilterline_withRandom to generate testing data
    filterLines = mergePeaksOnFilterline(scans)
    if args.generateCSV: filterlinePeaks_csv(filterLines, 'mergePeaksOnFilterline.csv')
    
    if args.prefilter: preFiltered_filterlines = {k: preliminaryFilter(v,
                                                                       int(args.prefilterArgs[0]),
                                                                       int(args.prefilterArgs[1]),
                                                                       float(args.prefilterArgs[2])) for k, v in filterLines.iteritems()}
    if  args.preliminaryReductionFilter: preFiltered_filterlines = {k: preliminaryReductionFilter(v,
                                                                                                  float(args.prefilterArgs[0]),
                                                                                                  int(args.prefilterArgs[1])) for k, v in filterLines.iteritems()}
    if not args.prefilter and not args.preliminaryReductionFilter: 
        preFiltered_filterlines = {k: preliminaryFilter(v) for k, v in filterLines.iteritems()}
    if args.generateCSV: filterlinePeaks_csv(preFiltered_filterlines,'preliminaryFilter.csv')    
    
    ''' create bins for peaks '''
    if args.binsDecimal:filterlines_withBins = {k: generateBins_decimalPlaces(v,
                                                                              int(args.binsArgs[0])) for k, v in filterLines.iteritems()}
    if args.binsResolution:filterlines_withBins = {k: generateBins_resolution(v,
                                                                              int(args.binsArgs[0])) for k, v in filterLines.iteritems()}
    if args.binsTheoResolution:filterlines_withBins = {k: generateBins_theoreticalResolution(v,
                                                                                             int(args.binsArgs[0])) for k, v in preFiltered_filterlines.iteritems()}
    if not args.binsDecimal and not args.binsResolution and not args.binsTheoResolution:
        filterlines_withBins = {k: generateBins_decimalPlaces(v) for k, v in filterLines.iteritems()}
    if args.generateCSV: filterlinePeaks_csv(filterlines_withBins,'generateBins_decimalPlaces.csv')
    
    ''' put each mass in a bin '''
    if args.inWindowBin:filterlines_inBins = {k: sortMassIn_sortWindow(v,
                                                                       int(args.sortArgs[0])) for k, v in filterlines_withBins.iteritems()}
    if args.inFirstBin:filterlines_inBins = {k: sortMassIn_FirstBin(v) for k, v in filterlines_withBins.iteritems()}
    if args.inNarrowBin:filterlines_inBins = {k: sortMassIn_NarrowestBin(v) for k, v in filterlines_withBins.iteritems()}
    if not args.inWindowBin and not args.inFirstBin and not args.inNarrowBin:
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