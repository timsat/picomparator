# picomparator
Image comparer and browser

## Installation
1. Install [Python 2.7](https://www.python.org/downloads/release/python-2711/)
2. Install [wxPython](http://www.wxpython.org/download.php#msw). The arch of the library must be the same as Python's one.
3. Install [GhostScript](https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs919/gs919w32.exe). It will be required by _ImageMagick_
4. Install [ImageMagick](http://www.imagemagick.org/download/binaries/ImageMagick-7.0.1-3-Q8-x64-dll.exe), allow the installer to modify `PATH` variable, so you do not need to add paths later.

## Setup
Copy `settings.py.win`/`settings.py.linux` to `settings.py`
```
CONVERT_CMD = ["convert", "-density", "170", "-limit", "thread", "2"]
                ^^^^^^^   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                command           command-line params
```
* `-density` - resolution of PDF->PNG convertion
* `-limit thread` - number of threads to perform convertion in parallel

Almost the same for `COMPARE_CMD`. Other settings are self-describing.

## Usage
```
usage: python picomparator.py [-h] beforedir afterdir reportfile

Compares images in 2 directories and browses them

positional arguments:
  beforedir   path to the images before the tested change
  afterdir    path to the images after the tested change
  reportfile  file with filenames and differences in CSV format e.g.
              differences.csv

optional arguments:
  -h, --help  show this help message and exit
```
`reportfile` should contain filenames related to `<afterdir>/convertedPdfFiles` or `<beforedir>/convertedPdfFile`, so please set the parameters correctly, for example like this:
```
python picomparator 10.0.0.0001 10.0.0.0002 differences.csv
```
