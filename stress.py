# stress testing if a https://aniwave.to/ has limitations 
# with requests library

import requests

# lookslike we dont need selenium
req = requests.get("https://aniwave.to/home")

# https://aniwave.to/watch/one-piece.ov8/ep-1

