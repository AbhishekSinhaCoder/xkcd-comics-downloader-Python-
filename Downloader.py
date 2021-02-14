import requests
from bs4 import BeautifulSoup
import os
import json 

dl_dir = './images/'

nmbr_of_pages = 2424

print("Starting to download", nmbr_of_pages, "images")

for i in range(1, nmbr_of_pages+1):
    idx = str(i)
    r = requests.get("https://xkcd.com/" + idx + "/")
    if r.status_code == 200:
        try:
            print("Downloading image", idx)
            soup = BeautifulSoup(r.content, features="html.parser")
            comic_div = soup.body.find("div", {"id": "comic"})
            img_url = "https:" + comic_div.find("img")["src"]

            os.mkdir("./images/" + idx) 

            dictionary ={
                "url": img_url,
                "name": soup.body.find("div", {"id": "ctitle"}).text, 
                "transcript": soup.body.find("div", {"id": "transcript"}).text
            }

            with open("./images/" + idx + "/description.json", "w") as outfile:  
                json.dump(dictionary, outfile) 

            img_r = requests.get(img_url)
            with open("./images/" + idx + "/" + os.path.basename(img_url), 'wb') as f:
                f.write(img_r.content)
        except:
            print("Skipping image", idx)
    else:
        print("Skipping image", idx)
