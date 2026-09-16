Version: Pre-Alpha

Description: 
The purpose of this porgram (or chain of file executions) is to provide a proof of concept for extracting and processing data. The current data is forged, predictable, and has small file sizes compared to the expected data. Currently I am generating the data before extracting and isolating a particular event (via a specific id) that can then be processed from an array of number to a meaningful representation that can be interpreted at a glance. Aulthough its far from optimised its designed to be able to adapt to the actual format of the real data and expandable to process more than just one type of data at once. 

How to use:
Generating new data;
- Open The RawData folder and clear/delete the CSV files present. 
- Run the program 'GenData.py'
- This will create new, uniform random data

Extracting data;

- Note: Currently hard coded to extract tackle data (as thats the only data with meaning rn)
- open the 'ExtractedData' folder and ensure there are no files present before starting extraction. 
Note: If there is files present it will append the extra data (including the header) to the end and break the processing data step as the header is a string, not a number.
- open 'ExtractData.py'
- This will create a file in the folder 'ExtractedData' with the tackle data

Processing Data;

- Note: The .m file requires MatLAB to run, I tried to build this into an exe to work independently from matlab, with little success (will keep working on that tho).
- With MATLAB, Open 'ProcessData.m'
- Run it.
- Observe.

Notes:
The python files shouldn't use any libraies that you would need to install. The .m must run inside MATLAB at this point (I dont like that either). As a compramise, I will provide a .png example of what its output looks like.
The data is uniformly generated from memory and as such is very predictable.
The speed of the files are very fast due to small file sizes, however, they are far from optimised currently. I have many techniques in mind to improve the effiecieny of a more developed version of this program.

