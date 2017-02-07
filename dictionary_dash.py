# -*- coding: utf-8 -*-
'''
Dictionary Dash Junior
Created on Tue Nov  1 17:18:50 2016

ARGUMENTS:
startWord is a string consisting of start word
endWord is a string consisting of end word
dictionaryPath is the filename+path to the dictionary
printSteps is 0 or 1 and indicates whether to print out summary at each step

@author: Chris Lim
'''

def main(startWord, endWord, dictionaryPath, printSteps):

    # library import
    import dictionary_dash_lib
    from timeit import default_timer as timer
    
    getWordDoS = dictionary_dash_lib.getWordDoS
    returnWordPath_idx = dictionary_dash_lib.returnWordPath_idx
    startTime = timer()
    
    # read in dictionary and strip newline indicators
    fo = open(dictionaryPath, 'r')
    dictionary = []
    for line in fo.readlines():
        dictionary.append(line.strip('\n'))
    fo.close()
    
    print('\n-------------------------------------------------------\n')
    print('filename: {0}, word count: {1}'.format(fo.name, len(dictionary)))
    print('dictionary loaded\n'.format(len(dictionary)))
       
    # define loop condition and errorFlag
    keepGoing = True
    errorFlag = False
    
    # basic input validation and error checks
    # check that start word, end word and dictionary aren't empty and are strings
    if not(startWord) or type(startWord) != str or not(startWord.isalpha()):
        keepGoing = False
        errorFlag = True
        print('start word is empty or not a string or is non-alphabetic')
    if not(endWord) or type(endWord) != str or not(endWord.isalpha()):
        keepGoing = False
        errorFlag = True
        print('end word is empty or not a string or is non-alphabetic')
    if not(dictionary) or any(item.isalpha() == False for item in dictionary):
        keepGoing = False
        errorFlag = True
        print('dictionary is empty or contains non-alphabetic characters')   
         
    # check that start word and end word are the same length
    if errorFlag == False:        
        # get word length and key length (wordLength-1)
        wordLength = len(startWord)
        keyLength = wordLength - 1
        
        if len(startWord) != len(endWord):
            keepGoing = False
            errorFlag = True
            print('Start and end words are not the same length')      
            
        # remove all non-relevant words in the dictionary
        print('cleaning dictionary...')
        toRemove = [i for i,x in enumerate(dictionary) if len(x) != wordLength]
        for i in sorted(toRemove, reverse=True):
            del dictionary[i]    
        # check there are still words in the dictionary
        if not(dictionary):
            keepGoing = False
            errorFlag = True
            print('dictionary is now empty')
            print('dictionary does not contain relevant words to start and end words\n')
        else:
            print('dictionary contains {0} relevant words\n'.format(len(dictionary)))
        
    
    # housekeeping (check if start and end words are in dictionary, add if not)
    startWord_idx = 0
    endWord_idx = 0
    if startWord in dictionary:
        print('start word found')
        startWord_idx = dictionary.index(startWord)
    else:
        print('start word not found, adding to dictionary')
        startWord_idx = len(dictionary)
        dictionary.append(startWord)
        
        
    if endWord in dictionary:
        print('end word found')
        endWord_idx = dictionary.index(endWord)
    else:
        print('end word not found, adding to dictionary')
        endWord_idx = len(dictionary)
        dictionary.append(endWord)
        
    # create stacks for processing priority (and add start word)
    tierStack_idx = [startWord_idx]
    tierStack_ParentStep = [0]
    nextTierStack_idx = []
    nextTierStack_ParentStep = []
    nextTierStack_EndWordDoS = []
    
    # initialise counters, set error flag
    stepNo = 0
    tierLevel = 1
    
    # record status of each move
    statusStepNo = []
    statusNodeVisited = []
    statusStepOfParent = []
    statusTier = []
    statusNoOfChildren = []
    
    # time to start the recursive loop
    if keepGoing:
        print('\nstarting the loop \n')
    else:
        print('\nsome error found - exit program')
    
    # main iterative loop
    while keepGoing:
        
        #read indexes of current word and parent in dictionary
        currentIDX = tierStack_idx[0]
        parentStepNo = tierStack_ParentStep[0]
    
        # construct word path back through decision tree
        currentWordPath_idx = returnWordPath_idx(tierLevel, currentIDX, 
                                                 parentStepNo, statusNodeVisited, 
                                                 statusStepOfParent)
                
        # get current word to end word DoS
        currentToEndDoS = getWordDoS(endWord, dictionary[currentIDX])
                                     
        # print some stuff to show we're doing stuff
        if printSteps > 0:
            print('-------------------------------------')
            print('step number: {0} \n'.format(stepNo))
            print('current word: {0}'.format(dictionary[tierStack_idx[0]]))
            print('Current tier: {0}'.format(tierLevel))
            print('Current DoS to end word: {0}'.format(currentToEndDoS))
    

        
        # find children of current words (but discount words in wordpath, set to -1)
        # build DoS from current word to each word in dictionary
        currentToDictionaryDoS = []
        for i in range(0, len(dictionary)):
            if i in currentWordPath_idx:
                currentToDictionaryDoS.append(-1)
            else:
                currentToDictionaryDoS.append(getWordDoS(dictionary[i], 
                                                         dictionary[currentIDX]))
                
        # from this list, get the valid moves (where DoS == keyLength)
        validMoves = [i for i,x in enumerate(currentToDictionaryDoS)if x==keyLength]
    
        # look at the children (valid moves) and see if end word is amongst them
        if endWord_idx in validMoves:
            # we've found the word!
            if printSteps > 0:
                print('Hoorah, job done! End word found amongst children')
            
            # update status block with values
            statusStepNo.append(stepNo)
            statusNodeVisited.append(currentIDX)
            statusStepOfParent.append(parentStepNo)
            statusTier.append(tierLevel)
            statusNoOfChildren.append(len(validMoves))
            
            # clear stack which should end the loop
            tierStack_idx.clear()
            tierStack_ParentStep.clear()
            keepGoing = False
            
            # add 'last move' to statusblock as we won't iterate again
            statusStepNo.append(stepNo+1)
            statusNodeVisited.append(endWord_idx)
            statusStepOfParent.append(stepNo)
            statusTier.append(tierLevel+1)
            statusNoOfChildren.append(-1)
            
        else:
            # move on to the next word
            # only add children to the stack that get us closer to the end goal
            for item in validMoves:
                validMovesToEndDoS = getWordDoS(dictionary[item], endWord)
                if validMovesToEndDoS >= currentToEndDoS:
                    nextTierStack_idx.append(item)
                    nextTierStack_ParentStep.append(stepNo)
                    nextTierStack_EndWordDoS.append(validMovesToEndDoS)
                    
            # pop first item in stack
            tierStack_idx.pop(0)
            tierStack_ParentStep.pop(0)
            if printSteps > 0:
                print('\npopping items from tierStack...')
                print('items in tierStack: {0}'.format(len(tierStack_idx)))
                print('items in nextTierStack: {0}'.format(len(nextTierStack_idx)))
            
            # update status block with values
            statusStepNo.append(stepNo)
            statusNodeVisited.append(currentIDX)
            statusStepOfParent.append(parentStepNo)
            statusTier.append(tierLevel)
            statusNoOfChildren.append(len(validMoves))
            
            # if tierStack is now empty, we can move to next tier
            if not tierStack_idx:
                if not nextTierStack_idx:
                    # if nextTierStack is empty then we're out of moves
                    keepGoing = False
                    errorFlag = True
                    if printSteps > 0:
                        print('We are out of moves - exiting loop')
                                    
                else:
                    # if some options in the next tier are better, remove the others
                    # get index of values to remove
                    toRemove = [i for i,x in enumerate(nextTierStack_EndWordDoS) if x < max(nextTierStack_EndWordDoS)]
                                
                    # remove values that aren't closer to the answer
                    for i in sorted(toRemove, reverse=True):
                        del nextTierStack_idx[i]
                        del nextTierStack_ParentStep[i]
                        del nextTierStack_EndWordDoS[i]
    
                    # move nextTierStack values to tierStack
                    tierStack_idx = tierStack_idx + nextTierStack_idx
                    tierStack_ParentStep = tierStack_ParentStep + nextTierStack_ParentStep
                    
                    # clear nextTierStack
                    nextTierStack_idx.clear()
                    nextTierStack_ParentStep.clear()
                    nextTierStack_EndWordDoS.clear()
                    
                    # increment tierLevel
                    tierLevel = tierLevel+1
                    
                    # if tierLevel > len(dictionary) - we're in trouble
                    if tierLevel > len(dictionary):
                        keepGoing = False
                        errorFlag = True
                        if printSteps > 0:
                            print('We are out of moves - exiting loop')
                        
                        
            # end if statement 
                        
        # increment stepNo
        stepNo = stepNo + 1
        if printSteps > 0:
            print('\nending step number {0}'.format(stepNo))
        
    #end while loop
    endTime = timer()
    
    # if we've ended loop and errorFlag = False then we have a path
    # if this is the case then print summary - else don't bother
    if errorFlag == False:
        # reconstruct wordPath by popping last values of status vectors
        finalIndex = statusNodeVisited.pop()
        finalParentStepNo = statusStepOfParent.pop()
        finalTier = statusTier.pop()
    
        currentWordPath_idx = returnWordPath_idx(finalTier, finalIndex, 
                                                 finalParentStepNo, 
                                                 statusNodeVisited, 
                                                 statusStepOfParent)
        
        # flip currentWordPath to go start to finish
        currentWordPath_idx.reverse()
        currentWordPath = []
        
        for idx in currentWordPath_idx:
            currentWordPath.append(dictionary[idx])
            
        # print the result
        print('\n \nSummary:')
        print('Path found: {0}'.format(currentWordPath))
        print('Path length: {0}'.format(tierLevel))
        print('Number of steps required: {0}'.format(stepNo))
        print('Execution time: {0:6f} seconds'.format(endTime - startTime))
        
    else:
        # print summary of how far we got
        # print the result
        print('\n \nSummary:')
        print('No path found')
        print('Number of tiers searched: {0}'.format(tierLevel))
        print('Number of steps taken: {0}'.format(stepNo))
        print('Execution time: {0:6f} seconds'.format(endTime - startTime))
            
        # create empty currentWordPath to return
        currentWordPath = []
    
    print('program finished')    
    return currentWordPath
    
        
        
        
                
                

                            
                
            
        
        
        
            




    
    
    

    





