import tkinter as tk #For file dialogue (opening/saving csvs)
from tkinter import filedialog
import csv #For effiency in andling csv files
import matplotlib #For data visualisation (emulates MATLAB) NOTUSED YET
import os #Save/create files
import sqlite3 #For database

#Declare Dynamic Varaibles (settings). Will be user inputs later.
teamToAnalyse = "NSW Waratahs" #Enter ID as int or name as string.
#Declare (Global) Varaibles
root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True) #Keep above other windows
#Functions
def readRawData(fileLocation: str, teamID: int = 0, teamName: str = ""):
    if fileLocation.endswith(".csv") == False: print("readRawData Warning! - Gven file was not a CSV file. A CSV file is expected. Proceeding...")
    else: print("readRawData Info - CSV file path accepted.")
    try: 
        with open(fileLocation) as CSVFile:
            print("readRawData Info - Attempting to reading file contents...")
            CSVFileContents = csv.reader(CSVFile)
            headerData = next(CSVFileContents)
            print("readRawData Info - File contents read. Initalising MainDB...")
            DBConnection = sqlite3.connect('MainDB.db')
            DBCursor = DBConnection.cursor()
            Query = "CREATE TABLE IF NOT EXISTS AllData (" + ",".join([header + " TEXT" for header in headerData]) + ")"
            DBCursor.execute(Query)
            QuestionMarks = ", ".join(["?"] * len(headerData))
            Query = "INSERT OR IGNORE INTO AllData VALUES ("+ QuestionMarks +")"
            DBCursor.executemany(Query, list(CSVFileContents))
            DBConnection.commit()
            DBConnection.close()
            print("readRawData Info - MainDB created and data accepted. Filtering data...")
            DBConnection = sqlite3.connect('MainDB.db')
            DBCursor = DBConnection.cursor()
            Query = "SELECT DISTINCT action FROM AllData"
            DBCursor.execute(Query)
            for uniqueActionID in DBCursor.fetchall():
                uniqueActionID = uniqueActionID[0]
                Name = '"' + str("ActionSubtable-" + uniqueActionID).replace('"', '""') + '"' #start & end " as it contains a '-'. Replace " with "" to prevent SQL injection.
                Query = "CREATE TABLE IF NOT EXISTS " + Name + " AS SELECT * FROM AllData WHERE action = ?"
                DBCursor.execute(Query, (uniqueActionID,))
            DBConnection.commit()
            DBConnection.close()
            print("readRawData Info - MainDB Initalised.")
    except FileNotFoundError:
        print("readRawData Error - The given file was not found. Escalating to the higher ups (and likey crashing).")
        raise
#Main
print("Main Info - Program Initalising: Asking user for CSV files related to the team they wish to analyse.")
userGivenFilePaths = filedialog.askopenfilenames(parent=root, title="Select match CSV file(s)", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
print("Main Info - File(s) given: \n - " + "\n - ".join(str(fileLocation) for fileLocation in userGivenFilePaths))
for fileLocation in userGivenFilePaths:
    try: readRawData(fileLocation, int(teamToAnalyse), "") #If teamID was given
    except ValueError: readRawData(fileLocation, 0, teamToAnalyse) #If teamID was not given (name was)
print("Main Info - Data saved. What would you like to do with this data?")

userInput = input("A - Save all extracted data to unique CSVs. \nB - Extract a specific actionID to a CSV.\nC - Do not save extraction and proceed to data visulisation.\n")
userInput = userInput.strip().lower()
while userInput:
    if userInput.startswith("a"):
        print("Main Info - Option A selected.")
        DBConnection = sqlite3.connect('MainDB.db')
        DBCursor = DBConnection.cursor()
        Query = "SELECT DISTINCT action FROM AllData"
        DBCursor.execute(Query)
        QueryResult = DBCursor.fetchall()
        actionIDs = [actionID[0] for actionID in QueryResult]
        userInput = input("Option A Request - Preparing to create/write " + str(len(actionIDs)) + " files. Proceed? y/n\n")
        userInput = userInput.strip().lower()
        if userInput.startswith("n"):
            print("Option A Info - User rejected saving of files. And no data was saved. Breaking.")
            break
        elif userInput.startswith("y"):
            for actionID in actionIDs:
                Name = '"' + str("ActionSubtable-" + actionID).replace('"', '""') + '"' #start & end " as it contains a '-'. Replace " with "" to prevent SQL injection.
                Query = "SELECT * FROM " + Name 
                DBCursor.execute(Query)
                QueryResult = DBCursor.fetchall()
                with open("./ExtractedData/" + str(actionID) + "-" + QueryResult[0][15] + ".csv", "w") as fileToWrite: fileToWrite.write("\n".join(",".join(rowData) for rowData in QueryResult))
            print("Main Info - Written Data of every action that was in the internal database to " + str(len(actionIDs)) + " files.")
        DBConnection.commit()
        DBConnection.close()
    elif userInput.startswith("b"):
        DBConnection = sqlite3.connect('MainDB.db')
        DBCursor = DBConnection.cursor()
        Query = "SELECT DISTINCT action, actionName FROM AllData"
        DBCursor.execute(Query)
        QueryResult = DBCursor.fetchall()
        actionIDs = [rowData[0] for rowData in QueryResult]
        actionNames = [rowData[1] for rowData in QueryResult]
        print("Main Info - Option B selected.")
        userInput = input("Option B Request - What actionID would you like to be saved? A reference list will be provided now:\n - " + "\n - ".join([str(actionIDs[i]) + " -> " + actionNames[i] for i in range(len(actionIDs))]) + "\n")
        try: userInput = str(int(userInput.strip().lower()))
        except ValueError: print("Option B Error - Expected actionID to be entered as an integer. Proceeding anyway (and hoping for the best)")
        if userInput in list(actionIDs): print("Option B Info - Input of actionID accepted. Opening save dialogue...")
        else:
            print("Option B Error - Input of actionID declined. Cannot save an actionID that is absent. Breaking.")
            break
        userGivenFilePath = filedialog.asksaveasfilename(parent=root, title="Save File As", defaultextension=".csv", filetypes=[("Comma Seperated Value File", "*.csv"), ("All Files", "*.*")])
        if userGivenFilePath:
            Name = '"' + str("ActionSubtable-" + userInput).replace('"', '""') + '"' #start & end " as it contains a '-'. Replace " with "" to prevent SQL injection.
            Query = "SELECT * FROM " + Name 
            DBCursor.execute(Query)
            QueryResult = DBCursor.fetchall()
            with open(userGivenFilePath, "w") as fileToWrite: fileToWrite.writelines("\n".join(",".join(rowData) for rowData in QueryResult))
            print("Option B Info - Saved the data for actionID '" + str(userInput) + "' to the file path of: " + str(userGivenFilePath))
        else: print("Option B Info - No file path of given. And no data was saved.")
    elif userInput.startswith("c"):
        print("Main Info - Option C selected. WIP.")
        #WIP
    else: print("Main Warning: Input not regignised. expected 'A', 'B', 'C'. ")
    break
"""
Givens:
    - Looking at team as a whole. Individual player metrics are very posible but out of scope of this version.
"""
