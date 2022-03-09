# Collect data using lab recorder and lsl

Building off the experiment from Gaddy and Klein, this code shifts to continuous data collection and markers. It is intended to support multiple streams of data from different data sources (audio, EMG, throat mic audio, IMU, etc). These larger combined files can then be epoched using the markers and written into smaller files to use other code from Gaddy and Klein.

To set up:
1) OpenBCI for EMG (and acc) and other recording scripts (audio, etc) out over LSL
2) Markers from the a python script (WRITE THIS)
3) Lab recorder (and Neuropype in the future for live) to pull all data together.
4) Script to filter and parse the data. (WRITE THIS)