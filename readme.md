TODO List

# TODO might have to write something to automate the chapter names if that's part of the url in some chapters

# TODO sort the library JSON file books alphabetically

# TODO potentially rewrite the manner in which it goes to next chapter by looking for an <a> tag that includes text "Next Chapter". If it does, then copy page and then click link to next page. Stop the program if there is no "Next Chapter" <a> tag.

# TODO Maybe figure out a way to dynamically change the file name based on the sites book. (Use h1 tag? Use librabry.json file?)

# TODO maybe rewrite the sendRequest function to check for valid url address/ address that has a proper book in it

# TODO change the recursion state so that it ends when it has reached the most recent chapter. Potentially when it tries to load a site that doesn't exist. EQ try: load page. except: close program. Might have to search page text and if '#404' shows, then stop program. Otherwise, might just have to specify the number of chapters.

# TODO write if statements for book existence etc

'''
Use the os.chdir() function.

> > > import os
> > > os.getcwd()
> > > '/home/username'
> > > os.chdir(r'/home/username/Downloads')
> > > os.getcwd()
> > > '/home/username/Downloads'

You can get the current working directory using the os.getcwd function. The os.chdir function changes the current working directory to some other directory that you specify. (one which contains your file) and then you can open the file using a normal open(fileName, 'r') call.
'''
