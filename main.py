import customtkinter, os, math, random, shutil, json
from Pyrchive import ArchiveManager
from tkinter import filedialog, messagebox
from tktooltip import ToolTip
#from PIL import Image

global __location__
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


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
        self.settingsButton=customtkinter.CTkButton(self.optionButtonsFrame, text="Settings")
        self.settingsButton.pack(side="left", padx=5,pady=5)
        self.uploadButton=customtkinter.CTkButton(self.optionButtonsFrame,text="Upload")
        self.uploadButton.pack(side="left", padx=5,pady=5)
        self.savedSearchesDropdown=customtkinter.CTkOptionMenu(self.optionButtonsFrame, values=["Saved Searches: "])
        self.savedSearchesDropdown.pack(side="left", padx=5,pady=5)
        self.showAllTagsButton=customtkinter.CTkButton(self.optionButtonsFrame,text="Show All Tags")
        self.showAllTagsButton.pack(side="left", padx=5,pady=5)
        self.randomButton=customtkinter.CTkButton(self.optionButtonsFrame, text= "Random")
        self.randomButton.pack(side="left",padx=5,pady=5)
        self.refreshButton=customtkinter.CTkButton(self.optionButtonsFrame, text=r"↻", width=10, height=10)
        self.refreshButton.pack(side="right",padx=5,pady=5)
        self.fileCountLabel=customtkinter.CTkLabel(self.optionButtonsFrame,text=f"Total File Count: {len(self.Archive.archiveList)}")
        self.fileCountLabel.pack(side="left",padx=5,pady=5)
        self.optionButtonsFrame.pack(padx=10, pady=5, fill="x")

        #Search Frame
        self.searchFrame = customtkinter.CTkFrame(self)
        self.saveButton = customtkinter.CTkButton(self.searchFrame, text="Save",width=50)
        self.saveButton.pack(side="left")
        self.searchBar= customtkinter.CTkEntry(self.searchFrame,placeholder_text="Search")
        self.searchBar.bind("<Return>")
        self.searchBar.pack(padx=5,side="left", fill="x",expand=True)
        self.searchButton = customtkinter.CTkButton(self.searchFrame, text="Search", width=80)
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
        self.entryFrame=customtkinter.CTkFrame(self.bottomFrame, fg_color="transparent")
        self.entryFrame.pack(side="left",fill="both", expand=True)
        self.bottomFrame.pack(fill="both",expand=True,padx=10,pady=5)

        #Put the page buttons on the browse frame
        #self.pageButtonFrame = customtkinter.CTkFrame(self, fg_color="transparent")
        #self.pageLeft = customtkinter.CTkButton(self.pageButtonFrame, text="Previous")
        #self.pageLeft.grid(row=0, column=0)
        #self.currentPageLabel = customtkinter.CTkLabel(self.pageButtonFrame, text=f"Page: {self.pageIndex+1}")
        #self.currentPageLabel.grid(row=0, column=1)
        #self.pageRight = customtkinter.CTkButton(self.pageButtonFrame, text="Next")
        #self.pageRight.grid(row=0, column=2)
        #self.pageButtonFrame.pack()
    def clearEntryFrame(self):
        for child in self.entryFrame.winfo_children():
            child.destroy()

    def setBrowseEntries(self, **kwargs):
        self.clearEntryFrame()
        entryList = self.Archive.archiveList
        for key, value in kwargs.items():
            if key == "entryList" : entryList = value

    def setViewEntry(self):
        self.clearEntryFrame()
        frame = customtkinter.CTkFrame(self.entryFrame, fg_color="red")
        frame.pack(expand=True, fill="both")



if __name__ == "__main__":
    app=App()
    app.mainloop()
