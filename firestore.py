import streamlit as st
from google.cloud import firestore

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from streamlit_autorefresh import st_autorefresh

db = firestore.Client.from_service_account_json("firestore-key.json")


doc_ref = db.collection("players")


st_autorefresh(interval=60*60*1000, key='scrapper')

def create_teams_df(param):
    url = "https://sflendas.lgleite.com/index.php?page=html/rosters/roster{}.htm".format(param)
    

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-features=VizDisplayCompositor")    
    wd = webdriver.Chrome(ChromeDriverManager().install(), options=options)


    wd.get(url)    
    team_name = wd.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table/tbody/tr[1]/td/table[1]/tbody/tr[1]/td/table[1]/tbody/tr[1]/td/table[1]/tbody/tr[1]/td/table[1]/tbody/tr[1]/td/p/b/font').text
    stats = wd.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table/tbody/tr[1]/td/table[1]/tbody/tr[5]/td/table/tbody')

    roster = stats.find_elements(By.TAG_NAME, 'tr')
    roster_size = len(roster)

    i = 3
    while i <= roster_size:
        player = wd.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table/tbody/tr[1]/td/table[1]/tbody/tr[5]/td/table/tbody/tr[{}]/td[2]/font/a'.format(i)).text        
        j = 2 
        stats_list = []   
        while j <= 14:
            player_stats = wd.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table/tbody/tr[1]/td/table[1]/tbody/tr[5]/td/table/tbody/tr[{}]/td[{}]/font'.format(i, j)).text
            
            j += 1
            stats_list.append(player_stats)
            
        i += 1
        player = {
            'Name':stats_list[0],
            'Position':stats_list[1],
            'Games':stats_list[2],
            'MPG':stats_list[3],
            'PPG':stats_list[4],
            'RPG':stats_list[5],
            'APG':stats_list[6],
            'SPG':stats_list[7],
            'BPG':stats_list[8],
            'TPG':stats_list[9],
            'FG%':stats_list[10],
            'FT%':stats_list[11],
            '3P%':stats_list[12],
            'Team': team_name
        }
        doc_ref.document(f'{stats_list[0]}').set(player)
        
    
    
    
    print(team_name)

i = 1
while i != 30  :
    create_teams_df(i)
    i += 1