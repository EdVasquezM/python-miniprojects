#! /usr/bin/python3
# by Edwin Mauricio Vasquez Mejia (emvasquezm@gmail.com) for 7th@rt 3.0 project
# DNIA - Universidad Nacional de Colombia
# if you use an alternative delimiter in your CSV please modify delimeter value on lines 46, 70
import json, csv

movieName = input("Enter movie name: ") #getting data from user
sectionName = input("Enter section name: ")

def checkCSVFile(sCVSFileName): # check  if the CVS file exist
    try:
        f = open(sCVSFileName+".csv")
        f.close()
        fName = sCVSFileName+".csv"
    except FileNotFoundError:
        print(".csv file not found/exist")
        fName = checkCSVFile(input("Enter .csv file name (without .csv): "))
    return fName

#get the .csv file name
sCVSFileName = checkCSVFile(input("Enter .csv file name (without .csv): "))
section = {} #json arrangement to be writed in the .son file

#write the .json file
def writeJsonFile(fToWrite):
    print("Writing: "+fToWrite)
    with open(fToWrite, 'w') as jsonFile:
        jsonFile.write(json.dumps(section, indent=4))

#read the .csv files and gets data to the json arrangement (section)
def doSection():
    section["film"] = movieName
    section["section"] = sectionName
    section["activities"] = []
    actLabel = ''

    def addToSection():
        activities  = {}
        activities["label"] = actLabel
        activities["link"] = actLink
        activities["steps"] = []
        activities["steps"].append(steps)
        section["activities"].append(activities)

    with open(sCVSFileName, 'rt') as csvFile:
        csvReader = csv.DictReader(csvFile, delimiter=',')
        for row in csvReader:
            if row['Activity-label']:
                if actLabel:
                    addToSection()
                actLabel = row['Activity-label']
                row.pop('Activity-label')
                actLink = row['Activity-link']
                row.pop('Activity-link')
                steps = {}
                steps["label"] = row['step-label']
                row.pop('step-label')
                steps["primitives"] = []
            steps["primitives"].append({k: v for k, v in row.items() if v is not ''})
        addToSection()
    writeJsonFile("section.json")

def doPuzzle():
    section["rows"] = ''
    section["cols"] = ''
    section["words"] = []
    pFileName = 'puzzle_01.json'

    with open(sCVSFileName, 'rt') as csvFile:
        csvReader = csv.DictReader(csvFile, delimiter=',')
        for row in csvReader:
            if row['filename']:
                pFileName = row['filename']+".json";
                section["rows"] = row['rows']
                section["cols"] = row['cols']
            row.pop('filename')
            row.pop('rows')
            row.pop('cols')
            section["words"].append(row)
    writeJsonFile(pFileName)

# verify wich type of .csv is for puzzle, section or ask again if is unknown
def checkPuzzle():
    if (input("Is "+sCVSFileName+" for a section file? [y/n]: ") == "y"):
        print("Reading: "+sCVSFileName)
        doSection()
    elif (input("Is "+sCVSFileName+" for a puzzle? [y/n]: ") == "y"):
        print("Reading: "+sCVSFileName)
        doPuzzle()
    else :
        print("Didn't understand your answer")
        checkPuzzle()

checkPuzzle()
