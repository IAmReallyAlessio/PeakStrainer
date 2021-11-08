from pathlib import Path
from ms_deisotope import MSFileLoader
from ms_deisotope.output.mzml import MzMLSerializer

# from https://github.com/mobiusklein/ms_deisotope/tree/master/ms_deisotope/test


def get_file_pairs(path):
    p = Path(path)
    files = p.glob("*.mzml")
    pairs = zip(*[iter(files)] * 2)
    return pairs


def print_reader(reader):
    for bunch in reader:
        print(bunch.precursor.title)
        print(bunch.precursor.annotations["filter string"])
        bunch.precursor.pick_peaks()
        print(bunch.precursor.peak_set)
        for p in bunch.products:
            print(p.title)
            print(p.annotations["filter string"])
            p.pick_peaks()
            print(p.peak_set)
            break
        break
    reader.reset()
    print("done")


def test_writer(reader):
    # https://mobiusklein.github.io/ms_deisotope/docs/_build/html/output/mzml.html
    with open("out.mzML", "wb") as fh:
        writer = MzMLSerializer(fh, n_spectra=len(reader))

        writer.copy_metadata_from(reader)
        bunch = next(reader)
        bunch.precursor.arrays = [
            bunch.precursor.arrays.mz[:100],
            bunch.precursor.arrays.intensity[:100],
        ]
        bunch.precursor.pick_peaks()
        writer.save(bunch.precursor, deconvoluted=False)

        writer.close()


def main():
    p = Path(r"lib\pair_spectra\tests\20211018_Peakstrainer_pairwise")
    p = next(p.glob("*.mzml"))
    reader = MSFileLoader(str(p))
    print_reader(reader)
    test_writer(reader)


if __name__ == "__main__":
    main()

