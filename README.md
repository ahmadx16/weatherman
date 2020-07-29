# Weather  Man  ![alt text](https://img.icons8.com/office/40/000000/cloud.png)


This program calculates reports of the weather data of Muree. It generates and prints following reports.
* Yearly Report
* Monthly Report
* Monthly Chart

Check out the details of reports below

**Important Note:** This program requires a *weatherfiles.zip* (a file with Muree's weather dataset) to execute.  

## Instructions

 This program uses *xlrd* library for reading .xlsx files. Install library *xlrd* using following command. Skip this step if it is already installed
```shell
pip3 install xlrd
```
You can learn more about xlrd [here](https://pypi.org/project/xlrd/).
If you do not have python3-pip visit link [here](https://pip.pypa.io/en/stable/installing/) for details of installation.

___
## Generating Reports

This section describes what data is generated on reports and how to print different reports.

### Yearly Reports

Yearly report extracts and displays following elements of a given year
* Highest Temperature
* Lowest Temprature
* Lowest Humidity

To get year report run command
```shell
python3 weatherman.py /path/to/zip-file -e YEAR
```
Replace the "YEAR" above with any year between 2004 and 2016 (inclusive). Make sure to give the path of folder that contains *weatherfiles.zip* file.

**Example Command:**

```shell
python3 weatherman.py ./ -e 2011
```
**Output:**
```shell
-- Year 2011 Report --
Highest: 38C on August 07
Lowest: -3C on January 15
Humidity: 8% on December 25
```

### Monthly Reports

Monthly report extracts and displays following elements of a given month and year
* Average Highest Temperature
* Average Lowest Temprature
* Average Mean Humidity

To get month report run following command
```shell
python3 weatherman.py /path/to/zip-file -a YEAR/MONTH
```

**Example Command:**

```shell
python3 weatherman.py ./ -a 2007/6
```
**Output:**
```shell
-- June 2007 Report --
Average Highest: 24C 
Average Lowest: 18C
Average Mean Humidity: 60% 
```

### Month Charts

The colored "+" bar is displayed for each day with red for highest temperature and blue for lowest temperature of the day.

To diplay charts of a given month simply run command
```shell
python3 weatherman.py /path/to/zip-file -a YEAR/MONTH
```


**Example Command:**

```shell
python3 weatherman.py ./ -c 2009/3
```
**Output:**

```shell
March 2009
01 ++++++++++++++++++++ 8C - 12C
02 +++++++++++++++++++++++++++ 10C - 17C
03 ++++++++++++++++++++++ 8C - 14C
04 ++++++++++++++++++ 8C - 10C
05 ++++++++++++++++++++++ 8C - 14C
...
```

### Multiple Reports

You can also print multiple reports providing relevent flag arguments
* -e for year report
* -a for month report
* -c for month chart



**Example Command:**

```shell
python3 weatherman.py ./ -e 2004 -a 2006/12 -c 2009/2
```

**Output:**

```shell
-- Year 2004 Report --
Highest: 29C on June 04
Lowest: 0C on December 17
Humidity: 10% on December 03

-- December 2006 Report --
Average Highest: 9C 
Average Lowest: 7C
Average Mean Humidity: 52% 

February 2009
01 ++++++++++++++++++ 6C - 12C
02 ++++++++++++++++++++ 8C - 12C
03 ++++++++++++ 4C - 8C
04 ++++++++++++++ 6C - 8C
05 ++ 0C - 2C
...
```