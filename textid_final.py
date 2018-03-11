#
# textmodel.py
#
# TextModel project!
#
# name(s): Alice Chi
#

from collections import defaultdict
import string
from porterstemmer import create_stem
import math

PUNCTUATION = ['.', '!', '?']

TextModel1 = [ ]       # start with the empty list

words1 = {}            # default dictionary for counting words 
TextModel1 +=  [ words1 ]        # add that dictionary in...

wordlengths1 = {}      # default dictionary for counting wordlengths
TextModel1 +=  [ wordlengths1 ]  # add that dictionary in...

stems1 = {}            # default dictionary for counting stems
TextModel1 +=  [ stems1 ]        # add that dictionary in...

sentencelengths1 = {}  # default dictionary for counting sentence lengths
TextModel1 +=  [ sentencelengths1 ]  # add that dictionary in...

# create another of your own...
punctuation1 = {}       # default dictionary for counting punctuation
TextModel1 +=  [ punctuation1 ]    # add that dictionary in...

# a function to print all of the dictionaries in a TextModel1

def printAllDictionaries( TM ):
    """ a function to print all of the dictionaries in TM
        input: TM, a text model (a list of 5 or more dictionaries)
    """
    words = TM[0]
    wordlengths = TM[1]
    stems = TM[2]
    sentencelengths = TM[3]
    punct = TM[4]

    print("\nWords:\n", words)
    print("\nWord lengths:\n", wordlengths)
    print("\nStems:\n", stems)
    print("\nSentence lengths:\n", sentencelengths)
    print("\nPunctuation:\n", punct)
    print("\n\n")


# include other functions here...

def readTextFromFile(filename):
    ''' take stext from a file and returns it as a string
    '''
    f1 = open(filename, 'r') #open file
    s = f1.read() #read file and save as string 'file'
    f1.close() #close file
    s.strip('\n') #gets rid of line breaks in the string
    return s

def cleanString(s):
    ''' takes in a string and removes punctuation and uppercase letters
    '''
    newstring = s.lower()

    for p in string.punctuation:
        newstring = newstring.replace(p,'')
    return newstring

def makeSentenceLengths(s):
    ''' returns dictionary of the occurance of sentence lengths
    '''

    wordlist = s.split()
    counter = 0
    D = {}

    for i in range(len(wordlist)):
        if wordlist[i][-1] in PUNCTUATION:
            counter += 1
            if counter in D:
                num = D[counter]
                D[counter] = num + 1
            else:
                D[counter] = 1
            counter = 0
        else:
            counter += 1
    return D

def makeWords(s):
    ''' Saves what words are used and their frequency in a dictionary
    '''
    cleanS = cleanString(s)
    wordlist = cleanS.split()
    D = {}

    for i in range(len(wordlist)):
        key = wordlist[i]
        if key in D:
            num = D[key]
            D[key] = num + 1
        else:
            D[key] = 1

    return D

def makeWordLengths(s):
    ''' Saves the length of the words used and their frequency in a dictionary
    '''
    cleanS = cleanString(s)        
    wordlist = cleanS.split()
    D = {}

    for i in range(len(wordlist)):
        key = len(wordlist[i])
        if key in D:
            num = D[key]
            D[key] = num + 1
        else:
            D[key] = 1

    return D

def makeStems(s):
    ''' Saves the frequency of stems used in a dictionary
    '''
    cleanS = cleanString(s)
    wordlist = cleanS.split()
    D = {}
    
    for i in range(len(wordlist)):
        key = create_stem(wordlist[i])
        if key in D:
            num = D[key]
            D[key] = num + 1
        else:
            D[key] = 1

    return D

def makePunctuation(s):
    ''' Saves the frequency of the punctuation used in a dictionary
    '''
    wordlist = s.split()
    D = {}
    
    for i in range(len(wordlist)):
        key = wordlist[i][-1]
        if key in string.punctuation:
            if key in D:
                num = D[key]
                D[key] = num + 1
            else:
                D[key] = 1
    return D

def normalizeDictionary(d):
    ''' normalizes the dictionary to make all values add up to 1.0
    '''
    D = {}
    total = 0

    for k in d:
        total += d[k]

    for k in d:
        value = d[k]
        D[k] = value / total

    return D

def smallestValue(nd1, nd2):
    ''' returns the smallest value across two dictionaries
    '''
    min1 = min(nd1.values())
    min2 = min(nd2.values())

    return min(min1, min2)

def compareDictionaries(d, nd1, nd2):
    ''' find the log probability that d came from nd1 and nd2 and return both values
    '''
    nd1 = normalizeDictionary(nd1)
    nd2 = normalizeDictionary(nd2)
    total1 = 0.0
    total2 = 0.0
    epsilon = smallestValue(nd1, nd2) / 2

    #loop through nd1
    for k in d:
        value = d[k]
        if k in nd1:
            total1 += value*math.log(nd1[k])
        else:
            total1 += value*math.log(epsilon)

    #loop throug nd2
    for k in d:
        value = d[k]
        if k in nd2:
            total2 += value*math.log(nd2[k])
        else:
            total2 += value*math.log(epsilon)

    return [total1, total2]

def createAllDictionaries(s): 
    """ should create out all five of self's 
        dictionaries in full - for testing and 
        checking how they are working...
    """
    sentencelengths = makeSentenceLengths(s)
    new_s = cleanString(s)
    words = makeWords(new_s)
    stems = makeStems(new_s)
    punct = makePunctuation(s)
    wordslengths = makeWordLengths(new_s)
    return [words, wordslengths, stems, sentencelengths, punct ]

def compareTextWithTwoModels(newmodel, model1, model2):
    ''' chooses wich text model is a most likely match
    '''
    #words
    words = compareDictionaries(newmodel[0], model1[0], model2[0])

    #wordslength
    wordslengths = compareDictionaries(newmodel[1], model1[1], model2[1])

    #stems
    stems = compareDictionaries(newmodel[2], model1[2], model2[2])

    #sentence length
    sentencelengths = compareDictionaries(newmodel[3], model1[3], model2[3])

    #punct
    punct = compareDictionaries(newmodel[4], model1[4], model2[4])

    print("words: " + "vsTM1: " + str(words[0]) + ", vsTM2: " + str(words[1]))
    print("wordslength: " + "vsTM1: " + str(wordslengths[0]) + ", vsTM2: " + str(wordslengths[1]))
    print("stems: " + "vsTM1: " + str(stems[0]) + ", vsTM2: " + str(stems[1]))
    print("sentencelengths: " + "vsTM1: " + str(sentencelengths[0]) + ", vsTM2: " + str(sentencelengths[1]))
    print("punct: " + "vsTM1: " + str(punct[0]) + ", vsTM2: " + str(punct[1]))

    TM1 = [words[0], wordslengths[0], stems[0], sentencelengths[0], punct[0]]
    TM2 = [words[1], wordslengths[1], stems[1], sentencelengths[1], punct[1]]

    counter1 = 0
    counter2 = 0

    for i in range(len(TM1)):
        if TM1[i] > TM2[i]:
            counter1 += 1
        else:
            counter2 += 1

    print("\nModel 1 wins on " + str(counter1) + " features")
    print("Model 2 wins on " + str(counter2) + " features\n")

    if counter1 > counter2:
        print("Model 1 is the better match!")
    else:
        print("Model 2 is the better match!")



# and, test things out here...
#print("TextModel1:")
#printAllDictionaries( TextModel1 )