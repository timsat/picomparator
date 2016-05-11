# picomparator
Image comparer and browser

```
usage: picomparator.py [-h] beforedir afterdir reportfile

Compares images in 2 directories and browses them

positional arguments:
  beforedir   path to the images before the tested change
  afterdir    path to the images after the tested change
  reportfile  file with filenames and differences in CSV format e.g.
              differences.csv

optional arguments:
  -h, --help  show this help message and exit
```
`reportfile` parameter should contain filenames related to `afterdir/convertedPdfFiles` or `beforedir/convertedPdfFile`, so please set the parameters correctly, for example like this:
```
./picomparator 10.0.0.0001 10.0.0.0002 differences.csv
```
