from pathlib import Path
from peakStrainer import mzML2Scans

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

if __name__ == "__main__":
    centroid_path = r'C:\Users\mirandaa\Downloads\centroid'

    stems,tails, suffix = stems_and_tails(centroid_path)

    scans = joined_mzmls(centroid_path, stems,tails, suffix)

    print(len(scans))
