from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json
import unicodedata
import os
from concurrent.futures import ThreadPoolExecutor

start_time = time.time()
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")

script_dir = os.path.dirname(os.path.abspath(__file__))
chrome_driver_path = os.path.join(script_dir, "chrome")

driver = webdriver.Chrome(options=chrome_options)
url = "https://lol.fandom.com/wiki/Category:Chinese_Residents"
players_results = []

def clean_text(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")

def fetch_player_results(href):
    player = {"name": "", "results": []}
    local_driver = webdriver.Chrome(options=chrome_options)

    try:
      print(f"{href}/Tournament_Results")
      local_driver.get(f"{href}/Tournament_Results")
      time.sleep(2)

      page_source = local_driver.page_source

      soup = BeautifulSoup(page_source, "html.parser")
      table = soup.find("table", {"class": "wikitable sortable hoverable-rows jquery-tablesorter"})

      if not table:
        return

      thead = table.find("thead").find_all("th")
      player = {
        "name": "",
        "url": f"{href}/Tournament_Results",
        "results": []
      }

      if len(thead) > 0:
        player["name"] = thead[0].text

      if len(table.find_all("tr")) > 2:
        for row in table.find_all("tr"):
          columns = row.find_all("td")
          if len(columns) < 3:
            continue

          player_data = {
            "date": clean_text(columns[0].text),
            "place": clean_text(columns[1].text),
            "tournament": clean_text(columns[2].text),
            "last_result": clean_text(columns[3].text),
            "team": clean_text(columns[4].text),
            "roster": clean_text(columns[5].text),
          }
          player["results"].append(player_data)

      players_results.append(player)
      return player
    except Exception as e:
      print(f"Error fetching player results: {e}")
      return None

try:
    while True:
        driver.get(url)
        time.sleep(5)
        links = driver.find_elements(By.CSS_SELECTOR, "div.page-content li a.to_hasTooltip")
        hrefs = [link.get_attribute("href") for link in links if link.get_attribute("href")]

        with ThreadPoolExecutor(max_workers=5) as executor:
          results = list(executor.map(fetch_player_results, hrefs))


        players_results.extend([player for player in results if player])

        try:
            driver.get(url)
            next_button = driver.find_element(By.XPATH, "//div[@id='mw-pages']//a[contains(@class, 'to_hasTooltip') and contains(text(), 'next page')]")
            next_url = next_button.get_attribute("href")
            url = next_url
            if len(players_results) > 1000:
                break
            if not next_button:
                break
        except Exception as e:
            print("Error: ", e)
            break

    with open("players_results.json", "w") as file:
        json.dump(players_results, file)
finally:
    driver.quit()
    end_time = time.time()
    print("Número de resultados: ", len(players_results))
    print(f"Tempo de execução: {end_time - start_time} segundos")
