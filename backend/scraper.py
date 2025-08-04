# scraper.py (Final Version 2 - Waits for H1 Title)

import time
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

OUTPUT_FILE = "abdominal_pain_data_final.json"
SYMPTOM_PAGE_URL = "https://www.mayoclinic.org/symptom-checker/abdominal-pain-in-adults-adult/related-factors/itt-20009075"

def scrape_mayo_clinic():
    """
    Scrapes Mayo Clinic by waiting for the H1 title to appear after clicking the cookie button.
    """
    print("Initializing VISIBLE ChromeDriver...")
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    driver.maximize_window()

    print(f"Navigating to: {SYMPTOM_PAGE_URL}")
    try:
        driver.get(SYMPTOM_PAGE_URL)

        # --- STEP 1: HANDLE THE COOKIE BANNER (Same as before) ---
        try:
            print("Looking for 'Accept' or 'I agree' cookie button...")
            cookie_xpath = "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')] | //button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'i agree')]"
            cookie_accept_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, cookie_xpath))
            )
            print("Button found! Clicking it...")
            cookie_accept_button.click()
            print("Cookie button successfully clicked.")
            time.sleep(3)
        except Exception as e:
            print(f"WARNING: Could not find a cookie button to click. Continuing... Details: {e}")

        # --- STEP 2: WAIT FOR THE H1 TITLE (This is the new, more robust logic) ---
        print("Waiting for main H1 title to load...")
        # We now wait for the h1 tag with the specific text. This is very reliable.
        title_xpath = "//h1[contains(text(), 'Abdominal pain in adults')]"
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, title_xpath))
        )
        print("H1 Title found! Page is considered loaded.")
        
        # --- STEP 3: PARSE THE DATA (Same as before) ---
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        factor_groups_data = []
        # We still use the original selector to get the data, but only after we know the page is loaded.
        factor_containers = soup.select('div.symptom-checker-selection div.row div.col-xs-12')
        for container in factor_containers:
            group_name_tag = container.find('strong')
            if group_name_tag:
                group_name = group_name_tag.get_text(strip=True)
                factors = [label.get_text(strip=True) for label in container.select('span.symptom-checker-label')]
                if group_name and factors:
                    factor_groups_data.append({"group_name": group_name, "factors": factors})
        
        print(f"Found {len(factor_groups_data)} factor groups.")
        
        emergency_info = None
        emergency_container = soup.find('h3', string='When to seek medical advice')
        if emergency_container:
            points = [item.get_text(strip=True) for item in emergency_container.find_next_sibling('ul').find_all('li')]
            emergency_info = {"title": "When to seek medical advice", "points": points}
            print("Found emergency medical advice information.")
        
        if not factor_groups_data and not emergency_info:
             print("\nCRITICAL ERROR: Page loaded but no data was extracted. The content structure may have changed.")
             time.sleep(5)
             return

        scraped_data = {
            "symptom": "Abdominal pain in adults",
            "source_url": SYMPTOM_PAGE_URL,
            "emergency_info": emergency_info,
            "factor_groups": factor_groups_data
        }

        with open(OUTPUT_FILE, 'w') as f:
            json.dump(scraped_data, f, indent=2)

        print(f"\nSUCCESS! Scraped data and saved it to '{OUTPUT_FILE}'")

    except Exception as e:
        print(f"An unexpected error occurred during the process: {e}")
        print("Pausing for 10 seconds before closing so you can inspect the browser.")
        time.sleep(10)
    finally:
        print("Closing the browser.")
        driver.quit()

if __name__ == "__main__":
    scrape_mayo_clinic()