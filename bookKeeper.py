#!/usr/bin/env python3

from urllib.request import Request, urlopen
import urllib.parse
import urllib.error
import json
import sys
import time
import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

# ! issues with library.json not being recognised intermittently
# ? Maybe add an update feature if the book isn't finished, so it captures new chapters and send a notification when a new chapter is out and written
# ? Could have a shell script that runs the program each day/week, with arguments that define the book and/or website
# ? Some way of pre-emptively estimating how big the filesize will be once the file has been written.
# TODO sort the library JSON file books alphabetically. QoL
# TODO could potentially just email the new chapter to me when it is written, so I don't have to look it up
# TODO add a more flexible default file saving system.  Have the pathways in the JSON?
# TODO prompt for url to use if there's no book yet/no url in the library.json

# ? ----------------- INPUTS -----------------

# TODO Maybe figure out a way to dynamically change the file name based on the sites book.  (Use h1 tag? Use librabry.json file?)
bookTitle = sys.argv[1]     # Use shell argument 1
bookFile = bookTitle + '.epub'
libraryJson = 'library.json'

# Load in external json file and create new object with it's data
data = json.load(open(libraryJson, 'r'))

chaptersNum = sys.argv[2]   # Use shell argument 2. # of chapters to read up to

# Check for specificity of preview chapter in shell statement
try:
    previewChap = sys.argv[3]
except:
    previewChap = False

print(bookTitle)

#
#
#

# ? ----------------- Check for book -----------------


def checkBookUrl(book):
    global url
    try:
        if data['books'][book]:
            url = data['books'][book]['url']
    except:
        url = input("Enter url: ")


checkBookUrl(bookTitle)

# ? ----------------- Send Request -----------------

# TODO maybe rewrite the sendRequest function to check for valid url address/ address that has a proper book in it


def sendReq(site, tag):  # sendRequest function to connect and parse url which returns desired tag

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


# ? ----------------- File/URL Reading -----------------

def scrub(site, bookfile):  # scrubbing function

    parent_dir = os.getcwd()
    try:
        # if book exists and isn't up to specified chapter.  Will error if book doesn't exist, going to the except statement
        if data['books'][bookTitle]['chapter'] <= int(chaptersNum):
            if nextChap(site, bookfile):

                print('Book Found')

                # ! change to UPDATE EPUB function
                writeEpub(bookfile, sendReq(site, 'p'), libraryJson)

                updateChapter(bookTitle, libraryJson)
                time.sleep(1)
                scrub(site, bookfile)
                return

        else:   # Return and finish executing program if there is nothing to update
            print("Up to date with specified chapters")
            return

    except:
        # IF book !exist: updateLibrary, writeBook, updateChapter

        os.chdir(parent_dir)
        updateLibrary(bookTitle, libraryJson, parent_dir)

        # ! change to CREATE NEW EPUB function
        writeEpub(bookfile, sendReq(site, 'p'), libraryJson)

        updateChapter(bookTitle, libraryJson)
        scrub(site, bookfile)
        return

#
#
#


# ? ----------------- WRITE TO FILE (txt)-----------------

# def writeBook(bookfile, tag, jsonFile):  # write to file function.
# data = json.load(open(jsonFile, 'r'))  # Load in json
# chapter = data['books'][bookTitle]['chapter']  # Read chapter data
# os.getcwd()
# parent_dir = os.getcwd()
# new_dir = "Books"
# path = os.path.join(parent_dir, new_dir)
# try:
# os.chdir(path)
##
# except:
# os.mkdir(path)
# os.chdir(path)
##
# open file to write to.  The second param: 'r' -read, 'w' -write, 'a' -append
# with open(bookfile, 'a') as file:
##
# file.write('\t' + 'CHAPTER ' + str(chapter) + '\n'*2)
# for tags in tag:           # iterate line by line through site
# try:
# line = tags.get_text()   # print only the text of the selected element
# file.write(line + '\n'*2)  # write line to file and add newline
# except:  # Used to capture characters that can't be encoded.  EG katakana etc.
# continue
# file.write('\n'*2)
# os.chdir(parent_dir)

#
#
#

# ? ----------------- WRITE NEW EPUB (epub)-----------------

def writeEpub(book, tag, jsonFile):  # write to file function.
    # Load in json
    os.getcwd()
    parent_dir = os.getcwd()
    new_dir = "Books"
    path = os.path.join(parent_dir, new_dir)

    lines = ''
    try:
        os.chdir(path)

    except:
        os.mkdir(path)
        os.chdir(path)

    for tags in tag:
        try:
            line = '<p>' + tags.get_text() + '</p>'
            lines = lines + line + '\n'
            # print(line)
        except:
            continue

    #createEpub(bookTitle, lines)
    addToEpub(bookTitle, lines)

    os.chdir(parent_dir)

# ? ----------------- CREATE EPUB-----------------


