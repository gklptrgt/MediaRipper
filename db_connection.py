import mysql.connector
from mysql.connector import Error
import ftplib
import os

class Comm:
    def __init__(self) -> None:
        self.switch = False
    def disconnect(self):
        if self.switch == True:
            try:
                if self.connection.is_connected():
                    self.cursor.close()
                    self.connection.close()
                    # print("MySQL connection is closed")
                    self.switch = False
            except:
                pass
        else:
            print("Connection is already closed!")
        
    def connect(self):
        if self.switch == False:
            try:
                self.connection = mysql.connector.connect(host='localhost', database='test2', user='root', password='')
                # self.connection = mysql.connector.connect(host='193.203.168.39', database='u817545168_nulled', user='u817545168_nulled', password='?KL?!1Cs4')
                if self.connection.is_connected():
                    db_Info = self.connection.get_server_info()
                    print("Connected to MySQL Server version ", db_Info)
                    
                    self.cursor = self.connection.cursor()
                    self.cursor.execute("select database();")
                    record = self.cursor.fetchone()
                    print("You're connected to database: ", record[0])
                    self.switch = True
                    
            except Error as e:
                print("1 Error while connecting to MySQL", e)
        
        else:
            print("Connection is already opened, first close")
            
    ### Operations on the database
            
    
    # check if exists
    def check_exists(self, slug) -> bool:
        
        query = f"SELECT series_slug FROM `series` WHERE series_slug ='{slug}' LIMIT 1"
        self.cursor.execute(query)        
        record = self.cursor.fetchone()
        if record:
            res = True
        else:
            res = False
        return res
    
    def add_data(self, hash, cats_db, title,slug, desc, image,episodes_list,release_date, latest):
        self.connect()
        # add data to the table.
        db_image = "upload/"+image

        seo_title = "WATCH " + title + " NOW FOR FREE "
        seo_desc = seo_title + "\n" + desc
        seo_keyword = "anime dex, animedex, watch anime online, free anime, anime stream, anime hd, english sub, kissanime, gogoanime, animeultima, 9anime, 123animes, animefreak, vidstreaming, gogo-stream, animekisa, zoro.to, gogoanime.run, animedex, animekisa"

        query = "INSERT INTO `series` (id, series_genres,series_access,series_name,series_slug,series_info,series_poster,seo_title,seo_description,seo_keyword) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(query,(hash, cats_db,"Free",title, slug, desc, db_image,seo_title,seo_desc,seo_keyword))
        self.connection.commit()

        query = "INSERT INTO `season` (id, series_id, season_name,season_slug,season_poster,seo_title,seo_description,seo_keyword) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(query,(hash, hash, "Season 1", "season-1",db_image,seo_title,seo_desc,seo_keyword))
        self.connection.commit()
        
        lastest_data = 0
        for item in episodes_list:
            ep_no = item['ep_no']
            url = item['url']

            video_title = "Episode " + ep_no
            video_slug = "episode-" + ep_no
            
            if latest == 1 and item == episodes_list[-1]:
                lastest_data = 1

            query = "INSERT INTO `episodes` (video_access, episode_series_id,episode_season_id,video_title,release_date,video_slug,video_image,video_url,latest) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(query,("Free",hash,hash,video_title,release_date,video_slug,db_image,url,lastest_data))
            self.connection.commit()

        self.disconnect()

        session = ftplib.FTP('178.16.128.82', 'u817545168.anime', 'GtScript20.')
        file = open(f'images/{image}','rb')
        session.storbinary(f'STOR {image}', file)
        file.close()
        session.quit()
        
        os.remove(f"images/{image}")

    