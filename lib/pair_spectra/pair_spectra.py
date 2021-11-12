from pathlib import Path
from ms_deisotope import MSFileLoader
from ms_deisotope.output.mzml import MzMLSerializer
import pandas as pd
from time import time

# from https://github.com/mobiusklein/ms_deisotope/tree/master/ms_deisotope/test
FILTER_NAME_VERSION = "pair_filter_spectra_0.1.0"


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
        bunch.products = None
        writer.save(bunch, deconvoluted=False)

        writer.close()


def cleanup(*args):
    for a in args:
        Path(a).unlink()
        print(f"deleted {a}")


def main():
    p = Path(r"lib\pair_spectra\tests\20211018_Peakstrainer_pairwise")
    p = next(p.glob("*.mzml"))
    reader = MSFileLoader(str(p))
    print_reader(reader)
    test_writer(reader)
    cleanup("out.mzML", "out.mzML-idx.json")
    print("TODO find_closest_with_iterator(reader1, reader2)")


def path2df(path):
    dfs = []
    with MSFileLoader(str(path)) as r:
        for b in r:
            a = b.precursor.arrays
            df = pd.DataFrame({"mz": a.mz, "intensitiy": a.intensity})
            df["scan_id"] = b.precursor.scan_id
            df["filter_string"] = b.precursor.annotations["filter string"]
            dfs.append(df)
            for p in b.products:
                a = p.arrays
                df = pd.DataFrame({"mz": a.mz, "intensitiy": a.intensity})
                df["scan_id"] = p.scan_id  # TODO  make them categoriacal?
                df["filter_string"] = p.annotations["filter string"]
                # df.set_index(['scan_id',"filter_string"], append=True, inplace=True)
                dfs.append(df)
    df = pd.concat(dfs)
    df["path_stem"] = path.stem
    df.set_index(["path_stem", "scan_id", "filter_string"], append=True, inplace=True)
    df.attrs = {"path": path}
    return df


def filterline_pair(filterline, df1, df2, cutoff=0.01):
    # TODO # https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
    # https://codereview.stackexchange.com/questions/28207/finding-the-closest-point-to-a-list-of-points
    # a.flat[np.abs(a - a0).argmin()]
    df = pd.concat([df1, df2])

    df.sort_values("mz", inplace=True)
    mask = (-df.mz.diff(-1) < cutoff) & (df.mz.diff() < cutoff)
    p1_mask = df.path == path1.stem
    p2_mask = df.path == path2.stem

    mz_i_reader1 = df.loc[mask & p1_mask, ["mz", "intensitiy"]].T.to_numpy()
    mz_i_reader2 = df.loc[mask & p2_mask, ["mz", "intensitiy"]].T.to_numpy()

    return mz_i_reader1, mz_i_reader2


def filter_pair(path1, path2):

    df1 = path2df(path1)
    df2 = path2df(path2)

    df = pd.concat([df1, df2])

    cutoff = 0.01
    groups = []
    for filter_line, group_df in df.groupby(level=3):
        group_df.sort_values("mz", inplace=True)
        group_df.sort_values("mz", inplace=True)
        mzdiff = group_df.mz.diff()
        filtered_group_df = group_df.loc[
            (mzdiff < cutoff) | (mzdiff.shift(-1) < cutoff)
        ]
        groups.append(filtered_group_df)

    filtered_df = pd.concat(groups)

    # Write out content
    reader1 = MSFileLoader(str(path1))
    key_part = (slice(None), path1.stem, slice(None))
    with open(path1.stem + "-f.mzML", "wb") as fh:
        writer = MzMLSerializer(fh, n_spectra=1)

        writer.copy_metadata_from(reader1)
        # writer.software_list.append(FILTER_NAME_VERSION)
        bunch = next(reader1)
        key = (*key_part, bunch.precursor.annotations["filter string"])
        bunch.precursor.arrays = filtered_df.loc[key, :].to_numpy().T.tolist()
        bunch.precursor.pick_peaks()

        for product in bunch.products:
            key = (*key_part, product.annotations["filter string"])
            product.arrays = filtered_df.loc[key, :].to_numpy().T.tolist()
            product.pick_peaks()

        writer.save(bunch, deconvoluted=False)

        writer.close()

    reader2 = MSFileLoader(str(path2))
    key_part = (slice(None), path2.stem, slice(None))
    with open(path2.stem + "-f.mzML", "wb") as fh:
        writer = MzMLSerializer(fh, n_spectra=1)

        writer.copy_metadata_from(reader2)
        # writer.software_list.append(FILTER_NAME_VERSION)

        bunch = next(reader2)
        key = (*key_part, bunch.precursor.annotations["filter string"])
        bunch.precursor.arrays = filtered_df.loc[key, :].to_numpy().T.tolist()
        bunch.precursor.pick_peaks()

        for product in bunch.products:
            key = (*key_part, product.annotations["filter string"])
            product.arrays = filtered_df.loc[key, :].to_numpy().T.tolist()
            product.pick_peaks()

        writer.save(bunch, deconvoluted=False)

        writer.close()


def pair_filter(path):
    pairs = get_file_pairs(path)
    for pair in pairs:
        filter_pair(*pair)


if __name__ == "__main__":
    import sys
    import time

    st = time.time()
    if len(sys.argv) != 1:
        pair_filter(sys.argv[1:])
    else:
        pair_filter(r"lib\pair_spectra\tests\20211018_Peakstrainer_pairwise")
    print(st - time.time())

