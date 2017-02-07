# -*- coding: utf-8 -*-
"""
Dictionary Dash Junior
Created on Tue Nov  1 18:29:37 2016

@author: Chris Lim
"""
def getWordDoS( word1, word2):
    # return degree of similarity for word1 and word2
    DoS = sum(1 for a, b in zip(word1, word2) if a == b)
    return DoS
    
def returnWordPath_idx(tierLevel, currentIDX, currentParentStepNo, statusNodeVisited, statusStepOfParent):
    # go back through status arrays and reconstruct wordPath
    currentWordPath_idx = [currentIDX]
    nextStepNo = currentParentStepNo
    if tierLevel > 1:
        for i in range(1,tierLevel):
            currentWordPath_idx.append(statusNodeVisited[nextStepNo])
            nextStepNo = (statusStepOfParent[nextStepNo])
            
    return currentWordPath_idx
    
    
