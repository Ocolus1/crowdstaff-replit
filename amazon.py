from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import os
import json
import names
import csv

# Define constants for filename
JSON_FILENAME = "stored_data.json"
CSV_FILENAME = "results.csv"

def generate_random_names(num=1):
    """
    Generate a list of random names.
    :param num: Number of names to generate.
    :return: List of names.
    """
    return [names.get_first_name() for _ in range(num)]

def select_month_year(driver, month, year, prefix):
    """
    Function to select month and year from dropdowns.
    :param driver: The Selenium WebDriver instance.
    :param month: Month in string format e.g. "January".
    :param year: Year in string format e.g. "2024".
    :param prefix: Should be either "from" or "to".
    """
    month_id = f"{prefix}Month"
    year_id = f"{prefix}Year"
    
    month_dict = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04',
        'May': '05', 'June': '06', 'July': '07', 'August': '08',
        'September': '09', 'October': '10', 'November': '11', 'December': '12'
    }
    
    # Select month from dropdown
    select_month = Select(driver.find_element(By.ID, month_id))
    select_month.select_by_value(month_dict[month])

    # Select year from dropdown
    select_year = Select(driver.find_element(By.ID, year_id))
    select_year.select_by_value(year)

def extract_table_data(driver, stored_data):
    # Extracting rows from table
    rows = driver.find_elements(By.XPATH, "//tr[contains(@id, 'wr_search_result_record_')]")
    
    new_data = []

    for row in rows:
        name = row.find_element(By.XPATH, ".//td[contains(@id, 'owner')]/div/a").text
        partner = row.find_element(By.XPATH, ".//td[contains(@id, 'partner')]/div/span").text
        location = row.find_element(By.XPATH, ".//td[contains(@id, 'eventLocation')]/div/span").text

        data_tuple = (name, partner, location)
        if not any(data == data_tuple for data in stored_data):
            new_data.append(data_tuple)
            stored_data.append(data_tuple)

    return new_data, stored_data

def extract_and_store(driver, stored_data, csv_data):
    """This function will click on the name header until all unique data for a name is scraped"""
    while True:
        # Click the name header to refresh results
        driver.find_elements(By.CLASS_NAME, 'mt-sort-link')[0].click()
        time.sleep(9)

        # Extract data and update the stored data
        new_data, stored_data = extract_table_data(driver, stored_data)

        # If no new data is found, break out of the loop
        if not new_data:
            break

        # Else, add the new data to csv_data
        csv_data.extend(new_data)

    return csv_data, stored_data

def main(search_date_from, search_date_to, num):
    
    # Split the dates
    from_month, from_year = search_date_from.split()
    to_month, to_year = search_date_to.split()
    
    url = "https://www.amazon.com/wedding/search?nameOrEmail=&ref_=wedding_home_stripe"
    
    # Set up the driver. Ensure you've the appropriate driver (like chromedriver) installed.
    options = Options()
    options.add_argument('-start-maximized')
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    
    # Load stored data
    if os.path.exists(JSON_FILENAME):
        with open(JSON_FILENAME, 'r') as json_file:
            try:
                stored_data = json.load(json_file)
            except json.JSONDecodeError:
                stored_data = []
    else:
        stored_data = []
        
    csv_data = []
    
    # Assuming we're generating num random names for this example.
    temp = 0
    for name in generate_random_names(num):
        # Input name into search field
        driver.find_element(By.ID, 'nameOrEmail').clear()
        driver.find_element(By.ID, 'nameOrEmail').send_keys(name)
        time.sleep(2)
        
        # Set the "from" and "to" dates
        select_month_year(driver, from_month, from_year, "from")
        time.sleep(2)
        select_month_year(driver, to_month, to_year, "to")
        time.sleep(2)
        
        # Submit the form
        driver.find_element(By.XPATH, '//input[@class="a-button-input"]').click()
        time.sleep(8)
        
        csv_data, stored_data = extract_and_store(driver, stored_data, csv_data)
        temp += 1
        print(f"Completed {temp} name(s) out of {num}")
        print(f"We have gotten {len(stored_data)} data entry")
        print()
        
    # Save stored data
    with open(JSON_FILENAME, 'w') as json_file:
        json.dump(stored_data, json_file)

    # Save csv data
    with open(CSV_FILENAME, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Name", "Partner", "Event Location"])
        writer.writerows(csv_data)

    # Close the driver after the loop
    driver.quit()

if __name__ == "__main__":
    # main("from what time", "to what time", number of names to generate)
    main("January 2024", "December 2024", 2)