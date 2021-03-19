import tokenStreamer
from nltk.stem import PorterStemmer
import collections
import blockHandler
import time
import helperMod
from pathlib import Path
import sys
import os

#module global index output block file
termsToBlockFile = 0

#block size from input
blockSize = 0

#================= Functions ===================
def getTokensPerBlock(blkSize):
    recTkStrm = []
    tokenDocPair = []
    for i in range(blkSize):
        tokenDocPair = tokenStreamer.getTokenDocPair()
        if (tokenDocPair != None):
            recTkStrm.append(tokenDocPair)
    #print(recTkStrm)
    return recTkStrm
    

def getTermIndex(recTokenStrm):
    termIndex = {}    
    ps = PorterStemmer()
    term = ''
    for i in recTokenStrm: #i is [token (index 0), docID (index 1)]
        #perform stemming
        term = ps.stem(i[0])
        #build index
        if term not in termIndex:
            termIndex[term] = [i[1]]
        else:
            termIndex[term].append(i[1])        
    
    #sort the index (dictionary by key)
    orderedDict = collections.OrderedDict(sorted(termIndex.items()))
    termIndex = dict(orderedDict)
    #print(termIndex)
    return termIndex



def storeIndexInBlocks(blkNum):
    recTokenStream = []
    termIndexTemp = {}
    fileName = ''
    global termsToBlockFile
    #while tokens are available from the tokenizer
    while(tokenStreamer.areTokensAvail()):
        #1. Get a stream (list of <token, docID> pairs)
        recTokenStream = getTokensPerBlock(blkNum)
        #print(recTokenStream)        
        #print('len of received token stream ', len(recTokenStream))
        #print('\n')

        #2. Build index
        termIndexTemp = getTermIndex(recTokenStream)         
        termsToBlockFile += 1
        fileName = 'out_termsToBlk' + str(termsToBlockFile) + '.txt'

        #3. Output to disk
        blockHandler.writeTermsToBlockFile(termIndexTemp, fileName)
        #print(termIndexTemp)
        #print('\n')
        
def noOfIndexedBlocks():
    global termsToBlockFile
    return termsToBlockFile
        

#================End of Functions ==============

#PROGRAM INPUT HANDLER
#get path to files
#print('Please key in directory to the input text files')
#inputPath = input()
inputPath = sys.argv[1]
print('<Echo> Path to Input Dataset: ' + inputPath)


#get block size for SPIMI algorithm
#print('Please specify the block size for SPIMI algorithm')
#blockSize = int(input())
blockSize = int(sys.argv[2])
print('<Echo> SPIMI Block Size: ' + str(blockSize))

#handle invalid input
#handle invalid path
givenPath = Path(inputPath)
if((givenPath.exists()) == False):
    print('Invalid given directory of input dataset. Nothing to do. Program ends.')
    sys.exit()
    
#handle zero block size
if(blockSize <= 0):
    print('Given SPIMI block size is invalid (less than or equal to 0). Nothing to do. Program ends.')
    sys.exit()


#0.Initialization
#Initialise working directory
helperMod.initWorkingDir(inputPath)
#Clean output files from previous run if any
helperMod.cleanPrevOutputFiles()
#Initialise tokenStreamer
tokenStreamer.initTokenStreamer(helperMod.getWorkingDir())

#1.Get tokens, index and store in blocks
start = time.time()
storeIndexInBlocks(blockSize)
end = time.time()


#2.Merge and sort created blocks in step 1 
start1 = time.time()
blockHandler.mergeBlockFiles()
end1 = time.time()


#3.Pretty print Output Inverted Index file
helperMod.prettyPrintDictFile('out_SPIMI_Output_Raw.txt', 'out_SPIMI_Output.txt')
print('Inverted index is created. Please find it in the file, out_SPIMI_Output.txt under the directory ' + inputPath) 

#4.Output time statistics file
#print('Time taken to index block size ' + str(blockSize) + ' is ' + str(end - start) + ' seconds')
#indexing blocks
helperMod.initTimeStatsFile(str(blockSize))
helperMod.storeTimeStatistics('Total number of indexed blocks', str(noOfIndexedBlocks()))
helperMod.storeTimeStatistics('Total time taken to index all blocks (in seconds)', str(end-start))
helperMod.storeTimeStatistics('Averge Time taken to index a block (in seconds)', str((end-start)/noOfIndexedBlocks()))

#merging blocks
helperMod.storeTimeStatistics('Total number of merged blocks', str(blockHandler.noOfMergedBlocks())) 
#print('Time taken to merge block size ' + str(blockSize) + ' is ' + str(end1 - start1) + ' seconds')
helperMod.storeTimeStatistics('Total time taken to merge all created blocks (in seconds)', str(end1-start1))
helperMod.storeTimeStatistics('Averge Time taken to merge two blocks (in seconds)', str((end1-start1)/blockHandler.noOfMergedBlocks()))
helperMod.storeTimeStatistics('Total time taken to create the inverted index (in seconds)', str((end-start)+(end1-start1)))
print('Time statistics file is created. Please find the file, out_timeStats4BlkSz' + str(blockSize) + '.txt ' + 'under the directory ' + inputPath) 

#5.Deinitialization
helperMod.deinitOpenFiles()
    
