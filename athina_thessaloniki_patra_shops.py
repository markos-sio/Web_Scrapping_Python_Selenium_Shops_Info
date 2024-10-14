import pandas as pd
import logging
import time
from typing import Optional, List, Dict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Base URL and delivery area paths
BASE_URL = 'The Base URL'
DELIVERY_AREAS = {
    'athina': 'delivery/athina',
    'thessaloniki': 'delivery/thessaloniki',
    'patra': 'delivery/patra',
}

path = "My chome driver path"

def fetch_page_content(url: str) -> Optional[webdriver.Chrome]:
    """Fetches the page content using Selenium."""
    try:
        service = Service(path)
        driver = webdriver.Chrome(service=service)
        driver.get(url)

        # Wait for a few seconds to allow the page to load
        time.sleep(5)

        logging.info("Page content fetched successfully.")
        return driver
    except Exception as e:
        logging.error(f"Error fetching page: {e}")
        return None

def extract_information(driver: webdriver.Chrome) -> List[Dict[str, str]]:
    """Extracts relevant information from the page using Selenium."""
    structured_data = []

    # Find all parent <div> elements with class "sc-cuaALn hxWvNq"
    parent_elements = driver.find_elements(By.CSS_SELECTOR, "div.sc-cuaALn.hxWvNq")

    for parent in parent_elements:
        try:
            # Extract shop name within the parent div
            name_element = parent.find_element(By.CSS_SELECTOR, "h3.sc-fBxSrQ.gisfcW")
            name = name_element.text if name_element else ''

            # Extract service type within the parent div
            service_element = parent.find_element(By.CSS_SELECTOR, "span.sc-dYZCwJ.sc-ddDelH.cEPfiP")
            service = service_element.text if service_element else ''

            # Extract delivery times and minimum consumption (loop through the elements within parent)
            delivery_elements = parent.find_elements(By.CSS_SELECTOR, "span.sc-dYZCwJ.cEPfiP")
            delivery_times = ""
            minimum_consumption = ""
            for element in delivery_elements:
                text = element.text
                if "-" in text:
                    delivery_times = text      
                else:
                    minimum_consumption = text

            # Extract rating within the parent div
            rating_element = parent.find_element(By.CSS_SELECTOR, "span.sc-hZOwmG.bSlFkx")
            rating = rating_element.text if rating_element else ''

            # Extract number of reviews within the parent div
            reviews_element = parent.find_element(By.CSS_SELECTOR, "div.sc-LwRDc.fIyFhK")
            reviews_text = reviews_element.text if reviews_element else 'Not provided'
            reviews = re.search(r'\((\d+)\)', reviews_text)
            reviews = reviews.group(1) if reviews else 'Not provided'

            # Extract delivery cost within the parent div
            delivery_cost_element = parent.find_element(By.CSS_SELECTOR, "span.sc-jMliHe.jbzmJK")
            delivery_cost = delivery_cost_element.text if delivery_cost_element else ''

            # Structure the extracted data
            structured_data.append({
                "Name": name,
                "Service": service,
                "Time": delivery_times,
                "Minimum Consumption": minimum_consumption,
                "Rating": rating,
                "Reviews": reviews,
                "Delivery Cost": delivery_cost
            })
        except Exception as e:
            logging.error(f"Error extracting information: {e}")

    logging.debug(f"Structured data: {structured_data}")
    return structured_data

def create_dataframe(data: List[Dict]) -> pd.DataFrame:
    """Creates a DataFrame from the list of extracted data."""
    return pd.DataFrame(data)

def save_to_excel(data_dict: Dict[str, pd.DataFrame], filename: str) -> None:
    """Saves multiple DataFrames to an Excel file with different sheets."""
    try:
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            for sheet_name, df in data_dict.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            logging.info(f"Excel file created successfully: {filename}")
    except Exception as e:
        logging.critical(f"An error occurred while saving the Excel file: {e}")

if __name__ == "__main__":
    all_structured_data = {}

    for city, area in DELIVERY_AREAS.items():
        logging.info(f"Fetching data for area: {city}")
        full_url = f"{BASE_URL}/{area}"
        driver = fetch_page_content(full_url)
        
        if driver:
            logging.info("Extracting information directly using Selenium...")
            structured_data = extract_information(driver)

            if structured_data:
                all_structured_data[city] = create_dataframe(structured_data)
            else:
                logging.error(f"No structured data for area: {area}")

            driver.quit()  # Close the browser after extraction

    if all_structured_data:
        logging.debug(f"Total structured data for DataFrame: {sum(len(df) for df in all_structured_data.values())} entries")
        save_to_excel(all_structured_data, 'athina_thessaloniki_patra.xlsx')
    else:
        logging.error("No structured data collected across all areas.")
