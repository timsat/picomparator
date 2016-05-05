# picomparator
Image comparer and browser

```
usage: picomparator [-h] [--filelist FILELIST] beforedir afterdir

Compares images in 2 directories and browses them

positional arguments:
  beforedir            path to the images before the tested change
  afterdir             path to the images after the tested change

optional arguments:
  -h, --help           show this help message and exit
  --filelist FILELIST  file with filenames and differences in CSV format e.g.
                       differences.csv
```
`FILELIST` parameter should contain filenames related to `afterdir` or `beforedir`, so please set the parameters correctly, for example like this:
```
./picomparator 10.0.0.0001/convertedPdfFiles 10.0.0.0002/convertedPdfFiles --filelist differences.csv
```
