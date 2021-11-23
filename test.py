import numpy as np
from selenium import webdriver

PROXY = "54.249.149.203:80"

webdriver.DesiredCapabilities.CHROME['proxy'] = {
    "httpProxy": PROXY,
    "ftpProxy": PROXY,
    "sslProxy": PROXY,
    "proxyType": "MANUAL"
}


driver = webdriver.Chrome()
driver.get("https://www.google.com/")



#//*[@id="ESALBUM11152"]/table/tbody/tr[55]