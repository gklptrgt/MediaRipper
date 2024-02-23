import csv_master
import tools
import bs4
import time

# Scraps gogoanime -> Anime List
# consider updating if 

for i in range(1,200):
    print(f"Current Page: {i}")
    link = f"https://ww4.gogoanime2.org/animelist/all/{i}"
    req = tools.link_checker(link)
    soup = bs4.BeautifulSoup(req.content, "lxml")

    x = soup.select(".listing a")
    for item in x:
        csv_master.add_to_atlas(item['title'], item['href'])
    
    time.sleep(0.5)

