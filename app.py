from bs4 import BeautifulSoup as soup
import urllib.request
import ssl
import requests

search = input("Search For: ")
webpage = "https://www.linkedin.com/jobs/search?keywords={}&location=Bangladesh".format(search)

ssl._create_default_https_context = ssl._create_unverified_context
wp = urllib.request.urlopen(webpage)
pw = wp.read()
page_soup = soup(pw, "html.parser")

#LINKEDIN
print("\n___LINKEDIN___\n")
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
print("\n___BDJOBS___\n")
data = {
    'txtsearch': search,
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
