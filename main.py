import random
import time
from archivebase import DataBaseEntry

files = []
print("Creating Files...")
creationtime=time.time()
for i in range(10000):
    temp = DataBaseEntry(ID= str(i), name="Name")
    temp.add_tag(random.choice(["Cameron","Christian","Grey","Ian"]))
    temp.add_tag(random.randint(2006,2023))
    temp.add_tag(random.choice(["Summer","Winter","Fall","Spring"]))
    files.append(temp)
print("Files Created in " + str(time.time()-creationtime) + " seconds.")

filter = ["Grey","2016"]

count = 0
sortTime= time.time()
print("Sorting Files...")
filteredFiles = []
for entry in files:
    if entry.filter(filter):
        filteredFiles.append(entry)
        count+=1
print("Sorted.")
print (f"Searched through {len(files)} items in {time.time()-sortTime} seconds.")
print (str(count) + " items found.")

for fileName in filteredFiles:
    print ("File " + str(fileName.ID) + " Tags " + str(fileName.tags))
    print (f"{fileName.ID} Tags {fileName.tags} uploaded {fileName.uploadDate}")
