import random

for fileNum in range(5):
    fileLength = random.randint(3500, 6000)
    fileName = "csvDataFile" + str(fileNum) + ".csv"
    dataMin = random.randint(1, 89)
    dataMax = random.randint(90, 200)
    with open(fileName, "w") as file:
        eventDict = {"1": "kick", "2": "tackle", "3": "pass"}
        lineData = ["EventNum", "EventIDType", "EventName", "EventData"]
        file.write(", ".join(lineData) + "\n")
        for fileLine in range(fileLength):
            eventID = random.randint(1, 3)
            eventType = eventDict[str(eventID)]
            if eventID == 2:
                eventData = random.randint(dataMin, dataMax)
            else:
                eventData = 0
            lineData = [str(fileLine+1), str(eventID), eventType, str(eventData)]
            file.write(",".join(lineData) + "\n")
