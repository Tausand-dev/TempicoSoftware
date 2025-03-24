import os

version="1.1.0"

#Here update the constants.py
def updateVersion(fileName,versionNumber):
    with open(fileName,'r') as file:
        lineas = file.readlines()
    file.close()
    
    for i, linea in enumerate(lineas):
        if 'VERSION' in linea:
            lineas[i] = f"VERSION="+'"'+versionNumber+'"'+"\n"
    
    with open(fileName, 'w') as file:
        file.writelines(lineas)

def updateRelease(fileReleaseStory,fileRelease):
    
    with open(fileReleaseStory, 'r') as filea:
        newRelease= filea.read()
    
    with open(fileRelease,'r') as originalRelease:
        oldRelease = originalRelease.read()
        
    allcontent= newRelease+"\n"+oldRelease
    
    with open(fileRelease,'w') as originalRelease:
        originalRelease.write(allcontent) 


absolutePathConstants= os.path.abspath("src\\constants.py")

updateVersion(absolutePathConstants,version)

absolutePathNewRelease= os.path.abspath("src\\releaseStory.md")
absolutePathOldRelease= os.path.abspath("README.md")

updateRelease(absolutePathNewRelease,absolutePathOldRelease)



    