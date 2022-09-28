#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re

from textblob import Word # used for actual spell check

def read_file(filename):
    if os.path.isfile(filename):
        with open(filename,'r') as f:
            data = f.readlines()
            f.close()
            # Split lines in to words
            data = [d.split() for d in data]
        return data
    else:
        print('File does not exist')

def check_spelling(line):
    print(line)
    accepted_answers = ['Y','n','new']
    #words = [word.lower() for word in line]
    words = [word for word in line]
    # remove punctuation
    #words = [re.sub(r'[^\w\s]','',word) for word in words]
    for i in range(len(words)):
        answer = ''
        # Check spelling
        correct = Word(words[i]).spellcheck()
        if words[i] != correct[0][0]:
            print('Word: ',words[i],', is probably incorrect,')
            print('Confidence: ',correct[0][1],' \nCorrect spelling: ',correct[0][0])
            # Ask user if they want to change the word
            while answer not in accepted_answers:
                answer = input(
                'Do you want to autocorrect the spelling (Y/n) or'+
                'replace with new word (new)?')
                if answer == 'Y':
                    words[i] = correct[0][0]
                    continue
                elif answer == 'new':
                    words[i] = input('New word: ')
                    continue
                elif answer == 'n':
                    continue
    return words


arguments = sys.argv

print('Given path: ',str(arguments[1]))
lines = read_file(str(arguments[1]))
if lines is not None:
    for i in range(len(lines)):
        lines[i] = check_spelling(lines[i])

# In this case replace the correct spelling
if int(arguments[2]) == 1:
    f = open(arguments[1],'w')
    for line in lines:
        f.write(' '.join(line))
        f.write('\n')
    f.close()
