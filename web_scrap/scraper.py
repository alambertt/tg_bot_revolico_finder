import time
import arrow

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

NO_DATA_AVAILABLE = "No disponible..."
TIMEOUT=10


def perform_search(url, search_text):
    print("Performing search...")

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument(
        "--no-sandbox"
    )  #! Mandatory option to run the script in a VPS

    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    driver.get(url)

    wait = WebDriverWait(driver, TIMEOUT)
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.send_keys(search_text)
    search_box.send_keys(Keys.RETURN)  # Simula la tecla Enter

    time.sleep(TIMEOUT)

    page_source = driver.page_source

    driver.quit()

    return page_source


def scrape_top_results(html_content, limit=10):
    print("Scraping top results...")
    soup = BeautifulSoup(html_content, "html.parser")

    li_elements = soup.select("ul li")[:limit]
    print(f"Encontrados {len(li_elements)} elementos")
    results = []

    # Extraer la información relevante de cada elemento
    for li in li_elements:
        # Fecha del anuncio
        datetime_tag = li.find("time")
        date_posted = ""
        if datetime_tag:
            datetime_str = datetime_tag.get("datetime")
            date_posted = pretty_date(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(datetime_str) / 1000.0)))
        else:
            date_posted = NO_DATA_AVAILABLE

        location_tag = li.select_one("span.iNbnEX")
        location = location_tag.text if location_tag else NO_DATA_AVAILABLE

        link_tag = li.find("a", href=True)
        link = (
            "https://revolico.com" + link_tag["href"] if link_tag else NO_DATA_AVAILABLE
        )

        ad_text = li.get_text().strip()
        if not ad_text:
            ad_text = NO_DATA_AVAILABLE

        results.append(
            {
                "date": date_posted,
                "location": location,
                "link": link,
                "text": ad_text,
            }
        )

    return results


def find(search_text="iPhone 14", base_url="https://revolico.com/", limit=10):
    search_results_page = perform_search(base_url, search_text)
    results = scrape_top_results(search_results_page, limit)
    return results

def pretty_date(date_posted):
    dt = arrow.get(date_posted, 'YYYY-MM-DD HH:mm:ss')
    return dt.humanize(locale='es')  # Cambiar 'es' al idioma que prefieras
