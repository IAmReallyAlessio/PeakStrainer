'''
Created on 16.08.2017

@author: mirandaa
'''
# todo: generate csv, change regression to lowess and use median instead of max
import time
import os
import logging
from collections import namedtuple
log = logging.getLogger(os.path.basename(__file__))
import pickle

import numpy as np
import pandas as pd

from lib import MSFileReader
from utils.peakStrainer_util import generatePsudoMGF 

def main(isolation_dist = 0.01):
    print('find ms2 scans')
    filename = r'C:\apps\eclipseRCP\workspace\PeakStrainer\tmp\liver_albert_50ug_50ul.raw'
#     scansDF, peaksDF = ThermoRawfile2DataFrames(filename)
#     scansDF.to_pickle('scansDF.pkl')
#     peaksDF.to_pickle('peaksDF.pkl')
#  # or DataFrame.to_hdf
        
    scansDF = pd.read_pickle('liver_albert_50ug_50ul_scansDF.pkl')
    peaksDF = pd.read_pickle('liver_albert_50ug_50ul_peaksDF.pkl') # if there are no peaks in the scan then the index is not there 
    peaksDF['scanNum'] =  peaksDF.index
#     scansDF = scansDF.loc[peaksDF.index.unique()]
    scansDF = scansDF[(scansDF.filterLine.str.contains(' ms2 '))]
      
    print('get repeated min 10 times')
    scansDF['count'] = scansDF.groupby('filterLine')['filterLine'].transform('count')
    selectFilterLines = scansDF[scansDF['count'] >= 10]['filterLine'].unique()
    
    print(' get description of non-repeating peaks')
    selectPeaksList=[]
    for idx, selectFilterLine in np.ndenumerate(selectFilterLines):
        selectScanNums = scansDF[scansDF['filterLine'] == selectFilterLine]['scanNum']
        selectPeaks = peaksDF.loc[selectScanNums]
        selectPeaks.sort_values('mass',inplace=True)
        selectPeaks['diff'] = selectPeaks['mass'].diff()  
        selectPeaks['diff1'] = selectPeaks['diff'].shift(-1) 
        selectPeaks['isolated'] = (selectPeaks['diff'] > isolation_dist) & (selectPeaks['diff1'] > isolation_dist)
        selectPeaksList.append(selectPeaks)
    if selectPeaksList : 
        selectPeaksDF = pd.concat(selectPeaksList)
#     selectPeaksDF = pd.read_pickle('selectPeaks4DF.pkl')
   
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

    q3_i_series= selectPeaksDF.groupby(['scanNum','isolated'])['intensity'].quantile(.75).rename("q3_i").reset_index()
    selectPeaksDF = selectPeaksDF.merge(q3_i_series)
    
    
    print('regress descriminant to trigger TOI, central peak intensity, ')
#     from sklearn.linear_model import LinearRegression
#     lr = LinearRegression()
#     X = selectPeaksDF[selectPeaksDF.isolated][[u'mass', u'intensity', u'resolution', u'baseline', u'noise', u'charge', u'TIC']]
    X = selectPeaksDF[selectPeaksDF.isolated].TIC
    y = selectPeaksDF[selectPeaksDF.isolated].q3_i
#     lr.fit(X, y)
#     predictions = lr.predict(X)
    import statsmodels.api as sm
    model = sm.OLS(y, X).fit()
    
    from scipy.interpolate import interp1d
    import statsmodels.api as sm
    
    lowess = sm.nonparametric.lowess(y, X, frac=.3)
    lowess_x = list(zip(*lowess))[0]
    lowess_y = list(zip(*lowess))[1]
    f = interp1d(lowess_x, lowess_y, bounds_error=False)
    
