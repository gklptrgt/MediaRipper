import csv



def add_to_csv(id, link):

    with open('test.csv','a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([id, link])



add_to_csv(1,"hhtpps:/google.com..")