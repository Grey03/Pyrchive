import datetime, json, os, random, logging

logger = logging.getLogger(__name__)

logging.basicConfig(filename="PyrchiveLogs.log", filemode="w",level=logging.INFO, format='%(levelname)s:%(asctime)s:%(name)s:%(message)s')


class archivemanager:
    def __init__(self):
        self.__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.archiveFilesDirectory = self.__location__ + "/pyrchiveFolders/archivedFiles/"
        self.archiveJsonDirectory = self.__location__ + "/pyrchiveFolders/pyrchiveJsonData/"
        self.entriesList = []
        logger.info("Archive manager initialized in {}".format(self.__location__))
    class taggroup:
        def __init__(self):
            #tag groups should be a grouping of tags that are similar to each other
            self.name = ""
            self.tags = []
            self.description = ""
            self.color = "cyan"
            logger.info("Tag group initialized")
    class archiveentry:
        def __init__(self, archive, **kwargs):
            #This is the basic entry, with all the attributes
            self.ID = -1
            self.title = ""
            self.creator = "" 
            self.tags = []
            self.fileLocation = ""
            self.notes = ""
            self.uploadDate = (datetime.datetime.now().__str__())
            for key, value in kwargs.items():
                if hasattr(self, key) and key != "tags":
                    setattr(self, key, value)
                elif key == "tags":
                    self.setTags(value)
                if key == "dict":
                    self.dictToArchiveEntry(value)
            if self.ID == -1:
                self.ID = archive.getID()
            logger.info(f"New entry initialized with the ID of {self.ID}")
        def setTags(self, tags):
            if type(tags) != list: raise TypeError("Tags must be a list")
            for i in range(len(tags)):
                tags[i] = tags[i].lower()
                tags[i] = tags[i].replace("-", "_")
                tags[i] = tags[i].replace("\n", "")
                tags[i] = tags[i].replace(" ", "_")
            tags = ([*set(tags)])
            tags.sort()
            self.tags = tags
            self.tags.sort()
        def dictToArchiveEntry(self, dictionary):
            for key, value in dictionary.items():
                if hasattr(self, key):
                    self.__setattr__(key, value)
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
    def entriesListToDictList(self):
        return [entry.__dict__() for entry in self.entriesList]
    def getID(self):
        if len(self.entriesList) == 0:
            return 0
        for position, entry in enumerate(self.entriesList):
            if position != entry.ID:
                return position
        return len(self.entriesList)
    def modifyEntry(self, entryID, newData):
        try: self.entriesList[entryID] = newData
        except: return False
    def addEntry(self, entry):
        try:
            self.entriesList.insert(entry["ID"], entry)
        except:
            self.entriesList.append(entry)   
    def refresh(self):
        self.saveEntries()
        self.loadEntries()
    def loadEntries(self):
        logger.info("Loading entries from %s", self.archiveJsonDirectory + "ArchiveEntries.json")
        try:
            with open(self.archiveJsonDirectory + "ArchiveEntries.json", "r") as f:
                temp = json.load(f)
                self.entriesList = [self.archiveentry(dict=entry) for entry in temp]
                return temp
        except Exception as inst:
                logger.warning("Error loading entries from %s. Creating empty array" + self.archiveJsonDirectory + "ArchiveEntries.json" + str(inst))
                self.entriesList = []
    def saveEntries(self):
        logger.info("Saving entries to %s", self.archiveJsonDirectory + "ArchiveEntries.json")
        try:
            with open(self.archiveJsonDirectory + "ArchiveEntries.json", "w") as f:
                json.dump(self.entriesListToDictList(), f, indent=4)
        except Exception as inst:
            logger.error("Failed to save archive. " + str(inst))
    def createTestEntry(self, **kwargs):
        logger.debug("Creating test entry")
        count = 1
        for key, value in kwargs.items():
            if key == "count": count = value
        for i in range(count):
            tags = [random.choice(["tag1", "tag2", "tag3", "tag4", "tag5"]), random.choice(["tag1", "tag2", "tag3", "tag4", "tag5"]), random.choice(["tag1", "tag2", "tag3", "tag4", "tag5"])]
            tempFile = self.archiveentry(self, title="title", tags=tags)
            logger.debug(tempFile.__dict__())
            self.addEntry(tempFile)
        logger.debug("Test Entry Creation Complete")


            





test = archivemanager()
test.loadEntries()
test.createTestEntry(count=100)
test.saveEntries()