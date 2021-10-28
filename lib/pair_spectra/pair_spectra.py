from pathlib import Path


def get_file_pairs(path):
    p = Path(path)
    files = p.glob("*.mzml")
    pairs = zip(*[iter(files)] * 2)
    return pairs


def main():
    print("hello world")


# if __name__ == '__main__':
#     main()
pairs = get_file_pairs(r"lib\pair_spectra\tests\20211018_Peakstrainer_pairwise")
for p in pairs:
    print(str(p[0].name), str(p[1].name))

