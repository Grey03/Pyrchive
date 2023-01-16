#from archivebase import DataBaseEntry
import customtkinter, os, math, random
from Pyrchive import ArchiveManager
from tkinter import filedialog, messagebox
from PIL import Image


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
        self.savedsearchesButton=customtkinter.CTkButton(self.optionButtonsFrame, text="Saved Searches")
        self.savedsearchesButton.pack(side="left", padx=5,pady=5)
        self.randomButton=customtkinter.CTkButton(self.optionButtonsFrame, text= "Random", command= lambda : self.random_tag())
        self.randomButton.pack(side="left",padx=5,pady=5)
        self.refreshButton=customtkinter.CTkButton(self.optionButtonsFrame, text=r"↻", width=10, height=10, command= lambda : self.reloadpage(self.pageIndex * 30))
        self.refreshButton.pack(side="right",padx=5,pady=5)
        self.fileCountLabel=customtkinter.CTkLabel(self.optionButtonsFrame,text=f"Total File Count: {len(self.Archive.archiveList)}")
        self.fileCountLabel.pack(side="left",padx=5,pady=5)
        self.optionButtonsFrame.pack(padx=10, pady=5, fill="x")

        #Search Frame
        self.searchFrame = customtkinter.CTkFrame(self)
        self.favoriteButton = customtkinter.CTkButton(self.searchFrame, text="Save",width=50)
        self.favoriteButton.pack(side="left")
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
    def uploadWindow(self):
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
            self.reloadpage(0)

            window.destroy()

            

        


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

        window.mainloop()
    def fileWindow(self, fileID,):
        window = customtkinter.CTkToplevel(self)
        window.resizable(False,False)
        

        file = self.Archive.archiveList[fileID]

        window.title("File " + str(fileID))

        def open():
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

        

        

        def save():
            if (len(tagsEntry.get("0.0", "end").split(" "))) <= 0:
                return messagebox.showerror("Please enter at least one tag")
            if titleBox.get() == "": return messagebox.showerror("Error", "Title cannot be empty")
            if creatorBox.get() == "": return messagebox.showerror("Error", "Creator cannot be empty")
            if os.path.exists(fileLocationEntry.get()) != True: return messagebox.showerror("Error", "File does not exist")
            newEntry = ArchiveManager.ArchiveEntry()
            newEntry.ID = int(IDEntry.get())
            newEntry.title = titleBox.get()
            newEntry.creator = creatorBox.get()
            tags = tagsEntry.get("0.0", "end").split(" ")
            tags[len(tags)-1] = tags[len(tags)-1].replace("\n", "")
            newEntry.addTag(tags)
            newEntry.misc_notes = notesEntry.get("0.0", "end")
            newEntry.data = fileLocationEntry.get()
            self.Archive.add_Entry(newEntry)
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

                images[fileID] = customtkinter.CTkButton(master=frames[frameCount], text=formatedTitle, font=("Roboto", 16), width=150, height=150, command=lambda e=fileID: self.fileWindow(self.Archive.archiveList[e].ID))
                images[fileID].grid(row=0, column=id, padx=5, pady=5)
            

        
        """
            images = {}
            for n in range(5):
                Archive = self.Archive.archiveList
                imageName =(f"{Archive[i].title[0:30]} | {Archive[i].ID}")

                #images[i] = customtkinter.CTkButton(master=self.imageFrame, text=imageName, width=100, height=100, command=lambda e=i: self.fileWindow(Archive[e].ID))
        """
    def openImage(self, fileID):
        os.startfile(self.Archive.archiveList[fileID].data)
    def tag_click(self, tag):
        self.searchBar.delete(0, "end")
        self.searchBar.insert("end", tag)
        self.search_click()
    def search_click(self, *args):
        self.reloadpage(0)
    def get_search(self):
        return self.searchBar.get().split(" ")
    def random_tag(self):
        self.searchBar.delete(0, "end")
        randomItem =random.choice(self.Archive.archiveList)
        randomTag =random.choice(randomItem.tags)
        self.searchBar.insert("end", randomTag)
        self.get_search()
        self.search_click()
    def reloadpage(self, startFrom):
        self.fileCountLabel.configure(text=f"Total File Count: {len(self.Archive.archiveList)}")

        pagetotal = math.ceil(len(self.Archive.filterFiles(filterList=self.get_search(), start=self.pageIndex, requestedFileCount=-1))/30)
        self.currentPageLabel.configure(text=f"Page: {self.pageIndex+1} of {pagetotal}")

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
app.Archive.loadArchiveFromJson()
app.Archive.loadTagGroupsFromJson()
App.reloadpage(app, 0)


app.mainloop()
