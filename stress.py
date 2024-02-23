# stress testing if a https://aniwave.to/ has limitations 
# with requests library

import requests
import bs4
from fake_headers import Headers

# lookslike we dont need selenium
link = "https://ww4.gogoanime2.org/anime/dead-mount-death-play-part-2"
# link2 = "https://kissanime.co/Anime/hack-G-U-Returner/OVA?id=44622"
# req = requests.get(link, headers=generate_header())

for x in range(1000):

    req = requests.get(link)
    print(req.status_code)
    soup = bs4.BeautifulSoup(req.content, "lxml")

    x = soup.select("h1")
    print(x)