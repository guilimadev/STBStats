from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

import streamlit as st


@st.cache(show_spinner=False)
def create_teams_df(param):
    url = "https://sflendas.lgleite.com/index.php?page=html/rosters/roster{}.htm".format(param)
    teste = 2

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
    table = wd.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table/tbody/tr[1]/td/table[1]/tbody/tr[5]/td/table/tbody')
    team_names = wd.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table/tbody/tr[1]/td/table[1]/tbody/tr[1]/td/table[1]/tbody/tr[1]/td/table[1]/tbody/tr[1]/td/table[1]/tbody/tr[1]/td/p/b/font').text
    headers = table.find_elements(By.TAG_NAME, 'u')
    
    print(team_names)
    roster = table.find_elements(By.TAG_NAME, 'tr')
    roster_size = len(roster)

    stats_names = []

    for header in headers:
        stats_names.append(header.text)
        



    df_players = pd.DataFrame(columns=stats_names)
    df_players = df_players.drop(['Player Statistics', 'ID'], axis=1)


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
    
        df_players.loc[len(df_players)] = stats_list

    df_players = df_players.replace('.', ',')
    df_players = df_players.astype({'MPG': 'float', 'APG': 'float', 'SPG': 'float', 'RPG': 'float', 'BPG': 'float', 'TPG': 'float', 'PPG': 'float'})
    
    df_players = df_players.assign(Team=team_names)
    return df_players
    

