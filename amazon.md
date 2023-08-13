
# Amazon Wedding Search Script

This script is designed to scrape wedding data from Amazon based on a set of randomly generated names. It takes into account the unique structure and behavior of the Amazon website.

## Install name Library

```
pip install names
```

## Libraries Used

- **selenium**: For web scraping functionality.
- **os**: To interact with the file system.
- **json**: To save and load scraped data in a JSON file.
- **names**: To generate random names.
- **csv**: To save results to a CSV file.

## Core Functions

- **generate_random_names(num=1)**: Generate a list of random names.
- **select_month_year(driver, month, year, prefix)**: Select month and year from dropdowns.
- **extract_table_data(driver, stored_data)**: Extract data from the search results table.
- **extract_and_store(driver, stored_data, csv_data)**: Click on the name header until all unique data for a name is scraped.
- **main(search_date_from, search_date_to)**: Main function to initialize and run the script.

## Steps to run the script

1. Ensure that you have Chrome and the chromedriver installed.
2. Set the date range you wish to search in the `main` function call at the end of the script.
3. Execute the script.

Note: This script uses JSON for data persistence to prevent scraping the same data more than once.
