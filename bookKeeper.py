#!/usr/bin/env python3
from msilib import schema
from pickle import TRUE
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
testUrl = 'https://bestlightnovel.com/novel_888108451/chapter_2334'


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
        tags = soup(tag)  # finds only selected tags eg. 'h1'
        return tags

#
#
#
#
#
#
#
#

# ? ----------------- File/URL Reading -----------------


def scrub(site, bookfile):  # scrubbing function
    data = json.load(open(libraryJson, 'r'))
    # If up to date with specified chapter number
    if data['books'][bookTitle]['chapter'] <= int(chaptersNum):
        # IF book exists and no new chapter to write: RETURN/close program
        if nextChap(site):
            # TODO write if statements for book existence etc

            # # Could potentially use scrub as a recursive function where it increments the url number until it somes up with a blank site/placeholder site. eg replace the chapter number in url

            data = json.load(open(libraryJson, 'r'))
            try:
                # IF book exists and new chapter to write:
                if data['books'][bookTitle]:
                    print('Book Found')
                    writeBook(bookfile, sendReq(site, 'p'), libraryJson)
                    updateChapter(bookTitle, libraryJson)
                    time.sleep(1)
                    scrub(site, bookfile)
                    return

            except:
                # IF book !exist: writeBook, updateChapter, updateLibrary
                updateLibrary(bookTitle, libraryJson)
                writeBook(bookfile, sendReq(site, 'p'), libraryJson)
                updateChapter(bookTitle, libraryJson)
                scrub(site, bookfile)
                return

    else:   # Return and finish executing program if there is nothing to update
        print("Up to date with specified chapters")
        return

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
    print('Chapter', data['books'][book]['chapter'])
    # Update targeted key's value in new 'data' json object
    data['books'][book]['chapter'] += 1  # Increment chapter by 1

    # Either write newfile or rewrite previous file(rewrite in this case) using the new 'data' json object
    with open(jsonFile, 'w') as writeFile:
        # .dump turn the data object into a string, as it can't write an object into the file. indent=4 causes it to have proper formatting in the output file
        json.dump(data, writeFile, indent=4)

    data = json.load(open(jsonFile, 'r'))

    # print(data['books'][book]["chapter"])
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

#
#
#
#
#
#
#
#

# ? ----------------- NEXT CHAPTER -----------------


# NOTE: This will cause the last chapter in the book to not be written. # TODO: Might have to add if statement to check if it is the last chapter in the series. Use specified chapter num.
# NOTE: This might also be an issue as the book will always be a chapter behind the most recent if the site doesn't do preview pages for the upcoming, incompleted chapters. Potentially write the file writing and sjson updating into this function so it write the page before it returns false.  That way it still writes the last url(AKA final chapter in series), as well as the most recently updated chapter if it's not complete yet. NOTE: this will only be viable if there is no preview pages for the next chapter, cause otherwise it will update the chapter number in the json when it has only written the preview for that chapter. NOTE: maybe check for a "Prev Chapter" <a> tag, to at least validate that it's a proper novel chapter url and doesn't write rnadom stuff from a chapter that doesn't exist(Still a problem with preview chapters.  Maybe have an arg specifying if the site has previews or not)

# Uses existence of <a> tag with 'Next Chapter' text, to check if there is a valid next chapter url to go to.
def nextChap(site):
    aTag = sendReq(site, 'a')
    for tag in aTag:
        try:
            line = tag.get_text()
            if line == 'NEXT CHAPTER':
                return True
        except:
            continue
    # if yes preview: just return false
    # if no preview and if "Prev Chapter" <a> tag: write current page, then return false
    print("No New Chapter")
    return False

#
#
#
#
#
#
#
#

# ? ----------------- SEND NOTIFICATION -----------------

# Notification to send if a new chapter has been written(apps: pushbullet, twilio, myNotifier)


scrub(url, bookFile)
