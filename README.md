MSPeakStrainer
=============

MSPeakStrainer is a tool to reduce the size of MS spectra,
with the goal of removing inconsistent signals
and combining the consistent signals.

Quick Start
-----------
 - Download [MSPeakStrainer.zip](https://idisk-srv1.mpi-cbg.de/~mirandaa/MSPeakStrainer.zip)
 - Unzip the file
 - run ```MSPeakStrainerApp.bat```   

Desktop Application
----
Run ```MSPeakStrainerApp.bat``` this will start the Desktop application.
Once one or more thermo.raw file are selected, you can click finish to process the file with default settings.
The Desktop application contains several pages where setting can be changed from the default.

If you don't change anything the default values are used.

Command line Application
-------
Run `MSPeakStrainer.py file.raw` from the command line to process the file with the default settings.
custom settings can be applied on the command line with ```utils\msps.py```

I would recommend that you look at the code in ```msPeakStrainer.py```
in the main method and update it there,
the code should be readable and you can change it to your setting.


## Options
msPeakStrainer can be configured to run in different ways,
but the default setting should work most of the time.
Just in case here are some options you can change.

Please note that some options are not available in the GUI.
one of the goals of the GUI is to maintain simplicity.
This is why some options are only in the code.

### Select Scans
A simple way to reduce the size of the file is by removing some scans.
Scan can be removed based on:
- Retention time, ie from ... to ... in seconds
- By filterline text, filterline is a short text that describes the scan,
	ie. filter line should include the text `NSI` or
	filter line should exclude the text `+`
- By Sample, this is mainly for testing, you can get 1 out of every _N_ scans,
	ie. take 1 out of every 10 scans 


### Pre-filter Peaks
At this stage we remove what seems to be random noise.
first we combine the spectra that has the same preconditions, 
ie. mode, selected ion m/z, etc.
And we count the peaks at a given m/z value,
if the count is very low, like 1 or 2, as compared to other peak counts,
then we consider those peaks random and discard them.

This step makes the most difference and facilitates the following steps

### Bin Generation
Now that we have peaks that can be combined, we try to combine them.
First we decide what peaks go together, to do this we use bins.
bins give us the lower and upper bounds of m/z,
all the peaks within those bound go together in a bin.

Some ways to make bins are:
- by decimal places, if the peaks are close enough... to a given decimal place,
then they are in the same bin.
- by measure resolution, given the raw file we read the peak resolution and make the bin as wide as the resolution, ie, peak width at 50% intensity
- by a resolution function, in some cases the measured resolution is inconsistent,
some peaks may be very wide or too narrow, so instead we extract a trendline for the resolution and use the trend instead of the measured value
- by resolution function, in case we cannot extract the resolution trendline we can just input function values to estimate the resolution, this way we get bins that grow or shrink across the m/z range

### Sort Peaks
Now that we defined the bins, we need to sort the peaks into the bins,
this would be trivial if the bins did not overlap,
but sometimes they do overlap so we need to decide how to handle it.

- Peak in first bin the matched, quick and straight forward,
works well if there is no bin overlap
- Peak in narrowest bin, this maintains peak resolution and underlying peaks can be detected, 
but it is computationally expensive and provides very small differences

- Peak in bin sort window, in this case we only check a few bins to see if the peak matches, it is less computationally expensive, than the others

### Filter Bins
By grouping peaks together into bins we can count how often peaks occur in a given m/z range.
We would expect these groups to have approximately the same number of peaks.
if the peaks are much less than expected then we filter those groups out

### Store Results
We can see the results of each step in the process trough csv files.
there are _comma separated values_ files, and also a psudo mzXML file.

