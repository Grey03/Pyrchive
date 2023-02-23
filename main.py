import customtkinter
import os
import shutil
import logging
import time
import math
import random

from Pyrchive import archivemanager
from tkinter import filedialog, messagebox
import tkinter as tk
from PIL import Image

logger = logging.getLogger(__name__)

global __location__
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    Thanks to https://stackoverflow.com/a/36221216
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        #x += self.widget.winfo_rootx() + 25
        #y += self.widget.winfo_rooty() + 20
        #Changed it to display near the mouse cursor instead of a set position
        x += self.widget.winfo_pointerx() + 12
        y += self.widget.winfo_pointery()
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

class App(customtkinter.CTk):         
    def __init__(self):
        super().__init__()
        self.title("Tarchive")
        #self.geometry(f"{1135}x{925}")
        self.minsize(1280, 700)

        self.Archive = archivemanager()
        self.Archive.loadAll()

        self.pageIndex = 1
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
            logger.debug(searchList)
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
            try:
                child.destroy()
            except Exception as inst:
                message = ("Error deleting child: %s" % inst)
                messagebox.ERROR(message)
                logger.error(message)

    def entryBrowseScreen(self, entries, **kwargs):
        start = 0
        for key,value in kwargs.items():
            if key == "start": start = value
        maxWidth = 6
        maxHeight = 8
        maxImages = maxWidth * maxHeight
        totalentries = len(entries)
        if len(entries) >= maxImages:
            entries = entries[start:maxImages]
        else:
            entries = entries[start:len(entries)-1]
        logger.info(f"Entering Browse Screen with {len(entries)} entries on screen.")
        App.clearFrame(self.mainFrame)
        browseScreen = customtkinter.CTkScrollableFrame(self.mainFrame)
        tupleWidth = tuple(range(maxWidth-2))
        tupleHeight = tuple(range(maxHeight-2))
        browseScreen.rowconfigure(tupleWidth, weight=1)
        browseScreen.columnconfigure(tupleHeight,weight=1)
        #browseScreen.grid(row=0, column=0, columnspan=3, sticky="nsew")
        browseScreen.pack(side="top", fill="both", expand="true")
        buttons = {}
        images = {}
        allTags = []
        defaultImage = (f"{str(__location__)}/pyrchiveFolders/Tagchivelogo.png")
        for ID, entry in enumerate(entries):
            #buttons[ID] = customtkinter.CTkButton(browseScreen, width=150,height=150, text=entry.get("ID", "Invalid ID"), command = lambda e=ID: self.entryViewScreen(entries[e]))
            fileLocation = entry.get("fileLocation", defaultImage)
            if not os.path.exists(fileLocation):
                fileLocation = defaultImage
            maxImageX = 150
            maxImageY = 150
            try:
                image = Image.open(fileLocation)
            except Exception as inst:
                image = Image.open(defaultImage)
                logger.warning("Error openining image: " + str(inst))


            largestSide = max(image.size)
            if largestSide == image.size[0] and largestSide > maxImageX:
                resizeScale = (math.floor(largestSide/maxImageX))
            elif largestSide == image.size[1] and largestSide > maxImageY:
                resizeScale = (math.floor(largestSide/maxImageY))
            newSize = (math.floor(image.size[0]/resizeScale), math.floor(image.size[1]/resizeScale))
            image = image.resize(newSize)

            images[ID] = customtkinter.CTkImage(dark_image=image, size=image.size)
            buttons[ID] = customtkinter.CTkButton(browseScreen, width=image.size[0],height=image.size[1], image=images[ID], text="" ,fg_color="transparent", command = lambda e=ID: self.entryViewScreen(entries[e], buttons[ID]))
            buttons[ID].tip = CreateToolTip(buttons[ID], f"{entry.get('ID', 'Invalid ID')}: {entry.get('title', 'Invalid Title')}")
            buttons[ID].grid(row=math.floor(ID/maxWidth), column=ID%maxWidth, padx=5, pady=5, sticky="nsew")
            allTags.extend(entry.get("tags",""))
        self.tagListDisplay(allTags)

        pagesFrame = customtkinter.CTkFrame(self.mainFrame)
        backArrow = customtkinter.CTkButton(pagesFrame, width=30, height=30, text="⬅️")
        backArrow.pack(side="left", padx=5, pady=5)

        currentPageEntry = customtkinter.CTkEntry(pagesFrame, placeholder_text=self.pageIndex, width=30, height=30)
        currentPageEntry.bind("<Return>", lambda e: self.pageSelect(e))
        currentPageEntry.pack(side="left", padx=5, pady=5)

        ofPageLabel = customtkinter.CTkLabel(pagesFrame, text=f"of {math.ceil(totalentries / maxImages)}")
        ofPageLabel.pack(side="left", padx=5, pady=5)

        forwardArrow = customtkinter.CTkButton(pagesFrame, width=30, height=30, text="➡️")
        forwardArrow.pack(side="left", padx=5, pady=5)

        #pagesFrame.grid(row=1, column=1, sticky="ew")
        pagesFrame.pack(padx=5, pady=5)

        
    def browseBack():
        print ("Back")
    def browseForward():
        print ("Forward")
    def pageSelect(*args):
        print ("Going to page")
        print (args)
            
    def entryViewScreen(self, entry, button):
        App.clearFrame(self.mainFrame)
        logger.info(f"Opening window for entry {entry.get('ID', 'Invalid ID')}")

        mediaWindow = customtkinter.CTkScrollableFrame(self.mainFrame)
        defaultImage = (f"{str(__location__)}/pyrchiveFolders/Tagchivelogo.png")
        fileLocation = entry.get("fileLocation", defaultImage)

        if not os.path.exists(fileLocation):
            fileLocation = defaultImage
        maxImageX = self.winfo_screenwidth() - 200
        maxImageY = 9999
        try:
            image = Image.open(fileLocation)
        except Exception as inst:
            image = Image.open(defaultImage)
            logger.warning("Error openining image: " + str(inst))

        largestSide = max(image.size)
        resizeScale = 1
        if largestSide == image.size[0] and largestSide > maxImageX:
            resizeScale = (math.floor(largestSide/maxImageX))
        elif largestSide == image.size[1] and largestSide > maxImageY:
            resizeScale = (math.floor(largestSide/maxImageY))
        newSize = (math.floor(image.size[0]/resizeScale), math.floor(image.size[1]/resizeScale))
        image = image.resize(newSize)

        ctkImage = customtkinter.CTkImage(dark_image=image, size=image.size)
        ctkImageButton = customtkinter.CTkButton(mediaWindow, image=ctkImage, text="", width=image.size[0], height=image.size[1], hover=False, fg_color="transparent", command=lambda : os.startfile(fileLocation))
        ctkImageButton.pack()
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
        self.savedSearchesDropdown.configure(values=self.Archive.savedSearches)

    def exit(self):
        #print (self.winfo_geometry())
        self.Archive.saveAll()
        self.destroy()
        



fileStartTime = time.time()
if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", lambda: app.exit())
    app.mainloop()

