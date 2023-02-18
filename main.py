import customtkinter
import os
import shutil
import logging
import time
import math
import random

from Pyrchive import archivemanager
from tkinter import filedialog, messagebox
from tktooltip import ToolTip
from PIL import Image, ImageTk


logger = logging.getLogger(__name__)

global __location__
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

class App(customtkinter.CTk):         
    def __init__(self):
        super().__init__()
        self.title("Tarchive")
        #self.geometry(f"{1135}x{925}")
        self.minsize(950, 700)

        self.Archive = archivemanager()
        self.Archive.loadAll()

        self.pageIndex = 0
        self.filecount = len(self.Archive.entriesList)

        logger.info("Tarchive App initialized")

        #Top Buttons Frame
        self.optionButtonsFrame=customtkinter.CTkFrame(self)
        #-+-+-+-+-+-
        self.settingsButton=customtkinter.CTkButton(self.optionButtonsFrame, text="Settings")
        self.settingsButton.pack(side="left", padx=5,pady=5)
        self.uploadButton=customtkinter.CTkButton(self.optionButtonsFrame,text="Upload")
        self.uploadButton.pack(side="left", padx=5,pady=5)
        self.savedSearchesDropdown=customtkinter.CTkOptionMenu(self.optionButtonsFrame, values=(self.Archive.savedSearches), command=lambda e: self.autoSearch(e))
        self.savedSearchesDropdown.set("Saved Searches: ")
        self.savedSearchesDropdown.pack(side="left", padx=5,pady=5)
        #self.showAllTagsButton=customtkinter.CTkButton(self.optionButtonsFrame,text="Show All Tags")
        #self.showAllTagsButton.pack(side="left", padx=5,pady=5)
        self.randomButton=customtkinter.CTkButton(self.optionButtonsFrame, text= "Random", command= lambda: self.autoSearch(random.choice(self.Archive.getAllTags())))
        self.randomButton.pack(side="left",padx=5,pady=5)
        #self.refreshButton=customtkinter.CTkButton(self.optionButtonsFrame, text=r"↻", font=("Roboto", 16, "bold"), width=30, height=30)
        #self.refreshButton.pack(side="right",padx=5,pady=5)
        self.fileCountLabel=customtkinter.CTkLabel(self.optionButtonsFrame,text=f"Total File Count: {self.filecount}")
        self.fileCountLabel.pack(side="left",padx=5,pady=5)
        self.optionButtonsFrame.pack(padx=10, pady=5, fill="x")

        self.searchFrame = customtkinter.CTkFrame(self)
        self.saveButton = customtkinter.CTkButton(self.searchFrame, text="💾", font=("Roboto", 16, "bold"), width=30, height=30, command=lambda: self.saveSearch())
        self.saveButton.pack(side="left")
        self.searchBar= customtkinter.CTkEntry(self.searchFrame,placeholder_text="Search")
        self.searchBar.bind("<Return>",command= lambda e: self.search())
        self.searchBar.pack(padx=5,side="left", fill="x",expand=True)
        self.clearButton = customtkinter.CTkButton(self.searchFrame, text="Clear", width=80, command = lambda: self.searchBar.delete("0", "end"))
        self.clearButton.pack(side="left", padx=5, pady=5)
        self.searchButton = customtkinter.CTkButton(self.searchFrame, text="Search", width=80, command= lambda: self.search())
        self.searchButton.pack(side="left", padx=5, pady=5)
        self.searchFrame.pack(padx=10, pady=5,fill="x")

        self.bottomFrame=customtkinter.CTkFrame(self, fg_color="transparent")
        self.tagFrame=customtkinter.CTkFrame(self.bottomFrame, width=200)
        self.tagLabel=customtkinter.CTkLabel(self.tagFrame, text="Tags", font=("Roboto", 13, "bold"))
        self.tagLabel.pack(padx=5,pady=0)
        self.tagListFrame = customtkinter.CTkFrame(self.tagFrame)
        self.tagListFrame.pack(padx=5,pady=5, expand=True, fill="both")
        self.tagFrame.pack(side="left", fill="y")
        self.mainFrame=customtkinter.CTkFrame(self.bottomFrame, fg_color="transparent")
        self.mainFrame.pack(side="left",fill="both", expand=True)
        self.bottomFrame.pack(fill="both",expand=True,padx=10,pady=5)

        logger.info(f"Started in {'%.2f' % (time.time() - fileStartTime)}s.")

        self.autoSearch("")

    def clearSearch(self):
        self.searchBar.delete("0","end")
    def fillSearch(self, fillWords):
        self.clearSearch()
        self.searchBar.insert("end", fillWords)
    def autoSearch(self, search):
        self.fillSearch(search)
        self.search()
    def search(self, *args):
        if self.searchBar.get() != "":
            searchList = (self.searchBar.get().split(" "))
            searchList = [*set(searchList)]
            print (searchList)
            try:
                searchList.remove(" ")
            except:
                pass
            try:
                searchList.remove("")
            except:
                pass
        else:
            searchList = []
        x = self.Archive.filterEntryList(searchList, -1)
        App.entryBrowseScreen(self, x)
    def clearFrame(self):
        if len(self.winfo_children()) < 1:
            return
        for child in self.winfo_children():
            child.destroy()
    def entryBrowseScreen(self, entries, **kwargs):
        logger.info(f"Entering Browse Screen with {len(entries)} entries on screen.")
        start = 0
        for key,value in kwargs.items():
            if key == "start": start = value
        maxWidth = 10
        maxImages = 60
        entries = entries[start:maxImages]
        App.clearFrame(self.mainFrame)
        buttons = {}
        allTags = []
        for ID, entry in enumerate(entries):
            buttons[ID] = customtkinter.CTkButton(self.mainFrame, width=150,height=150, text=entry.get("ID", "Invalid ID"), command = lambda e=ID: self.entryViewScreen(entries[e]))
            buttons[ID].grid(row=math.floor(ID/maxWidth), column=ID%maxWidth, padx=5, pady=5)
            allTags.extend(entry.get("tags",""))
        self.tagListDisplay(allTags)
        
            
    def entryViewScreen(self, entry):
        print(entry)
        App.clearFrame(self.mainFrame)
        logger.info(f"Opening window for entry {entry.get('ID', 'Invalid ID')}")

        mediaWindow = customtkinter.CTkFrame(self.mainFrame)
        #run function to either display a video or an image
        mediaWindow.pack(fill="both", expand=True, padx=10, pady=10)

        infoFrame = customtkinter.CTkFrame(self.mainFrame)
        ID = customtkinter.CTkLabel(infoFrame, text="ID: " + str(entry.get("ID", "Invalid ID")))
        ID.grid(row=0,column=0, sticky="w")
        title = customtkinter.CTkEntry(infoFrame, placeholder_text="Title: " + entry.get("title", "Invalid Title"))
        title.grid(row=1,column=0, sticky="w")
        title.insert("end", entry.get("title", "Invalid Title"))
        
        creator = customtkinter.CTkEntry(infoFrame, placeholder_text="Creator: " + entry.get("creator", "Invalid Creator"))
        creator.insert("end", entry.get("creator", "Invalid Creator"))
        creator.grid(row=2,column=0, sticky="w")
        infoFrame.pack(fill="both", expand=True, padx=10, pady=10)

        bottomButtonFrame = customtkinter.CTkFrame(self.mainFrame)
        bottomButtonFrame.pack(fill="both", expand=True, padx=10, pady=10)

    def tagListDisplay(self, tags):
        logging.info("Loading tag list...")
        App.clearFrame(self.tagListFrame)
        finalTags = ["(" + str(tags.count(tag)) + ") " + (str(tag)) for tag in tags]
        finalTags = [*set(finalTags)]
        finalTags.sort(reverse=True)
        tagButtonsList = {}
        for tag in finalTags:
            tagButtonsList[tag] = customtkinter.CTkFrame(self.tagListFrame)
            tagName = tag.split(" ")

            tagButton = customtkinter.CTkButton(tagButtonsList[tag], fg_color="transparent", text=tag, command=lambda e=tagName: self.autoSearch(e[len(e)-1]))
            addButton = customtkinter.CTkButton(tagButtonsList[tag], fg_color="transparent", text="+", width=30, height=30, command=lambda e=tagName: self.addTagToSearch(e[len(e)-1]))
            removebutton = customtkinter.CTkButton(tagButtonsList[tag], fg_color="transparent",text="-", width=30, height=30, command=lambda e=tagName: self.removeTagFromSearch(e[len(e)-1]))

            tagButton.pack(side="left")
            addButton.pack(side="left")
            removebutton.pack(side="left")
            tagButtonsList[tag].pack()

    def addTagToSearch(self, newTag):
        searchBar = self.searchBar.get()
        if newTag not in searchBar.split():
            if len(searchBar) > 0:
                searchBar = searchBar + " "
            searchBar = searchBar + newTag
        self.fillSearch(searchBar)

    def removeTagFromSearch(self, targetTag):
        searchBar = self.searchBar.get().replace(targetTag, "")
        self.fillSearch(searchBar)

    def saveSearch(self):
        searchBar = self.searchBar.get()
        self.Archive.savedSearches.append(searchBar)
        self.savedSearchesDropdowns.configure(values=self.Archive.savedSearches)

    def exit(self):
        self.Archive.saveAll()
        self.destroy()
        



fileStartTime = time.time()
if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", lambda: app.exit())
    app.mainloop()

