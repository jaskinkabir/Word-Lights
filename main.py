import os
from scripts.epic_utils import getSettings
from scripts.Palette_Generator import Gisa
from scripts.Tuya_Logic import DeviceManager, CloudBulb
from tkinter import *
from tkinter import ttk





dm = DeviceManager()
gs = Gisa()

def setColors(word: str, addPalette:bool = False):
    for file in os.listdir('./temp/'):
        os.remove('./temp/'+file)
    
        print("cleared temp")
        

    
    colors = gs.getWordPalette(word, addPalette)
    
    orderedLights = getSettings()['Tuya']['orderedLights']
    
    for i, light in enumerate(orderedLights):
        bulb: CloudBulb = dm.getDevice(light)
        
        bulb.setColor(colors[i])


def colorCommand(*args):
    word = wordVar.get()
    addPalette = paletteOption.get()
    
    setColors(word, addPalette)
    

root = Tk(
    screenName="Word Lights"
)
root.title = "Word Lights"

def weezer():
    for device in dm.devices.values():
        device.weezer()



mainframe = ttk.Frame(root, padding="5 5 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

wordVar = StringVar()
wordEntry = ttk.Entry(mainframe, width=7, textvariable=wordVar)
wordEntry.grid(column=2, row=1, sticky=(W, E))

paletteOption = BooleanVar()
paletteCheckBox = ttk.Checkbutton(mainframe, text="Add ' color palette' to end of query", variable=paletteOption)
paletteCheckBox.grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Generate and set colors", command=colorCommand).grid(column=3, row=3, sticky=W)
ttk.Button(mainframe, text="Reset GISA", command=lambda: gs.resetGisa()).grid(column=3, row=4, sticky=W)
ttk.Button(mainframe, text="Weezer", command=weezer).grid(column=3, row=5, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

wordEntry.focus()
root.bind("<Return>", colorCommand)


print("setup complete")
root.mainloop()


