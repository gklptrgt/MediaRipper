# takes link from atlas and does full scrap on the pages
# then adds them to the db with hash_title and image_title

import tools
import csv_master
import bs4
import requests
import os
from hashlib import blake2b
from db_connection import Comm

def hash_text(stringx: str) -> str:
    key = b"GtScript2023"  # replace with a longer or random key if possible
    h = blake2b(key=key, digest_size=6)
    h.update(stringx.encode("utf-8"))
    return h.hexdigest()

images_folder = None

def check_image_directory() -> dict:
    global images_folder
    print("Directory Check")
    directory_folder = "images"
    if os.path.isdir(directory_folder):
        print("Directory '{}' exists".format(directory_folder))
        images_folder = os.path.abspath(directory_folder)
    else:
        os.mkdir(directory_folder)
        print("Directory '{}' does not exist".format(directory_folder))
        print(f"Directory made: {os.path.isdir(directory_folder)}")
        check_image_directory()

db = Comm()

check_image_directory()

rows = csv_master.read_from_atlas()
cats = csv_master.read_cats()
for row in rows:
    sub_link = row[1]
    attack_link = "https://ww4.gogoanime2.org" + sub_link
    slug = sub_link[7:].strip()
    hashed = hash_text(slug)

    db.connect()
    if db.check_exists(slug):
        print(f"{slug} - Already Exists")
        continue
    db.disconnect()
    req = tools.link_checker(attack_link)

    # scraping anime information
    soup = bs4.BeautifulSoup(req.content, "lxml")
    temp_title = soup.select("h1")
    # title
    title = temp_title[0].text.strip()
    # slug

    # desc
    # Desc has Type | Genre | Status | Released
    desc = ""
    genre_list = None
    release_date = None
    status = None # add Ongoing links to the active_anime_list.csv
    temp_desc = soup.select(".type")
    for x in temp_desc:
        text = x.text
        if "Type" in text:
            t_demo = text.split(":")
            manip =  t_demo[0].strip()+ ": " + t_demo[1].strip() + " |"
            desc += manip
        if "Genre" in text:
            text = text.replace("\n","")
            text = text.replace(" ","")
            text = text.replace(","," | ")
            g_demo = text.split(":")
            genre_list = g_demo[1].split(" | ")
        if "Released" in text:
            r_demo = text.split(":")
            manip = r_demo[0].strip() + ": " + r_demo[1].strip() + " |"
            release_date = r_demo[1].strip()
            desc += manip
        if "Status" in text:
            s_demo = text.split(":")
            manip = s_demo[0].strip() + ": " + s_demo[1].strip() + " |"
            status = s_demo[1].strip()
            desc += manip

    # image download link
    temp_img = soup.select(".anime_info_body_bg img")
    for img in temp_img:
        download_link = "https://ww4.gogoanime2.org" + img['src']

    img_data = requests.get(download_link).content
    with open(f'{images_folder}/{slug}.jpg', 'wb') as handler:
        handler.write(img_data)
        print("Image downloaded.")

    img_name = f"{slug}.jpg"
    # episode links
    episodes = []
    temp_eps = soup.select("#episode_related a")
    for ep in temp_eps:
        episode_link = "https://ww4.gogoanime2.org" + ep['href']
        episodes.append(episode_link)
    
    episodes_list = []
    for ep in episodes:
        episodes_urls = {}
        req = tools.link_checker(ep)
        episode_no = ep.split("/")[-1]
        print("1",episode_no)
        soup = bs4.BeautifulSoup(req.content, "lxml")

        video_tmp = soup.select("#playerframe")
        for x in video_tmp:
            video_link = x['src']

        episodes_urls["ep_no"] = episode_no
        episodes_urls["url"] = video_link

        episodes_list.append(episodes_urls)
    cats_list_db = []
    while True:
        try:
            check = genre_list.pop()
            for cat in cats:
                if check in cat:
                    cats_list_db.append(cat[0])
        except:
            break
    
    cats_db = ""
    for item in cats_list_db:
        if item == cats_list_db[-1]:
            cats_db += item
        else:
            cats_db += item + ","

    print("title:",title)
    print("slug :",slug)
    print("Genre:",cats_db)
    print("img  :",img_name)
    print("desc :",desc)
    print("episo:",episodes_list)
    db.connect()
    db.add_data(hashed,cats_db,title,slug,desc,img_name,episodes_list,release_date)
    db.disconnect()

    if status == "Ongoing":
        csv_master.add_to_ongoing(attack_link)
        
    break

# print(cats)