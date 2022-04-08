#!/usr/bin/env python3
from msilib import schema
from urllib.request import Request, urlopen
import urllib.parse
import urllib.error
import json
import sys
import time
import os
from bs4 import BeautifulSoup

# ? Site scrubber, to write online novels to notepad/word/whatever for offline reading
# ? It goes over each site page chapter and creates new chapters, and continues to next webpage(aka next chapter) until there're no more chapters
# ? Maybe add an update feature if the book isn't finished, so it captures new chapters and send a notification when a new chapter is out and written
# ? Potentially, also have it work for graphic novels to save the pictures
# ? Could have a shell script that runs the program each day/week, with arguments that define the book and/or website
# ? Maybe choose which file to write to using the arguments in the shell script
# ? Must keep track of which chapter it is up to (use JSON file?), so as to only add new chapters to the offline file, and not duplicate already read and written chapters.
# ? Some way of roughly evaluating how big the file will be once the program has file has been written. (Prompt user?) Potentially no as this may get in the way of automating in the shell script
# TODO might have to write something to automate the chapter names if that's part of the url in some chapters
# TODO sort the library JSON file books alphabetically
# TODO potentially rewrite the manner in which it goes to next chapter by looking for an <a> tag that includes text "Next Chapter". If it does, then copy page and then click link to next page.  Stop the program if there is no "Next Chapter" <a> tag.

# ? ----------------- INPUTS -----------------
# ! variable 'url' below won't work as the website itself is blocking the request.  Figure out workaround, once a basic webscraper is working on sites that do allow it
#       # Use shell argument to define url
url = 'https://bestlightnovel.com/novel_888108451/chapter_'
# testUrl = 'https://beautiful-soup-4.readthedocs.io/en/latest/#making-the-soup'
testUrl = 'https://www.webscrapingapi.com/python-web-scraping/'


# TODO Maybe figure out a way to dynamically change the file name based on the sites book.  (Use h1 tag? Use librabry.json file?)
bookTitle = sys.argv[1]     # Use shell argument 1
bookFile = bookTitle + '.txt'
libraryJson = 'library.json'
chaptersNum = sys.argv[2]   # Use shell argument 2. # of chapters to read up to
print(bookTitle)
#
#
#
#
#
#
#
#

# ? ----------------- Send Request -----------------


# TODO maybe rewrite the sendRequest function to check for valid url address/ address that has a proper book in it


def sendReq(site, tag):  # sendRequest function to connect and parse url which returns desired tag
    data = json.load(open(libraryJson, 'r'))
    # TODO change the recursion state so that it ends when it has reached the most recent chapter. Potentially when it tries to load a site that doesn't exist. EQ try: load page. except: close program.  Might have to search page text and if '#404' shows, then stop program. Otherwise, might just have to specify the number of chapters.
    if data['books'][bookTitle]['chapter'] <= int(chaptersNum):
        bookUrl = site + str(data['books'][bookTitle]['chapter'])  # + '.html'
        req = Request(bookUrl, headers={'User-Agent': 'Mozilla/5.0'})
        urlOpen = urlopen(req).read()
        soup = BeautifulSoup(urlOpen, 'html.parser')
        pTags = soup(tag)  # finds only selected tags eg. 'h1'
        return pTags

# ? ----------------- File/URL Reading -----------------


