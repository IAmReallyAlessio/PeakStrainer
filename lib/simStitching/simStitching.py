'''
Created on 28.04.2017

@author: mirandaa
'''
import xml.etree.ElementTree as ET
import sys, os
from base64 import b64decode, b64encode
from array import array
import re
from collections import defaultdict, namedtuple
from itertools import compress, ifilter
import copy




def main(fileName = None):

    scans = getMZXMLEncondedScans(fileName)
    with file('scans.csv', 'wb') as outfile:
        for scan in scans:
            line = str((scan[0],scan[1],scan[3]))
            outfile.write(line[1:-1]+'\n')
    msScan = [scan for scan in scans if ' ms ' in scan[1].lower() and ' full ' in scan[1].lower()]
    scans = [scan for scan in scans if 'sim' in scan[1].lower()]
    
    decodedScans =[]
    for scan in scans:
        masses, intens = decode_mzXML_Peaks(scan[2]) 
        decodedScans.append(scan+(masses, intens))
    
    with file('simScans.csv', 'wb') as outfile:
        for decodedScan in decodedScans:
            head = (decodedScan[0],decodedScan[1],decodedScan[3])
            masses = decodedScan[4]
            intens = decodedScan[5]
            for massintens in zip(masses, intens):
                line = head + massintens
                line = str(line)
                outfile.write(line[1:-1]+'\n')
        
    
    filterlines = [scan[1] for scan in scans]
    filterlines = sorted(filterlines)
    
    filterlineSplits = []
    Filterline = namedtuple('Filterline', 'head low high filterline')
    for filterline in filterlines:
        m = re.match(r'(.*)\[(\d+\.\d*)-(\d+\.\d*)\]', filterline)
        filterlineSplits.append(Filterline(m.group(1), float(m.group(2)), float(m.group(3)), m.group(0)))
    
    sortedFilterLine = sorted(filterlineSplits)
    
    filterLineCols = zip(*sortedFilterLine)
    filterLineCols = map(list,filterLineCols)
    
    uniqueFilterLines = defaultdict(set)
    overlap = False
    step = 0
    for idx, _ in enumerate(filterLineCols[0]):
        head = filterLineCols[0][idx]
        low =  filterLineCols[1][idx]
        high = filterLineCols[2][idx]
        
        if idx+1 < len(filterLineCols[0]):
            nextHead = filterLineCols[0][idx+1]
            nextLow =  filterLineCols[1][idx+1]
            nextHigh = filterLineCols[2][idx+1]
        #else: # no change still the last
            
        
        old_overlap = overlap 
        overlap = ( head == nextHead and  high > nextLow and high < nextHigh) # high < nextHigh to avoid subsumes
        first = head not in uniqueFilterLines.keys() #first, so trim low
        last = old_overlap == True and overlap == False
        old_step= step
        step = (high - nextLow)/2
        
        if first and not overlap: #first and only
#             filterLineCols[1][idx] = filterLineCols[1][idx] + step  
            low =  filterLineCols[1][idx]
            uniqueFilterLines[head].add(low)
            high = filterLineCols[2][idx]
            uniqueFilterLines[head].add(high)
        
        if first and overlap:
            filterLineCols[1][idx] = filterLineCols[1][idx] + step  
            low =  filterLineCols[1][idx]
            uniqueFilterLines[head].add(low)
        if last:
            filterLineCols[2][idx] = filterLineCols[2][idx] - old_step
            high = filterLineCols[2][idx]
            uniqueFilterLines[head].add(high)
        
        if overlap:
            mid = (high + nextLow)/2
            filterLineCols[2][idx] = mid
            filterLineCols[1][idx+1] = mid
            
    newFilterline = []
    for head in filterLineCols[0]:
        if uniqueFilterLines[head]:
            newFilterline.append(head +'['+ str(min(uniqueFilterLines[head])) + '-' + str(max(uniqueFilterLines[head]))+']')
    
    filterLineCols.append(newFilterline)
    with file('newScans.csv', 'wb') as outfile:
        for line in zip(*filterLineCols):
            line = str(line)
            outfile.write(line[1:-1]+'\n')
    
    orderedScans = []
    for line in zip(*filterLineCols):
        lineHead = line[3]
        for scan in decodedScans:
            scanHead =  scan[1]
            if scanHead == lineHead:
                orderedScans.append(scan)
                break # only take the first in case there are duplicates

    filterLineCols.append(orderedScans)
    
