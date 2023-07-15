# Web Scraping Job Listings with Selenium

This Python script uses Selenium to scrape job listings from a website. It navigates to the job listings page, scrolls to load all the jobs, and then extracts information about each job. The script also remembers which job listings it has already scraped, so it only scrapes new listings each time it runs.

## Setting Up a Virtual Environment

Before running the script, it's a good practice to create a virtual environment. This isolates your project and its dependencies from other projects and system-wide packages, which can help prevent conflicts between different versions of packages.

To create a virtual environment, follow these steps:

1. Open a terminal and navigate to the directory where you saved the script.

2. Run the following command to create a virtual environment named `venv`:

    ```bash
    python -m venv venv
    ```


3. Activate the virtual environment:

- On Windows, run: `.\venv\Scripts\activate`
- On Unix or MacOS, run: `source venv/bin/activate`

You should now see `(venv)` at the start of your command prompt, indicating that the virtual environment is active.

## Installing Dependencies

The script requires several Python packages. These dependencies are listed in a file named `requirements.txt`.

To install the dependencies, make sure your virtual environment is active, and then run the following command:

```pip install -r requirements.txt```


This will install all the required packages in your virtual environment.

Now you're ready to run the script as described in the [How to Use](#how-to-use) section.


You also need to have the Chrome browser installed, and you need to download the appropriate version of ChromeDriver and add it to your system's PATH. You can download ChromeDriver from the [ChromeDriver website](https://sites.google.com/a/chromium.org/chromedriver/).

## How to Use

To use this script, follow these steps:

1. Save the script to a file, for example `scraper.py`.

2. Open a terminal and navigate to the directory where you saved the script.

3. Run the script by typing `python scraper.py` and pressing Enter.

The script will open a new Chrome window, navigate to the website, and start scraping job listings. It saves the scraped data to a CSV file named `jobs.csv`.

## Customizing the Script

You can customize this script to scrape job listings from a different website by modifying the URLs and the XPaths used to find elements on the page.

You also need to provide your own username and password for the website. Replace `'johndoe@gmail.com'` and `'johndoe!'` with your own username and password.

## Understanding the Code

The script is organized into a class named `Scraper` that contains several methods:

- `__init__`: Initializes a new instance of the class. Sets up the Selenium webdriver and other instance variables.

- `load_scraped_links` and `save_scraped_links`: Load and save the list of job listings that have already been scraped.

- `accept_cookies`: Navigates to the website and accepts the cookie policy.

- `login`: Logs in to the website using the provided username and password.

- `navigate_to_jobs`: Navigates to the page with the job listings.

- `scrape_jobs`: Scrolls to load all the job listings and finds the links to the individual job pages.

- `extract_job_info`: Navigates to each job page and extracts information about the job.

- `save_to_csv`: Saves the scraped data to a CSV file.

- `main`: The main method that calls all the other methods in the correct order.

The script uses the Selenium library to interact with the website. It uses the `webdriver.Chrome` class to control the Chrome browser, and it uses the `WebDriverWait` and `expected_conditions` classes to wait for elements to appear on the page. It finds elements using the `find_element` and `find_elements` methods and the `By` class to specify how to locate the elements. It extracts text from elements using the `text` property, and it clicks on elements using the `click` method. It also uses JavaScript to scroll the page.
