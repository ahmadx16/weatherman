# Weather  Man

## How To Run

* Make sure to have *weatherfiles.zip* in current directory
* Make sure the path provided refers to existing folder
* Libraries required are *zipfile,os,re,xlrd,sys,datetime,shutil*

Replace YEAR and MONTH with integer values below

To get year report run command
```shell
python weatherman.py /path/to/dataset/ -e YEAR
```

To get month report run command
```shell
python weatherman.py /path/to/dataset/ -a YEAR/MONTH
```

To get month chart run command
```shell
python weatherman.py /path/to/dataset/ -c YEAR/MONTH
```

To get multiple reports add multiple attributes EG:
```shell
python weatherman.py /path/to/dataset/ -c YEAR/MONTH -e YEAR -a YEAR/MONTH
```