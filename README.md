Version: Pre-Alpha

Description: 
The purpose of this program (or chain of file executions) is to provide a proof of concept for extracting and processing data. The current data is forged, predictable, and has small file sizes compared to the expected data. Currently I am generating the data before extracting and isolating a particular event (via a specific id) that can then be processed from an array of number to a meaningful representation that can be interpreted at a glance. Aulthough its far from optimised its designed to be able to adapt to the actual format of the real data and expandable to process more than just one type of data at once. 

How to use:

Extracting data;

- Idealy place the raw, unfiltered data within the 'RawData' folder for ease of access.
- open/run 'ExtractData.py'
- It will prompt you immediately to open this raw csv file.
- Follow the instrctions the program offers.
 - Can save all data to unique csv files in bulk
 - Can save only one type of actionID data to a single file
 - WIP -> can show detailed select graphs from the data entered.

Processing Data;

- Currently can only save the filtered data

Notes/Requirements (Listed version is what has been tested to work, other versions may work but have not been tested)
- tkinter/csv/os are all preinstalled with python(3.14.7)
- matplotlib will need to be installed using "pip install matplotlib==3.11.2" 

- The data is processed very fast, so no optimisation is required at this point.
