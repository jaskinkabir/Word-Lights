from colorthief import ColorThief
from google_images_search import GoogleImagesSearch
from random import choice
from os import remove
import turtle
from scripts.epic_utils import getSettings

class ImgTest:
    def __init__(self, name):
        self.name = name
    
    def download(self):
        print(f"Downloaded {self.name}")

class Gist:
    def __init__(self, api_key, search_id):
        pass
    def search(self, search_params):
        self.results = [
            ImgTest(search_params['q'])
        ]




class Gisa:
    def __init__(self):
        
        try:
            self.settings = getSettings()['Google']
        except FileNotFoundError:
            print("Settings.yaml not found")
        self.gis = GoogleImagesSearch(self.settings["api_key"], self.settings["search_id"])
        
    def getWordPalette(self, word: str, addPalette: bool = False, algStrength = 2):
        print('Searching for ' + word)
        img = self.getImg(word, addPalette)
        

        print('Downloading image')
        img.download('./temp/')
        
        print('Generating palette...')
        return ColorThief(img.path).get_palette(
            color_count = len(getSettings()["Tuya"]['orderedLights']),
            quality = algStrength
        )
        
    
    def getImg(self, query: str, addPalette: bool = False):
        numRes = 4
        
        q = query + [' color palette' if addPalette else '' for x in range(1)][0]
        
        params = {
            'q' : q,
            'num': numRes,
            'imgColorType': 'color'
        }
        
        self.gis.search(search_params=params)
        
        return choice(self.gis.results())
    
    def resetGisa(self):
        self.gis = GoogleImagesSearch(self.settings["api_key"], self.settings["search_id"])
        print("Reset gisa")
        