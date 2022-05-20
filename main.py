from selenium import webdriver
import time
from datetime import date
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os

# sets driver
firefox_options = webdriver.FirefoxOptions()
arguments = ["--incognito", "--window-size=1100,500", "--user-agent=Mozilla/5.0 (X11; Linux i686; rv:99.0) Gecko/20100101 Firefox/99.0"]
for argument in arguments:
    firefox_options.add_argument(argument)
#"--headless"

# set browser
browser = webdriver.Firefox(options=firefox_options)
browser.delete_all_cookies()

days_ago = input("days ago(14,3,1): ")

class Job:
    def __init__(self,title, link):
        self.title = title
        self.link = link


def save_jobs(jobs):
    today = date.today()
    #create path if not exist
    path = str(today) +"_within"+ days_ago +"days"
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

    #write to file
    f = open("./"+path + "/README.md", "w+")
    for job in jobs:
        text = "[" + job.title + "]" + "(" + job.link + ")"
        f.write(text + "\n\n\n")
    f.close()  

job_array = []
def get_jobs(start_at):
    global job_array
    url = "https://uk.indeed.com/jobs?q=Junior%20Developer&l=Cambridge%20CB4&sc=0bf%3Aexrec()%3B&&start="+str(start_at)+"&radius=100&fromage=" + days_ago + "&vjk=eb53d109f5cc3c4b"
    browser.get(url)
    job_list = browser.find_element(By.CLASS_NAME,"jobsearch-ResultsList")
    jobs = job_list.find_elements(By.TAG_NAME, "li")
    for job in jobs:
        if len(job.find_elements(By.CSS_SELECTOR, "* .salaryOnly") ) > 0:
            title_containers = job.find_elements(By.CSS_SELECTOR, "* .jobTitle")
            for title_container in title_containers:
                title_link_element = title_container.find_element(By.TAG_NAME, "a")
                title_element = title_link_element.find_element(By.TAG_NAME, "span")
                title = title_element.get_attribute("innerText")
                link = title_link_element.get_attribute("href")
                if "junior" in title.lower():
                    #push to jobs
                    job_array.append(Job(title,link))

    next_page_el = browser.find_elements(By.CSS_SELECTOR, ".pagination-list li:last-child a")
    if len(next_page_el) > 0 and next_page_el[0].get_attribute("aria-label") == "Next":
        #increment and run again
        start_at += 10
        get_jobs(start_at) 
    else:
        #save or quit
        if len(job_array) > 0:
            save_jobs(job_array)
        
    



get_jobs(0)