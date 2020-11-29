from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import urllib.request
import ssl
import requests
import os
import time

search = input("Search For: ")
print("\n")

ssl._create_default_https_context = ssl._create_unverified_context

#LINKEDIN
search_linkedin = search.replace(" ","%20")
webpage = "https://www.linkedin.com/jobs/search?keywords={}&location=Bangladesh".format(search_linkedin)

DIR = (os.path.dirname(os.path.realpath(__file__)))
DRIVERPATH = os.path.join(DIR,"geckodriver.exe")

#Test
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=DRIVERPATH)

SCROLL_PAUSE_TIME = 0.5
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
driver.get(webpage)

while True:
    time.sleep(4)
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

page = driver.execute_script('return document.body.innerHTML')
page_soup = soup(''.join(page), 'html.parser')

print("\n__________LINKEDIN__________\n")
for jobLink in page_soup.find_all("a", {"class":"result-card__full-card-link"}):
    jobLink = jobLink.get('href')
    job = urllib.request.urlopen(jobLink)
    pw = job.read()
    job_page_html= soup(pw, "html.parser")

    #JOB TITLE
    jobTitle = job_page_html.find("h1", {"class":"topcard__title"})
    print("JOB TITLE: {}".format(jobTitle.text))

    #COMPANY NAME
    try:
        companyName = job_page_html.find("a", {"class":"topcard__org-name-link"})
        print("COMPANY NAME: {}".format(companyName.text))
    except AttributeError:
        companyName = job_page_html.find("span", {"class":"topcard__flavor"})
        print("COMPANY NAME: {}".format(companyName.text))

    #POSTED
    postedTime = job_page_html.find("span", {"class":"posted-time-ago__text"})
    print("POSTED: {}".format(postedTime.text))

    #JOBLINK
    print("JOB LINK: {}\n".format(jobLink))

#BDJOBS
search_bdjobs = search.replace(" ","+")
print("\n__________BDJOBS__________\n")
data = {
    'txtsearch': search_bdjobs,
    'qOT': '0',
    'hidJobSearch': 'jobsearch'
}

base = "https://jobs.bdjobs.com/"
url = "https://jobs.bdjobs.com/jobsearch.asp"
response = requests.post(url, data=data)
doc = soup(response.text, 'html.parser')

for div in doc.find_all("div",{"class":"job-title-text"}):
    for all_a in div.find_all("a",{"target":"_blank"}):
        jobLink = all_a.get('href')
        jobTitle = all_a.text

        #Opening the Job Page for more details
        wp = urllib.request.urlopen("https://jobs.bdjobs.com/{}".format(jobLink))
        pw = wp.read()
        page_soup = soup(pw, "html.parser")

        Company_Name = page_soup.find("h3",{"class":"company-name"})

        print("JOB TITLE: {}".format(jobTitle.strip()))
        print("COMPANY NAME: {}".format((Company_Name.text).strip()))
        print("JOB LINK: https://jobs.bdjobs.com/{}\n".format(jobLink))