#     print '\n'.join(map(str,zip(*filterLineCols)))
    
    stittchedMass = defaultdict(list)
    stittchedIntes = defaultdict(list)
    for line in  zip(*filterLineCols):
        masss = line[5][4]
        intens = line[5][5] 
        low = line[1]
        high = line[2]
        filterline = line[3]
        stitchedFilterline = line[4] 
        rtime = line[5][3]
        
        filterPass = [mass >= low or mass<high for mass in masss ]
        compressedMass = list(ifilter(lambda mass: mass >= low or mass<high , masss))
        compressedIntest = list(compress(filterPass, intens))
        
        stittchedMass[stitchedFilterline].extend(compressedMass)   
        stittchedIntes[stitchedFilterline].extend(compressedIntest)
    
    scanPeaks = {}
    for e in stittchedMass:
        print (e,min(stittchedMass[e]),max(stittchedMass[e]))
        scanPeaks[e]=(stittchedMass[e], stittchedIntes[e])
    
    with file('outScans.csv', 'wb') as outfile:
        for e in scanPeaks:
            line = (e,min(scanPeaks[e][0]),max(scanPeaks[e][1]))
            line = str(line)
            outfile.write(line[1:-1]+'\n')
            
    write2templateMzXML(outputFile(fileName), scanPeaks)
    
    '''start validation'''
    
    selections = []
    for line in zip(*filterLineCols):
        masss = line[5][4]
        intens = line[5][5] 
        low = line[1]
        high = line[2]
        filterline = line[3]
        stitchedFilterline = line[4] 
        rtime = line[5][3]
        
        center = (high+low)/2
        minInten = max(intens)*0.05
        intensPass =[inten > minInten for inten in intens]
        
        massCandidates = list(compress(masss, intensPass))
        
        cleanPass = []
        for idx, _ in enumerate(massCandidates[:-1]):
            if idx == 0 :continue
            passes =  (massCandidates[idx] - massCandidates[idx-1])>=0.5
            passes = passes and (massCandidates[idx+1] - massCandidates[idx])>=0.5
            cleanPass.append(passes)
        
        massCandidates = list(compress(massCandidates, cleanPass))
        count = len(massCandidates)
        mode = count/2
        selection =  massCandidates[mode] if mode else None
        for selection in massCandidates:
            if selection:
                selections.append((selection, intens[masss.index(selection)], filterline, stitchedFilterline))
            else:
                    print 'no selection for sim {}'.format(filterline)
        
    
    with file('validationSimSelection.csv', 'wb') as outfile:
        for e in selections:
            line = str(e)
            outfile.write(line[1:-1]+'\n')
    
    
    print 'get the  mutiupl ems '
    msMasses=[]
    msIntens = []
    msFilterLine =[]
    for scan in msScan:
        masses, intens =  decode_mzXML_Peaks(scan[2])
        msMasses.extend(masses)
        msIntens.extend(intens)
        msFilterLine.extend([scan[1]]*len(masses))
            
        
    
    with file('validationMSPeaks.csv', 'wb') as outfile:
        for e in zip(msMasses, msIntens,msFilterLine ):
            line = str(e)
            outfile.write(line[1:-1]+'\n')
    
    def modematch(strin1 , string2):
        if ' - ' in strin1 and ' - ' in string2: return True
        if ' + ' in strin1 and ' + ' in string2: return True
        return False
         
    comparable = []
    found = None
    for s_mass,s_intens, s_filterline, s_stichedFilterline in selections:
        for idx, m_mass in  enumerate(msMasses):
            if round(s_mass,2) == round(m_mass,2) and modematch(s_filterline,msFilterLine[idx] ):
                found = True
                comparable.append(( m_mass, msIntens[idx],msFilterLine[idx],'',s_mass,s_intens,s_filterline, s_stichedFilterline))
                
        if not found:
            print 'no match found for {} in ms'.format((round(s_mass,1),s_intens))
    
    with file('validationCompare.csv', 'wb') as outfile:
        for e in comparable:
            line = str(e)
            outfile.write(line[1:-1]+'\n')              
    
    
    print 'get offset and output to csv'

