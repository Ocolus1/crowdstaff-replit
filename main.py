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
            time.sleep(10)
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
            self.driver.get(job_link)
            self.wait.until(EC.url_to_be(job_link))
            time.sleep(5)
            print(f"Job link {i}: ", job_link)
            self.driver.get(job_link)
            self.wait.until(EC.url_to_be(job_link))
            self.wait = WebDriverWait(self.driver, 10)
            time.sleep(5)
            try:
                wait = WebDriverWait(self.driver, 10)
                organization_element = wait.until(EC.presence_of_element_located((By.XPATH, './/p[@class="sc-ldMllC gUdPCj"]')))
                organization = organization_element.text
            except NoSuchElementException:
                print(f"Could not find organization element for job link: {job_link}")
                organization = None
            job_position = self.driver.find_element(By.XPATH,'.//p[@class="sc-bLqSdX VuJyj"]').text
            job_code = self.driver.find_element(By.XPATH,'.//p[@class="sc-kgDbTy hjUIEE"]').text
            location = self.driver.find_element(By.XPATH,'.//p[@class="sc-ilsNdd hDiSpo"]/span').text
            divs = self.driver.find_elements(By.XPATH,'.//div[@class="sc-jMWxgM kXMJoW wysiwyg-output"]')
            summary = divs[0].text.split('\n') if len(divs) > 0 else []
            roles_responsibilities = divs[1].text.split('\n') if len(divs) > 1 else []
            divs = self.driver.find_elements(By.XPATH,'.//div[@class="sc-dNkQa kWYEjC text-12p"]')
            required_skills = [div.text for div in divs]
            if len(required_skills) == 0: 
                required_skills = None
            divs = self.driver.find_elements(By.XPATH, './/ul[@class="sc-dIMhSk jIrqzB"]/div')
            lis = {}
            keys = ['Available', 'Experience', 'Term', 'Starting', 'Type:', 'Auth:', 'Certifications:', 'Benefits:', 'Rate:\nUSD\n$', 'Rate:\nUSD\n$']
            for i, div in enumerate(divs):
                text = div.find_element(By.TAG_NAME, 'li').text
                for key in keys:
                    if key in text:
                        lis[key] = text
            position = lis.get('Available', None)
            years_of_experience  = lis.get('Experience', None)
            contract_length = lis.get('Term', None)
            starting_period  = lis.get('Starting', None)
            work_type = lis.get('Type:', None)
            work_auth = lis.get('Auth:', None)
            certifications = lis.get('Certifications:', None)
            benefits = lis.get('Benefits:', None)
            pay_rate = lis.get('Rate:\nUSD\n$', None)
            reward_rate = lis.get('Rate:\nUSD\n$', None)
            
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
    scraper.main('emailaddress', 'password!')
