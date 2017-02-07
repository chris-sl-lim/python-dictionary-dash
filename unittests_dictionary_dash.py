# -*- coding: utf-8 -*-
"""
Dictionary Dash Junior - unit tests
Created on Thu Nov  3 13:22:37 2016

@author: Chris Lim
"""

#import modules
import unittest
from dictionary_dash import main

# dictionary_dash.main('hog','cog','dictionary_test.txt', 1)

class DictionaryDashTestCases(unittest.TestCase):
    """Tests for `dictionary_dash.main()`."""
    # preparing to test
    def setUp(self):
        """ Setting up for the test """
        print('---------------------------------------------\n')
        print('STARTING TEST...')

    def test_emptyStartWord(self):
        print('Pass empty start word')
        startWord = ''
        endWord = 'cog'
        dictionaryPath = 'dictionary_test.txt'
        self.assertFalse((main(startWord, endWord, dictionaryPath, 0)))
        
    def test_integerStartWord(self):
        print('Pass non-string start word')
        startWord = 4
        endWord = 'cog'
        dictionaryPath = 'dictionary_test.txt'
        self.assertFalse((main(startWord, endWord, dictionaryPath, 0)))
        
    def test_nonAlphabeticStartWord(self):
        print('Pass non-alphabetic start word')
        startWord = '4'
        endWord = 'cog'
        dictionaryPath = 'dictionary_test.txt'
        self.assertFalse((main(startWord, endWord, dictionaryPath, 0)))        
        
    def test_emptyEndWord(self):            
        print('Pass empty end word')
        startWord = 'cog'
        endWord = ''
        dictionaryPath = 'dictionary_test.txt'
        self.assertFalse((main(startWord, endWord, dictionaryPath, 0)))
        
    def test_integerEndWord(self):
        print('Pass non-string end word')
        startWord = 'hit'
        endWord = 4
        dictionaryPath = 'dictionary_test.txt'
        self.assertFalse((main(startWord, endWord, dictionaryPath, 0)))
        
    def test_nonAlphabeticEndWord(self):
        print('Pass non-alphabetic end word')
        startWord = 'hit'
        endWord = '4'
        dictionaryPath = 'dictionary_test.txt'
        self.assertFalse((main(startWord, endWord, dictionaryPath, 0)))  
        
    def test_emptyDictionary(self):
        print('Pass empty dictionary')
        startWord = 'cog'
        endWord = 'dog'
        dictionaryPath = 'dictionary_test_empty.txt'
        self.assertFalse((main(startWord, endWord, dictionaryPath, 0)))
        
    def test_mismatchWords(self):
        print('Pass mismatching words')
        startWord = 'cogff'
        endWord = 'dog'
        dictionaryPath = 'dictionary_test.txt'
        self.assertFalse((main(startWord, endWord, dictionaryPath, 0)))
        
    def test_noPath(self):
        print('Pass no path case')
        startWord = 'hit'
        endWord = 'hfx'
        dictionaryPath = 'dictionary_test.txt'
        self.assertFalse((main(startWord, endWord, dictionaryPath, 0)))
        
    def test_irrelevantDictionary(self):
        print('Pass irrelevant dictionary')
        startWord = 'bgf'
        endWord = 'hfg'
        dictionaryPath = '10k_dictionary_4letter.txt'
        self.assertFalse((main(startWord, endWord, dictionaryPath, 0)))

    def test_dictionaryPathInvalid(self):
        print('Pass invalid dictionary path')
        startWord = 'bgf'
        endWord = 'hfg'
        dictionaryPath = 'i_dont_exist.txt'
        with self.assertRaises(FileNotFoundError):
            main(startWord, endWord, dictionaryPath, 0)
        
    def test_exampleCase(self):
        print('Pass case given in original task description')
        startWord = 'hit'
        endWord = 'cog'
        dictionaryPath = 'dictionary_test.txt'
        self.assertTrue((main(startWord, endWord, dictionaryPath, 0)))
        
    def test_10k_dictionary_3letters(self):
        print('Pass 3 letter case - 10k dictionary')
        startWord = 'gsx'
        endWord = 'cod'
        dictionaryPath = '10k_dictionary_3letter.txt'
        self.assertTrue((main(startWord, endWord, dictionaryPath, 0)))
        
    def test_10k_dictionary_4letters(self):
        print('Pass 4 letter case - 10k dictionary')
        startWord = 'nuyd'
        endWord = 'cgua'
        dictionaryPath = '10k_dictionary_4letter.txt'
        self.assertTrue((main(startWord, endWord, dictionaryPath, 0)))
        
    def test_10k_dictionary_5letters(self):
        print('Pass 5 letter case - 10k dictionary')
        startWord = 'rocyv'
        endWord = 'otvqk'
        dictionaryPath = '10k_dictionary_5letter.txt'
        self.assertTrue((main(startWord, endWord, dictionaryPath, 0)))        

if __name__ == '__main__':
    unittest.main()