def createEpub(book, lines):
    epubBook = epub.EpubBook()
    epubBook.set_title(book)
    epubBook.set_language('en')

    chapter = data['books'][book]['chapter']  # Read chapter data
    chapTitle = 'Chapter ' + str(chapter)
    createChap = epub.EpubHtml(
        title=chapTitle, file_name=chapTitle + '.xhtml', lang='en', uid=chapTitle)
    createChap.content = u'' + lines
    epubBook.add_item(createChap)

    # Table of Contents
    epubBook.toc = (epub.Link(chapTitle + '.xhtml',
                              bookTitle, bookTitle), (epub.Section("Chapters: "), (createChap,)))

    # define CSS style
    style = 'BODY {color: white;}'
    nav_css = epub.EpubItem(
        uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

    # add CSS file
    epubBook.add_item(nav_css)

    epubBook.add_item(epub.EpubNcx())
    epubBook.add_item(epub.EpubNav())

    # basic spine
    epubBook.spine = ['nav', createChap]

    # write to file
    epub.write_epub(bookTitle + '.epub', epubBook, {})


# ? ----------------- UPDATE EPUB-----------------

    # TODO create function that appends new chapter and TOC to existing epub (https://github.com/aerkalov/ebooklib/issues/217)
    # read existing epub file and append/extend to it.  Might need to remove and add the EpubNcx and EpubNav items


def addToEpub(book, lines):

    bookEpub = epub.read_epub(bookFile)
    chapter = data['books'][book]['chapter']
    chapTitle = 'Chapter ' + str(chapter)
    addChap = epub.EpubHtml(
        title=chapTitle, file_name=chapTitle + '.xhtml', lang='en', uid=chapTitle)
    addChap.content = u'' + lines
    bookEpub.add_item(addChap)
    bookEpub.spine.extend((addChap,))
    bookEpub.toc.append(addChap)

    bookEpub.items.remove(bookEpub.get_item_with_id('ncx'))
    bookEpub.items.remove(bookEpub.get_item_with_id('nav'))

    bookEpub.add_item(epub.EpubNcx())
    bookEpub.add_item(epub.EpubNav())

    epub.write_epub(bookTitle + '.epub', bookEpub, {})
    # ? ----------------- UPDATE CHAPTER -----------------


def updateChapter(book, jsonFile):    # update file's chapter + 1

    print('Chapter', data['books'][book]['chapter'])
    # Update targeted key's value in new 'data' json object
    data['books'][book]['chapter'] += 1  # Increment chapter by 1

    # Either write newfile or rewrite previous file(rewrite in this case) using the new 'data' json object
    with open(jsonFile, 'w') as writeFile:
        # .dump turn the data object into a string, as it can't write an object into the file. indent=4 causes it to have proper formatting in the output file
        json.dump(data, writeFile, indent=4)

    print("Updated " + book)
    return

#
#
#


# ? ----------------- UPDATE LIBRARY -----------------

# BUG: this functions will update the json file in the wrong format if used on a pre-existing key/entry.  But works properly if used to create a new entry
def updateLibrary(book, jsonFile, dir):  # Appends new book entry into library json
    os.chdir(dir)
    print(str(dir))

    data['books'][book] = {'title': book, 'chapter': 1, 'url': url}

    with open(jsonFile, 'r+') as updateFile:
        json.dump(data, updateFile, indent=4)
    print('Added New Book: ' + book)
    return

#
#
#


# ? ----------------- NEXT CHAPTER -----------------

# NOTE: This will cause the last chapter in the book to not be written. # TODO: Might have to add if statement to check if it is the last chapter in the series. Use specified chapter num.
# NOTE: This might also be an issue as the book will always be a chapter behind the most recent if the site doesn't do preview pages for the upcoming, incompleted chapters. Potentially write the file writing and json updating into this function so it write the page before it returns false.  That way it still writes the last url(AKA final chapter in series), as well as the most recently updated chapter if it's not complete yet. NOTE: this will only be viable if there is no preview pages for the next chapter, cause otherwise it will update the chapter number in the json when it has only written the preview for that chapter.

# TODO alter the <a> tag text so that it is consistent uppercase or lowercase

# Uses existence of <a> tag with 'Next Chapter' text, to check if there is a valid next chapter url to go to.
def nextChap(site, bookTitle):
    aTag = sendReq(site, 'a')
    for tag in aTag:
        try:
            line = tag.get_text()
            if line == 'NEXT CHAPTER':
                return True
        except:
            continue

    # if yes preview: just return false
    if previewChap:
        # write the last chapter if it's the last one specified
        if data['books'][bookTitle]['chapter'] == int(chaptersNum):
            writeEpub(bookTitle, sendReq(site, 'p'), libraryJson)
            updateChapter(bookTitle, libraryJson)
            print('Last Chapter')
            return False
        print("No New Chapter")
        return False

    # if no preview and if "Prev Chapter" <a> tag: write current page, then return false
    if previewChap == False:
        for tag in aTag:
            try:
                line = tag.get_text()
                if line == 'PREV CHAPTER':
                    writeEpub(bookTitle, sendReq(site, 'p'), libraryJson)
                    updateChapter(bookTitle, libraryJson)
                    print('Most Recent Chapter')
                    return False
            except:
                continue
        print("No New Chapter")
        return False

#
#
#


# ? ----------------- SEND NOTIFICATION -----------------

# Notification to send if a new chapter has been written(apps: pushbullet, twilio, myNotifier)

scrub(url, bookFile)
