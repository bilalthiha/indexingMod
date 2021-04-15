import glob
import os
import ast
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
    
def printOutputFile(srcFileName, descFileName): #document frequency + unique docIds [doc_freq, docId1, docId2, ... , docIdN]
    curLine = 'init'
        
    inFile = open(srcFileName, 'r', encoding ='utf-8')
    outFile = open(descFileName, 'a', encoding ='utf-8')

    while(curLine != ''):
        term = ''
        frequency = 0
        docIdListRaw = []
        docIdList = []
        prevId = -1 #invalid doc Id num for initialization
        freqDocIdList = []
        modLine = ''
        docIdDict = {}
        
        #read a line from the input file
        curLine = inFile.readline()
        
        if (curLine != ''):
            #get dictionary key
            term = curLine[:curLine.index(':')]
            
            #get doc ID list
            docIdListRaw = ast.literal_eval(curLine[(curLine.index(':')+ 1):])
            
            #parse covert string doc ID list into int doc ID
            for i in docIdListRaw: 
                docIdList.append(int(i[:i.index('.txt')]))
                
            #count docIds (doc frequency) and unique-fy docIds
            for j in docIdList:
                if j in docIdDict.keys():
                    docIdDict[j] = docIdDict[j] + 1
                else:
                    docIdDict[j] = 1

            for k in docIdDict.keys():
                freqDocIdList.append(k)

            for v in docIdDict.values():
                frequency += v                
                
                
            #doc frequency is index 0
            freqDocIdList.insert(0, frequency)
            
            #prepare and write line to output file
            modLine = term + ':' + str(freqDocIdList) + '\n'
            outFile.write(modLine)
            
    inFile.close()
    outFile.close()
    
def printOutputFileForRanking(srcFileName, descFileName, docSize): #document frequency + unique <termFreq, docId> pairs [doc_freq, termFreq1, docId1, termFreq2, docId2, ... , termFreqN, docIdN]
    curLine = 'init'
        
    inFile = open(srcFileName, 'r', encoding ='utf-8')
    outFile = open(descFileName, 'a', encoding ='utf-8')
    outFile.write('Total documents:' + docSize + '\n')

    while(curLine != ''):
        term = ''
        frequency = 0
        docIdListRaw = []
        docIdList = []
        prevId = -1 #invalid doc Id num for initialization
        freqDocIdList = []
        modLine = ''
        docIdDict = {}
        
        #read a line from the input file
        curLine = inFile.readline()
        
        if (curLine != ''):
            #get dictionary key
            term = curLine[:curLine.index(':')]
            
            #get doc ID list
            docIdListRaw = ast.literal_eval(curLine[(curLine.index(':')+ 1):])
            
            #parse covert string doc ID list into int doc ID
            for i in docIdListRaw: 
                docIdList.append(int(i[:i.index('.txt')]))
                
            #count docIds (doc frequency) and unique-fy docIds
            for j in docIdList:
                if j in docIdDict.keys():
                    docIdDict[j] = docIdDict[j] + 1
                else:
                    docIdDict[j] = 1

            for k,v in docIdDict.items():                
                freqDocIdList.append(v) #append term frequency for each docId
                freqDocIdList.append(k)

            for v in docIdDict.values():                
                frequency += v     
            
            #doc frequency is index 0
            freqDocIdList.insert(0, frequency)
            
            #prepare and write line to output file
            modLine = term + ':' + str(freqDocIdList) + '\n'
            outFile.write(modLine)
            
    inFile.close()
    outFile.close()

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
