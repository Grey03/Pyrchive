import random
import time

class DataBaseEntry:
    def __init__(self, ID):
        self.ID = ID
        self.tags = []
    def add_tag(self, tag):
        self.tags.append(tag)

    def has_tags(self, filter):
        tagsFound=0
        for tag in filter:
            if tag not in self.tags:
                break
            else:
                tagsFound+=1
        if (tagsFound == len(filter)):
            return True

files = []
print("Creating Files...")
creationtime=time.time()
for i in range(5000):
    temp = DataBaseEntry(str(i))
    temp.add_tag(random.choice(["Cameron","Christian","Grey","Ian"]))
    temp.add_tag(random.randint(2006,2023))
    temp.add_tag(random.choice(["Summer","Winter","Fall","Spring"]))
    files.append(temp)
print("Files Created in " + str(time.time()-creationtime) + " seconds.")

filter = ["Grey",2016]

count = 0
sortTime= time.time()
print("Sorting Files...")
filteredFiles = []
for entry in files:
    if entry.has_tags(filter):
        filteredFiles.append(entry)
        count+=1
print("Sorted.")
print ("Searched through " + str(len(files)) + " items in " + str(time.time() - sortTime) + " seconds.")
print (str(count) + " items found.")

for fileName in filteredFiles:
    print ("File " + str(fileName.ID) + " Tags " + str(fileName.tags))
