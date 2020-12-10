from pathlib import Path
from peakStrainer import mzML2Scans
import pickle
import ms_deisotope
from ms_deisotope.output.mzml import MzMLSerializer
from ms_peak_picker.test.common import make_peak
from ms_peak_picker.peak_set import FittedPeak, PeakSet
from ms_peak_picker.reprofile import reprofile

def stems_and_tails(path):
    p = Path(path)
    stems = set()
    tails = set()
    suffix = None
    for f in p.glob('*.mzml'):
        stems.add(f.stem[:-4])
        tails.add(f.stem[-4:])
        suffix = f.suffix
    return stems,tails, suffix

def joined_mzmls(centroid_path, stems,tails, suffix):
    joined_mzmls = []
    new_paths = []
    for stem in stems:
        joined_mzml = []
        for tail in tails:
            p = Path(centroid_path) / (stem + tail + suffix)
            MSrawscans = mzML2Scans(str(p))
            joined_mzml.extend(MSrawscans)
        joined_mzmls.append(joined_mzml)
        new_paths.append(Path(centroid_path) / (stem + suffix))
    return joined_mzmls, new_paths

def writeMZML(filepath, filtered_bins):
    p = Path(filepath)
    base_file = str(next(p.parent.glob(str( p.stem) + '*' )))

    reader = ms_deisotope.MSFileLoader(base_file)
    with open(filepath, 'wb') as fh:
        writer = MzMLSerializer(fh)
        writer.copy_metadata_from(reader)

        bunch = next((b for b in reader if ' ms ' in b.precursor.annotations['filter string']))
        try:
            msnScan = next((b.products[0] for b in reader if b.products))
        except StopIteration:
            msnScan = None

        fake_rt = 1
        first_ms1 = None
        msNscans = []
        for filterline, values in filtered_bins.items():
            peak_set = PeakSet([make_peak(*point) for point in zip(*values)])
            peak_set.reindex()
            reprofiled_peaks = reprofile([make_peak(*point) for point in zip(*values)])

            bunch.precursor.annotations['filter string'] = filterline
            bunch.precursor.scan_time = fake_rt
            fake_rt +=1
            bunch.precursor.peak_set = peak_set

            if not first_ms1 and ' ms ' in filterline:
                first_ms1 = bunch.precursor.clone()
                continue
            if msnScan and ' ms2 ' in filterline:
                clone = msnScan.clone()
                clone.annotations['filter string'] = bunch.precursor.annotations['filter string']
                clone.scan_time = bunch.precursor.scan_time
                clone.peak_set = bunch.precursor.peak_set
                msNscans.append(clone)
                continue
        
            writer.save(bunch)
        
        bunch.precursor.annotations['filter string'] = first_ms1.annotations['filter string']
        bunch.precursor.scan_time = first_ms1.scan_time
        bunch.precursor.peak_set = first_ms1.peak_set
        bunch.products.extend(msNscans)
        writer.save(bunch)

        writer.complete()
        fh.flush()
        writer.format()

if __name__ == "__main__":
    filepath = r'C:\\Users\\mirandaa\\Downloads\\centroid\\20200902_1_Ultra-10_Ldyzer-100_plasma-10_s-1_075NH4HCO2-Full ms_FT Res_30000-AGC Target_100000_neg.mzML'
    p = Path(filepath)
    base_file = str(next(p.parent.glob(str( p.stem) + '*' )))
    pikl = r'filtered_bins.pkl'
    with open(pikl, 'rb') as handle:
        filtered_bins = pickle.load(handle)
    writeMZML(filepath, filtered_bins)

    
    #https://github.com/mobiusklein/ms_peak_picker
    #https://github.com/mobiusklein/ms_peak_picker/blob/e08aed4d5eabe848702af2a55b4850adb0fbd9c6/ms_peak_picker/reprofile.py#L89
    # https://mobiusklein.github.io/ms_deisotope/docs/_build/html/output/mzml.html




