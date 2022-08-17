# Copyright (C) 2022 OSME Education - All Rights Reserved
# Author: Xiaofeng Fu
# Description: Collect entry requirement for Manchester master degree

import re
import requests
import os
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin

def get_dynamic_soup(url: str) -> BeautifulSoup:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        soup = BeautifulSoup(page.content(), "html.parser")
        browser.close()
        return soup

def writeData(group):
    with open('manchester.csv','a+',encoding='utf-8') as f:
        f.write(group[0]+','+group[1]+','+group[2]+','+group[3]+','+group[4]+'\n')
    print("---------------------------------------")

print("***** OSME Edu Programme Collector *****")
root_url = "https://www.manchester.ac.uk/study/masters/courses/list/?k=&s=All"
headers = {"Content-Type": "application/json",
                    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
                    "Connection": "close"}
urls = []
programmes = []
requirements = []
application_dates = []
study_modes = []
start_dates = []
s = requests.Session()
s.mount('http://',HTTPAdapter(max_retries=5))
s.mount('https://',HTTPAdapter(max_retries=5))

bs = get_dynamic_soup(root_url)

for programme in bs.select('div[id*="course-list"] li a'):
    urls.append(urljoin(root_url, programme['href']))
    group = ['-','-','-','-','-']
    group[0] = programme.text
    programmes.append(group)

for i in range(len(urls)):
    try:
        resp = s.request("GET",url=urls[i], headers=headers, timeout=(30,60))
    except requests.exceptions.RequestException as e:
        print(e)
    resp.encoding = 'utf-8'
    content = resp.text
    group = programmes[i]

    print("No: "+str(i)+" programme: "+ group[0] + "\nProgress: {:.2f}%".format(100*i/len(urls)))

    bs = BeautifulSoup(content, 'html.parser')
    
    apply_section = bs.select('div[class*="course-profile-content"] div dd[class*="how-to-apply"]')
    if (not isinstance(apply_section, list) or apply_section == []):
        writeData(group)
        continue
    group[2] = '"'+apply_section[0].text+'"'

    #entry requirements
    requirement_section = bs.select('div[class*="course-profile-content"] div')[1]
    if (isinstance(requirement_section, list)):
        writeData(group)
        continue
    group[1] = '"'+requirement_section.text+'"'

    study_mode = ''
    if bs.findAll(text=re.compile('full-time')) != []:
        study_mode = study_mode + 'full-time'
    if bs.findAll(text=re.compile('part-time')) != []:
        study_mode = study_mode + ' part-time'
    if study_mode != '':
        group[3] = study_mode

    start_time = bs.findAll(text=re.compile('beginning'))
    if isinstance(start_time, list) and start_time != []:
        group[4] = start_time[0]
    writeData(group)
print("Finish!")
