import customtkinter, os, math, random, shutil, json
from Pyrchive import ArchiveManager
from tkinter import filedialog, messagebox
from tktooltip import ToolTip
#from PIL import Image

global colors
global __location__
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

colors = json.load(open(str(__location__) + "/colors.json"))
colors = colors["DefaultColors"]

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):         
    def __init__(self):
        super().__init__()



        self.title("Tarchive")
        self.geometry(f"{1135}x{925}")
        
        self.Archive = ArchiveManager()
        self.pageIndex = 0

        #Top Buttons Frame
        self.optionButtonsFrame=customtkinter.CTkFrame(self)
        #-+-+-+-+-+-
        self.settingsButton=customtkinter.CTkButton(self.optionButtonsFrame, text="Settings", command=lambda :self.settingsWindow())
        self.settingsButton.pack(side="left", padx=5,pady=5)
        self.uploadButton=customtkinter.CTkButton(self.optionButtonsFrame,text="Upload", command=lambda : self.uploadWindow())
        self.uploadButton.pack(side="left", padx=5,pady=5)
        self.savedSearchesDropdown=customtkinter.CTkOptionMenu(self.optionButtonsFrame, values=["Saved Searches: "], command=lambda event: self.saved_search_click(event))
        self.savedSearchesDropdown.pack(side="left", padx=5,pady=5)
        self.showAllTagsButton=customtkinter.CTkButton(self.optionButtonsFrame,text="Show All Tags", command=lambda : self.showTagsList())
        self.showAllTagsButton.pack(side="left", padx=5,pady=5)
        self.randomButton=customtkinter.CTkButton(self.optionButtonsFrame, text= "Random", command= lambda : self.random_tag())
        self.randomButton.pack(side="left",padx=5,pady=5)
        self.refreshButton=customtkinter.CTkButton(self.optionButtonsFrame, text=r"↻", width=10, height=10, command= lambda : self.reloadpage(self.pageIndex * 30))
        self.refreshButton.pack(side="right",padx=5,pady=5)
        self.fileCountLabel=customtkinter.CTkLabel(self.optionButtonsFrame,text=f"Total File Count: {len(self.Archive.archiveList)}")
        self.fileCountLabel.pack(side="left",padx=5,pady=5)
        self.optionButtonsFrame.pack(padx=10, pady=5, fill="x")

        #Search Frame
        self.searchFrame = customtkinter.CTkFrame(self)
        self.saveButton = customtkinter.CTkButton(self.searchFrame, text="Save",width=50, command = lambda : self.save_search_click())
        self.saveButton.pack(side="left")
        self.searchBar= customtkinter.CTkEntry(self.searchFrame,placeholder_text="Search")
        self.searchBar.bind("<Return>", command=lambda a : self.search_click(a))
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
        self.pageLeft = customtkinter.CTkButton(self.pageButtonFrame, text="Previous", command=lambda: self.previousPage())
        self.pageLeft.grid(row=0, column=0)
        self.currentPageLabel = customtkinter.CTkLabel(self.pageButtonFrame, text=f"Page: {self.pageIndex+1}")
        self.currentPageLabel.grid(row=0, column=1)
        self.pageRight = customtkinter.CTkButton(self.pageButtonFrame, text="Next", command=lambda: self.nextPage())
        self.pageRight.grid(row=0, column=2)
        self.pageButtonFrame.pack()
    def showTagsList(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry("600x400")
        window.resizable(False,False)
        window.title("Tags List")

        mainList = customtkinter.CTkTextbox(window, state="normal", font=("Roboto", 24, "bold"), width=window.winfo_width(), height=window.winfo_height())
        tags = self.Archive.get_all_tags()
        mainList.insert("end", "\n".join(tags))
        mainList.configure(state="disabled")
        mainList.pack(padx=5, pady=5)

        window.mainloop()
    def savedSearchEditor(self):
        window = customtkinter.CTkToplevel(self)
        window.resizable(False,False)
        window.title("Saved Search Editor")

        def deleteSearch(listID):
            self.Archive.savedSearches.pop(listID-1)
            self.Archive.saveSavesToJson()
            refreshWindow()
            self.reloadpage(0)

        def refreshWindow():
            for children in window.winfo_children():
                children.destroy()
            self.Archive.loadTagGroupsFromJson()
            self.Archive.loadSavesFromJson()
            searchFrame = {}
            for i in range(len(self.Archive.savedSearches)):
                savedSearch = self.Archive.savedSearches[i]

                searchFrame[i] = customtkinter.CTkFrame(window)
                EntryBox = customtkinter.CTkEntry(searchFrame[i], width=500)
                EntryBox.insert("end", str(" ".join(savedSearch)))
                EntryBox.configure(state="readonly")
                EntryBox.pack(side="left")
                DeleteButton = customtkinter.CTkButton(searchFrame[i], text="X", width=10, height=10, fg_color="red", hover_color="darkred",font=("Roboto", 12, "bold"),command=lambda : deleteSearch(i))
                DeleteButton.pack(side="left")
                searchFrame[i].pack()
        
        refreshWindow()
        


        window.mainloop()
    def tagGroupEditor(self):
        global colors
        window = customtkinter.CTkToplevel(self)
        window.resizable(False,False)
        window.title("Tag Group Editor")

        mainFrame = customtkinter.CTkFrame(window)
        def createNewTagGroup():
            tagGroup = ArchiveManager.TagGroup()
            tagGroup.name="NewTagGroup"
            tagGroup.color = colors["DarkGray"]
            tagGroup.tags = []
            tagGroup.description = ""
            self.Archive.tagGroupList.append(tagGroup)
            self.Archive.saveTagGroupsToJson()
            self.reloadpage(0)
            loadGroup()

        def dropDownClick(dropdown, entry, **kwargs):
            #This is kinda bad so i should fix this another time
            refresh = False
            for key, value in kwargs.items():
                if key == "refresh": refresh = value
            entry.delete(0,"end")
            entry.insert("end", dropdown.get())
            if refresh:
                loadGroup(Name = entry.get())
        tagGroupNameEntry = customtkinter.CTkEntry(mainFrame, placeholder_text="Name")
        tagGroupDropdown = customtkinter.CTkOptionMenu(mainFrame, values=["Tag Groups"], command=lambda e: dropDownClick(tagGroupDropdown, tagGroupNameEntry, refresh=True))
        #Make color list with all hexes
        def colorDropDownClick(dropdown, entry):
            entry.delete(0,"end")
            entry.insert("end", colors[dropdown.get()])
        colorEntry = customtkinter.CTkEntry(mainFrame, placeholder_text="Color ARGB: ")
        colorDropdown = customtkinter.CTkOptionMenu(mainFrame, values=["colorDropdown"], command=lambda e: colorDropDownClick(colorDropdown, colorEntry))
  
        tagsLabel = customtkinter.CTkLabel(mainFrame, text="Tags")
        tagsTextBox = customtkinter.CTkTextbox(mainFrame)
        descriptionLabel = customtkinter.CTkLabel(mainFrame, text="Description")
        descriptionTextBox = customtkinter.CTkTextbox(mainFrame)

        saveButton = customtkinter.CTkButton(window, text="Save", command = lambda : saveGroup(tagGroupDropdown,tagGroupNameEntry))
        createNewButton = customtkinter.CTkButton(window, text="Create New Tag Group", command=lambda: createNewTagGroup())


        tagGroupDropdown.grid(row=0, column=0, padx=5, pady=5)
        tagGroupNameEntry.grid(row=0, column=1, padx=5, pady=5)
        colorDropdown.grid(row=1, column=0, padx=5, pady=5)
        colorEntry.grid(row=1, column=1, padx=5, pady=5)
        tagsLabel.grid(row=2, column=0, padx=5, pady=5)
        tagsTextBox.grid(row=3, column=0, padx=5, pady=5)
        descriptionLabel.grid(row=2, column=1, padx=5, pady=5)
        descriptionTextBox.grid(row=3, column=1, padx=5, pady=5)

        mainFrame.pack()
        saveButton.pack(padx=5, pady=5)
        createNewButton.pack(padx= 5, pady=5)

        def saveGroup(tagGroupDrop,tagGroupEntry):
            file = ArchiveManager.TagGroup()
            newFile = False
            try:
                for TagGroup in self.Archive.tagGroupList:
                    if TagGroup.name == tagGroupDrop.get():
                        file = TagGroup
            except:
                newFile= True
                print ("Failed to find group making new group")
            file.name = tagGroupEntry.get()
            file.color = colorEntry.get()
            tags =tagsTextBox.get("0.0", "end").split(" ")
            file.tags = [*set(tags)]
            file.set_Tags(tags)
            if descriptionTextBox.get("0.0", "end").replace("\n","") == "":
                file.description = ""
            else:
                file.description = descriptionTextBox.get("0.0", "end")
            if newFile:
                self.Archive.tagGroupList.append(file)
            self.Archive.saveTagGroupsToJson()
            self.reloadpage(0)
            window.destroy()

        def colorFinder(hexColor):
            for key, value in colors.items():
                if value == hexColor:
                    return str(key)
            return "Custom Color"

        def loadGroup(**TagGroupName):
            global colors
            ID = 0
            Name = ""
            for key, value in TagGroupName.items():
                if key == "ID": ID = value
                if key == "Name" : Name = value
            global colors

            if Name != "":
                count = 0
                for TagGroup in self.Archive.tagGroupList:
                    if TagGroup.name == Name:
                        ID = count
                    count+=1

            tagGroup = self.Archive.tagGroupList[ID]

            tagNames=[tagName.name for tagName in self.Archive.tagGroupList]
            tagGroupDropdown.configure(values=tagNames)
            tagGroupDropdown.set(tagNames[ID])

            dropDownClick(tagGroupDropdown, tagGroupNameEntry)
            
            colorList = list(colors.keys())
            colorDropdown.configure(values= colorList)
            colorDropdown.set(colorFinder(tagGroup.color))

            colorEntry.delete(0,"end")
            colorEntry.insert("end", tagGroup.color)

            tagGroupNameEntry.delete("0", "end")
            tagGroupNameEntry.insert("0", tagNames[ID])

            tagsTextBox.delete("0.0", "end")
            tagsTextBox.insert("0.0", " ".join(tagGroup.tags))

            descriptionTextBox.delete("0.0", "end")
            descriptionTextBox.insert("0.0", tagGroup.description)

        self.Archive.loadTagGroupsFromJson()
        if len(self.Archive.tagGroupList) > 0:
            loadGroup(ID=0)
        else:
            createNewTagGroup()

        window.mainloop()
    def uploadWindow(self):
        window = customtkinter.CTkToplevel(self)
        window.resizable(False,False)
        window.title("Upload File")

        global newData
        newData = ""

        def update_selected_file(file):
            global newData
            newData = file
        def select_file(EntryBox):
            update_selected_file(filedialog.askopenfilename(filetypes=[("All Files", "*.*")],))
            global newData
            EntryBox.configure(state="normal")
            EntryBox.delete(0, "end")
            EntryBox.insert(0, newData)
            EntryBox.configure(state="readonly")
        def copy_file_to_locals(filename):
            if str(__location__) in filename.split("/"):
                return filename
            file = open(filename, "rb") 
            thefilename=filename.split("/")[-1]
            localFileFolder = open(str(__location__) + "/localFiles/"+ thefilename, "wb")
            shutil.copyfileobj(file, localFileFolder)
            return str(__location__) + "/localFiles/"+ thefilename
        def uploadEntry(self, title, creator, tags, notes):
            global newData
            if (len(tags.get("0.0", "end").split(" "))) <= 0:
                return messagebox.showerror("Please enter at least one tag")
            if title.get() == "": return messagebox.showerror("Error", "Title cannot be empty")
            if os.path.exists(newData) != True: return messagebox.showerror("Error", "File does not exist")
            newEntry = ArchiveManager.ArchiveEntry()
            newEntry.title = title.get()
            newEntry.creator = creator.get()
            tags = tags.get("0.0", "end").split(" ")
            tags[len(tags)-1] = tags[len(tags)-1].replace("\n", "")
            newEntry.addTag(tags)
            newEntry.misc_notes = notes.get("0.0", "end")
            if self.Archive.localFiles:
                newData = copy_file_to_locals(newData)
            newEntry.data = newData

            self.Archive.add_Entry(newEntry)
            self.Archive.saveArchiveToJson()
            self.reloadpage(0)

            window.destroy()
 
        mainBox = customtkinter.CTkFrame(window)

        titleLabel = customtkinter.CTkLabel(mainBox, text="Title:")
        titleBox = customtkinter.CTkEntry(master=mainBox, placeholder_text="Title")
        allTagsButton = customtkinter.CTkButton(mainBox, text="View All Tags", command=lambda : self.showTagsList())
        creatorLabel = customtkinter.CTkLabel(mainBox, text="Creator:")
        creatorBox = customtkinter.CTkEntry(master=mainBox, placeholder_text="Creator")
        tagsLabel = customtkinter.CTkLabel(master=mainBox, text="Tags")
        tagsEntry = customtkinter.CTkTextbox(master=mainBox)
        notesLabel = customtkinter.CTkLabel(master=mainBox, text="Notes")
        notesEntry = customtkinter.CTkTextbox(master=mainBox)
        
        titleLabel.grid(row=0, column=0, sticky="w", padx=5,pady=5)
        titleBox.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        allTagsButton.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        creatorLabel.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        creatorBox.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        tagsLabel.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        tagsEntry.grid(row=5, column=0, sticky="w", padx=5, pady=5)
        notesLabel.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        notesEntry.grid(row=5, column=1, sticky="w", padx=5, pady=5)

        mainBox.pack()

        selectedFileEntry = customtkinter.CTkEntry(master=window, placeholder_text="Selected File: ", width=400)
        selectedFileEntry.configure(state="readonly")
        openFileDialog = customtkinter.CTkButton(master=window, text="Upload File", command=lambda : select_file(selectedFileEntry))
        
        saveButton = customtkinter.CTkButton(master=window, text="Save", command=lambda: uploadEntry(self=self,title=titleBox, creator=creatorBox, tags=tagsEntry, notes=notesEntry,))

        openFileDialog.pack(padx=5, pady=5)
        selectedFileEntry.pack(padx=5, pady=5)

        saveButton.pack(padx=5, pady=5)

        window.mainloop()
    def fileWindow(self, fileID,):
        window = customtkinter.CTkToplevel(self)
        window.resizable(False,False)
        

        file = self.Archive.archiveList[fileID]

        window.title("File " + str(fileID))

        def open():
            if self.Archive.localFiles:
                if  os.path.exists(str(__location__) + file.data):
                    os.system('"' + str(__location__) + file.data + '"')
                else: messagebox.showerror("Error", f"Error opening file {file.data}, file may not exist, has been deleted/moved, or may/may not require the local file setting")
            if os.path.exists(file.data):
                os.system('"' + file.data + '"')
            else:
                messagebox.showerror("Error", f"Error opening file {file.data}, file may not exist or has been deleted/moved.")

        mainFrame = customtkinter.CTkFrame(window, fg_color="transparent")

        titleLabel = customtkinter.CTkLabel(mainFrame, text="Title:")
        titleBox = customtkinter.CTkEntry(mainFrame, placeholder_text="Title", width=200)
        creatorLabel = customtkinter.CTkLabel(mainFrame, text="Creator:")
        creatorBox = customtkinter.CTkEntry(mainFrame, placeholder_text="Creator", width=200)
        tagsLabel = customtkinter.CTkLabel(mainFrame, text="Tags")
        tagsEntry = customtkinter.CTkTextbox(mainFrame, width=200)
        notesLabel = customtkinter.CTkLabel(mainFrame, text="Notes")
        notesEntry = customtkinter.CTkTextbox(mainFrame, width=200)

        uploadLabel = customtkinter.CTkLabel(mainFrame, text="Upload Date:")
        uploadEntry = customtkinter.CTkEntry(mainFrame, placeholder_text="Upload Date", width=200)

        IDLabel = customtkinter.CTkLabel(mainFrame, text="ID:")
        IDEntry = customtkinter.CTkEntry(mainFrame, placeholder_text="ID", width=200)

        def edit(self):
            self.editWindow(file.ID)
            print ("Edit")
            window.quit()

        fileLocationLabel = customtkinter.CTkLabel(window, text="File Location:")
        fileLocation = customtkinter.CTkEntry(window, placeholder_text="File Location:", width=400)
        editButton = customtkinter.CTkButton(window, text="Edit", command=lambda : edit(self))
        openButton = customtkinter.CTkButton(window, text="Open", command=lambda : open())
        


        mainFrame.pack()
        
        titleLabel.grid(row=0, column=0, sticky="w", padx=5,pady=5)
        titleBox.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        creatorLabel.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        creatorBox.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        tagsLabel.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        tagsEntry.grid(row=5, column=0, sticky="w", padx=5, pady=5)
        notesLabel.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        notesEntry.grid(row=5, column=1, sticky="w", padx=5, pady=5)


        uploadLabel.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        uploadEntry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        IDLabel.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        IDEntry.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        fileLocationLabel.pack(padx=5, pady=5)
        fileLocation.pack(padx=5, pady=5)
        editButton.pack(padx=5, pady=5)
        openButton.pack(padx=5, pady=5)



        def import_data(mainWindow):
            titleBox.insert("end", file.title)
            titleBox.configure(state="readonly")
            creatorBox.insert("end", file.creator)
            creatorBox.configure(state="readonly")
            tags = " ".join(str(e) for e in file.tags)
            tagsEntry.insert("end", tags)
            tagsEntry.configure(state="disabled")
            notesEntry.insert("end", file.misc_notes)
            notesEntry.configure(state="disabled")
            IDEntry.insert("end", file.ID)
            IDEntry.configure(state="readonly")
            uploadEntry.insert("end", file.upload_date)
            uploadEntry.configure(state="readonly")
            fileLocation.insert("end", file.data)
            fileLocation.configure(state="readonly")


        import_data(window)

        window.mainloop()
    def editWindow(self, fileID,):
        window = customtkinter.CTkToplevel(self)
        window.resizable(False,False)
        window.title("Edit File")

        file = self.Archive.archiveList[fileID]

        mainFrame = customtkinter.CTkFrame(window, fg_color="transparent")

        titleLabel = customtkinter.CTkLabel(mainFrame, text="Title:")
        titleBox = customtkinter.CTkEntry(mainFrame, placeholder_text="Title", width=200)
        creatorLabel = customtkinter.CTkLabel(mainFrame, text="Creator:")
        creatorBox = customtkinter.CTkEntry(mainFrame, placeholder_text="Creator", width=200)
        tagsLabel = customtkinter.CTkLabel(mainFrame, text="Tags")
        tagsEntry = customtkinter.CTkTextbox(mainFrame, width=200)
        notesLabel = customtkinter.CTkLabel(mainFrame, text="Notes")
        notesEntry = customtkinter.CTkTextbox(mainFrame, width=200)
        uploadLabel = customtkinter.CTkLabel(mainFrame, text="Upload Date:")
        uploadEntry = customtkinter.CTkEntry(mainFrame, placeholder_text="Upload Date", width=200)
        IDLabel = customtkinter.CTkLabel(mainFrame, text="ID:")
        IDEntry = customtkinter.CTkEntry(mainFrame, placeholder_text="ID", width=200)

    
        mainFrame.pack()

        

        fileLocationLabel = customtkinter.CTkLabel(window, text="File Location:")
        fileLocationEntry = customtkinter.CTkEntry(window, placeholder_text="File Location: ", width=400)

        def newLocation():
            fileLocationEntry.configure(state="normal")
            fileLocationEntry.delete("0", "end")
            x = str(filedialog.askopenfilename(filetypes=[("All Files", "*.*")]))
            fileLocationEntry.insert("end", x)
            fileLocationEntry.configure(state="readonly")

        fileLocationSelector = customtkinter.CTkButton(window, text="Browse to New File", command=lambda : newLocation())


        

        

        def save():
            if (len(tagsEntry.get("0.0", "end").split(" "))) <= 0:
                return messagebox.showerror("Please enter at least one tag")
            if titleBox.get() == "": return messagebox.showerror("Error", "Title cannot be empty")
            if os.path.exists(fileLocationEntry.get()) != True: return messagebox.showerror("Error", "File does not exist")
            newEntry = ArchiveManager.ArchiveEntry()
            newEntry.ID = int(IDEntry.get())
            newEntry.title = titleBox.get()
            newEntry.creator = creatorBox.get()
            tags = tagsEntry.get("0.0", "end").split(" ")
            tags[len(tags)-1] = tags[len(tags)-1].replace("\n", "")
            newEntry.addTag(tags)
            if newEntry.misc_notes.replace("\n","")=="":
                newEntry.misc_notes = ""
            else:
                newEntry.misc_notes = notesEntry.get("0.0", "end")
            newEntry.data = fileLocationEntry.get() 
            print (fileLocationEntry.get())
            if os.path.exists(fileLocationEntry.get()):
                self.data = fileLocationEntry.get()
            self.Archive.update_Entry(newEntry)
            self.Archive.saveArchiveToJson()
            self.reloadpage(0)

            window.destroy()

        def delete():
            x= messagebox.askyesno("Are you sure?", "Do you want to delete this entry?", icon='warning')
            if x != True: return
            self.Archive.delete_entry(int(IDEntry.get()))
            self.Archive.saveArchiveToJson()
            self.reloadpage(0)
            window.destroy()

        saveButton = customtkinter.CTkButton(window, text="Save", command=save)
        deleteButton = customtkinter.CTkButton(window, text="Delete File", command=lambda : delete())
            

        titleLabel.grid(row=0, column=0, sticky="w", padx=5,pady=5)
        titleBox.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        creatorLabel.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        creatorBox.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        tagsLabel.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        tagsEntry.grid(row=5, column=0, sticky="w", padx=5, pady=5)
        notesLabel.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        notesEntry.grid(row=5, column=1, sticky="w", padx=5, pady=5)
        uploadLabel.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        uploadEntry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        IDLabel.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        IDEntry.grid(row=3, column=1, sticky="w", padx=5, pady=5)


        fileLocationLabel.pack(padx=5, pady=5)
        fileLocationEntry.pack(padx=5, pady=5)
        fileLocationSelector.pack(padx=5, pady=5)
        saveButton.pack(padx=5, pady=5)
        deleteButton.pack(padx=5, pady=5)

        


        def import_data():
            titleBox.insert("end", file.title)
            creatorBox.insert("end", file.creator)
            tags = " ".join(str(e) for e in file.tags)
            tagsEntry.insert("end", tags)
            notesEntry.insert("end", file.misc_notes)
            IDEntry.insert("end", file.ID)
            IDEntry.configure(state="readonly")
            uploadEntry.insert("end", file.upload_date)
            uploadEntry.configure(state="readonly")
            fileLocationEntry.insert("end", file.data)
            fileLocationEntry.configure(state="readonly")



        import_data()

        window.mainloop()
    def settingsWindow(self):
        window = customtkinter.CTkToplevel(self)
        window.resizable(False,False)
        window.title("Settings")

        def openFileChange(self, switch):
            self.Archive.openFilesImmediately = bool(switch.get())
            self.Archive.saveSettingsToJson()
        def openMenuChange(self, switch):
            self.Archive.openMenuImmediately = bool(switch.get())
            self.Archive.saveSettingsToJson()
        def localFileChange(self, switch):
            self.Archive.localFiles = bool(switch.get())
            self.Archive.saveSettingsToJson()
        settingsLabel = customtkinter.CTkLabel(window, text="Settings", font=("Roboto", 24, "bold"))
        settingsLabel.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        openFile = customtkinter.CTkCheckBox(window, text="Open Files Immediately", command=lambda : openFileChange(self, openFile))
        openFile.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ToolTip(openFile, msg="Opens the file immediatly when clicking a file in the browser")

        openMenu = customtkinter.CTkCheckBox(window, text="Open Files' Menu", command=lambda : openMenuChange(self, openMenu))
        openMenu.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ToolTip(openMenu, msg="Opens the file's menu when clicking a file in the browser")

        localFiles = customtkinter.CTkCheckBox(window, text="Local Files", command=lambda : localFileChange(self, localFiles))
        localFiles.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        ToolTip(localFiles, msg="When uploading a file, the file will be placed in the local files directory")

        def openLocalFile():
            os.startfile(str(__location__)+"/localFiles")

        localFileButton = customtkinter.CTkButton(window, text="Local File", command=lambda : openLocalFile())
        localFileButton.grid(row=4, column=0, sticky="w", padx=5, pady=5)


        tagGroupEditorButton = customtkinter.CTkButton(window, text="Tag Group Editor", command=lambda : self.tagGroupEditor())
        tagGroupEditorButton.grid(row=5, column=0, sticky="w", padx=5, pady=5)

        savedSearchEditorButton = customtkinter.CTkButton(window, text="Saved Search Editor", command=lambda : self.savedSearchEditor())
        savedSearchEditorButton.grid(row=5, column=1, sticky="w", padx=5, pady=5)

        def loadSettings(self):
            self.Archive.loadSettingsFromJson()
            def setSwitch(switch, state:bool):
                if state: switch.select()
                else: switch.deselect()
            setSwitch(openFile, self.Archive.openFilesImmediately)
            setSwitch(openMenu, self.Archive.openMenuImmediately)
            setSwitch(localFiles, self.Archive.localFiles)

        loadSettings(self)



        
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
                        if tagcolor.startswith("#"):
                            tagcolor = tagcolor[3:]
                            tagcolor = "#" + tagcolor
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
        #WORK ON THIS GET IT GOOD, MAYBE USE ARRAYS IN FRAMES?!
        for widgets in self.imageFrame.winfo_children():
            widgets.destroy()
        frameWidth = (math.ceil(len(fileIDs)/6))
        frames = {}
        for frameCount in range(frameWidth):
            frames[frameCount] = customtkinter.CTkFrame(self.imageFrame, fg_color="transparent",height=175)
            frames[frameCount].pack()
            images ={}
            for id in range(frameCount*6, (frameCount+1)*6):
                fileID = fileIDs[id]
                file = self.Archive.archiveList[int(fileID)]

                if (len(file.title) > 12): formatedTitle = (f"{file.title[0:12]}... | {file.ID}")
                else: formatedTitle = (f"{file.title[0:15]} | {file.ID}")

                images[fileID] = customtkinter.CTkButton(master=frames[frameCount], text=formatedTitle, font=("Roboto", 16), width=150, height=150, command=lambda e=fileID: self.openFile(self.Archive.archiveList[e].ID))
                #icon = customtkinter.CTkImage(dark_image=Image.open(file.data), size=(50,50))
                #images[fileID].configure(image=icon)
                images[fileID].grid(row=0, column=id, padx=5, pady=5)
            

        
        """
            images = {}
            for n in range(5):
                Archive = self.Archive.archiveList
                imageName =(f"{Archive[i].title[0:30]} | {Archive[i].ID}")

                #images[i] = customtkinter.CTkButton(master=self.imageFrame, text=imageName, width=100, height=100, command=lambda e=i: self.fileWindow(Archive[e].ID))
        """
    def openFile(self, fileID):
        if self.Archive.openFilesImmediately:
            os.startfile(self.Archive.archiveList[fileID].data)
        if self.Archive.openMenuImmediately:
            self.fileWindow(fileID)
    def tag_click(self, tag):
        self.searchBar.insert("end", " " + tag)
        self.search_click()
    def search_click(self, *args):
        self.reloadpage(0)
    def get_search(self):
        return self.searchBar.get().split(" ")
    def save_search_click(self):
        #when you click save not the drop down
        newSave = ([*set(self.searchBar.get().split(" "))])
        try: newSave.remove("")
        except: pass
        self.Archive.savedSearches.append(newSave)
        self.Archive.saveSavesToJson()
        self.reloadpage(0)
    def saved_search_click(self, search):
        #when you click the drop down not the save
        self.searchBar.delete(0, "end")
        self.searchBar.insert("end", search)
        self.search_click()
    def random_tag(self):
        self.searchBar.delete(0, "end")
        randomItem =random.choice(self.Archive.archiveList)
        randomTag =random.choice(randomItem.tags)
        self.searchBar.insert("end", randomTag)
        self.search_click()
    def reloadpage(self, startFrom):
        self.fileCountLabel.configure(text=f"Total File Count: {len(self.Archive.archiveList)}")

        pagetotal = math.ceil(len(self.Archive.filterFiles(filterList=self.get_search(), start=self.pageIndex, requestedFileCount=-1))/30)
        self.currentPageLabel.configure(text=f" Page: {self.pageIndex+1} of {pagetotal} ")
        saves = self.Archive.savedSearches
        finalSaveList=[]
        for save in saves:
            finalSaveList.append(" ".join(save))
        self.savedSearchesDropdown.configure(values=finalSaveList)

        try:
            currentfiles = (self.Archive.filterFiles(filterList=self.get_search(), start=startFrom, requestedFileCount=30))
            self.refreshTags(self.Archive, self.averageTags(self.Archive.archiveList, 42), 42)
            App.refreshImages(self,currentfiles)
        except:
            pass
    def previousPage(self):
        if self.pageIndex > 0:
            self.pageIndex -= 1
            self.reloadpage(self.pageIndex * 30)
    def nextPage(self):
        pagetotal = math.ceil(len(self.Archive.filterFiles(filterList=self.get_search(), start=self.pageIndex, requestedFileCount=-1))/30)
        if self.pageIndex + 1 < pagetotal:
            self.pageIndex += 1
            self.reloadpage(self.pageIndex * 30)
app=App()
app.Archive.loadAll()
App.reloadpage(app, 0)

app.mainloop()
