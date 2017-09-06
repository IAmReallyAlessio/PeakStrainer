'''
Created on 16.08.2017

@author: mirandaa
'''
import time
import os
import logging
log = logging.getLogger(os.path.basename(__file__))
import pickle

import numpy as np
import pandas as pd

from lib import MSFileReader
from utils.peakStrainer_util import generatePsudoMGF 

def main(isolation_dist = 0.01):
    print('find ms2 scans')
    filename = r'C:\apps\eclipseRCP\workspace\PeakStrainer\tmp\qc_02_QC04_.raw'
#     scansDF, peaksDF = ThermoRawfile2DataFrames(filename)
#     scansDF.to_pickle('scansDF.pkl')
#     peaksDF.to_pickle('peaksDF.pkl')
#  # or DataFrame.to_hdf
        
    scansDF = pd.read_pickle('scansDF.pkl')
    peaksDF = pd.read_pickle('peaksDF.pkl')
    scansDF = scansDF[(scansDF.filterLine.str.contains(' ms2 '))]
      
    print('get repeated min 10 times')
    scansDF['count'] = scansDF.groupby('filterLine')['filterLine'].transform('count')
    selectFilterLines = scansDF[scansDF['count'] >= 10]['filterLine'].unique()
    
    print(' get description of non-repeating peaks')
#     selectPeaksList=[]
#     for idx, selectFilterLine in np.ndenumerate(selectFilterLines):
#         selectScanNums = scansDF[scansDF['filterLine'] == selectFilterLine]['scanNum']
#         selectPeaks = peaksDF.loc[selectScanNums]
#         selectPeaks.sort_values('mass',inplace=True)
#         selectPeaks['diff'] = selectPeaks['mass'].diff()  
#         selectPeaks['diff1'] = selectPeaks['diff'].shift(-1) 
#         selectPeaks['isolated'] = (selectPeaks['diff'] > isolation_dist) & (selectPeaks['diff1'] > isolation_dist)
#         selectPeaksList.append(selectPeaks)
#     selectPeaksDF = pd.concat(selectPeaksList)
    selectPeaksDF = pd.read_pickle('selectPeaks10DF.pkl')
   
    print(' get description of repeating peaks')
    selectPeaksDF[selectPeaksDF['isolated']].describe()
    selectPeaksDF[~selectPeaksDF['isolated']].describe()
    
    print('find descriminanat')
    selectPeaksDF['scanNum'] = selectPeaksDF.index
    selectPeaksDF['TIC'] = selectPeaksDF.groupby('scanNum')['intensity'].transform('sum')
#     selectPeaksDF['min_i'] = selectPeaksDF.groupby(['scanNum','isolated'])['intensity'].transform('min')
    selectPeaksDF['max_i'] = selectPeaksDF.groupby(['scanNum','isolated'])['intensity'].transform('max')
#     selectPeaksDF['median_i'] = selectPeaksDF.groupby(['scanNum','isolated'])['intensity'].transform('median')
#     selectPeaksDF['mean_i'] = selectPeaksDF.groupby(['scanNum','isolated'])['intensity'].transform('mean')
    
    
    print('regress descriminant to trigger TOI, central peak intensity, ')
#     from sklearn.linear_model import LinearRegression
#     lr = LinearRegression()
#     X = selectPeaksDF[selectPeaksDF.isolated][[u'mass', u'intensity', u'resolution', u'baseline', u'noise', u'charge', u'TIC']]
    X = selectPeaksDF[selectPeaksDF.isolated].TIC
    y = selectPeaksDF[selectPeaksDF.isolated].max_i
#     lr.fit(X, y)
#     predictions = lr.predict(X)
    import statsmodels.api as sm
    model = sm.OLS(y, X).fit()
#     predictions = model.predict(X)
#     predictionsDF = selectPeaksDF[selectPeaksDF.isolated]
#     predictionsDF['predictions'] =predictions
    print('filter based on descrimenant regresssion')
    peaksDF['scanNum'] = peaksDF.index
    peaksDF['TIC'] = peaksDF.groupby('scanNum')['intensity'].transform('sum')
    peaksDF['prediction'] = model.predict(peaksDF['TIC'])
    peaksDF['pass'] = peaksDF['intensity'] > peaksDF['prediction'] 
    
    #peaksDF.loc[scansDF[scansDF['count'] < 10].index]
    print('evaluate filter efficiency')
    selectPeaksDF['prediction'] = model.predict(selectPeaksDF['TIC'])
    selectPeaksDF['pass'] = selectPeaksDF['intensity'] > selectPeaksDF['prediction']
    
    
#                 no pass    pass    
# not isolated    3524    5343    8867
# isolated        3959    3070    7029
#                 7483    8413    15896

    print('make the file')
#     (masses, intens) = scanPeaksAll[scan]
    scanPeaksAll = {}
    scanPeaks_thresh= {}
    for scan in scansDF.itertuples():
        scanNum = scan.scanNum
        filterLine = scan.filterLine
        charge = int(scansDF.loc[scanNum].chargeState)
        header  = '{} {} {}'.format(scanNum, filterLine, charge)
        masses = peaksDF[peaksDF['scanNum'] == scanNum].mass.tolist()
        intens = peaksDF[peaksDF['scanNum'] == scanNum].intensity.tolist()
        scanPeaksAll[header] = (masses,intens)
        masses_fil = peaksDF[(peaksDF['pass']) & (peaksDF['scanNum'] == scanNum)].mass.tolist()
        intens_fil = peaksDF[(peaksDF['pass']) & (peaksDF['scanNum'] == scanNum)].intensity.tolist()
        scanPeaks_thresh[header] = (masses_fil, intens_fil)
    
    generatePsudoMGF('qc_02_QC04_reprateThresh-all.mgf', scanPeaksAll)
    generatePsudoMGF('qc_02_QC04_reprateThresh-thre.mgf', scanPeaks_thresh)
    

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
    
    

if __name__ == '__main__':
    main()