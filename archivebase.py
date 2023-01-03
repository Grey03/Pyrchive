from datetime import datetime

class DataBaseEntry:
    global alltags
    alltags = []

    def __init__(self, ID):
        self.ID = int(ID)
        self.name = str
        self.tags = []
        self.location = str
        #Saving the upload dat from least timespan to largest timespan but also with the time time of the day
        self.uploadDate = datetime.now()

    def get_all_tags():
        return alltags

    def sort_tags(self):
        self.tags.sort()

    def refresh_alltag(self):
        for tag in self.tags:
            if tag not in alltags:
                alltags.append(tag)
                alltags.sort

    def add_tag(self, newtag):
        newtag = str(newtag).lower()
        if newtag not in self.tags:
            self.tags.append(newtag)
            self.sort_tags()
            self.refresh_alltag()

    def remove_tag(self, tag):
        tag = str(tag)
        if tag in self.tags:
            self.tags.remove(tag)

    #Just do this in main code
    #def set_tags(self, newtags):
    #    for tag in newtags:
    #        self.add_tag(tag)

    def filter(self, filterList):
        positiveTerms = []
        negativeTerms = []
        for term in filterList:
            if str(term).find("-", 0, 1) != -1:
                negativeTerms.append(term.replace("-",""))
            else:
                positiveTerms.append(term)

        if(len(negativeTerms) > 0):
            for negTerm in negativeTerms:
                if negTerm in self.tags:
                    return False
        if(len(positiveTerms) > 0):
            for posTerm in positiveTerms:
                if posTerm not in self.tags:
                    return False
        return True