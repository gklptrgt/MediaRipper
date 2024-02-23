# takes link from atlas and does full scrap on the pages
# then adds them to the db with hash_title and image_title

import tools
import csv_master
import bs4

rows = csv_master.read_from_atlas()

for row in rows:
    sub_link = row[1]
    attack_link = "https://ww4.gogoanime2.org" + sub_link
    
    req = tools.link_checker(attack_link)
    
    # scraping anime information
    soup = bs4.BeautifulSoup(req.content, "lxml")

    temp_title = soup.select("h1")
    # title
    title = temp_title[0].text.strip()
    # slug
    slug = sub_link[7:].strip()
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

    print("title:",title)
    print("slug :",slug)
    print("img  :",download_link)
    print("desc :",desc)
    print("episo:",episodes_list)

    # uploading data to the db and ftp

    # done for first anime
    break