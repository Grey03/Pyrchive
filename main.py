#from archivebase import DataBaseEntry
import customtkinter, os, random
from Pyrchive import ArchiveManager

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()



        self.title("Tarchive")
        #self.geometry(f"{900}x{500}")
        
        self.Archive = ArchiveManager()

        #Top Buttons Frame
        self.optionButtonsFrame=customtkinter.CTkFrame(self)
        #-+-+-+-+-+-
        self.settingsButton=customtkinter.CTkButton(self.optionButtonsFrame, text="Settings")
        self.settingsButton.pack(side="left", padx=5,pady=5)
        self.uploadButton=customtkinter.CTkButton(self.optionButtonsFrame,text="Upload")
        self.uploadButton.pack(side="left", padx=5,pady=5)
        self.savedsearchesButton=customtkinter.CTkButton(self.optionButtonsFrame, text="Saved Searches")
        self.savedsearchesButton.pack(side="left", padx=5,pady=5)
        self.randomButton=customtkinter.CTkButton(self.optionButtonsFrame, text= "Random")
        self.randomButton.pack(side="left",padx=5,pady=5)
        self.refreshButton=customtkinter.CTkButton(self.optionButtonsFrame, text=r"↻", width=10, height=10, command=self.search_click)
        self.refreshButton.pack(side="right",padx=5,pady=5)
        self.optionButtonsFrame.pack(padx=10, pady=5, fill="x")

        #Search Frame
        self.searchFrame = customtkinter.CTkFrame(self)
        self.favoriteButton = customtkinter.CTkButton(self.searchFrame, text="Save",width=50)
        self.favoriteButton.pack(side="left")
        self.searchBar= customtkinter.CTkEntry(self.searchFrame,placeholder_text="Search")
        self.searchBar.pack(padx=5,side="left", fill="x",expand=True)
        self.searchButton = customtkinter.CTkButton(self.searchFrame, text="Search", width=80, command=self.search_click)
        self.searchButton.pack(side="left")
        self.searchFrame.pack(padx=10, pady=5,fill="x")

        #Bottom Frame
        self.bottomFrame=customtkinter.CTkFrame(self, fg_color="transparent")
        self.tagFrame=customtkinter.CTkFrame(self.bottomFrame, width=200)
        self.tagLabel=customtkinter.CTkLabel(self.tagFrame, text="Tags", font=("Roboto", 13, "bold"))
        self.tagLabel.pack(padx=5,pady=0)
        self.tagList = customtkinter.CTkFrame(self.tagFrame)
        self.tagList.pack(padx=5,pady=5, expand=True, fill="both")
        self.tagFrame.pack(side="left", fill="y")
        self.imageFrame=customtkinter.CTkFrame(self.bottomFrame, fg_color="transparent")
        self.imageFrame.pack(side="left",fill="both", expand=True)
        self.bottomFrame.pack(fill="both",expand=True,padx=10,pady=5)

        self.pageButtonFrame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.pageLeft = customtkinter.CTkButton(self.pageButtonFrame, text="Previous")
        self.pageLeft.pack(side="left")
        self.pageRight = customtkinter.CTkButton(self.pageButtonFrame, text="Next")
        self.pageRight.pack(side="right")
        self.pageButtonFrame.pack(fill="both")



    #42 tags fit
    def refreshTags(self, archive, tagsToShow, maxTags):
        for widgets in self.tagList.winfo_children():
            widgets.destroy()
        foundTags = 0
        widget = {}
        #when ready, make it get tag.name for the tag and the tag.group.color for the color
        for i in range(len(tagsToShow)):
            tag = tagsToShow[i]
            tagname = tag[1] 
            tagcolor = "darkgrey"
            if foundTags < maxTags:
                for tagGroup in archive.tagGroupList:
                    if str(tagname) in tagGroup.tags:
                        tagcolor = tagGroup.color
                try:
                    widget[i]= customtkinter.CTkButton(master=self.tagList, text=(tagname + f"({tag[0]})"), font=("Roboto", 13, "underline"), text_color=tagcolor ,fg_color="transparent", height=0,corner_radius=0, command=lambda e = i: self.tag_click(tagsToShow[e][1]))
                    widget[i].pack(fill="x")
                    foundTags = foundTags + 1
                except:
                    print ("FAILED")
                    pass
    def averageTags(self, files, maxTags):

        if maxTags == 0:
            maxTags=30
        tagsToShow = []
        for file in files:
            for tag in file.tags:
                tagsToShow.append(tag)
        tagsToShow.sort()
        individualTags = [*set(tagsToShow)]

        tagCountList = []
        for tag in individualTags:
            tagCountList.append([tagsToShow.count(tag),tag])

        tagCountList.sort()
        tagCountList.reverse()
        return tagCountList
    def refreshImages(self, fileIDs):
        for widgets in self.imageFrame.winfo_children():
            widgets.destroy()
        y = 0
        x=0
        images = {}
        for i in range(len(fileIDs)):
            images[i] = customtkinter.CTkButton(master=self.imageFrame, text=str(fileIDs[i]), width=100, height=100, command=lambda e = i: self.openImage(e))
            images[i].grid(row=y, column=x, padx=10, pady=10)
            x+=1
            if x >= 6:
                x = 0
                y+=1

    def openImage(self, fileID):
        os.startfile(self.Archive.archiveList[fileID].data)
  
    def tag_click(self, tag):
        self.searchBar.insert("end", tag+" ")
    def search_click(self):
        self.reloadpage(0)
    def get_search(self):
        return self.searchBar.get().split(" ")
    def reloadpage(self, startFrom):
        try:
            currentfiles = (self.Archive.filterFiles(filterList=self.get_search(), start=startFrom, requestedFileCount=30))
            self.refreshTags(self.Archive, self.averageTags(self.Archive.archiveList, 42), 42)
            App.refreshImages(self,currentfiles)
        except:
            pass
    def fakeArchive(self):
        for i in range(1000):
            tempfile = ArchiveManager.ArchiveEntry()
            id = len(self.Archive.archiveList)    
            tempfile.ID = id
            tempfile.title = "title " + str(id)
            tempfile.creator = "creator" + str(id)
            tempfile.addTag(random.choice(["grey","ian","cameron","christian"]))
            tempfile.addTag(random.choice(["grey","ian","cameron","christian"]))
            tempfile.addTag(random.randint(2006,2023))
            tempfile.addTag(random.choice(["summer","autumn","winter","spring"]))
            tempfile.data = "data" + str(id)
            tempfile.misc_notes = "misc_notes" + str(id)

            self.Archive.archiveList.append(tempfile)
            
            

        #for tag in tagsToShow:

