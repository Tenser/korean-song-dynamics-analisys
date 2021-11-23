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

URL = 'https://music.bugs.co.kr/years'

driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url=URL)
year = int(sys.argv[1])
i = 1
while True:
    element = driver.find_element(By.XPATH, '//*[@id="container"]/section/div/ul/li[{0}]/figure/figcaption/a[1]'.format(i))
    if element.get_attribute('title').find(str(year)+'년 베스트') != -1:
        element.click()
        time.sleep(2)
        break
    i += 1

song_list = []
code = driver.current_url.split('/')[-1]
print(code)

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
    song_list.append((title, singer, is_featuring))
driver.close()
print(song_list)

data = []
driver = webdriver.Chrome(executable_path='chromedriver')
rank = 1
for title, singer, is_featuring in song_list:
    row = [rank, title, singer, is_featuring]
    #driver = webdriver.Chrome(executable_path='chromedriver')
    try:
        driver.get(url='https://www.melon.com/search/song/index.htm?q={0}+{1}&section=&searchGnbYn=Y&kkoSpl=Y&kkoDpType=&mwkLogType=T'.format(title, singer))
        driver.find_element(By.XPATH, '//*[@id="frm_defaultList"]/div/table/tbody/tr/td[3]/div/div/a[1]').click()
        day = driver.find_element(By.XPATH, '//*[@id="downloadfrm"]/div/div/div[2]/div[2]/dl/dd[2]').text
        row.insert(0, day)
        genre = driver.find_element(By.XPATH, '//*[@id="downloadfrm"]/div/div/div[2]/div[2]/dl/dd[3]').text
        row.append(genre)
    except NoSuchElementException:
        continue

    try:
        driver.get(url='https://www.melon.com/search/total/index.htm?q={0}&section=&searchGnbYn=Y&kkoSpl=Y&kkoDpType=&mwkLogType=T'.format(singer))
        singer_type = driver.find_element(By.XPATH, '//*[@id="conts"]/div[3]/div/div[1]/dl/dd[2]').text
        singer_type = singer_type.split(', ')
        sex = singer_type[0]
        row.append(sex)
        if len(singer_type) > 1:
            is_solo = singer_type[1]
            row.append(is_solo)
        else:
            row.append('')
    except NoSuchElementException:
        row.append('')
        row.append('')

    print(row)
    data.append(row)
    rank += 1
    time.sleep(2)
driver.close()
data = np.array(data)
np.save('data/songs_' + str(year), data)
    
print(data)