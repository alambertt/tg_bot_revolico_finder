import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def perform_search(url, search_text):
    print("Performing search...")

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_experimental_option("prefs", {
    #   "profile.default_content_setting_values.cookies": 1,  # Habilita cookies
    #   "profile.block_third_party_cookies": False  # Permitir cookies de terceros
    # })
    # chrome_options.add_argument('window-size=1200x600')
    # chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # chrome_options.add_argument("user_agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15")

    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.get(url)
    
    # print(driver.page_source)
    
    wait = WebDriverWait(driver, 5)
    search_box = wait.until(EC.presence_of_element_located((By.NAME, 'q')))
    # Suponiendo que el cuadro de búsqueda tiene el atributo name='q'
    # search_box = driver.find_element_by_name("q")
    search_box.send_keys(search_text)
    search_box.send_keys(Keys.RETURN)  # Simula la tecla Enter

    # Espera para asegurar que la página tenga tiempo de cargar los resultados
    time.sleep(5)

    page_source = driver.page_source

    driver.quit()

    return page_source


def scrape_top_results(html_content, limit=10):
    print("Scraping top results...")
    soup = BeautifulSoup(html_content, "html.parser")

    li_elements = soup.select("ul li")[:limit]

    results = []
    for li in li_elements:
        results.append(
            li.text.strip()
        )  # Utilizo .strip() para eliminar espacios en blanco al inicio y al final

    return results


if __name__ == "__main__":
    base_url = "http://revolico.com/"  # Reemplaza con la URL real
    search_text = "iPhone 14"

    search_results_page = perform_search(base_url, search_text)
    results = scrape_top_results(search_results_page, 5)

    print("Top 10 resultados de la búsqueda:")
    for i, result in enumerate(results):
        print(f"{i+1}. {result}")