"""
app = App()
the_archive = ArchiveManager()
#tags=["tag1","tag2","tag3","tag4","tag5","tag6","tag7"]
for i in range(1000):
    tempfile = ArchiveManager.ArchiveEntry()
    id = len(the_archive.archiveList)    
    tempfile.ID = id
    tempfile.title = "title " + str(id)
    tempfile.creator = "creator" + str(id)
    tempfile.addTag(random.choice(["grey","ian","cameron","christian"]))
    tempfile.addTag(random.choice(["grey","ian","cameron","christian"]))
    tempfile.addTag(random.randint(2006,2023))
    tempfile.addTag(random.choice(["summer","autumn","winter","spring"]))
    tempfile.data = "data" + str(id)
    tempfile.misc_notes = "misc_notes" + str(id)

    the_archive.archiveList.append(tempfile)

tempTagGroup = ArchiveManager.TagGroup()
tempTagGroup.name = "The Boys"
tempTagGroup.color = "teal"
tempTagGroup.tags = ["christian","cameron","grey","ian"]

the_archive.tagGroupList.append(tempTagGroup)


app.refreshTags(the_archive, app.averageTags(the_archive.archiveList, 42), 42)
app.mainloop()

"""

app=App()
app.Archive.loadArchiveFromJson()
app.Archive.loadTagGroupsFromJson()
App.reloadpage(app, 0)

"""x = ArchiveManager.TagGroup()
x.name = "The Boys"
x.color = "teal"
x.tags = ["christian","cameron","grey","ian"]
app.Archive.tagGroupList.append(x)
app.Archive.saveTagGroupsToJson()"""


app.mainloop()
