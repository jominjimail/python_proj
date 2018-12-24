import requests
import pandas as pd
from bs4 import BeautifulSoup

page = requests.get("https://comic.naver.com/webtoon/weekdayList.nhn?week=fri")
soup = BeautifulSoup(page.content , 'html.parser')
friday = soup.find(class_="img_list")
#print(friday)

images=friday.find_all(class_="thumb")
first_image=images[0]
first_a=first_image.find("a")
first_title=first_a['title']
print(first_title)

descs = friday.find_all(class_="desc")
first_desc=descs[0]
first_desc_a = first_desc.find("a")
first_artist = first_desc_a.get_text()
print(first_artist)

ratings = friday.find_all(class_="rating_type")
first_rate = ratings[0].find("strong").get_text()

print(first_rate)

for image in images:
    one =image.find('a')['title']
    #print(one)

for desc in descs:
    one=desc.find('a').get_text()
    #print(one)

for rating in ratings:
    one =rating.find('strong').get_text()
    print(one)