#     see https://stackoverflow.com/questions/36252434/predicting-on-new-data-using-locally-weighted-regression-loess-lowess
#     predictions = model.predict(X)
#     predictionsDF = selectPeaksDF[selectPeaksDF.isolated]
#     predictionsDF['predictions'] =predictions
    print('filter based on descrimenant regresssion')
    peaksDF['scanNum'] = peaksDF.index
    peaksDF['TIC'] = peaksDF.groupby('scanNum')['intensity'].transform('sum')
    peaksDF['prediction_q3'] = model.predict(peaksDF['TIC'])
    peaksDF['lowess_q3'] = f(peaksDF['TIC'])
    peaksDF['pass_q3'] = peaksDF['intensity'] > peaksDF['prediction_q3']
    peaksDF['pass_lowess_q3'] = peaksDF['intensity'] > peaksDF['lowess_q3'] 
    
    #peaksDF.loc[scansDF[scansDF['count'] < 10].index]
    print('evaluate filter efficiency')
    selectPeaksDF['prediction_q3_i'] = model.predict(selectPeaksDF['TIC'])
    selectPeaksDF['lowess_q3_i'] = f(selectPeaksDF['TIC'])
    selectPeaksDF['pass_q3_i'] = selectPeaksDF['intensity'] > selectPeaksDF['prediction_q3_i']
    selectPeaksDF['pass_lowess_q3_i'] = selectPeaksDF['intensity'] > selectPeaksDF['lowess_q3_i']
    
    
#                 no pass    pass    
# not isolated    3524    5343    8867
# isolated        3959    3070    7029
#                 7483    8413    15896

    print('make the file')
#     (masses, intens) = scanPeaksAll[scan]
    scanPeaksAll = {}
    scanPeaks_thresh= {}
    allc = 0
    filc = 0
    for scan in scansDF.itertuples():
        scanNum = scan.scanNum
        filterLine = scan.filterLine
        charge = int(scansDF.loc[scanNum].chargeState)
        header  = '{} {} {}'.format(scanNum, filterLine, charge)
        masses = peaksDF[peaksDF['scanNum'] == scanNum].mass.tolist()
        intens = peaksDF[peaksDF['scanNum'] == scanNum].intensity.tolist()
        scanPeaksAll[header] = (masses,intens)
        allc += len(masses)
        masses_fil = peaksDF[(peaksDF['pass_lowess_q3']) & (peaksDF['scanNum'] == scanNum)].mass.tolist()
        intens_fil = peaksDF[(peaksDF['pass_lowess_q3']) & (peaksDF['scanNum'] == scanNum)].intensity.tolist()
        filc += len(masses_fil)
        scanPeaks_thresh[header] = (masses_fil, intens_fil)
    
    generatePsudoMGF('qc_02_QC04_-all_q3_lowess.mgf', scanPeaksAll)
    generatePsudoMGF('qc_02_QC04_-thre_q3_lowess.mgf', scanPeaks_thresh)
    peaksDF.to_csv('qc_02_QC04_-thre_q3.csv')

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
        if not peak_datas.mass:# there was no data
            peak_datas = (rawfile.GetMassListFromScanNum(scanNum)[0][0],
                               rawfile.GetMassListFromScanNum(scanNum)[0][1])
            
        retTime =  rawfile.RTFromScanNum(scanNum)*60
        chargeState= rawfile.GetTrailerExtraForScanNum(scanNum)['Charge State']
        isolationMass = rawfile.GetPrecursorInfoFromScanNum(scanNum).isolationMass if  rawfile.GetPrecursorInfoFromScanNum(scanNum) is not None else 0.0# or monoIsoMass
        row = [scanNum, filterLine, retTime, chargeState, isolationMass]
        MSrawscansDF.loc[scanNum] = row
        peak_datasT = zip(*peak_datas)
        if len(peak_datas)>2:
            peak_datasDF = pd.DataFrame(peak_datasT, index = [scanNum]*len(peak_datasT), columns=['mass', 'intensity', 'resolution', 'baseline', 'noise', 'charge'])
        else:
            peak_datasDF = pd.DataFrame(peak_datasT, index = [scanNum]*len(peak_datasT), columns=['mass', 'intensity'])
        peak_datasDF_list.append(peak_datasDF)
    MSPeakDatasDF=pd.concat(peak_datasDF_list) # concat is expensive so just once
    log.info('File Read time %f s', time.time()-startTime)
    log.info('Scan Count is %d', len(MSrawscansDF))
    
    return MSrawscansDF, MSPeakDatasDF
    
    

if __name__ == '__main__':
    main()