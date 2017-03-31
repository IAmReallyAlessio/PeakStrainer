'''
Created on 31.03.2017

@author: mirandaa
'''

import argparse
import logging

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
    scanfiltergroup.add_argument('--scanfilter', '-sr',nargs=2, required=False, 
                        help='filterScanBy_retentionTime: -sr 0.0 10000.0 ;lowSeconds=0.5, highSeconds=float("inf")')
    scanfiltergroup.add_argument('--scanfilter', '-sf',nargs=2, required=False, 
                        help='filterScanBy_filterline text: -sf ms False ;subtext =  ms , keep=False')
    scanfiltergroup.add_argument('--scanfilter', '-ss',nargs=1, required=False, 
                        help='filterScanBy_samples eg. 1 out of every 10: -ss 10 ;step_size = 10')
    
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
    sortBinsgroup.add_argument('--inFirstBin', '-i', required=False, 
                        help='sortMassIn_FirstBin')
    sortBinsgroup.add_argument('--inWindowBin', '-iw',nargs=1, required=False, 
                        help='sortMassIn_first bin in Window width 200: -iw 200  window = 200')
    sortBinsgroup.add_argument('--inNarrowBin', '-in', required=False, 
                        help='sortMassIn_NarrowestBin ')
    
    parser.add_argument('output_path', metavar='output_path', type=str, nargs='?', default='.', required=False,
                    help='Path for the output.mzxml file')

    args = parser.parse_args()
    print 'file is {} and csv is {}, logging {}'.format(args.filename, 
                                                        args.generateCSV,
                                                        loglevel(args.verbose))
    print ' Prefilter {}'.format(args.prefilter)

if __name__ == '__main__':
    main()