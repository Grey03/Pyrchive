from datetime import datetime

class DataBaseEntry:
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name
        self.tags = []
        #Saving the upload dat from least timespan to largest timespan but also with the time time of the day
        self.uploadDate = datetime.now().strftime("%d/%m/%Y, %H:%M:%S:%f")

    def add_tag(self, newtag):
        newtag = str(newtag)
        if newtag not in self.tags:
            self.tags.append(newtag)

    def remove_tag(self, tag):
        tag = str(tag)
        if tag in self.tags:
            self.tags.remove(tag)

    def set_tags(self, newtags):
        self.tags = list(newtags)

    def filter(self, filterList):
        positiveTerms = []
        negativeTerms = []
        for term in filterList:
            if str(term).find("-", 0, 1) != -1:
                negativeTerms.append(term)
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