def outputFile(fileName):
    dir,file = os.path.split(fileName)
    if not os.path.exists(dir+'\\stitched'):
        os.makedirs(dir+'\\stitched')
    newfilename = dir+'\\stitched\\'+file[:-6]+'-s'+file[-6:]
    return newfilename

def write2templateMzXML(newfilename, scanPeaks):
    namespaces = {'xmlns': 'http://sashimi.sourceforge.net/schema_revision/mzXML_3.0'}
    ET.register_namespace('', 'http://sashimi.sourceforge.net/schema_revision/mzXML_3.0')
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    tree = ET.parse(scriptPath+'\\template.mzXML')
    
    msRunElement = tree.find('.//xmlns:msRun', namespaces)
    scanTemplete = msRunElement.find('.//xmlns:scan', namespaces)
    
    
    for idx, scan in enumerate(scanPeaks):
        (masses, intens) = scanPeaks[scan]
        newScan = copy.deepcopy(scanTemplete)
        newScan.attrib['filterLine'] = scan
        newScan.attrib['peaksCount'] = str(len(masses))
        newScan.attrib['num']=str(idx+1)
        newScan.attrib['scanType']=scan.split()[4] 
        
        msLevel = 1 if ' ms ' in scan else 2
        if msLevel == 1:
            newScan.remove(newScan.find('.//xmlns:precursorMz', namespaces))
        else:
            precursorMz = newScan.find('.//xmlns:precursorMz', namespaces)
            precursorMz.attrib['activationMethod'] = scan.split()[6][7:10]
            precursorMz.text = scan.split()[6][:6]

        newScan.attrib['msLevel'] = str(msLevel)
        newScan.attrib['polarity'] = '-' if ' - ' in scan else '+'
        newScan.attrib['retentionTime'] = 'PT{}S'.format(0.0+idx)
        
        encodedPeaks = encodePeaks(masses, intens)
        newScan.find('.//xmlns:peaks', namespaces).text = encodedPeaks
        msRunElement.append(newScan)
    
    msRunElement.remove(scanTemplete)
    
    tree.write(newfilename, encoding='ISO-8859-1', xml_declaration=True)

def encodePeaks(masses, intens):
    peak_list = []
    for mass, intens in sorted(zip(masses, intens)):
        peak_list.append(mass)
        peak_list.append(intens)
    
    peaks = array('f',peak_list)
    if sys.byteorder != 'big':
        peaks.byteswap()
        
    encoded = b64encode(peaks)
    return encoded

def getMZXMLEncondedScans(filePath):
    #     TODO:handle different namespaces of mzxml 
    namespaces = {'xmlns': 'http://sashimi.sourceforge.net/schema_revision/mzXML_3.0'}
    ET.register_namespace('', 'http://sashimi.sourceforge.net/schema_revision/mzXML_3.0')
    tree = ET.parse(filePath)
 
    scanElems = tree.findall('.//xmlns:scan', namespaces)
    
    rawscans = []
    for scan in scanElems:
        encodedPeaks = scan.find('.//xmlns:peaks', namespaces).text
        scanNo = int(scan.attrib['num'])
        filterLine = scan.attrib['filterLine']
        retTime =  scan.attrib['retentionTime']
        object = (scanNo, filterLine, encodedPeaks, retTime)
        rawscans.append(object)

    return rawscans

def decode_mzXML_Peaks(encodedPeaks):
        '''
        Note zmass and intensity are together
       
        '''
        
        decoded = b64decode(encodedPeaks)
        peaks = array('f',decoded)
    
        if sys.byteorder != 'big':
            peaks.byteswap()
        
        mass = peaks[::2]
        intens = peaks[1::2]
        return mass, intens



if __name__ == '__main__':
    if len(sys.argv) > 0:
        main(sys.argv[1])
    else:
        main()
    