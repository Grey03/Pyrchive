import datetime, json, os, tkinter.messagebox, time

class archivemanager:
    def __init__(self):
        self.__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.jsonsLocation = self.__location__ + "\\pyrchiveFolders\\pyrchiveJsonData\\"
        self.openFilesImmediately = True
        self.openMenuImmediately = True
        self.localFiles = True
    class taggroup:
        def __init__(self):
            #tag groups should be a grouping of tags that are similar to each other
            self.name = ""
            self.tags = []
            self.description = ""
            self.color = "cyan"
    class archiveentry:
        def __init__(self, **kwargs):
            #This is the basic entry, with all the attributes
            self.ID = -1
            self.title = ""
            self.creator = "" 
            self.tags = []
            self.fileLocation = ""
            self.notes = ""
            self.uploadDate = (datetime.datetime.now().__str__())
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
        def __str__(self):
            #Returns a string representation of the dictionary of the object
            return json.dumps(self.__dict__(), indent=4, sort_keys=True)
        def __dict__(self):
            #Should return a dictionary that represent the entry
            return  {
                    "ID": self.ID,
                    "title": self.title,
                    "creator": self.creator,
                    "tags": self.tags,
                    "fileLocation" : self.fileLocation,
                    "notes": self.notes,
                    "uploadDate": self.uploadDate
                    }
        def hasTags(self, filterList):
            positiveList = []
            negativeList = []
            for filterWord in filterList:
                if filterWord.startswith("-"):
                    negativeList.append(filterWord.lower().replace("-", ""))
                else:
                    positiveList.append(filterWord.lower())
            for negativeTerm in negativeList:
                if negativeTerm in self.tags:
                    return False
            for positiveTag in positiveList:
                if positiveTag not in self.tags:
                    return False
            return True
    def getNewID(self):
        #Looks for any unused ID in the database to reuse and returns a new one if one is not found.
        try:
            for idx, file in enumerate(self.getEntries()):
                if idx != file["ID"]: return idx
            return len(self.getEntries())
        except:
            return 0
    def getEntryByID(self, ID):
        #Gets the entries from the json, then tries to return the specific entry asked for
        try:
            for file in self.getEntries():
                if file["ID"] == ID: return file
            return None
        except: tkinter.messagebox.showerror("Error", "Could not find entry with ID " + str(ID))
    def getEntries(self):
        #Returns a list of dictionaries that represent all the entries in the archive
        try:
            with open(self.jsonsLocation + "/ArchiveEntries.json", "r") as jsonFile:
                return json.load(jsonFile)
        except:
            return []
    def filterEntries(self, filterList, start, filterCount):
        entries = self.getEntries()
        if filterCount == -1: filterCount = len(entries)
        foundFiles = []
        timeToSort = time.time()
        for entryLocation in range(start, len(entries)):
            entry = self.archiveentry(**entries[entryLocation])
            if entry.hasTags(filterList):
                foundFiles.append(entry)
            if len(foundFiles) >= filterCount:
                break
        return {"files": foundFiles,
            "sortTime": time.time()-timeToSort}
    def saveEntry(self, file):
        #First checks to see if the file is a dictionary because this should only function with the dictionary format of an entry.
        saveTime = time.time()
        if type(file) != dict:
            raise ValueError("File must be a dictionary")
        #Loads entire list of entries into a list
        if len(self.getEntries()) > 0:
            entriesList = self.getEntries()
        else:
            entriesList = []
        #This controls how its modified, aka where a new file should be placed or an edit that should be made
        if len(entriesList)> file["ID"] and entriesList[file["ID"]]["ID"] == file["ID"]:
            entriesList[file["ID"]] = file
        elif len(entriesList)> file["ID"]:
            entriesList.insert(file["ID"],file)
        else:
            entriesList.append(file)
        try:
            with open(self.jsonsLocation + "/ArchiveEntries.json", "w") as jsonFile:
                json.dump(entriesList, jsonFile,indent=4)
        except:
            raise tkinter.messagebox.showerror(title="Error", message=("Could not save"))
        return (time.time()-saveTime)
    def createTestEntry(self, **kwargs):
        #Allows me to quickly create a new entry for testing purposes    
        ID=self.getNewID()
        for key, value in kwargs.items():
            if key == "ID" and value <= self.getNewID(): ID = value
        newEntry = self.archiveentry(ID=ID, title="title", creator="creator", tags=["tag1", "tag2", "tag3"], fileLocation = "fileLocation", notes = "notes")
        self.saveEntry(newEntry.__dict__())


        
temp = archivemanager()

creatingFilesTime = time.time()

for i in range(1):
    temp.createTestEntry()
print (time.time()-creatingFilesTime)


x = temp.filterEntries(["tag1", "cat"], 0, -1)
for entry in x["files"]:
    print (entry, x["sortTime"])
