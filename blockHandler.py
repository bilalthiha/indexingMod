import os
import ast
import collections
import helperMod
import tokenStreamer

from pathlib import Path
from shutil import copyfile
#global file list for merge sort
mergeBlockList = []
#merged file num
mergedFileId = 0

#================== Functions=======================
def writeToBlockFile(termIdx, blFileName):    
    bFile = open(blFileName, 'w', encoding ='utf-8')
    bFile.write(str(termIdx))
    bFile.close()

def writeTermsToBlockFile(termIndex, blockFileName):
    writeToBlockFile(termIndex, blockFileName)
    mergeBlockList.append(blockFileName)    

def readABlockFile(blFileName):
    rFile = open(blFileName, 'r', encoding ='utf-8')
    content = rFile.read()
    rFile.close()
    #print(content)
    return content

def mergeTwoBlocksIntoOne(blockA, blockB):
    blockOut = blockA
    for k,v in blockB.items():
        if k not in blockOut.keys():
            blockOut[k] = v
        else:
            blockOut[k] = blockOut[k] + v

    #sort the index (dictionary by key)
    orderedDict = collections.OrderedDict(sorted(blockOut.items()))   
    blockOut = dict(orderedDict)

    #sort the posting list for each term in dictionary
    for k in blockOut.keys():
        blockOut[k] = helperMod.getSortedLargeList(blockOut[k])
        
    return blockOut

def mergeTwoBlockFiles():
    global mergedFileId
    
    bFileA = mergeBlockList.pop(0)
    bFileB = mergeBlockList.pop(0)
        
    index1 = ast.literal_eval(readABlockFile(bFileA))
    index2 = ast.literal_eval(readABlockFile(bFileB))
    mergedIndex = mergeTwoBlocksIntoOne(index1, index2)
    mergedFileId += 1
    mergedFileName = 'out_mergedFile' + str(mergedFileId) + '.txt'
    writeToBlockFile(mergedIndex, mergedFileName)
    mergeBlockList.append(mergedFileName)

    #The last remaining file is output of the SPIMI algorithm!
    if (len(mergeBlockList) == 1):
        copyfile(mergedFileName, 'out_SPIMI_Output_Raw.txt')
    

def mergeBlockFiles():
    #sanity check, at the start of requesting merge, merge block list should not be empty
    if (len(mergeBlockList) == 0):
        print('Nothing (0 files) to merge!')
        return
    else:
        #when there are more than 1 block file, merge those until 1 block file is left
        while (len(mergeBlockList) != 1):
            mergeTwoBlockFiles()
            
def noOfMergedBlocks():
    global mergedFileId
    return mergedFileId        
    
#================== End of Functions================
