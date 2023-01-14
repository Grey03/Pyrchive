import datetime,random
class ArchiveManager:

    def __init__(self):
        self.archiveList = []
        self.tagGroupList = []
    class tagGroup:
        def __init__(self):
            self.name = ""
            self.tags = []
            self.description = ""
            self.color = "cyan"
        def is_in_group(self, tag):
            return tag.lower() in self.tags
    class ArchiveEntry:
        def __init__(self):
            self.ID = int
            self.title = str
            self.creator = str 
            self.tags = []
            self.data = str
            self.misc_notes = str
            self.upload_date = datetime.datetime.now()       
        def addTag(self, tags):
            if type(tags) != list:
                tags = [tags]
            if type(tags) == list:
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
    def filterFiles(self, filterList, requestedFileCount):
        finalFiles = []
        if requestedFileCount == 0:
            #Default setting
            requestedFileCount = 30
        for file in self.archiveList:
            if ArchiveManager.ArchiveEntry.filter(file, filterList):
                finalFiles.append(file.ID)
                if len(finalFiles) == requestedFileCount:
                    return finalFiles
        return finalFiles
    def add_Entry(self, entry, *position):
        if position == int:
            try:
                self.archiveList.pop(position)
            except:
                pass
            self.archiveList.insert(position, entry)
        else:
            try:
                self.archiveList.pop(entry.ID)
            except:
                pass
            self.archiveList.insert(entry.ID, entry)
    def get_ID(self):
        return (len(self.archiveList))
    def get_file(self, fileID):
        return self.archiveList[fileID]
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
        


#Archive = ArchiveManager()
#ArchiveManager.archiveTest(self=Archive,fileCount=1000)
#x = ArchiveManager.ArchiveEntry()
#x.tags = ["cat"]
#print (ArchiveManager.ArchiveEntry.filter(x, ["cat",""]))