def scrub(site, bookfile):  # scrubbing function
    data = json.load(open(libraryJson, 'r'))
    if data['books'][bookTitle]['chapter'] <= int(chaptersNum):
        # ### Use if statement if chapter number on site is greater than in json file. Also check if it's a dummy page using number of characters in the sites p tag?
        # ? alternate. If <a>Next Chapter</a>: do stuff. Might need to use sendReq() to target <a> tag and only check for "Next Chapter"(if sendReq(site, 'a').getText() == 'Next Chapter': (will need to iterate through site due to multiple tags))
        # ### Return and finish executing program if there is nothing to update

        # TODO write if statements for book existence etc

        # # Could potentially use scrub as a recursive function where it increments the url number until it somes up with a blank site/placeholder site. eg replace the chapter number in url
        # ? If edited to click next chapter button.  Needs to check if valid url, and implement program if next chapter exists, then recur. (if nextChapter: writeBook(), updateChapter(), scrub(), return. else: return)

        data = json.load(open(libraryJson, 'r'))
        try:
            # Check if book exists in library
            # and data['books'][bookTitle]['chapter'] === currentChapter: NOTE: current chapter checked by url ending?
            # Since url is based off
            if data['books'][bookTitle]:
                print('Book Found')
                writeBook(bookfile, sendReq(site, 'p'), libraryJson)
                updateChapter(bookTitle, libraryJson)
                time.sleep(2)
                scrub(site, bookfile)
                return

        except:
            # IF book !exist: writeBook, updateChapter, updateLibrary
            updateLibrary(bookTitle, libraryJson)
            writeBook(bookfile, sendReq(site, 'p'), libraryJson)
            updateChapter(bookTitle, libraryJson)
            scrub(site, bookfile)
            return

    else:
        return

    # IF book exists and no new chapter to write: RETURN/close program

    # IF book exists and new chapter to write:

    # ELSE: return/close program if something unnexpected happens

#
#
#
#
#
#
#


# ? ----------------- WRITE TO FILE -----------------

def writeBook(bookfile, tag, jsonFile):  # write to file function.
    data = json.load(open(jsonFile, 'r'))  # Load in json
    chapter = data['books'][bookTitle]['chapter']  # Read chapter data
    os.getcwd()
    os.chdir(r'\Users\James Hillman\Documents\Books')

    # open file to write to.  The second param: 'r' -read, 'w' -write, 'a' -append
    with open(bookfile, 'a') as file:

        file.write('\t' + 'CHAPTER ' + str(chapter) + '\n'*2)
        for tags in tag:           # iterate line by line through site
            try:
                line = tags.get_text()   # print only the text of the selected element
                file.write(line + '\n'*2)  # write line to file and add newline
            except:  # Used to capture characters that can't be encoded.  EG katakana etc.
                continue
        file.write('\n'*2)
    os.chdir(r'C:\Users\James Hillman\Documents\Personal Repos\BookKeeper')


'''
Use the os.chdir() function.

>>> import os
>>> os.getcwd()
'/home/username'
>>> os.chdir(r'/home/username/Downloads')
>>> os.getcwd()
'/home/username/Downloads'

You can get the current working directory using the os.getcwd function. The os.chdir function changes the current working directory to some other directory that you specify. (one which contains your file) and then you can open the file using a normal open(fileName, 'r') call.
'''

#
#
#
#
#
#
#


# ? ----------------- UPDATE CHAPTER -----------------

def updateChapter(book, jsonFile):    # update file's chapter + 1
    # Load in external json file and create new object with it's data
    data = json.load(open(jsonFile, 'r'))
    print(data['books'][book]['chapter'])
    # Update targeted key's value in new 'data' json object
    data['books'][book]['chapter'] += 1  # Increment chapter by 1

    # Either write newfile or rewrite previous file(rewrite in this case) using the new 'data' json object
    with open(jsonFile, 'w') as writeFile:
        # .dump turn the data object into a string, as it can't write an object into the file. indent=4 causes it to have proper formatting in the output file
        json.dump(data, writeFile, indent=4)

    data = json.load(open(jsonFile, 'r'))

    print(data['books'][book]["chapter"])
    print("Updated " + book)
    return

#
#
#
#
#
#
#
#
#
#

# ? ----------------- UPDATE LIBRARY -----------------


# BUG: this functions will update the json file in the wrong format if used on a pre-existing key/entry.  But works properly if sed to create a new entry
def updateLibrary(book, jsonFile):  # Dunno if necessary. Might use a book list to reference so that if the book exists already, then append('a') to the corresponding file, otherwise, write('w') to new file
    data = json.load(open(jsonFile, 'r'))
    data['books'][book] = {'title': book, 'chapter': 1}

    with open(jsonFile, 'r+') as updateFile:
        json.dump(data, updateFile, indent=4)
    print('Added New Book: ' + book)
    return


# Might need to use a sleeper to prevent sites from auto blocking this if it's doing too many requests too quickly

# ? ----------------- SEND NOTIFICATION -----------------

# Notification to send if a new chapter has been written(apps: pushbullet, twilio, myNotifier)


scrub(url, bookFile)
