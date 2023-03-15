import customtkinter
import os
import shutil
import logging
import time
import math
import random
import cv2

from Pyrchive import archivemanager
from tkinter import filedialog, messagebox
import tkinter as tk
from PIL import Image

logger = logging.getLogger(__name__)

global __location__
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
videoFiles = [".avi",".mp4",".mov",".wmv",".mov",".mpeg",".flv",".m4v", '.webm']

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

def getVideoThumbnail(video_path):
    defaultImagePath = (f"{str(__location__)}/pyrchiveFolders/Tagchivelogo.png")
    try:
        video_capture = cv2.VideoCapture(video_path)
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0) # change 50 to the desired frame number
        ret, frame = video_capture.read()
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    except Exception as inst:
        image = Image.open(defaultImagePath)
        logger.error(f"Failed to get video thumbnail: {str(inst)}")
    return image

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    Thanks to https://stackoverflow.com/a/36221216
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 250     #miliseconds
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
        self.title("Pyrchive")
        #self.geometry(f"{1135}x{925}")
        self.minsize(1280, 700)
        self.iconbitmap(__location__ + "/pyrchiveFolders/icon.ico")

        self.Archive = archivemanager()
        self.Archive.loadAll()

        self.pageIndex = 0
        self.currentEntryBrowseCount = 0
        self.filecount = len(self.Archive.entriesList)

        logger.info("Pyrchive App initialized")

        #Top Buttons Frame
        self.optionButtonsFrame=customtkinter.CTkFrame(self)
        #-+-+-+-+-+-
        self.settingsButton=customtkinter.CTkButton(self.optionButtonsFrame, text="Settings", command=lambda: self.settingsScreen())
        self.settingsButton.pack(side="left", padx=5,pady=5)
        self.uploadButton=customtkinter.CTkButton(self.optionButtonsFrame,text="Upload", command= lambda: self.uploadEntry())
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
        self.tagListFrame = customtkinter.CTkFrame(self.tagFrame,fg_color="transparent")
        self.tagListFrame.pack(padx=5,pady=5, expand=True, fill="both")
        self.tagFrame.pack(side="left", fill="y")
        self.mainFrame=customtkinter.CTkFrame(self.bottomFrame, fg_color="transparent")
        self.mainFrame.pack(side="left",fill="both", expand=True)
        self.bottomFrame.pack(fill="both",expand=True,padx=10,pady=5)

        logger.info(f"Started in {'%.2f' % (time.time() - fileStartTime)}s.")

        self.autoSearch("")

    def clearSearch(self):
        self.searchBar.delete("0","end")
        self.search()
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
        x = self.Archive.filterEntryList(searchList, 48)
        self.currentEntryBrowseCount = len(x)
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

    def entryBrowseScreen(self, entries):
        browseScreenStartTime = time.time()
        entries.reverse()
        maxWidth = 6
        maxHeight = 8
        #Dont forget to update max image in the page forward
        maxImages = maxWidth * maxHeight

        start = maxImages * (self.pageIndex)
        totalentries = len(entries)
        if len(entries) >= maxImages:
            entries = entries[start:start + maxImages]
        else:
            entries = entries[start:len(entries)+1]
        logger.info(f"Entering Browse Screen with {len(entries)} entries on screen.")
        App.clearFrame(self.mainFrame)
        browseScreen = customtkinter.CTkScrollableFrame(self.mainFrame)
        tupleWidth = tuple(range(maxWidth-2))
        tupleHeight = tuple(range(maxHeight-2))
        browseScreen.rowconfigure(tupleWidth, weight=1)
        browseScreen.columnconfigure(tupleHeight,weight=1)
        #browseScreen.grid(row=0, column=0, columnspan=3, sticky="nsew")
        browseScreen.pack(side="top", fill="both", expand="true", padx=5)
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
            if os.path.splitext(fileLocation)[-1] in videoFiles:
                image = getVideoThumbnail(fileLocation)
            else:
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
            buttons[ID] = customtkinter.CTkButton(browseScreen, width=image.size[0],height=image.size[1], image=images[ID], text="" ,fg_color="transparent", command = lambda e=ID: self.entryViewScreen(entries[e]))
            buttons[ID].tip = CreateToolTip(buttons[ID], f"{entry.get('title', 'Invalid Title')}: {', '.join(entry.get('tags', 'Invalid Tags'))}")
            buttons[ID].grid(row=math.floor(ID/maxWidth), column=ID%maxWidth, padx=5, pady=5)
            allTags.extend(entry.get("tags",""))
        self.tagListDisplay(allTags)

        pagesFrame = customtkinter.CTkFrame(self.mainFrame)
        backArrow = customtkinter.CTkButton(pagesFrame, width=30, height=30, text="⬅️", command = lambda : self.browseBack())
        backArrow.pack(side="left", padx=5, pady=5)

        currentPageEntry = customtkinter.CTkEntry(pagesFrame, placeholder_text=self.pageIndex + 1, width=30, height=30)
        currentPageEntry.bind("<Return>", lambda e: self.pageSelect(currentPageEntry.get()))
        currentPageEntry.pack(side="left", padx=5, pady=5)

        ofPageLabel = customtkinter.CTkLabel(pagesFrame, text=f"of {math.ceil(totalentries / maxImages)}")
        ofPageLabel.pack(side="left", padx=5, pady=5)

        forwardArrow = customtkinter.CTkButton(pagesFrame, width=30, height=30, text="➡️", command = lambda: self.browseForward())
        forwardArrow.pack(side="left", padx=5, pady=5)

        #pagesFrame.grid(row=1, column=1, sticky="ew")
        pagesFrame.pack(padx=5, pady=5)
        logger.debug(f"Finished in {'%.2f' % (time.time() - browseScreenStartTime)}s.")
     
    def browseBack(self):
        if self.pageIndex > 0:
            self.pageIndex -= 1
            self.search()
    def browseForward(self):
        #Dont forget to update this when updating max images above
        maxImagesPerPage = 48
        if self.pageIndex < math.ceil(self.currentEntryBrowseCount / maxImagesPerPage):
            self.pageIndex +=1
            self.search()
    def pageSelect(self, text, *args):
        logger.info("Going to page " + text)
        if(text.isdigit()):
            maxImagesPerPage = 48
            totalPages = math.ceil(self.currentEntryBrowseCount / maxImagesPerPage)
            if int(text) <= totalPages and int(text) > 0:
                self.pageIndex = int(text) - 1
                self.search()
            else:
                logger.warn("User did not enter a valid number")
        else:
            logger.warn("User did not enter a number")

    def safeOpen(self, filelocation):
        try:
            os.startfile(filelocation)
        except: 
            try:
                os.startfile(__location__ + "/" + filelocation)
            except:
                messagebox.showerror("File Not Found", f"File {filelocation} not found.")
                logger.warning(f"File {filelocation} not found.")

            
    def entryViewScreen(self, entry, **kwargs):
        newEntry = False
        if kwargs.get("newEntry", False) != False:
            #it just works..
            newEntry = True
            
        App.clearFrame(self.mainFrame)
        logger.info(f"Opening window for entry {entry.get('ID', 'Invalid ID')}")

        mediaWindow = customtkinter.CTkScrollableFrame(self.mainFrame)
        defaultImage = (f"{str(__location__)}/pyrchiveFolders/Tagchivelogo.png")
        fileLocation = entry.get("fileLocation", defaultImage)


        if not os.path.exists(fileLocation):
            fileLocation = defaultImage
        maxImageX = int(self.geometry().split("x")[0]) - 300
        if os.path.splitext(fileLocation)[-1] in videoFiles:
            image = getVideoThumbnail(fileLocation)
        else:
            try:
                image = Image.open(fileLocation)
            except Exception as inst:
                image = Image.open(defaultImage)
                logger.warning("Error openining image: " + str(inst))
        if self.Archive.enlargeImages or image.size[0] > maxImageX:
            resizeScale = ((image.size[0]/maxImageX))
            newSize = (math.floor(image.size[0]/resizeScale), math.floor(image.size[1]/resizeScale))
            image = image.resize(newSize)

        ogLocation = entry.get("fileLocation")

        ctkImage = customtkinter.CTkImage(dark_image=image, size=image.size)
        ctkImageButton = customtkinter.CTkButton(mediaWindow, image=ctkImage, text="", width=image.size[0], height=image.size[1], hover=False, fg_color="transparent", command=lambda : self.safeOpen(fileLocation))
        ctkImageButton.pack()
        #run function to either display a video or an image

        mediaWindow.pack(fill="both", expand=True, padx=5, pady=5)

        infoFrame = customtkinter.CTkFrame(self.mainFrame, height=300)

        IDLabel = customtkinter.CTkLabel(infoFrame, text=f"ID:")
        ID = customtkinter.CTkLabel(infoFrame, text=str(entry.get("ID", "Invalid ID")))
        IDLabel.grid(row=0,column=0, sticky="w")
        ID.grid(row=0, column=1, sticky="w")

        titleLabel = customtkinter.CTkLabel(infoFrame, text="Title:")
        title = customtkinter.CTkEntry(infoFrame, placeholder_text=entry.get("title", "Invalid Title"))
        titleLabel.grid(row=1,column=0, sticky="w")
        title.grid(row=1,column=1, sticky="ew", padx=5)
        title.insert("end", entry.get("title", "Invalid Title"))
        
        creatorLabel = customtkinter.CTkLabel(infoFrame, text="Creator:")
        creator = customtkinter.CTkEntry(infoFrame, placeholder_text=entry.get("creator", "Invalid Creator"))
        creator.insert("end", entry.get("creator", "Invalid Creator"))
        creatorLabel.grid(row=2,column=0, sticky="w")
        creator.grid(row=2,column=1, sticky="ew", padx=5)

        dateLabel = customtkinter.CTkLabel(infoFrame, text="Date:")
        date = customtkinter.CTkLabel(infoFrame, text=str(entry.get("uploadDate", "Invalid Date")))
        dateLabel.grid(row=3, column=0, sticky="w")
        date.grid(row=3, column=1, sticky="ew", padx=5)

        fileLocation = entry.get("fileLocation", "Invalid File Location")

        locationButton = customtkinter.CTkButton(infoFrame, text="File: ", command=lambda: newFile(fileLocation), width=35)
        locationButton.grid(row=4, column=0, sticky="w")
        locationText = customtkinter.CTkLabel(infoFrame, text=entry.get("fileLocation", "Invalid File Location)"))
        locationText.grid(row=4, column=1, sticky="ew", padx=5)


        tagsLabel = customtkinter.CTkLabel(infoFrame, text="Tags: ")
        tagsBox = customtkinter.CTkTextbox(infoFrame, height=100, wrap="word")
        tagsBox.insert("end", " ".join(entry.get("tags", "Invalid Tags")))
        tagsLabel.grid(row=5, column=0, sticky="w")
        tagsBox.grid(row=6, column=0, sticky="ew", columnspan=6, padx=1)

        descriptionLabel = customtkinter.CTkLabel(infoFrame, text="Description: ")
        descriptionBox = customtkinter.CTkTextbox(infoFrame, height=100, wrap="word")
        descriptionBox.insert("end", (entry.get("notes", "Invalid Description")))
        descriptionLabel.grid(row=0, column=2, sticky="w")
        descriptionBox.grid(row=1, column=2, sticky="ew", rowspan=5, columnspan=3, padx=1)

        

        infoFrame.pack(padx=5, pady=5, expand=False, fill="x")

        def moveToLocal():
            try:
                os.remove(__location__ + "/pyrchiveFolders/archivedFiles/" + str(os.path.basename(ogLocation)))
                logger.info(f"Removed {ogLocation}")
            except:
                pass
            try:
                messagebox.showinfo("Please Wait", "Copying file to localFiles...")
                shutil.copy(locationText.cget("text"), __location__ + "/pyrchiveFolders/archivedFiles/" )
                messagebox.showinfo("File Copied", f"File {locationText.cget('text')} copied to {__location__}/pyrchiveFolders/archivedFiles/")
                logger.info(f"File {locationText.cget('text')} copied to {__location__}/pyrchiveFolders/archivedFiles/")
            except Exception as inst:
                logger.error(f"Could not copy file {locationText.cget('text')} to {__location__ + '/pyrchiveFolders/archivedFiles/'}: {inst}")
                messagebox.showerror("Error", f"Could not copy file {locationText.cget('text')} to {__location__ + '/pyrchiveFolders/archivedFiles/'}: {inst}")
                return None
            
        def save():
            saveToLocal = self.Archive.copyToLocal
            temp = locationText.cget("text")
            if saveToLocal and locationText.cget("text").find(__location__.replace("\\","/")) == -1:
                moveToLocal()
                location = __location__.replace("\\", "/") + "/pyrchiveFolders/archivedFiles/" +str(os.path.basename(locationText.cget("text")))
            else:
                location = locationText.cget("text")

            logger.info("Saving entry " + location)

            saveData = {
                "ID": entry["ID"],
                "title": title.get(),
                "creator": creator.get(),
                "tags": tagsBox.get("0.0", "end").replace("\n","").split(" "),
                "fileLocation": location,
                "notes": descriptionBox.get("0.0", "end").rsplit("\n",1)[0],
                "uploadDate": entry.get("uploadDate", "Invalid Date")
            }
            if newEntry == self.Archive.removeOriginalFile == self.Archive.copyToLocal:
                try:
                    os.remove(temp)
                except Exception as inst:
                    logger.error(f"Could not remove file {temp}: {inst}")
            try:
                self.Archive.addEntry(saveData)
            except:
                logger.warning(f"Entry {entry.get('ID', 'Invalid ID')} not found in archive appending to archive")
                self.Archive.entriesList.append(saveData)

            self.Archive.saveEntries()
            self.search()

        def newFile(*args):
            try:
                x = filedialog.askopenfilename(initialfile=args[0],title="Select File")
            except:
                x = filedialog.askopenfilename(title="Select File")
            if os.path.exists(x):
                fileLocation = x
                locationText.configure(text=fileLocation)

        def deleteEntry(entry):
            if messagebox.askyesno("Delete Entry", "Are you sure you want to delete this entry?"):
                fixedLocation = (__location__.replace("\\", "/"))
                if entry["fileLocation"].find(fixedLocation) != -1:
                    try:
                        os.remove(entry["fileLocation"])
                    except Exception as inst:
                        logger.warning(f"Could not remove file {entry['fileLocation']}: {inst}")
                self.Archive.deleteEntry(entry.get("ID"))
                self.Archive.saveEntries()
                self.search()

        buttonFrame = customtkinter.CTkFrame(infoFrame)

        saveButton = customtkinter.CTkButton(buttonFrame, text="Save", command = lambda: save())
        #saveButton.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        saveButton.pack(side="left", expand=True, fill="x", padx=5)

        backButton = customtkinter.CTkButton(buttonFrame, text="Back", command = lambda: self.search())
        #backButton.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        backButton.pack(side="left", expand=True, fill="x", padx=5)

        deleteButton = customtkinter.CTkButton(buttonFrame, text="Delete", fg_color="red", hover_color="darkred",command = lambda : deleteEntry(entry))
        deleteButton.pack(side="left", expand=True, fill="x", padx=5)
        
        buttonFrame.grid(row=7, column=1, padx=5, pady=5, sticky="ew")

        self.tagListDisplay(entry.get("tags", ["NO", "TAGS", "FOUND"]))

    def uploadEntry(self, *args):
        try:
            file = filedialog.askopenfilename(initialfile=args[0],title="Select File")
        except:
            file = filedialog.askopenfilename(title="Select File")
        if os.path.exists(file):
            self.newEntryScreen(file)

    def newEntryScreen(self, entryFileLocation):
        newEntry = self.Archive.createEntry()
        newEntry["fileLocation"] = entryFileLocation
        self.entryViewScreen(newEntry, newEntry=True)

    def settingsScreen(self):
        App.clearFrame(self.mainFrame)
        logger.info(f"Opening window for settings")

        buttonsFrame = customtkinter.CTkFrame(self.mainFrame)

        generalSettingsButton = customtkinter.CTkButton(buttonsFrame, text="General Settings", font=("Calibri", 30, "bold"), command= lambda: self.generalSettingsScreen())
        generalSettingsButton.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

        savedSearchesEditor = customtkinter.CTkButton(buttonsFrame, text="Saved Search Settings", font=("Calibri", 30, "bold"), command= lambda: self.savedSearchesEditorScreen())
        savedSearchesEditor.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

        buttonsFrame.pack(padx=5, pady=5, expand=True)

        backButton = customtkinter.CTkButton(self.mainFrame, text="Back", command= lambda: self.search())
        backButton.pack(pady=5, padx=5)

    def generalSettingsScreen(self):
        App.clearFrame(self.mainFrame)

        settingsFrame = customtkinter.CTkFrame(self.mainFrame)

        #---------Start of Settings-------
        copyToLocalSwitch = customtkinter.CTkSwitch(settingsFrame, text="Copy to files to local folder")
        copyToLocalSwitch.tip = CreateToolTip(copyToLocalSwitch, text="Copies files from their location on your computer to the local folder. This is so if the file is moved, it will not disrupt the archiver.")
        if (self.Archive.copyToLocal):
            copyToLocalSwitch.select()
        else:
            copyToLocalSwitch.deselect()
        copyToLocalSwitch.grid(row=0, column=0, padx=5, pady=5, sticky="nswe")

        removeOriginalFileSwitch = customtkinter.CTkSwitch(settingsFrame, text="Remove original file once uploaded to archive")
        removeOriginalFileSwitch.tip = CreateToolTip(removeOriginalFileSwitch, text="Removes the original file from its location on your computer. This is so if the file is moved instead of copied. This only happens when uploading.")
        if (self.Archive.removeOriginalFile):
            removeOriginalFileSwitch.select()
        else:
            removeOriginalFileSwitch.deselect()
        removeOriginalFileSwitch.grid(row=0, column=1, padx=5, pady=5, sticky="nswe")

        scaleImagesSwitch = customtkinter.CTkSwitch(settingsFrame, text="Scale Images")
        scaleImagesSwitch.tip = CreateToolTip(scaleImagesSwitch, text="When viewing an entry, the images will be upscaled to fit in the window.")
        if (self.Archive.enlargeImages):
            scaleImagesSwitch.select()
        else:
            scaleImagesSwitch.deselect()
        scaleImagesSwitch.grid(row=0, column=2, padx=5, pady=5, sticky="nswe")

        localFolderButton = customtkinter.CTkButton(settingsFrame, text="Local Folder", command= lambda: os.startfile(__location__ + "/pyrchiveFolders/archivedFiles/"))
        localFolderButton.grid(row=1, column=0, padx=5, pady=5, sticky="nswe")

        def saveSettings():
            self.Archive.copyToLocal = bool(copyToLocalSwitch.get())
            self.Archive.removeOriginalFile = bool(removeOriginalFileSwitch.get())
            self.Archive.enlargeImages = bool(scaleImagesSwitch.get())
            self.Archive.saveSettings()

        #---------End of Settings-------

        settingsFrame.pack(padx=5, pady=5, expand=True, fill="both")

        saveButton = customtkinter.CTkButton(self.mainFrame, text="Save", command = lambda: saveSettings())
        saveButton.pack(padx=5, pady=5)

        backButton = customtkinter.CTkButton(self.mainFrame, text="Back", command = lambda: self.settingsScreen())
        backButton.pack(padx=5, pady=5)

    def deleteSavedSearch(self, ID, buttonFRAME):
        if messagebox.askyesno("Delete Saved Search", f"Are you sure you want to delete {ID}?"):
            try:
                self.Archive.savedSearches.remove(ID)
                self.savedSearchesDropdown.configure(values=self.Archive.savedSearches)
                buttonFRAME.destroy()
            except Exception as inst:
                messagebox.showerror("Error", f"Could not delete saved search {ID}: {inst}")

    def savedSearchesEditorScreen(self):
        App.clearFrame(self.mainFrame)

        allSearches = customtkinter.CTkScrollableFrame(self.mainFrame)

        if len(self.Archive.savedSearches) == 0:
            DefaultText = customtkinter.CTkLabel(allSearches, text="No Saved Searches", font=("Calibri", 20, "bold")) 
            DefaultText.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        pairings = {}
        for id, savedSearch in enumerate(self.Archive.savedSearches):
            pairings[id] = customtkinter.CTkFrame(allSearches)
            label = customtkinter.CTkLabel(pairings[id], text=savedSearch)
            label.grid(row=id, column=1, sticky="w")
            button = customtkinter.CTkButton(pairings[id], width=30, text="x", fg_color="red", hover_color="darkred", font=("Calibri", 20, "bold"), command=lambda e=savedSearch, id=id: self.deleteSavedSearch(e, pairings[id]))
            button.grid(row=id, column=0, padx=10, pady=10, sticky="w")
            pairings[id].pack(padx=5, pady=5, side="top", fill="x")

        allSearches.pack(padx=5, pady=5, expand=True, fill="both")

        backButton = customtkinter.CTkButton(self.mainFrame, text="Back", command=lambda: self.settingsScreen())
        backButton.pack(padx=5, pady=5)


    def tagListDisplay(self, tags):
        logging.info("Loading tag list...")
        App.clearFrame(self.tagListFrame)
        finalTags = ["(" + str(self.Archive.getAllTagsData()[tag]) + ") " + (str(tag)) for tag in tags]
        finalTags = [*set(finalTags)]
        finalTags.sort(reverse=True)
        tagButtonsList = {}
        for tag in finalTags:
            tagButtonsList[tag] = customtkinter.CTkFrame(self.tagListFrame)
            tagName = tag.split(" ")

            tagButton = customtkinter.CTkButton(tagButtonsList[tag], text=tag, command=lambda e=tagName: self.autoSearch(e[len(e)-1]))
            tagButton.tip = CreateToolTip(tagButton, text=tag.split(" ")[1])
            addButton = customtkinter.CTkButton(tagButtonsList[tag], text="+", width=30, height=30, command=lambda e=tagName: self.addTagToSearch(e[len(e)-1]))
            addButton.tip = CreateToolTip(addButton, text="Add tag to search")
    
            removebutton = customtkinter.CTkButton(tagButtonsList[tag], text="-", width=30, height=30, command=lambda e=tagName: self.removeTagFromSearch(e[len(e)-1]))
            removebutton.tip = CreateToolTip(removebutton, text="Remove tag from search")

            tagButton.pack(side="left", padx=1, pady=1)
            addButton.pack(side="left", padx=1, pady=1)
            removebutton.pack(side="left", padx=1, pady=1)
            tagButtonsList[tag].pack()

    def addTagToSearch(self, newTag):
        searchBar = self.searchBar.get()
        if searchBar.endswith(""):
            searchBar = searchBar + " "
        searchBar = searchBar + newTag
        self.fillSearch(searchBar)

    def removeTagFromSearch(self, targetTag):
        searchBar = self.searchBar.get()
        if searchBar.endswith(""):
            searchBar = searchBar + " "
        searchBar = searchBar + ("-"+targetTag)

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

