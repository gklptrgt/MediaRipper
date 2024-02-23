import csv

def add_to_atlas(id, link):
    with open('atlas.csv','a', newline='',  encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([id, link])
