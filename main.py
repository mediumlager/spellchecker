#!/usr/bin/env python3

import os
import sys
import re
import platform

from textblob import Word # used for actual spell check
import PyPDF2
import getch

def read_pdf(filename):
    lines = []
    fileobj = open(filename,'rb')
    filereader = PyPDF2.PdfFileReader(fileobj)
    for i in range(filereader.numPages):
        page = filereader.getPage(i)
        text = page.extractText().split(" ")
        line = []
        for j in range(len(text)):
            line.append(text[j])
        lines.append(line)
    return lines

def read_file(filename):
    if os.path.isfile(filename):
        with open(filename,'r') as f:
            lines = f.readlines()
            f.close()
            # Split lines in to words
            lines = [d.split() for d in lines]
        return lines
    else:
        print('File does not exist')

def check_spelling(line, type):
    accepted_answers = ['Y','n','new']
    words = [word.lower() for word in line]
    words = [word for word in line]
    # remove punctuation
    words = [re.sub(r'[^\w\s]','',word) for word in words]
    for i in range(len(words)):
        answer = ''
        # Check spelling
        correct = Word(words[i]).spellcheck()
        if words[i] != correct[0][0]:
            print('Word:    >',words[i],'<   is probably incorrect,')
            print('         Correct spelling: ',correct[0][0])
            print('         Confidence: ',correct[0][1])

            if type == '.txt':
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
            elif type == '.pdf':
                getch.pause('   Press the anykey to continue.')
    return words


arguments = sys.argv

print('Given path: ',str(arguments[1]))
type = os.path.splitext(arguments[1])[1]
if type == '.pdf':
    print("Note: .pdf file can't be changed, correct words will be listed instead.")
    lines = read_pdf(str(arguments[1]))

if type == '.txt':
    lines = read_file(str(arguments[1]))
# If file was opened correctly
if lines is not None:
    if type == '.txt':
        for i in range(len(lines)):
            lines[i] = check_spelling(lines[i], type)
    else:
        for i in range(len(lines)):
            check_spelling(lines[i],type)
# File does not exit, end program
else:
    sys.exit()
# In this case replace the correct spelling
if int(arguments[2]) == 1 and type != '.pdf':
    f = open(arguments[1],'w')
    for line in lines:
        f.write(' '.join(line))
        f.write('\n')
    f.close()
