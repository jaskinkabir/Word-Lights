import os
from scripts.epic_utils import getSettings
from scripts.Palette_Generator import Gisa
from scripts.Tuya_Logic import DeviceManager, CloudBulb
from tkinter import *
from tkinter import ttk
from time import sleep, time

from random import randint, seed, uniform, choice




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
    gs.resetGisa()
    
    word = wordVar.get()
    addPalette = paletteOption.get()
    
    setColors(word, addPalette)
    

root = Tk(
    screenName="Word Lights"
)
root.title("Word Lights")

def weezer():
    for device in dm.devices.values():
        device.weezer()
        
def white():
    for device in dm.devices.values():
        device.setWhite()
        
        
        
randMode = False
def toggleRandom():
    global randMode
    randMode = not randMode
    randBtnTxt.set("Random Mode On" if randMode else "Random Mode Off")
    

    
    
def randomTime():
    while True:
        seed(time())
        sleep(randint(1, 4))
        sleep()
        
        for deviceNum in dm.devices.keys():
            device = dm.devices[deviceNum]
            device.setColor((randint(0,255), randint(0,255), randint(0,255)))
            
    
        
        
randBtnTxt = StringVar()
randBtnTxt.set("Random Mode Off")


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
ttk.Button(mainframe, text="Weezer", command=weezer).grid(column=3, row=5, sticky=W)
ttk.Button(mainframe, text="White", command=white).grid(column=3, row=4, sticky=W)
randButton = ttk.Button(mainframe, textvariable=randBtnTxt, command=toggleRandom).grid(column=3, row=6, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

wordEntry.focus()
root.bind("<Return>", colorCommand)


print("setup complete")
while True:
    if randMode:
        seed(time())
        interval = uniform(0.2, 2.8)
        print(f"Setting Random Colors after {interval} seconds")
        sleep(interval)
        
        for device in dm.devices.values():
            device.setColor((randint(0,255), randint(0,255), randint(0,255)))
            sleep(uniform(0.1, 0.33))
    root.update_idletasks()
    root.update()
            
        
        
    
    


