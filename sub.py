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
        if os.path.exists('sub_scraped_links.json'):
            with open('sub_scraped_links.json', 'r') as f:
                try:
                    self.scraped_links = json.load(f)
                except json.JSONDecodeError:
                    self.scraped_links = []
        else:
            self.scraped_links = []


    def save_scraped_links(self):
        with open('sub_scraped_links.json', 'w') as f:
            json.dump(self.scraped_links, f)
        
    def login(self, username, password):
        self.driver.get('https://my.recruitifi.com/app/login')
        self.wait.until(EC.url_to_be('https://my.recruitifi.com/app/login'))
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-cy="gdpr-button"]'))).click()
        self.driver.find_element(By.ID, 'email').send_keys(username)
        self.driver.find_element(By.XPATH, '//button[@data-cy="sign-in-form-button"]').click()
        time.sleep(6)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[@data-cy="sign-in-form-button"]').click()
        time.sleep(15)


    def navigate_to_jobs(self):
        self.driver.get('https://my.recruitifi.com/app/my-jobcasts/active?industry=%5BHealth%5D')
        self.wait.until(EC.url_to_be('https://my.recruitifi.com/app/my-jobcasts/active?industry=%5BHealth%5D'))
        self.wait = WebDriverWait(self.driver, 10)
        time.sleep(13)
        

    def scrape_jobs(self):
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)
            new_jobs = self.driver.find_elements(By.XPATH, '//*[@data-cy="jobcast-card-active"]')
            self.jobs = new_jobs
            break


    def extract_job_info(self):
        job_info = []
        job_links = []
        for job in self.jobs:
            job_links.append(job)
        
        print(f"Job links collected : {len(job_links)}")

        for i, job_link in enumerate(job_links):
            print(f"Getting job number {i}: ")
            url = "https://my.recruitifi.com/app/my-jobcasts/active?industry=%5BHealth%5D"
            self.driver.get(url)
            self.wait.until(EC.url_to_be(url))
            self.wait = WebDriverWait(self.driver, 10)
            if i == 2 :
                break
            time.sleep(15)
            new_jobs = self.driver.find_elements(By.XPATH, f'//*[@data-cy="jobcast-card-active"]')  
            new_job = new_jobs[i]
            est_earnings = new_job.find_elements(By.XPATH, './/button')[3].text.split("\n")[0]
            new_job = self.driver.find_elements(By.XPATH, f'//*[@data-cy="jobcast-card-title"]')[i].click()
            time.sleep(10)
            
            # This is the code that skips repeat links
            if self.driver.current_url in self.scraped_links:
                print(f"Skipping number {i} : ", self.driver.current_url)
                continue
            self.scraped_links.append(self.driver.current_url)
            ## This is the end of the code
            
            organization = self.driver.find_elements(By.XPATH,'.//h5')[1].text
            jobpost_id = self.driver.find_elements(By.XPATH,'.//textarea')[0].text
            job_position = self.driver.find_elements(By.XPATH,'.//textarea')[2].text
            level = self.driver.find_elements(By.XPATH,'.//textarea')[4].text
            reports_to = self.driver.find_elements(By.XPATH,'.//textarea')[6].text
            vacant_since = self.driver.find_elements(By.XPATH,'.//textarea')[8].text
            vacancies = self.driver.find_elements(By.XPATH,'.//textarea')[10].text
            travel_required = self.driver.find_elements(By.XPATH,'.//textarea')[12].text
            visa_support = self.driver.find_elements(By.XPATH,'.//textarea')[14].text
            report_to_location = self.driver.find_elements(By.XPATH,'.//textarea')[16].text
            country = self.driver.find_elements(By.XPATH,'.//textarea')[18].text
            city = self.driver.find_elements(By.XPATH,'.//textarea')[20].text
            state = self.driver.find_elements(By.XPATH,'.//textarea')[22].text
            postal_code = self.driver.find_elements(By.XPATH,'.//textarea')[24].text
            currency = self.driver.find_elements(By.XPATH,'.//textarea')[26].text
            minimum_salary = self.driver.find_elements(By.XPATH,'.//textarea')[28].text
            maximum_salary = self.driver.find_elements(By.XPATH,'.//textarea')[30].text
            signing_bonus = self.driver.find_elements(By.XPATH,'.//textarea')[32].text
            bonus_description = self.driver.find_elements(By.XPATH,'.//textarea')[34].text
            relocation_package = self.driver.find_elements(By.XPATH,'.//textarea')[36].text
            
            job_description = self.driver.find_elements(By.XPATH,'.//div[@class="wysiwyg-text"]')[0].text
            company_culture = self.driver.find_elements(By.XPATH,'.//div[@class="wysiwyg-text"]')[1].text
            divs = self.driver.find_elements(By.XPATH,'.//div[starts-with(@class, "checkbox-panel disabled checkbox-panel-checked-ie")]')
            benefits = " ".join([div.text for div in divs])
            must_have = self.driver.find_elements(By.XPATH,'.//div[@class="page-card-form-section"]')[7].text
            
            job_info.append({
                'organization': organization,
                'est_earnings': est_earnings,
                'job_position': job_position,
                'jobpost_id': jobpost_id,
                'level': level,
                'reports_to': reports_to,
                'vacant_since': vacant_since,
                'vacancies': vacancies,
                'travel_required': travel_required,
                'visa_support': visa_support,
                'report_to_location': report_to_location,
                'country': country,
                'city': city,
                'state': state,
                'postal_code': postal_code,
                'currency': currency,
                'minimum_salary': minimum_salary,
                'maximum_salary': maximum_salary,
                'signing_bonus': signing_bonus,
                'bonus_description': bonus_description,
                'relocation_package': relocation_package,
                'job_description': job_description,
                'company_culture': company_culture,
                'benefits': benefits,
                'must_have': must_have
            })
            
        print("All done!")
        
        return job_info

    def save_to_csv(self, data, filename):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)

    def main(self, username, password):
        self.load_scraped_links()
        self.login(username, password)
        self.navigate_to_jobs()
        self.scrape_jobs()
        job_info = self.extract_job_info()
        self.save_to_csv(job_info, 'jobs2.csv')
        self.save_scraped_links()

if __name__ == '__main__':
    scraper = Scraper()
    scraper.main('hello@napkinhealth.com', 'Cleanuponaisle6!')
    # scraper.main('emailaddress', 'password')