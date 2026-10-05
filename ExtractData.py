import tkinter as tk #For file dialogue (opening/saving csvs)
from tkinter import filedialog
import csv #For effiency in andling csv files
import matplotlib #For data visualisation (emulates MATLAB)
import os #Save/create files

#Declare Dynamic Varaibles (settings). Will be user inputs later.
teamToAnalyse = "NSW Waratahs" #Enter ID as int or name as string.

#Declare (Global) Varaibles
actionDict = {} #Dictionary of sets of tuples/string array (the row data)
root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True) #Keep above other windows
#Functions
def retreiveData(fileLocation: str, teamID: int = 0, teamName: str = ""):
    if fileLocation.endswith(".csv") == False: print("retreiveData Warning! - Gven file was not a CSV file. A CSV file is expected. Proceeding...")
    else: print("retreiveData Info - CSV file path accepted.")
    try: 
        with open(fileLocation) as CSVFile:
            print("retreiveData Info - Attempting to reading file contents...")
            CSVFileContents = csv.reader(CSVFile)
            print("retreiveData Info - File contents read. Filtering the data...")
            for rowData in CSVFileContents:
                if rowData[4] == teamID or rowData[5] == teamName: actionDict.setdefault(str(rowData[14]), []).append(rowData) #Matches desired team to analyse, add it to the actionDict with key = actionID
            print("retreiveData Info - File contents filtered and initalised, ready to interpret.")
    except FileNotFoundError:
        print("retreiveData Error - The given file was not found. Escalating to the higher ups (and likey crashing).")
        raise
    
#Main
print("Main Info - Program Initalising: Asking user for CSV files related to the team they wish to analyse.")
userGivenFilePaths = filedialog.askopenfilenames(parent=root, title="Select match CSV file(s)", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
print("Main Info - File(s) given: \n - " + "\n - ".join(str(fileLocation) for fileLocation in userGivenFilePaths))
for fileLocation in userGivenFilePaths:
    try: retreiveData(fileLocation, int(teamToAnalyse), "") #If teamID was given
    except ValueError: retreiveData(fileLocation, 0, teamToAnalyse) #If teamID was not given (name was)
print("Main Info - Data saved. What would you like to do with this data?")

userInput = input("A - Save all extracted data to unique CSVs. \nB - Extract a specific actionID to a CSV.\nC - Do not save extraction and proceed to data visulisation.\n")
userInput = userInput.strip().lower()
while userInput:
    if userInput.startswith("a"):
        print("Main Info - Option A selected.")
        actionKeys = list(actionDict)
        userInput = input("Option A Request - Preparing to create/write " + str(len(actionKeys)) + " files. Proceed? y/n\n")
        userInput = userInput.strip().lower()
        if userInput.startswith("n"):
            print("Option A Info - User rejected saving of files. And no data was saved. Breaking.")
            break
        elif userInput.startswith("y"):
            for actionKey in actionKeys:
                with open("./ExtractedData/" + str(actionKey) + "-" + actionDict[str(actionKey)][1][15] + ".csv", "w") as fileToWrite: fileToWrite.write("\n".join(",".join(rowData) for rowData in actionDict[actionKey]))
            print("Main Info - Written Data of every action that was in the internal database to " + str(len(actionKeys)) + " files.")
    elif userInput.startswith("b"):
        print("Main Info - Option B selected.")
        userInput = input("Option B Request - What actionID would you like to be saved? A reference list will be provided now:\n - " + "\n - ".join([str(actionKey) + " -> " + actionDict[actionKey][1][15] for actionKey in actionDict.keys()]) + "\n")
        try: userInput = str(int(userInput.strip().lower()))
        except ValueError: print("Option B Error - Expected actionID to be entered as an integer. Proceeding anyway (and hoping for the best)")
        if userInput in list(actionDict): print("Option B Info - Input of actionID accepted. Opening save dialogue...")
        else:
            print("Option B Error - Input of actionID declined. Cannot save an actionID that is absent. Breaking.")
            break
        userGivenFilePath = filedialog.asksaveasfilename(parent=root, title="Save File As", defaultextension=".csv", filetypes=[("Comma Seperated Value File", "*.csv"), ("All Files", "*.*")])
        if userGivenFilePath:
            with open(userGivenFilePath, "w") as fileToWrite: fileToWrite.writelines("\n".join(",".join(rowData) for rowData in actionDict[userInput]))
            print("Option B Info - Saved the data for actionID '" + str(userInput) + "' to the file path of: " + str(userGivenFilePath))
        else: print("Option B Info - No file path of given. And no data was saved.")
    elif userInput.startswith("c"):
        print("Main Info - Option C selected.")
        #WIP
    else: print("Main Warning: Input not regignised. expected 'A', 'B', 'C'. ")
    break
"""
Givens:
    - Looking at team as a whole. Individual player metrics are very posible but out of scope of this version.
"""
