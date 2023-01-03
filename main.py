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
        self.closeAppFrame=customtkinter.CTkFrame(self.optionButtonsFrame)
        self.closeAppButton=customtkinter.CTkButton(self.closeAppFrame, text="X",width=30, command=self.closeApp,fg_color="red" ,hover_color="darkred")
        self.closeAppButton.pack()
        self.closeAppFrame.pack(side="right",padx=5,pady=5)
        #-+-+-+-+-+-
        self.mainbuttonsFrame=customtkinter.CTkFrame(self.optionButtonsFrame)
        self.settingsButton=customtkinter.CTkButton(self.mainbuttonsFrame, text="Settings")
        self.settingsButton.pack(side="left", padx=5,pady=5)
        self.uploadButton=customtkinter.CTkButton(self.mainbuttonsFrame,text="Upload")
        self.uploadButton.pack(side="left", padx=5,pady=5)
        self.savedsearchesButton=customtkinter.CTkButton(self.mainbuttonsFrame, text="Saved Searches")
        self.savedsearchesButton.pack(side="left", padx=5,pady=5)
        self.randomButton=customtkinter.CTkButton(self.mainbuttonsFrame, text= "Random")
        self.randomButton.pack(side="left",padx=5,pady=5)
        self.mainbuttonsFrame.pack(side="left")
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
        self.tagFrame=customtkinter.CTkFrame(self.bottomFrame)
        self.tagLabel=customtkinter.CTkLabel(self.tagFrame, text="Tags", width=200)
        self.tagLabel.pack(padx=5,pady=10)
        self.tagFrame.pack(side="left", fill="y")
        self.imageFrame=customtkinter.CTkFrame(self.bottomFrame, fg_color="transparent")
        self.imageFrame.pack(side="left",fill="both", expand=True)
        self.bottomFrame.pack(fill="both",expand=True,padx=10,pady=5)
        
    def closeApp(self):
        self.destroy()

app = App()
app.mainloop()