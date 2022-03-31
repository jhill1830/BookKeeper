#!/usr/bin/env python3
import urllib.request
import urllib.parse
import urllib.error
import json
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
# ! variable 'url' below won't work as the website itself is blocking the request.  Figure out workaround, once a basic webscraper is working on sites that do allow it
url = 'https://novelfull.com/reverend-insanity/chapter-323.html'
# testUrl = 'https://beautiful-soup-4.readthedocs.io/en/latest/#making-the-soup'
testUrl = 'https://www.webscrapingapi.com/python-web-scraping/'

# TODO Maybe figure out a way to dynamically change the file name based on the sites book.  (Use h1 tag? Use librabry.json file?)
bookFile = 'file.txt'
jsonFile = 'library.json'


# ? ----------------- File/URL Reading -----------------

def scrub(site, book):  # scrubbing function
    urlOpen = urllib.request.urlopen(site).read()
    soup = BeautifulSoup(urlOpen, 'html.parser')
    pTags = soup('p')  # finds only selected tags eg. 'h1'

    # TODO Use JSON file to find which chapter it is up to and reference that against most recent update for site. Potentially use this as the chapter variable as well(~ chapter = json.chapter + 1)
    # ### Use if statement if chapter number on site is greater than in json file. Also check if it's a dummy page using number of characters in the sites p tag?
    # ### Return and finish executing program if there is nothing to update

# TODO write if statements for book existence etc
    # IF book exists and no new chapter to write: RETURN/close program

    # IF book exists and new chapter to write:
    writeBook(book, pTags)  # write to file function.
    updateChapter(0)  # update chapter json

    # IF book !exist: writeBook, updateChapter, updateLibrary

    # ELSE: return/close program if something unnexpected happens


# ? ----------------- WRITE TO FILE -----------------

def writeBook(book, tag):
    # TODO Potentially use JSON as the chapter variable as well(~ chapter = json.chapter + 1)
    chapter = 'test 0'

    # open file to write to.  The second param: 'r' -read, 'w' -write, 'a' -append
    with open(book, 'w') as file:
        file.write('\t' + 'CHAPTER ' + str(chapter) + '\n'*2)
        for tags in tag:           # iterate line by line through site
            line = tags.get_text()   # print only the text of the selected element
            file.write(line + '\n')  # write line to file and add newline
        file.write('\n'*2)


# ? ----------------- UPDATE JSON -----------------

def updateChapter(json):
    # update file's chapter += 1
    return


def updateLibrary(json):  # Dunno if necessary. Might use a book list to reference so that if the book exists already, then append('a') to the corresponding file, otherwise, write('w') to new file
    # add book name to list
    return
# Might need to use a sleeper to prevent sites from auto blocking this if it's doing too many requests too quickly


# scrub(testUrl, bookFile)

# with open(bookFile, 'r') as file:   # Read File
#    print(file.read())
#    characters = file.tell()    # Counts the number of characters in the file
#    print(characters)

# with open('library.json') as file:
# source = file.read()


# ? #### READING AND WRITING TO JSON
# TODO Need to clean this up and turn into proper function as this is just to learn how to utilise json files
# Load in external json file and create new object with it's data
data = json.load(open(jsonFile, 'r'))
print(data['books']['book2']["chapter"])

# Update targeted key's value in new 'data' json object
data['books']['book2']['chapter'] += 1  # Increment chapter by 1

# Either write newfile or rewrite previous file(rewrite in this case) using the new 'data' json object
with open(jsonFile, 'w') as writeFile:

    # .dump turn the data object into a string, as it can't write an object into the file. indent=4 causes it to have proper formatting in the output file
    json.dump(data, writeFile, indent=4)


data = json.load(open(jsonFile, 'r'))
print(data['books']['book2']["chapter"])

# Need to write schema to add new books into json file.  Will add this if the shell's book argument isn't already recognised in json book titles
