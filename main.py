import random
import time
from archivebase import DataBaseEntry

files = []
print("Creating Files...")
creationtime=time.time()
for i in range(10000):
    temp = DataBaseEntry(ID= str(i))
    temp.add_tag(random.choice(["Cameron","Christian","Grey","Ian"]))
    temp.add_tag(random.choice(["Cameron","Christian","Grey","Ian"]))
    temp.add_tag(random.choice(["Summer","Winter","Fall","Spring"]))
    files.append(temp)
print("Files Created in " + str(time.time()-creationtime) + " seconds.")

filter = ["grey","-ian"]
filter.sort()

count = 0
sortTime= time.time()
print("Sorting Files...")
filteredFiles = []
for entry in files:
    if entry.filter(filter):
        filteredFiles.append(entry)
        count+=1
print("Sorted.")
sortTime2 = time.time()


for fileName in filteredFiles:
    print ("File " + str(fileName.ID) + " Tags " + str(fileName.tags))
    print (f"{fileName.ID} Tags {fileName.tags} uploaded {fileName.uploadDate}")

print (str(count) + " items found.")
print (f"Searched through {len(files)} items in {sortTime2-sortTime} seconds.")
