from typing import Union
import time
import logging
import os
import concurrent.futures
import pandas as pd
import csv
import warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fuzzywuzzy import fuzz
from pprint import pprint
warnings.filterwarnings("ignore")

logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('selenium').setLevel(logging.ERROR)

PAGE_URL = "https://www.footballtransfers.com/us/values/players/most-valuable-soccer-players/playing-in-uk-premier-league/{page_idx}"
START_PAGE = 1
NUMBER_OF_PAGES = 22
MAX_WORKERS = 10
BATCH_SIZE = 2
FUZZY_THRESHOLD = 90
manual_name_mapping = {
    'Bobby Reid': 'Bobby De Cordova-Reid',
    'Felipe Morato': 'Morato',
    'Hee-chan Hwang': 'Hwang Hee-chan',
    'Heung-min Son': 'Son Heung-min',
    'Idrissa Gueye': 'Idrissa Gana Gueye',
    'Igor Júlio': 'Igor',  
    'J. Philogene': 'Jaden Philogene Bidace',  
    'Jérémy Doku': 'Jeremy Doku',
    'Manuel Ugarte': 'Manuel Ugarte Ribeiro',
    'Nathan Wood': 'Nathan Wood-Gordon', 
    'O. Hutchinson': 'Omari Hutchinson',
    'Rasmus Winther Højlund': 'Rasmus Højlund',
    'Victor Kristiansen': 'Victor Bernth Kristiansen'
}
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.page_load_strategy = 'eager'
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Chrome(options=chrome_options)

def extract_players_from_csv(input_csv='results.csv', output_csv='IV/result_final.csv'):
    df = pd.read_csv(input_csv) 
    df['Minutes'] = df['Minutes'].astype(str).str.replace(",", "").astype(float)
    df = df[df['Minutes'] >= 900]
    selected_columns = ['Player', 'Nation', 'Team', 'Position', 'Age']
    df_filtered = df[selected_columns].copy()
    df_filtered['Transfer Fee'] = None
    df_filtered.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"Saved {len(df_filtered)} eligible players to {output_csv}")
    return df_filtered

def is_name_match(crawled_name, existing_names):
    if not existing_names:
        return True  
    for existing_name in existing_names:
        mapped_name = manual_name_mapping.get(existing_name, existing_name)
        similarity = fuzz.ratio(crawled_name.lower(), mapped_name.lower())
        if similarity >= FUZZY_THRESHOLD:
            return True
    return False

def check_and_get_player_data(player_url: str, local_driver=None) -> Union[bool, dict]:
    if not local_driver:
        return False

    driver = local_driver
    try:
        driver.get(player_url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "playerInfoTop-bar"))
            )
        except:
            print(f"Timeout waiting for player profile page: {player_url}")
            return False

        soup = BeautifulSoup(driver.page_source, "html.parser")
        player_data = {
            "name": None,
            "value": None
        }

        try:
            name_element = soup.find("h1", class_="h1-medium")
            if name_element:
                player_data["name"] = name_element.text.strip()
        except:
            pass

        try:
            value_element = soup.find("div", class_="player-value-large")
            if value_element:
                value_tag = value_element.find("span", class_="player-tag")
                if value_tag:
                    player_data["value"] = value_tag.text.strip()
        except:
            pass

        return player_data if player_data["name"] else False

    except Exception as e:
        print(f"Error extracting player data from {player_url}: {str(e)}")
        return False

def process_player(player_url):
    local_driver = setup_driver()
    try:
        print(f'Processing player: {player_url}')
        result = check_and_get_player_data(player_url, local_driver)
        return result
    except Exception as e:
        print(f"Error processing player {player_url}: {str(e)}")
        return False
    finally:
        local_driver.quit()

def get_player_urls_from_page(page_idx):
    driver = setup_driver()
    player_urls = []
    try:
        url = PAGE_URL.format(page_idx=page_idx)
        print(f"Accessing page: {url}")
        driver.get(url)

        time.sleep(3)
        driver.execute_script("window.scrollBy(0, 500)")
        time.sleep(2)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "player-table-body"))
            )
        except:
            print(f"Timeout waiting for player table on page {page_idx}")
            return []

        soup = BeautifulSoup(driver.find_element(By.ID, "player-table-body").get_attribute("innerHTML"), "html.parser")
        player_elements = soup.find_all("tr")
        print(f"Found {len(player_elements)} players on page {page_idx}")

        for element in player_elements:
            try:
                div_text = element.find("div", class_="text")
                if div_text:
                    a_tag = div_text.find("a")
                    if a_tag and "href" in a_tag.attrs:
                        player_url = a_tag["href"]
                        player_urls.append(player_url)
                    else:
                        print("Anchor tag or href not found.")
                else:
                    print("Div with class 'text' not found.")
            except Exception as e:
                print(f"Error extracting player URL: {str(e)}")

        player_urls = list(set(player_urls))
        return player_urls

    except Exception as e:
        print(f"Error processing page {page_idx}: {str(e)}")
        return []
    finally:
        driver.quit()

update_count = 0 
def save_progress(player_data_list, filename='result_final.csv'):
    if len(player_data_list) == 0 or not os.path.exists(filename):
        return
    global update_count
    try:
        df = pd.read_csv(filename)
        for idx, row in df.iterrows():
            for player in player_data_list:  
                normalized_csv_name = manual_name_mapping.get(row["Player"], row["Player"])
                if (normalized_csv_name.lower() == player["name"].lower() or
                    fuzz.ratio(normalized_csv_name.lower(), player["name"].lower()) >= FUZZY_THRESHOLD):
                        if pd.isna(row["Transfer Fee"]) or row["Transfer Fee"] != player["value"]:
                            df.at[idx, "Transfer Fee"] = player["value"]
                            update_count += 1
                        break
            for player in player_data_list:
                if row["Player"].strip().lower() == player["name"].strip().lower():
                    if pd.isna(row["Transfer Fee"]) or row["Transfer Fee"] != player["value"]:
                        df.at[idx, "Transfer Fee"] = player["value"]
                        update_count += 1
                    break
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Total updated players: {update_count} in {filename}")

    except Exception as e:
        print(f"Error saving to CSV: {str(e)}")
def process_all_players():
    all_player_urls = []
    for page_idx in range(START_PAGE, START_PAGE + NUMBER_OF_PAGES):
        page_urls = get_player_urls_from_page(page_idx)
        all_player_urls.extend(page_urls)

    print(f"Total players to process: {len(all_player_urls)}")

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(process_player, url): url for url in all_player_urls}
            player_data_list = []

            for future in concurrent.futures.as_completed(futures):
                url = futures[future]
                try:
                    player_data = future.result()
                    if isinstance(player_data, dict):
                        player_data_list.append(player_data)
                except Exception as e:
                    print(f"Error processing {url}: {str(e)}")

            save_progress(player_data_list)

    except Exception as e:
        print(f"Error in main execution: {str(e)}")
        
def main():
    extract_players_from_csv('results.csv', 'result_final.csv')
    process_all_players()
if __name__ == "__main__":
    main()
