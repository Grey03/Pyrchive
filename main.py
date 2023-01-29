import customtkinter, os
from pyrchive import archivemanager
from tkinter import filedialog, messagebox
from tktooltip import ToolTip

global __location__
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):         
    def __init__(self):
        super().__init__()
        self.title("Tarchive")
        self.geometry(f"{1135}x{925}")
        self.Archive = archivemanager()
        self.pageIndex = 0

        def TopFrame():
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
            self.fileCountLabel=customtkinter.CTkLabel(self.optionButtonsFrame,text=f"Total File Count: {9}")
            self.fileCountLabel.pack(side="left",padx=5,pady=5)
            self.optionButtonsFrame.pack(padx=10, pady=5, fill="x")
        TopFrame()
        def SearchFrame():
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
        SearchFrame()
        def BottomFrame():
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
        BottomFrame()


if __name__ == "__main__":
    app=App()
    app.mainloop()

