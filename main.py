from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os
import json

class Scraper:
    def __init__(self):
        options = Options()
        options.add_argument('-start-maximized')
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.jobs = []


    def load_scraped_links(self):
        if os.path.exists('scraped_links.json'):
            with open('scraped_links.json', 'r') as f:
                try:
                    self.scraped_links = json.load(f)
                except json.JSONDecodeError:
                    self.scraped_links = []
        else:
            self.scraped_links = []


    def save_scraped_links(self):
        with open('scraped_links.json', 'w') as f:
            json.dump(self.scraped_links, f)


    def accept_cookies(self):
        self.driver.get('https://prosperix.com/')
        self.wait.until(EC.url_to_be('https://prosperix.com/'))
        self.wait = WebDriverWait(self.driver, 10)
        self.wait.until(EC.element_to_be_clickable((By.ID, 'hs-eu-confirmation-button'))).click()
        
        
    def login(self, username, password):
        self.driver.get('https://auth.crowdstaffing.com/login')
        self.wait.until(EC.url_to_be('https://auth.crowdstaffing.com/login'))
        self.driver.find_element(By.NAME, 'user.login').send_keys(username)
        self.driver.find_element(By.NAME, 'user.password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(15)


    def navigate_to_jobs(self):
        self.driver.get('https://napkinhealth.crowdstaffing.com/job-marketplace?smartsearch=eyJpZCI6IjFjMzU1MWY1LTY4NDEtNDdhMi1hMGI0LWJiOWE4ZTE5NWRkNSIsInVzZXJfaWQiOiIwNjAzYzc4ZC0wOGM4LTQ0YWYtYTU5My04ZDViMGM1OTVlZjciLCJuYW1lIjoiSGVhbHRoQ2FyZSBDYXRlZ29yeSIsImFsZXJ0X2VuYWJsZWQiOmZhbHNlLCJvcGVyYW5kIjp7Imdyb3VwcyI6W3siZmlsdGVycyI6W3sidHlwZSI6InRleHQiLCJ2YWx1ZSI6IkhlYWx0aCBDYXJlIiwiYXR0cmlidXRlIjoiY2F0ZWdvcnlfbmFtZSIsImNvbmRpdGlvbiI6IklzIn1dLCJvcGVyYXRvciI6ImFuZCJ9XSwib3BlcmF0b3IiOiJhbmQifX0%3D&sort=eyJvcmRlcl9maWVsZCI6InB1Ymxpc2hlZF9hdCIsIm9yZGVyIjoiZGVzYyJ9')
        self.wait.until(EC.url_to_be('https://napkinhealth.crowdstaffing.com/job-marketplace?smartsearch=eyJpZCI6IjFjMzU1MWY1LTY4NDEtNDdhMi1hMGI0LWJiOWE4ZTE5NWRkNSIsInVzZXJfaWQiOiIwNjAzYzc4ZC0wOGM4LTQ0YWYtYTU5My04ZDViMGM1OTVlZjciLCJuYW1lIjoiSGVhbHRoQ2FyZSBDYXRlZ29yeSIsImFsZXJ0X2VuYWJsZWQiOmZhbHNlLCJvcGVyYW5kIjp7Imdyb3VwcyI6W3siZmlsdGVycyI6W3sidHlwZSI6InRleHQiLCJ2YWx1ZSI6IkhlYWx0aCBDYXJlIiwiYXR0cmlidXRlIjoiY2F0ZWdvcnlfbmFtZSIsImNvbmRpdGlvbiI6IklzIn1dLCJvcGVyYXRvciI6ImFuZCJ9XSwib3BlcmF0b3IiOiJhbmQifX0%3D&sort=eyJvcmRlcl9maWVsZCI6InB1Ymxpc2hlZF9hdCIsIm9yZGVyIjoiZGVzYyJ9'))
        self.wait = WebDriverWait(self.driver, 10)
        time.sleep(13)
        

    def scrape_jobs(self):
        while True:
            self.driver.execute_script(
                "document.querySelector('.sc-dwalKd.bKEtSx.sc-hUTmXr.hYvMzg').scrollTop = document.querySelector('.sc-dwalKd.bKEtSx.sc-hUTmXr.hYvMzg').scrollHeight")
            time.sleep(15)
            new_jobs = self.driver.find_elements(By.XPATH, '//div[@class="sc-dXsUDb iwLnYx relative"]')
            if len(new_jobs) == len(self.jobs):
                break
            self.jobs = new_jobs


    def extract_job_info(self):
        job_info = []
        job_links = []
        for job in self.jobs:
            links = job.find_elements(By.TAG_NAME, 'a')
            if links:
                job_link = links[0].get_attribute('href')
                if job_link in self.scraped_links:
                    continue
                self.scraped_links.append(job_link)
                job_links.append(job_link)
        
        print(f"Job links collected : {len(job_links)}")

        for i, job_link in enumerate(job_links):
            print(f"Job link {i}: ", job_link)
            self.driver.get(job_link)
            self.wait.until(EC.url_to_be(job_link))
            self.wait = WebDriverWait(self.driver, 10)
            time.sleep(15)
            try:
                wait = WebDriverWait(self.driver, 15)
                organization_element = wait.until(EC.presence_of_element_located((By.XPATH, './/p[@class="sc-ldMllC gUdPCj"]')))
                organization = organization_element.text
            except NoSuchElementException:
                print(f"Could not find organization element for job link: {job_link}")
                organization = None
            job_position = self.driver.find_element(By.XPATH,'.//p[@class="sc-bLqSdX VuJyj"]').text
            job_code = self.driver.find_element(By.XPATH,'.//p[@class="sc-kgDbTy hjUIEE"]').text
            location = self.driver.find_element(By.XPATH,'.//p[@class="sc-ilsNdd hDiSpo"]/span[2]').text.split("in ")[1]
            divs = self.driver.find_elements(By.XPATH,'.//div[@class="sc-jMWxgM kXMJoW wysiwyg-output"]')
            summary = "\n".join(divs[0].text.split('\n')) if len(divs) > 0 else ""
            roles_responsibilities = "\n".join(divs[1].text.split('\n')) if len(divs) > 1 else ""
            divs = self.driver.find_elements(By.XPATH,'.//div[@class="sc-dNkQa kWYEjC text-12p"]')
            required_skills = " ".join([div.text for div in divs])
            if len(required_skills) == 0: 
                required_skills = None
            divs = self.driver.find_elements(By.XPATH, './/ul[@class="sc-dIMhSk jIrqzB"]/div')
            lis = {}
            keys = ['Available', 'Experience', 'Term', 'Starting', 'Type:', 'Auth:', 'Certifications:', 'Benefits:', 'Pay Rate:', 'Reward Rate:']
            for i, div in enumerate(divs):
                text = div.find_element(By.TAG_NAME, 'li').text
                for key in keys:
                    if key in text:
                        lis[key] = text
            position = lis.get('Available').split(' ')[0] if lis.get('Available') is not None else None
            years_of_experience  = lis.get('Experience').split(' Experience')[0] if lis.get('Experience') is not None else None
            contract_length = lis.get('Term').split(' Term')[0] if lis.get('Term') is not None else None
            starting_period  = lis.get('Starting').split('Starting ')[1] if lis.get('Starting') is not None else None
            work_type = lis.get('Type:').split(': ')[1] if lis.get('Type:') is not None else None
            work_auth = lis.get('Auth:').split(': ')[1] if lis.get('Auth:') is not None else None
            certifications = lis.get('Certifications:').split(': ')[1] if lis.get('Certifications:') is not None else None
            benefits = lis.get('Benefits:').split(': ')[1] if lis.get('Benefits:') is not None else None
            pay_rate = "$" + lis.get('Pay Rate:').split('$')[1].replace("\n", "") if lis.get('Pay Rate:') is not None else None
            reward_rate = "$" + lis.get('Reward Rate:').split('$')[1].replace("\n", "") if lis.get('Reward Rate:') is not None else None

            
            job_info.append({
                'organization': organization,
                'job_position': job_position,
                'job_code': job_code,
                'location': location,
                'summary': summary,
                'roles_responsibilities': roles_responsibilities,
                'required_skills': required_skills,
                'position': position,
                'years_of_experience': years_of_experience,
                'contract_length': contract_length,
                'starting_period': starting_period,
                'work_type': work_type,
                'work_auth': work_auth,
                'certifications': certifications,
                'benefits': benefits,
                'pay_rate': pay_rate,
                'reward_rate': reward_rate,
            })
            
        print("All done!")
        
        return job_info

    def save_to_csv(self, data, filename):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)

    def main(self, username, password):
        self.load_scraped_links()
        self.accept_cookies()
        self.login(username, password)
        self.navigate_to_jobs()
        self.scrape_jobs()
        job_info = self.extract_job_info()
        self.save_to_csv(job_info, 'jobs.csv')
        self.save_scraped_links()

if __name__ == '__main__':
    scraper = Scraper()
    scraper.main('emailaddress', 'password')