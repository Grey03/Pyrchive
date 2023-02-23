import datetime, json, os, random, logging

logger = logging.getLogger(__name__)

logging.basicConfig(filename="PyrchiveLogs.log", filemode="w",level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')


class archivemanager:
    def __init__(self):
        self.__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.archiveFilesDirectory = self.__location__ + "/pyrchiveFolders/archivedFiles/"
        self.archiveJsonDirectory = self.__location__ + "/pyrchiveFolders/pyrchiveJsonData/"
        self.entriesList = []
        self.tagGroupList = []
        self.savedSearches = []

        #Settings
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
            "ID": len(self.entriesList),
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
        posList = [word.lower() for word in filterList if not word.startswith("-")]
        negList = [word.lower().replace("-", "") for word in filterList if word.startswith("-")]
        for negTerm in negList:
            if negTerm in entryTags:
                return False
        for posTerm in posList:
            if posTerm not in entryTags:
                return False
        return True
    
    def filterEntryList(self, filterList, entryCount):
        if len(filterList) > 0:
            finalentries = [entry for entry in self.entriesList if archivemanager.hasTags(filterList, entry["tags"])]
            if entryCount != -1 and (len(finalentries) > entryCount):
                return finalentries[0:entryCount]
            return finalentries
        else:
            return self.entriesList[0:entryCount]

    def addEntry(self, entry):
        try:
            self.entriesList.insert(entry["ID"], entry)
        except:
            self.entriesList.append(entry)

    def getAllTags(self):
        allTags = []
        for entry in self.entriesList:
            for tag in entry["tags"]:
                if tag not in allTags:
                    allTags.append(tag)
        return allTags

    def loadAll(self):
        self.loadEntries()
        self.loadSettings()
        #self.loadTagGroups()
        self.loadSavedSearches()
    def saveAll(self):
        self.saveEntries()
        self.saveSettings()
        #self.saveTagGroups()
        self.saveSavedSearches()

    def loadSettings(self):
        logger.info("Loading Tag Groups from %s", self.archiveJsonDirectory + "ArchiveSettings.json")
        #try:
        #    with open(self.archiveJsonDirectory + "ArchiveSettings.json", "r") as f:
        #        return json.load(f)
        #except Exception as inst:
        #        logger.warning("Error loading settings from ArchiveSettings.json: " + str(inst))
        #        self.tagGroupList = []
    def saveSettings(self):
        logger.info("Saving Tag Groups to %s", self.archiveJsonDirectory + "ArchiveSettings.json")
        #try:
        #    with open(self.archiveJsonDirectory + "TagGroups.json", "w") as f:
        #        json.dump(self.tagGroupList, f, indent=4)
        #except Exception as inst: 
        #    logger.error("Failed to save settings: " + str(inst))

    def loadTagGroups(self):
        logger.info("Loading Tag Groups from %s", self.archiveJsonDirectory + "TagGroups.json")
        try:
            with open(self.archiveJsonDirectory + "TagGroups.json", "r") as f:
                self.tagGroupList = json.load(f)
        except Exception as inst:
                logger.warning("Error loading tagGroups from SavedSearches.json: " + str(inst))
                self.tagGroupList = []
    def saveTagGroups(self):
        logger.info("Saving Tag Groups to %s", self.archiveJsonDirectory + "TagGroups.json")
        try:
            with open(self.archiveJsonDirectory + "TagGroups.json", "w") as f:
                json.dump(self.tagGroupList, f, indent=4)
        except Exception as inst: 
            logger.error("Failed to save tag groups: " + str(inst))

    def loadSavedSearches(self):
        logger.info("Loading Tag Groups from %s", self.archiveJsonDirectory + "SavedSearches.json")
        try:
            with open(self.archiveJsonDirectory + "SavedSearches.json", "r") as f:
                self.savedSearches = json.load(f)
        except Exception as inst:
                logger.warning("Error loading saved searches from SavedSearches.json: " + str(inst))
                self.savedSearches = []
    def saveSavedSearches(self):
        logger.info("Saving Tag Groups to %s", self.archiveJsonDirectory + "SavedSearches.json")
        try:
            with open(self.archiveJsonDirectory + "SavedSearches.json", "w") as f:
                json.dump(self.savedSearches, f, indent=4)
        except Exception as inst: 
            logger.error("Failed to save savedSearches: " + str(inst))

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


            





"""test = archivemanager()
test.loadEntries()
test.loadTagGroups()
print (test.tagGroupList)"""