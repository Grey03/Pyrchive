import datetime,random,json
from pathlib import Path
class ArchiveManager:

    def __init__(self):
        self.archiveList = []
        self.tagGroupList = []
        self.savedSearches = []
        self.openFilesImmediately = True
        self.openMenuImmediately = True
        self.localFiles = True
    class TagGroup:
        def __init__(self):
            self.name = ""
            self.tags = []
            self.description = ""
            self.color = "cyan"
        def is_in_group(self, tag):
            return tag.lower() in self.tags
        def __str__(self):
            return json.dumps(self.__dict__(), indent=4)
        def __dict__(self):
            return {"name":self.name, "tags":self.tags, "description":self.description, "color":self.color}
        def toJSON(self):
            return json.dumps((self.__dict__()), ensure_ascii=False, indent=4)
    class ArchiveEntry:
        def __init__(self):
            self.ID = -1
            self.title = ""
            self.creator = "" 
            self.tags = []
            self.data = ""
            self.misc_notes = ""
            self.upload_date = (datetime.datetime.now().__str__())       
        def addTag(self, tags):
            if type(tags) != list:
                tags = [tags]
            if  len(tags) > 0:
                for tag in tags:
                    if str(tag) not in self.tags:
                        self.tags.append(str(tag).lower())
                        self.tags.sort()
        def filter(self, filterList):
            positiveTerms = []
            negativeTerms = []
            for term in filterList:
                if str(term).lower().find("-", 0, 1) != -1:
                    negativeTerms.append(str(term.replace("-","")).lower())
                else:
                    positiveTerms.append(str(term).lower())

            if(len(negativeTerms) > 0):
                for negTerm in negativeTerms:
                    if str(negTerm) in self.tags:
                        return False
            if(len(positiveTerms) > 0):
                for posTerm in positiveTerms:
                    if str(posTerm) not in self.tags:
                        return False
            return True
        def __str__(self):
            return json.dumps(self.__dict__(), indent=4)
        def __dict__(self):
            return {
                "ID": self.ID,
                "title": self.title,
                "creator": self.creator,
                "tags": self.tags,
                "data": r"{}".format(self.data),
                "misc_notes": self.misc_notes,
                "upload_date": self.upload_date
            }
        def toJSON(self):
            return json.dumps((self.__dict__()), ensure_ascii=False, indent=4)
            
            #return json.dumps(dictToBytes, indent=4)
            #return json.dumps(dictionary, sort_keys=True, indent=4)

    def filterFiles(self, filterList, start, requestedFileCount): 
        if requestedFileCount < 0:
            requestedFileCount = len(self.archiveList)            
        
        filterList = [*set(filterList)]
        try:
            filterList.remove("")
        except:
            pass
        finalFiles = []
        for i in range(start, len(self.archiveList)):
            file = self.archiveList[i]
            if ArchiveManager.ArchiveEntry.filter(file, filterList):
                finalFiles.append(file.ID)
                if len(finalFiles) == requestedFileCount:
                    return finalFiles
        return finalFiles
    def update_Entry(self, entry):
        self.archiveList[entry.ID] = entry
    def add_Entry(self, entry):
        if entry.ID == -1:
            entry.ID = self.get_ID()
        try:
            self.archiveList.insert(entry.ID,entry)
        except:
            self.archiveList.append(entry)
    def get_ID(self):
        for i in range(len(self.archiveList)):
            if i != self.archiveList[i].ID:
                return i
        return len(self.archiveList)
    def delete_entry(self, fileID):
        for i in range(len(self.archiveList)):
            if self.archiveList[i].ID == fileID:
                self.archiveList.pop(i)
                return True
        return False
    def get_file(self, fileID):
        return self.archiveList[fileID]
    def get_all_tags(self):
        tagList = []
        for entry in self.archiveList:
            for tag in entry.tags:
                if tag not in tagList:
                    tagList.append(tag)
                    tagList.sort()
        return tagList
    def add_TagGroup(self, TagGroup):
        for group in self.tagGroupList:
            if TagGroup.name == group.name:
                self.tagGroupList.pop(group.name)
                self.tagGroupList.append(TagGroup)
                self.tagGroupList.sort()
                return
            
        self.tagGroupList.append(TagGroup)
        self.tagGroupList.sort()
    def update_TagGroup(self, oldTagGroupName, TagGroup):
        for group in self.tagGroupList:
            if oldTagGroupName == group.name:
                self.tagGroupList.pop(group.name)
        self.tagGroupList.append(TagGroup)
        self.tagGroupList.sort()
    def get_TagGroup(self, name):
        for group in self.tagGroupList:
            if name == group.name:
                return group
        return None
    def archiveTest(self, fileCount):
        for i in range(fileCount):
            tempfile = ArchiveManager.ArchiveEntry()
            id = len(self.archiveList)    
            tempfile.ID = id
            tempfile.title = "title " + str(id)
            tempfile.uploader = "uploader" + str(id)
            tempfile.addTag("cat")
            tempfile.addTag("dog")
            tempfile.addTag((random.randint(0,5)))
            tempfile.data = "data" + str(id)
            tempfile.misc_notes = "misc_notes" + str(id)

            self.archiveList.append(tempfile)
                
        print (ArchiveManager.filterFiles(self=self,filterList=["cat", "1"], requestedFileCount=30))
        print (len(self.archiveList))
        print (self.archiveList[0].title)
        print (self.archiveList[0].tags)
    def loadArchiveFromJson(self):
        fileLocation = str(Path.cwd())
        try:
            with open(fileLocation + '\ArchiveEntries.json', 'r') as f:
                data = json.load(f)
                for item in data:
                    loadedFile = ArchiveManager.ArchiveEntry()
                    loadedFile.ID = item['ID']
                    loadedFile.title = item['title']
                    loadedFile.creator = item['creator']
                    loadedFile.addTag(item['tags'])
                    loadedFile.data = r"{}".format(item['data'])
                    loadedFile.misc_notes = item['misc_notes']
                    loadedFile.upload_date = item['upload_date']
                    self.archiveList.append(loadedFile)
                #self.tagGroupList = data['tagGroupList']
                f.close
        except:
            pass
    def saveArchiveToJson(self):
        fileLocation = str(Path.cwd())
        json_string = json.dumps([ob.__dict__() for ob in self.archiveList], indent=4, ensure_ascii=False)
        with open(fileLocation + '\ArchiveEntries.json', 'w') as f:   
            f.write(json_string)
            f.close()
    def loadTagGroupsFromJson(self):
        fileLocation = str(Path.cwd())
        tempTagGroupList = []
        with open(fileLocation + '\TagGroups.json', 'r') as f:
            data = json.load(f)
            for item in data:
                loadedTagGroup = ArchiveManager.TagGroup()
                loadedTagGroup.name = item['name']
                loadedTagGroup.tags = item['tags']
                loadedTagGroup.description = item['description']
                loadedTagGroup.color = item['color']
                tempTagGroupList.append(loadedTagGroup)
            self.tagGroupList = tempTagGroupList
            f.close
    def saveTagGroupsToJson(self):
        fileLocation = str(Path.cwd())
        json_string = json.dumps([ob.__dict__() for ob in self.tagGroupList], indent=4, ensure_ascii=False)
        with open(fileLocation + '\TagGroups.json', 'w') as f:
            f.write(json_string)
            f.close()
    def loadSavesFromJson(self):
        fileLocation = str(Path.cwd())
        with open(fileLocation + '\SavedSearches.json', 'r') as f:
            data = json.load(f)
            self.savedSearches = data
    def saveSavesToJson(self):
        fileLocation = str(Path.cwd())
        json_string = json.dumps(self.savedSearches, indent=4, ensure_ascii=False)
        with open(fileLocation + '\SavedSearches.json', 'w') as f:
            f.write(json_string)
            f.close()
    def loadSettingsFromJson(self):
        try:
            fileLocation = str(Path.cwd())
            with open(fileLocation + '\ArchiveSettings.json', 'r') as f:
                data = json.load(f)
                self.openFilesImmediately = data['openFilesImmediately']
                self.openMenuImmediately = data['openMenuImmediately']
                self.localFiles = data['localFiles']
                f.close
        except:
            self.saveSavesToJson()
    def saveSettingsToJson(self):
        fileLocation = str(Path.cwd())
        settings = {"openFilesImmediately": self.openFilesImmediately,
                    "openMenuImmediately": self.openMenuImmediately,
                    "localFiles": self.localFiles}
        with open(fileLocation + '\ArchiveSettings.json', 'w') as f:
            f.write(json.dumps(settings, indent=4, ensure_ascii=False))
            f.close()
    def loadAll(self):
        self.loadArchiveFromJson()
        self.loadTagGroupsFromJson()
        self.loadSavesFromJson()
        self.loadSettingsFromJson()
    def saveAll(self):
        self.saveArchiveToJson()
        self.saveTagGroupsToJson()
        self.saveSavesToJson()
        self.saveSettingsToJson()


#Archive = ArchiveManager()
#ArchiveManager.archiveTest(self=Archive,fileCount=100000)
#Archive.saveArchiveToJson()
#Archive.loadArchiveFromJson()
#x = ArchiveManager.ArchiveEntry()
#x.tags = ["cat"]
#print (ArchiveManager.filterFiles(Archive, ["cat"], 3))
