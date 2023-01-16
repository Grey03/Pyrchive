#from archivebase import DataBaseEntry
import customtkinter, os, random
from Pyrchive import ArchiveManager
from tkinter import filedialog, messagebox



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
        self.uploadButton.bind("<Button-1>", command=self.uploadWindow)
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
    def uploadWindow(self, event):
        window = customtkinter.CTkToplevel(self)
        window.resizable(False,False)
        window.title("Upload File")

        global newData
        newData = ""

        def update_selected_file(file):
            global newData
            newData = file

        def select_file():
             update_selected_file(filedialog.askopenfilename(filetypes=[("All Files", "*.*")],))

        def uploadEntry(self, title, creator, tags, notes):
            global newData
            if (len(tags.get("0.0", "end").split(" "))) <= 0:
                return messagebox.showerror("Please enter at least one tag")
            if title.get() == "": return messagebox.showerror("Error", "Title cannot be empty")
            if creator.get() == "": return messagebox.showerror("Error", "Creator cannot be empty")
            if os.path.exists(newData) != True: return messagebox.showerror("Error", "File does not exist")
            newEntry = ArchiveManager.ArchiveEntry()
            newEntry.title = title.get()
            newEntry.creator = creator.get()
            tags = tags.get("0.0", "end").split(" ")
            tags[len(tags)-1] = tags[len(tags)-1].replace("\n", "")
            newEntry.addTag(tags)
            newEntry.misc_notes = notes.get("0.0", "end")
            newEntry.data = newData

            self.Archive.add_Entry(newEntry)
            self.Archive.saveArchiveToJson()

            #window.destroy()

            

        


        titleLabel = customtkinter.CTkLabel(window, text="Title:")
        titleBox = customtkinter.CTkEntry(master=window, placeholder_text="Title")
        creatorLabel = customtkinter.CTkLabel(window, text="Creator:")
        creatorBox = customtkinter.CTkEntry(master=window, placeholder_text="Creator")
        tagsLabel = customtkinter.CTkLabel(master=window, text="Tags")
        tagsEntry = customtkinter.CTkTextbox(master=window)
        openFileDialog = customtkinter.CTkButton(master=window, text="Upload File", command=select_file)
        notesLabel = customtkinter.CTkLabel(master=window, text="Notes")
        notesEntry = customtkinter.CTkTextbox(master=window)

        saveButton = customtkinter.CTkButton(master=window, text="Save", command=lambda: uploadEntry(self=self,title=titleBox, creator=creatorBox, tags=tagsEntry, notes=notesEntry,))

        exitButton = customtkinter.CTkButton(master=window, text="Exit")
        
        titleLabel.grid(row=0, column=0, sticky="w", padx=5,pady=5)
        titleBox.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        creatorLabel.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        creatorBox.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        tagsLabel.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        tagsEntry.grid(row=5, column=0, sticky="w", padx=5, pady=5)
        notesLabel.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        notesEntry.grid(row=5, column=1, sticky="w", padx=5, pady=5)

        openFileDialog.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        saveButton.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        exitButton.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        window.mainloop()
    def fileWindow(self, fileID,):
        window = customtkinter.CTkToplevel(self)
        window.resizable(False,False)
        window.title("Upload File")

        file = self.Archive.archiveList[fileID]

        if os.path.exists(file.data):
            os.system(file.data)
        else:
            messagebox.showerror("Error", f"Error opening file {file.data}, file may not exist or has been deleted/moved.")

        titleLabel = customtkinter.CTkLabel(window, text="Title:")
        titleBox = customtkinter.CTkEntry(master=window, placeholder_text="Title")
        creatorLabel = customtkinter.CTkLabel(window, text="Creator:")
        creatorBox = customtkinter.CTkEntry(master=window, placeholder_text="Creator")
        tagsLabel = customtkinter.CTkLabel(master=window, text="Tags")
        tagsEntry = customtkinter.CTkTextbox(master=window)
        notesLabel = customtkinter.CTkLabel(master=window, text="Notes")
        notesEntry = customtkinter.CTkTextbox(master=window)

        IDLabel = customtkinter.CTkLabel(master=window, text="ID:")
        IDEntry = customtkinter.CTkEntry(master=window, placeholder_text="ID")

        def edit():
            print ("Edit")
            window.quit()
            return

        editButton = customtkinter.CTkButton(master=window, text="Edit", command=edit)
        #editButton.bind("<Button-1>", edit)



        
        titleLabel.grid(row=0, column=0, sticky="w", padx=5,pady=5)
        titleBox.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        creatorLabel.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        creatorBox.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        tagsLabel.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        tagsEntry.grid(row=5, column=0, sticky="w", padx=5, pady=5)
        notesLabel.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        notesEntry.grid(row=5, column=1, sticky="w", padx=5, pady=5)

        IDLabel.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        IDEntry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        editButton.grid(row=3, column=1, sticky="w", padx=5, pady=5)



        def import_data(mainWindow):
            titleBox.insert("end", newEntry.title)
            titleBox.configure(state="readonly")
            creatorBox.insert("end", newEntry.creator)
            creatorBox.configure(state="readonly")
            tags = ", ".join(str(e) for e in newEntry.tags)
            tagsEntry.insert("end", tags)
            tagsEntry.configure(state="disabled")
            notesEntry.insert("end", newEntry.misc_notes)
            notesEntry.configure(state="disabled")
            IDEntry.insert("end", newEntry.ID)
            IDEntry.configure(state="readonly")


        import_data(window)

        window.mainloop()


        
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
            images[i] = customtkinter.CTkButton(master=self.imageFrame, text=str(self.Archive.archiveList[fileIDs[i]].title), width=100, height=100, command=lambda e = i: self.fileWindow(e))
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
