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
    desc_title = '<span class="desc-title">'
    desc_item = '<span class="desc-item">'
    desc_obj_end ='</span>'
    genre_list = None
    release_date = None
    status = None # add Ongoing links to the active_anime_list.csv
    temp_desc = soup.select(".type")
    for x in temp_desc:
        text = x.text
        if "Type" in text:
            t_demo = text.split(":")
            manip = desc_title + t_demo[0].strip() + desc_obj_end + ":" +desc_item +t_demo[1].strip() +desc_obj_end + "<br>"
            desc += manip
        if "Genre" in text:
            text = text.replace("\n","")
            text = text.replace(" ","")
            text = text.replace(","," | ")
            g_demo = text.split(":")
            genre_list = g_demo[1].split(" | ")
            manip = desc_title + g_demo[0].strip() + desc_obj_end + ":" + desc_item + g_demo[1].strip() +desc_obj_end + "<br>"
            desc += manip
        if "Released" in text:
            r_demo = text.split(":")
            manip = desc_title + r_demo[0].strip() + desc_obj_end + ":" + desc_item + r_demo[1].strip() + desc_obj_end+ "<br>"
            release_date = r_demo[1].strip()
            desc += manip
        if "Status" in text:
            s_demo = text.split(":")
            manip = desc_title + s_demo[0].strip() + desc_obj_end + ":" + desc_item + s_demo[1].strip() + desc_obj_end+ "<br>"
            status = s_demo[1].strip()
            desc += manip

    # image download link
    temp_img = soup.select(".anime_info_body_bg img")
    for img in temp_img:
        download_link = "https://ww4.gogoanime2.org" + img['src']


    print("title:",title)
    print("slug :",slug)
    print("img  :",download_link)
    print("desc :",desc)



    # scraping anime episodes links


    # going trough anime episode links and scraping the video src

    # uploading data to the db and ftp

    # done for first anime
    break