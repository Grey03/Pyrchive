#from archivebase import DataBaseEntry
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()



        self.title("Tarchive")
        self.geometry(f"{900}x{500}")
        #self.attributes("-fullscreen", True)

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
        self.optionButtonsFrame.pack(padx=10, pady=5, fill="x")

        #Search Frame
        self.searchFrame = customtkinter.CTkFrame(self)
        self.favoriteButton = customtkinter.CTkButton(self.searchFrame, text="Save",width=50)
        self.favoriteButton.pack(side="left")
        self.searchBar= customtkinter.CTkEntry(self.searchFrame,placeholder_text="Search")
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
        self.imageFrame=customtkinter.CTkFrame(self.bottomFrame, fg_color="transparent")
        self.imageFrame.pack(side="left",fill="both", expand=True)
        self.bottomFrame.pack(fill="both",expand=True,padx=10,pady=5)

    def refreshTags(self, tagsToShow):
        self.tagList.destroy()
        #when ready, make it get tag.name for the tag and the tag.group.color for the color
        for tag in tagsToShow:
            tagname = tag
            tagcolor = "darkgrey"
            customtkinter.CTkButton(master=self.tagFrame, text=tagname, font=("Roboto", 13, "underline"), text_color=tagcolor ,fg_color="transparent", height=0,corner_radius=0).pack(fill="x")

app = App()
tags=["tag1","tag2","tag3","tag4","tag5","tag6","tag7"]
app.refreshTags(tags)
app.mainloop()

