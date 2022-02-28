#!/usr/bin/python3
# by Edwin Mauricio Vasquez Mejia (emvasquezm@gmail.com) for 7th@rt 3.0 project
# DNIA - Universidad Nacional de Colombia
import os
from zipfile import ZipFile
from datetime import date

print("This program will create a 7th@rt 3.0 SCORM Package with the files inside a directory \n must be in the same folder of that directory!")

movieName = input("Enter movie name: ") #getting data from user
sectionName = input("Enter section name: ")
pkgPath = input("Enter directory name: ")

#gets al list of files with folders an sub-folders
def getList(dirPath):
    allFiles = list()
    with os.scandir(dirPath) as entries:
        for entry in entries:
            if entry.is_dir():
                allFiles = allFiles + getList(entry)
            else:
                allFiles.append(entry.path)
    return allFiles

print("Scanning files... ")
#list of files with directory name
listOfFiles = getList(pkgPath)
listOfFiles.sort()
#list of files whitout directory name to write it in the manifest of the package
lOfFiles = sorted({x.replace(pkgPath+'/', '') for x in listOfFiles})
print("Done!")

#text to write in the manifest file
tToWrite = list()
tToWrite.append('<manifest xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"')
tToWrite.append('          xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"')
tToWrite.append('          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
tToWrite.append('          identifier="com.scorm.manifesttemplates.scorm12"')
tToWrite.append('          version="1"')
tToWrite.append('          xsi:schemaLocation="xsd/imscp_rootv1p1p2.xsd')
tToWrite.append('                              xsd/imsmd_rootv1p2p1.xsd')
tToWrite.append('                              xsd/adlcp_rootv1p2.xsd">')
tToWrite.append('	<metadata>')
tToWrite.append('		<schema>ADL SCORM</schema>')
tToWrite.append('		<schemaversion>1.2</schemaversion>')
tToWrite.append('		<lom:lom>')
tToWrite.append('			<lom:general>')
tToWrite.append('				<lom:description>')
tToWrite.append('					<lom:string language="es-US">This is the SCORM package of '+movieName+'/'+sectionName+' from 7th@rt Project 3.0 by emvasquezm@gmail.com</lom:string>')
tToWrite.append('				</lom:description>')
tToWrite.append('			</lom:general>')
tToWrite.append('		</lom:lom>')
tToWrite.append('	</metadata>')
tToWrite.append('	<organizations default="B0">')
tToWrite.append('		<organization identifier="B0" adlseq:objectivesGlobalToSystem="false">')
tToWrite.append('			<title>7th@rt/'+movieName+'</title>')
tToWrite.append('			<item identifier="i1" identifierref="r1" isvisible="true">')
tToWrite.append('				<title>'+sectionName+'</title>')
tToWrite.append('			</item>')
tToWrite.append('		</organization>')
tToWrite.append('	</organizations>')
tToWrite.append('	<resources>')
tToWrite.append('		<resource identifier="r1" type="webcontent" adlcp:scormType="sco" href="index.html">')
tToWrite.append('			<file href="index.html"/>')
tToWrite.append('	    <dependency identifierref="COMMON_FILES"/>')
tToWrite.append('		</resource>')
tToWrite.append('		<resource identifier="COMMON_FILES" type="webcontent" adlcp:scormType="asset">')
for entry in lOfFiles:
    tToWrite.append('	    <file href="'+entry+'"/>')
tToWrite.append('		</resource>')
tToWrite.append('	</resources>')
tToWrite.append('</manifest>')

#write the manifest file
with open(os.path.join(pkgPath, "imsmanifest.xml"), 'w') as xmlFile:
    print("Writing manifest...")
    xmlFile.writelines("%s\n" % line for line in tToWrite)
print("Done!")

#create zip file (Scorm package)
with ZipFile(movieName+'_'+sectionName+'_SCORM_'+date.today().strftime("%d%b%Y")+'.zip', 'w') as zipObj:
    print("Writing .zip...")
    for fDir, f in zip(listOfFiles, lOfFiles):
        zipObj.write(fDir, f)
print("Done!")
