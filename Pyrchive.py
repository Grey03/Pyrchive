import datetime,json, os
global __location__
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

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
    class ArchiveEntry:
        def __init__(self, **kwargs):
            self.ID = -1
            self.title = ""
            self.creator = "" 
            self.tags = []
            self.data = ""
            self.misc_notes = ""
            self.upload_date = (datetime.datetime.now().__str__())
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value) 
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