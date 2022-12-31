import asyncio
import random
from base64 import b64decode
from io import BytesIO

import requests


class StableDiffusionHandler:
    def __init__(self):
        self.ready = False
        self.sdProcess = asyncio.run(self.launchSD())

    async def launchSD(self):
        # Run the stable diffusion script in WSL
        process = await asyncio.create_subprocess_exec(
            'wsl', 'sh', '/home/jaskin/playground/python/stable-diffusion/startTxtImg.sh',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Wait for the process to complete
        stdout, stderr = await process.communicate()

        # Check the return code to see if the process completed successfully
        if process.returncode == 0:
            # The process completed successfully
            # Check if the message "Ready to generate images" was printed
            if "Ready to generate images" in stdout.decode():
                # Stable diffusion is ready to generate images
                self.ready = True
                return process
            else:
                # Stable diffusion is not ready to generate images
                return None
        else:
            # There was an error
            print(stderr)
            return None
        
    async def generateImage(self, text) -> dict:
        """
        Args:
            text (string): text to generate image from

        Returns:
            dict: 
                'imgFile' is a BytesIO object containing the image, 
                'duration' is the time it took to generate the image
        """
        response = requests.post("http://localhost:7860/run/predict", 
            json = {
                "data": [
                    text, # Text to generate image from
                    72, #ddim steps
                    1, #n iter
                    1, # batch size
                    256, #height
                    256, #width
                    7.5, #scale
                    0, #ddim eta
                    2, #unet bs
                    'cuda', #
                    str(random.randint(0, 1000000000)), #seed
                    "outputs/txt2img-samples", #output dir
                    'png', #output format
                    True, #turbo
                    False, #full precision
                    'plms', #sampler
                    
                ]
            }
        ).json()
        
        imgStr = response["data"][0]
        duration = response["duration"]
        
        decodedImg = b64decode(imgStr)
        
        imgFile = BytesIO(decodedImg)
        
        return {
            'imgFile': imgFile,
            'duration': duration
        }


