#!/usr/bin/env python3
from lib2to3.pgen2.token import COMMENT
from tkinter.tix import NoteBook
import urllib.request
import urllib.parse
import urllib.error
from xml.etree.ElementTree import Comment
from bs4 import BeautifulSoup

# ? Site scrubber, to write online novels to notepad/word/whatever for offline reading
# ? It goes over each site page chapter and creates new chapters, and continues to next webpage(aka next chapter) until there're no more chapters
# ? Maybe add an update feature if the book isn't finished, so it captures new chapters and send a notification when a new chapter is out and written
# ? Potentially, also have it work for graphic novels to save the pictures
# ? Could have a shell script that runs the program each day/week, with arguments that define the book and/or website
# ? Maybe choose which file to write to using the arguments in the shell script
# ? Must keep track of which chapter it is up to (use JSON file?), so as to only add new chapters to the offline file, and not duplicate already read and written chapters.
# ? Some way of roughly evaluating how big the file will be once the program has file has been written. (Prompt user?) Potentially no as this may get in the way of automating in the shell script

# ! variable 'url' below won't work as the website itself is blocking the request.  FIgure out workaround, once a basic webscraper is working on sites that do allow it
url = 'https://novelfull.com/reverend-insanity/chapter-323.html'
testUrl = 'https://beautiful-soup-4.readthedocs.io/en/latest/#making-the-soup'

fhand = urllib.request.urlopen(testUrl).read()
soup = BeautifulSoup(fhand, 'html.parser')
# for line in fhand:
#    print(line.decode().strip())

pTags = soup('h1')          # finds only selected elements eg. 'h1'
for tags in pTags:          # iterate line by line through site
    print(tags.get_text())  # print only the text of the selected element

# print(pTags.get_text())
# print(fhand.read())
