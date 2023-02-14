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

    def createTagGroup(self, **kwargs):
        tagGroup = {
            "name": "",
            "tags": [],
            "description": "",
            "color": "cyan"
            }
        
        for key, value in kwargs.items():
            if hasattr(tagGroup, key):
                tagGroup.__setattr__(key, value)

        return tagGroup
    def createEntry(self, **kwargs):
        entryDict = {
            "title": "",
            "creator": "",
            "tags": [],
            "fileLocation": "",
            "notes": "",
            "uploadDate": datetime.datetime.now().__str__()
        }

        for key, value in kwargs.items():
            if hasattr(entryDict, key) and key != "uploadDate":
                entryDict.__setattr__(key, value)

        return entryDict
    
    def hasTags(filterList, entryTags):
        posList = []
        negList = []
        for filterWord in filterList:
            if filterWord.startswith("-"): negList.append(filterWord.lower().replace("-", ""))
            else: posList.append(filterWord.lower())
        for negTerm, in negList:
            if negTerm in entryTags:
                return False
        for posTerm in posList:
            if posTerm not in entryTags:
                return False
        return True
    
    def filterEntryList(self, filterList, entryCount):
        finalentries = [entry for entry in self.entriesList if archivemanager.hasTags(filterList, entry["tags"])]
        if entryCount != -1 and (len(finalentries) > entryCount):
            return finalentries[0:entryCount]
        return finalentries

    def addEntry(self, entry):
        try:
            self.entriesList.insert(entry["ID"], entry)
        except:
            self.entriesList.append(entry)  
    def loadEntries(self):
        logger.info("Loading entries from %s", self.archiveJsonDirectory + "ArchiveEntries.json")
        try:
            with open(self.archiveJsonDirectory + "ArchiveEntries.json", "r") as f:
                self.entriesList = json.load(f)
        except Exception as inst:
                logger.warning("Error loading entries from ArchiveEntries.json: " + str(inst))
                self.entriesList = []
    def saveEntries(self):
        logger.info("Saving entries to %s", self.archiveJsonDirectory + "ArchiveEntries.json")
        try:
            with open(self.archiveJsonDirectory + "ArchiveEntries.json", "w") as f:
                json.dump(self.entriesList, f, indent=4)
        except Exception as inst:
            logger.error("Failed to save archive: " + str(inst))
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
x = (test.filterEntryList(["tag1"], -1))
for entry in x:
    print (entry["tags"])