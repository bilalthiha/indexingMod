import glob
import os
#module global to track previous closing bracket (])
isPrevCB = False
#global for misc file names
timeStatFlName = ''
timeStatFile = None
#global for block size
blkSize = 0

#================== Functions=======================
def initWorkingDir(inPath):
    global workingDir
    #change working directory
    os.chdir(inPath)
    workingDir = inPath

def getWorkingDir():
    global workingDir
    #return working direcotry to application
    return workingDir
    
def getSortedLargeList(flList):
    intFiles = []
    strFiles = []
    sortedFileList = []
    for i in flList:
        idx = i.index('.')
        if (i[:idx].isnumeric()):
            intFiles.append(int(i[:idx]))
        else:
            strFiles.append(i)
            
    #sort int files and save them as original string files
    intFiles.sort()
    for j in intFiles:
        sortedFileList.append(str(j) + '.txt')

    #sort str files
    strFiles.sort()
    sortedFileList = sortedFileList + strFiles
        
    return sortedFileList

def prettyPrintDictFile(srcDictFileName, descPrettyFileName):
    global isPrevCB
    curItem = ''
    modItem = ''    
    dictFile = open(srcDictFileName, 'r', encoding ='utf-8')
    finFile = open(descPrettyFileName, 'a', encoding ='utf-8')

    curItem = dictFile.read(1)
    while(curItem != ''):
        #print new lines per dict item, remove ugly characters
        curItem = dictFile.read(1)
        if(curItem == ']'):
            modItem = curItem + '\n'
            isPrevCB = True
        elif((curItem == '{') or (curItem == '}') or (curItem == ' ') or (curItem == ',' and isPrevCB == True)):
            modItem = ''
            isPrevCB = False
        else:
            modItem = curItem
            isPrevCB = False
        finFile.write(modItem)
    dictFile.close()
    finFile.close()

def cleanPrevOutputFiles():
    flName2Del = ''
    #get list of files with 'out_' prefix
    obsFileList = glob.glob("out_*.txt")
    #print(obsFileList)
    while (len(obsFileList) > 0):
        flName2Del = obsFileList.pop(0)
        os.remove(flName2Del)

def storeTimeStatistics(it, val):
    global timeStatFile
    global timeStatFlName
    global blkSize
    timeStatFlName = 'out_timeStats4BlkSz' + str(blkSize) + '.txt'
    timeStatFile = open(timeStatFlName, 'a', encoding ='utf-8')
    timeStatFile.write(it + ' : ' + val + '\n')

def initTimeStatsFile(blockSize):
    global blkSize
    blkSize = blockSize
    timeStatFlName = 'out_timeStats4BlkSz' + str(blkSize) + '.txt'
    timeStatFile = open(timeStatFlName, 'a', encoding ='utf-8')
    timeStatFile.write('SPIMI Block Size' + ' : ' + blockSize + '\n' )    
    
def deinitOpenFiles():
    global timeStatFile
    timeStatFile.close()
    
#================== End of Functions================
