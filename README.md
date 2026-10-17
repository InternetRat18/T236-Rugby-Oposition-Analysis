# Rugby Opposition Analysis Dashboard

Version: Pre-Alpha

Description: The purpose of this program (or chain of file executions) is to provide a proof of concept for extracting and processing data. The current data is forged, predictable, and has small file sizes compared to the expected data. Currently I am generating the data before extracting and isolating a particular event (via a specific id) that can then be processed from an array of number to a meaningful representation that can be interpreted at a glance. Aulthough its far from optimised its designed to be able to adapt to the actual format of the real data and expandable to process more than just one type of data at once.

## Setup

1. Put the match CSV files in **RawData** (or select them when prompted by **ExtractData.py**).

2. Open/Run:

   ```
   py ExtractData.py
   ```

   * It will prompt you immediately to open this raw csv file.
   * Follow the instrctions the program offers.
   * Can save all data to unique csv files in bulk
   * Can save only one type of actionID data to a single file
   * WIP -> can show detailed select graphs from the data entered.
   * It will create *MainDB.db* in its current working directory. Run it from this project folder so the API finds the same database.



3. Python dependencies:
      * Installed:
     ```
   tkinter/csv/os
    ```
      * Require installation:

   ```
   Flask -> py -m pip install flask
   ```


4. Start the API and webpage:

   ```
   py api.py
   ```

5. Open <http://127.0.0.1:5000>
