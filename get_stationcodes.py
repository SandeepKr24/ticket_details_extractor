# Scrapes a website on the internet that contains all the station names and codes of Indian Railways
# This is later used to match the station names extracted from the ticket pdf

import pandas as pd
from io import StringIO
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

names = []
scodes = []

for i in range(5):
    url = f"https://www.cleartrip.com/trains/stations/list?page={i+1}"

    driver.get(url)

    station_codes = driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
    for codes in station_codes:
        scodes.append(codes.text)

    station_names = driver.find_elements(By.XPATH, '//tbody/tr/td[2]/a')
    for stations in station_names:
        names.append(stations.text)

driver.quit()

d = {'names': names, 'codes': scodes}

df = pd.DataFrame(data=d, index=None)

df['Stations'] = df['names'] + " " + "(" + df['codes'] + ")"
df = df.drop(['names', 'codes'], axis=1)

df.to_csv('./station_codes.csv', index=False)