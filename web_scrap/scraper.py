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
    chrome_options.add_argument("--no-sandbox") #! Mandatory option to run the script in a VPS
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
    
    
    wait = WebDriverWait(driver, 5)
    search_box = wait.until(EC.presence_of_element_located((By.NAME, 'q')))
    search_box.send_keys(search_text)
    search_box.send_keys(Keys.RETURN)  # Simula la tecla Enter

    time.sleep(5)

    page_source = driver.page_source

    driver.quit()

    return page_source


def scrape_top_results(html_content, limit=10):
    print("Scraping top results...")
    soup = BeautifulSoup(html_content, "html.parser")

    li_elements = soup.select("ul li")[:limit]
    print(f'Encontrados {len(li_elements)} elementos')
    results = []
    
    # Extraer la información relevante de cada elemento
    for li in li_elements:
        # Fecha del anuncio
        datetime_tag = li.find('time')
        date_posted = ''
        if datetime_tag:
            datetime_str = datetime_tag.get('datetime')
            # Convertir la fecha (si es necesario)
            date_posted = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(datetime_str) / 1000.0))
        else:
            date_posted = "No disponible"

        location_tag = li.select_one('span.iNbnEX')
        location = location_tag.text if location_tag else "No disponible"

        link_tag = li.find('a', href=True)
        link = 'https://revolico.com'+link_tag['href'] if link_tag else "No disponible"

        results.append({'date': date_posted, 'location': location, 'link': link})

    return results


if __name__ == "__main__":
    base_url = "https://revolico.com/"  # Reemplaza con la URL real
    search_text = "iPhone 14"

    search_results_page = perform_search(base_url, search_text)
    results = scrape_top_results(search_results_page, 5)

    print("Top 10 resultados de la búsqueda:")
    for i, result in enumerate(results):
        print(f"{i+1}. Fecha: {result['date']}, Lugar: {result['location']}, Link: {result['link']}")
