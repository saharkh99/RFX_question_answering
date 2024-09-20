from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import google_colab_selenium as gs
import time
import requests
import os

# Initialize the WebDriver (update with your WebDriver path)
# service = Service(executable_path='/path/to/chromedriver')  # Update with your path
# driver = webdriver.Chrome(service=service)

driver = gs.Chrome()
# Define the URL of the search engine
search_url = "https://bcbid.gov.bc.ca/page.aspx/en/rfp/request_browse_public"  # Replace with the actual search engine URL
driver.get(search_url)

# Wait for the page to load
time.sleep(5)

# Find and interact with the dropdown
dropdown = driver.find_element(By.CSS_SELECTOR, "div[data-selector='body_x_selRtgrouCode']")
dropdown.click()

# Wait for the dropdown options to appear
time.sleep(1)

# Select relevant categories
categories = {
    "itb": "Invitation to Bid",
    "itq": "Invitation to Quote",
    "rfp": "Request for Proposal",
    "Rft": "Request for Tenders",
    "io": "Invitation to Offer"
}

for value in categories.keys():
    category_element = driver.find_element(By.CSS_SELECTOR, f"li[data-value='{value}']")
    category_element.click()

# Wait for selection to register
time.sleep(1)

# Click the search button
search_button = driver.find_element(By.ID, 'body_x_prxFilterBar_x_cmdSearchBtn')
search_button.click()

# Wait for results to load
time.sleep(5)

# Extract the page source after the results are loaded
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Find all <a> tags and extract 'href' attributes
links = ["https://bcbid.gov.bc.ca" + a['href'] for a in soup.find_all('a', href=True)]

# Close the WebDriver
driver.quit()

# Function to download files from the provided links
def download_file(url, folder="downloaded_files"):
    """Downloads the file from the specified URL into the designated folder."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful

        # Parse filename from URL or set a default
        filename = url.split('/')[-1] or 'downloaded_file.pdf'
        save_path = os.path.join(folder, filename)

        # Create the directory if it does not exist
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Save the file
        with open(save_path, 'wb') as f:
            f.write(response.content)

        print(f"File downloaded successfully: {save_path}")
    except requests.RequestException as e:
        print(f"Error downloading the file: {e}")

# Loop through each link to download relevant files
for url in links:
    print(f"Processing URL: {url}")
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP issues

    # Parse the HTML to find the download link
    soup = BeautifulSoup(response.text, 'html.parser')
    a_tag = soup.find('a', href=True, id="body_x_tabc_rfp_ext_prxrfp_ext_x_prxDoc_x_grid_grd__ctl2_files_x_btnDownload_C2A03403-3B4F-45EA-B9BD-700C8E4CB7DC")
    
    if a_tag:
        download_link = "https://bcbid.gov.bc.ca" + a_tag['href']
        print(f"Found download link: {download_link}")
        download_file(download_link)
    else:
        print("No download link found.")
