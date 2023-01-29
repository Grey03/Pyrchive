import datetime, json, os

class archivemanager:
    def __init__(self):
        self.__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
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