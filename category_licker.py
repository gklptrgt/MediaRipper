
import tools
import csv_master
import bs4

# https://ww4.gogoanime2.org/home
# .right a

req = tools.link_checker("https://ww4.gogoanime2.org/home")

# scraping anime information
soup = bs4.BeautifulSoup(req.content, "lxml")

xs = soup.select(".right a")
i = 1
for x in xs:
    name = x.text.strip()
    csv_master.add_to_cats(i, name)
    i += 1

