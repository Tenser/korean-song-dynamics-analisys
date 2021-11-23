import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import sys
import numpy as np
import re
import time
import datetime

url_list = {}

URL = 'https://music.bugs.co.kr/years'

driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url=URL)
now = datetime.datetime.today().year 
year = now
i = 1
while year > 2020:
    year -= 1
    if year % 10 == 0 and now - year > 10:
        i += 1
    element = driver.find_element(By.XPATH, '//*[@id="container"]/section/div/ul/li[{}]/figure/div/a[1]'.format(i))
    url_list[year] = element.get_attribute('href')
    i += 1
driver.close()
print(url_list)

song_list = {}
driver = webdriver.Chrome(executable_path='chromedriver')
for year, url in url_list.items():
    #driver = webdriver.Chrome(executable_path='chromedriver')
    driver.get(url=url)
    code = url.split('/')[-1]
    #element = driver.find_element(By.XPATH, '//*[@id="ESALBUM{0}"]/table/tbody/tr'.format(code))
    #size = element.size()
    #print(size)
    for i in range(1, 101):
        is_featuring = False
        try:
            title = driver.find_element(By.XPATH, '//*[@id="ESALBUM{0}"]/table/tbody/tr[{1}]/th/p/a'.format(code, i)).get_attribute('title')
        except NoSuchElementException:
            continue
        if title.find('Feat.') != -1:
            is_featuring = True
        title = re.sub(r'\([^)]*\)', '', title).strip()
        singer = driver.find_element(By.XPATH, '//*[@id="ESALBUM{0}"]/table/tbody/tr[{1}]/td[4]/p/a'.format(code, i)).get_attribute('title')
        singer = re.sub(r'\([^)]*\)', '', singer).strip()
        if year in song_list:
            song_list[year].append((title, singer, is_featuring))
        else:
            song_list[year] = [(title, singer, is_featuring)]
driver.close()
count = 0
for year in song_list.keys():
    count += len(song_list[year])
print(count)

data = []
driver = webdriver.Chrome(executable_path='chromedriver')
for year in song_list.keys():
    for title, singer, is_featuring in song_list[year]:
        row = [year, title, singer, is_featuring]
        #driver = webdriver.Chrome(executable_path='chromedriver')
        try:
            driver.get(url='https://www.melon.com/search/song/index.htm?q={0}+{1}&section=&searchGnbYn=Y&kkoSpl=Y&kkoDpType=&mwkLogType=T'.format(title, singer))
            driver.find_element(By.XPATH, '//*[@id="frm_defaultList"]/div/table/tbody/tr/td[3]/div/div/a[1]').click()
            genre = driver.find_element(By.XPATH, '//*[@id="downloadfrm"]/div/div/div[2]/div[2]/dl/dd[3]').text
            row.append(genre)
        except NoSuchElementException:
            row.append('')

        try:
            driver.get(url='https://www.melon.com/search/total/index.htm?q={0}&section=&searchGnbYn=Y&kkoSpl=Y&kkoDpType=&mwkLogType=T'.format(singer))
            singer_type = driver.find_element(By.XPATH, '//*[@id="conts"]/div[3]/div/div[1]/dl/dd[2]').text
            singer_type = singer_type.split(', ')
            sex = singer_type[0]
            is_solo = singer_type[1]
            row.append(sex)
            row.append(is_solo)
        except NoSuchElementException:
            row.append('')

        print(row)
        data.append(row)
        time.sleep(2)
driver.close()
data = np.array(data)
np.save('data/songs' + str(year), data)
    
print(data)