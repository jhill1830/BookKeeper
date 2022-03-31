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

# ? ----------------- INPUTS -----------------
url = 'https://novelfull.com/reverend-insanity/chapter-323.html'
testUrl = 'https://beautiful-soup-4.readthedocs.io/en/latest/#making-the-soup'

# TODO Maybe figure out a way to dynamically change the file name based on the sites book.  (Use h1 tag?)
bookFile = 'file.txt'

# ? ----------------- File/URL Reading -----------------
# ! variable 'url' below won't work as the website itself is blocking the request.  Figure out workaround, once a basic webscraper is working on sites that do allow it
urlOpen = urllib.request.urlopen(testUrl).read()
soup = BeautifulSoup(urlOpen, 'html.parser')


# ? ----------------- WRITE TO FILE -----------------
def scrub(site, book):  # scrubbing function
    pTags = site('h1')  # finds only selected elements eg. 'h1'
    with open(book, 'w') as file:    # open file to write to
        for tags in pTags:           # iterate line by line through site
            line = tags.get_text()   # print only the text of the selected element
            file.write(line + '\n')  # write line to file and add newline
    with open(book, 'r') as file:
        print(file.read())


scrub(soup, bookFile)


# ? ----------------- UPDATE JSON -----------------
