import nltk
import os
import helperMod
from pathlib import Path
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

#module global token buffer
tokenBuffer = []
#module global file list
fileList = []
#module global current file
curDoc = ''

#================== Functions=======================
def getFileList(inPath):
    flList = os.listdir(inPath)
    #flList = glob.glob("*.txt")
    return flList
    
def getDocSize(inPath):
    fList = os.listdir(inPath)
    #flList = glob.glob("*.txt")
    return len(fList)

def initTokenStreamer(inPath):    
    #initialise and sort file list
    global fileList
    global tokenBuffer
    tokenBuffer = []
    fileList = getFileList(inPath)
    #used for safe sorting of large lists in ascending order
    #The simple built-in .sort() optimises on big lists of numeric-named files
    fileList = helperMod.getSortedLargeList(fileList)    

def getTokensFromAFile(fileName):
    #get token stream (list) from a file
    #open the file and get its contents
    curFile = open(fileName, 'r', encoding ='utf-8')
    content = curFile.read()
    #print(content)
    curFile.close()

    #tokenize content
    tkzr = RegexpTokenizer(r'\w+')
    tokenizedWords = tkzr.tokenize(content)
    #print("Tokenized words are: " + str(tokenizedWords))

    #remove stop words
    stopWords = set(stopwords.words("english"))
    filteredWords=[]
    for w in tokenizedWords:
        if w not in stopWords:
            filteredWords.append(w)
    #print("Filtered words are: " + str(filteredWords))
    #print(len(filteredWords))
         
    #return [token 1, token 2, ...., token n]
    tokenStream = filteredWords
    return tokenStream

def getTokenDocPair():
    global tokenBuffer
    global fileList
    global curDoc
    tokenDocPair = []
    #token buffer is empty but there are still files to read
    if ((len(tokenBuffer) == 0) and (len(fileList) > 0)):
        curDoc = fileList.pop(0)
        tokenBuffer = getTokensFromAFile(curDoc)

    if(len(tokenBuffer) > 0):
        tokenDocPair = [tokenBuffer.pop(0), curDoc]
    else: #nothing to load up from files
        tokenDocPair = None    

    #return token-doc pair
    return tokenDocPair
    

def areTokensAvail():
    #not available if both file list and token buffer are empty
    if((len(fileList) == 0) and (len(tokenBuffer) == 0)):
        return False
    else:
        return True

def getTokenStreamFile1():
    tk1Stream = getTokensFromAFile('1.txt')
    return tk1Stream

#================== End of Functions ===============
