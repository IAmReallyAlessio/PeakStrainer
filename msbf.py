'''
Created on 31.03.2017

@author: mirandaa
'''

import argparse
import logging
from gooey import Gooey

def loglevel(v_count):
    if v_count is None: return logging.CRITICAL
    if v_count > 4 : return logging.NOTSET
    return [logging.CRITICAL,logging.ERROR,logging.WARN, logging.INFO,logging.DEBUG][v_count] 

@Gooey
def main():
    parser = argparse.ArgumentParser(description='Combine and filter spectra signals to remove random signals')
    parser.add_argument('filename', metavar='thermal-file.raw', type=str, nargs=1,
                    help='the thermal-raw file')
    parser.add_argument('--prefilter', '-p',nargs=3, help='prefilter settings: -p 2 2 0.5 ; decimal_places = 2, minCount = 2, minRepetitionRate = 0.5 ')  
    parser.add_argument('--csv', dest='generateCSV', action='store_true',
                    help='(generate csv report files (default: do not generate)')
    parser.add_argument('--verbose', '-v', action='count',
                        help='(set the logging level (up to -vvvvv)')

    args = parser.parse_args()
    print 'file is {} and csv is {}, logging {}'.format(args.filename, 
                                                        args.generateCSV,
                                                        loglevel(args.verbose))
    print ' Prefilter {}'.format(args.prefilter)

if __name__ == '__main__':
    main()