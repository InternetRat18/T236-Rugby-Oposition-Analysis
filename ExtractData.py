import os

#Declare Varaibles (settings)
folderPath = "./RawData" #Where the data to extract is located (localy)
EventTypeIntForTackle = 2 #Change this to the event ID that represents a tackle (or the data you want to extract.).
#Declare Varaibles (static) 
linesToAppend = [] #Will never be >1000 in size
EventTypeIntIndex = 1 #The column num (starting at 0) which the event ID are located
EventNameDict = {"1":"kick", "2":"tackle", "3":"pass"} #List of all IDs and their event name their representing (this could be auto-gened for large amounts of unique events)
#Declare functions
def appendLinesToFile(filePath: str, lines: list):
    with open(filePath, "a") as file:
        file.writelines(lines)
#Body of program
for fileNum, file in enumerate(os.listdir(folderPath)):
    if file.endswith(".csv"):
        with open(folderPath+"/"+file, "r") as csvRawFile:
            rawData = csvRawFile.readlines()
            if fileNum == 1: linesToAppend.append(rawData[0]) #Get the header info
            for dataLine in rawData:
                splitDataLine = dataLine.split(",")
                #Below iterates over every csv dataline in ./Data local folder
                if splitDataLine[EventTypeIntIndex] == str(EventTypeIntForTackle): #This line is a tackle
                    linesToAppend.append(dataLine) 
                    if len(linesToAppend) >= 1000: #If array is large, append them all to file (faster than individualy) then clear the variable
                        dataName = EventNameDict[str(EventTypeIntForTackle)]
                        appendLinesToFile("./ExtractedData/"+dataName+".csv", linesToAppend)
                        linesToAppend = []
print("Done") #Can tell if successful.
