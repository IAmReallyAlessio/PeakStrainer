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
    
    
    prefiltergroup = parser.add_mutually_exclusive_group()
    prefiltergroup.add_argument('--prefilter', '-p',nargs=3, required=False, 
                        help='Default prefilter settings: -p 2 2 0.5  decimal_places=2, minCount=2, minRepetitionRate=0.5')
    prefiltergroup.add_argument('--preliminaryReductionFilter', '-pr',nargs=2, required=False, 
                        help='Reduction settings: -p 0.10 10  reduce to 0.10 of original, minPeaks = 10')
      
    binGenerationgroup = parser.add_mutually_exclusive_group()
    binGenerationgroup.add_argument('--binsDecimal', '-b',nargs=3, required=False, 
                        help='generateBins  by decimalPlaces settings: -b 4  decimal_places = 4')
    binGenerationgroup.add_argument('--binsResolution', '-br',nargs=3, required=False, 
                        help='generateBins by resolution settings: -br 4  resolutions decimal_places = 4')
    binGenerationgroup.add_argument('--binsTheoResolution', '-bt',nargs=3, required=False, 
                        help='generateBins by theoretical Resolution settings: -bt 4  resolutions decimal_places = 4')
    

    args = parser.parse_args()
    print 'file is {} and csv is {}, logging {}'.format(args.filename, 
                                                        args.generateCSV,
                                                        loglevel(args.verbose))
    print ' Prefilter {}'.format(args.prefilter)

if __name__ == '__main__':
    main()