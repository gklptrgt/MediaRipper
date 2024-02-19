# stress testing if a https://aniwave.to/ has limitations 
# with requests library

import requests
import bs4
from fake_headers import Headers

def generate_header() -> str:
    result = {}    
    header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
    )
    
    result['User-Agent'] = header.generate()['User-Agent']
    return result
    print("A new User-Agent generated.")

# lookslike we dont need selenium
link = "https://aniwave.to/watch/one-piece.ov8/ep-1"

req = requests.get(link, headers=generate_header())


soup = bs4.BeautifulSoup(req.content, "lxml")

x = soup.select("#w-servers .active")
print(x)