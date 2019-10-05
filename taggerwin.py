import requests
from bs4 import BeautifulSoup
import time
import re
import sys
import os
import lxml
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH

links_list = []
mp3path = (input("Enter path to mp3's: "))
tempmp3 = []
fullmp3 = []
tempmp3 += [each for each in os.listdir(mp3path) if each.endswith('mp3')]
i = 0


for each in tempmp3:
    fullpathmp3 = str(mp3path + each)
    fullmp3.append(fullpathmp3)


mp31 = MP3File(fullmp3[0])
mp31.set_version(VERSION_2)
album_mp3 = str(mp31.album)
print(mp31.get_tags())
print(mp31.artist, ' - ', mp31.album, ' (', mp31.year, ')')
gnr = str(mp31.genre)
print(gnr.replace('\x00','; '))

headers = {
  "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}
search_url = "https://rateyourmusic.com/search?&searchtype=l&searchterm="
main_url = "https://rateyourmusic.com"
r = requests.get(str(search_url + album_mp3), headers=headers)
time.sleep(5)
soup = BeautifulSoup(r.text, 'html.parser')

#Getting Hrefs as numbered list
for album in soup.find_all('a', 'searchpage'):
    i += 1
    temp = main_url + str(album.get('href'))
    print(i, temp)
    links_list.append(temp)


link = input("Choose number of correct release: ")
lnk = links_list[int(link) - 1]
time.sleep(5)
r2 = requests.get(str(lnk), headers=headers)
soup2 = BeautifulSoup(r2.text, 'lxml')
print(lnk)

try:
    genres = soup2.find('span', 'release_pri_genres').get_text()
    genre = (re.sub(r'[,.]', ';', genres))
    print('Primary genres: ', genre)
except AttributeError:
    print('AttrErrPrimary')

try:
    sec_genres = soup2.find('span', 'release_sec_genres').get_text()
    sec_genre = (re.sub(r'[,;]', ';', sec_genres))
    print('Secondary: ', sec_genre)
    genres_merged = (str(genre + "; " + sec_genre))
except AttributeError:
    print('AttrErrSecondary')
    sec_genre = None
    genres_merged = genre



print('All Genres: ', genres_merged)

for file in fullmp3:
    mp3 = MP3File(file)
    mp3.set_version(VERSION_2)
    mp3.genre = genres_merged.replace('; ','\x00')
    mp3.save()
