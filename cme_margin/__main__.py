import sys
from pathlib import Path

from cme_margin.cme_margin import download, merge, read, write

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python -m cme_margin /path/to/file")
        sys.exit()

    # download margin
    new = download()

    # read existing margin file and merge with downloaded margin
    path = Path(sys.argv[1])
    if path.exists():
        old = read(path)
        result = merge(old, new)
    else:
        result = new

    # write to file
    write(result, path)
