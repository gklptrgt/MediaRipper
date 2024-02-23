import csv

def add_to_atlas(id, link):
    with open('atlas.csv','a', newline='',  encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([id, link])

def read_from_atlas():
    rows = []
    with open("atlas.csv", 'r', encoding="utf-8") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            rows.append(row)
    return rows

def add_to_cats(no, name):
    with open('cats.csv','a', newline='',  encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([no, name])
