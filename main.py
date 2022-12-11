from google.cloud import firestore
from google.oauth2 import service_account
import pandas as pd
import streamlit as st
import numpy as np
import json
from streamlit_autorefresh import st_autorefresh
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

st.set_page_config(page_title='STB Stats', page_icon=':basketball:', layout='wide')


import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)


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

st_autorefresh(interval=60*60*1000, key='dfbuilderrefresh')
def create_df():
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds)

    players = db.collection("players").stream()  
    players_dict = list(map(lambda x: x.to_dict(), players)) 
    dfs = []
    
    df_players = pd.DataFrame()            

   
    df_players = pd.DataFrame.from_dict(players_dict)
    
    
    print(df_players)
    print('Enter')
    now = datetime.now()
    print(now)
    return df_players

dfs = create_df()
 

st.title("STB Stats by " + ':bear:')

all_players, per_team = st.tabs(["Todos jogadores", "Por time" ])

df_all_players = dfs.copy()
df_all_players = df_all_players[['Name', 'Position', 'Games','MPG', 'PPG', 'RPG', 'APG', 'SPG', 'BPG', 'TPG', 'FG%', 'FT%', '3P%', 'Team']]
df_all_players = df_all_players.astype({'Games': 'int'})
df_all_players = df_all_players.replace('.', ',')
df_all_players = df_all_players.astype({'MPG': 'float', 'APG': 'float', 'SPG': 'float', 'RPG': 'float', 'BPG': 'float', 'TPG': 'float', 'PPG': 'float'})
df_all_players.index = [''] * len(df_all_players)
df_all_players = df_all_players.fillna(0)


df_per48 = df_all_players.copy()
df_per48['APG'] = df_per48['APG'] * 48 / df_per48['MPG']
df_per48['PPG'] = df_per48['PPG'] * 48 / df_per48['MPG']
df_per48['TPG'] = df_per48['TPG'] * 48 / df_per48['MPG']
df_per48['BPG'] = df_per48['BPG'] * 48 / df_per48['MPG']
df_per48['SPG'] = df_per48['SPG'] * 48 / df_per48['MPG']
df_per48['RPG'] = df_per48['RPG'] * 48 / df_per48['MPG']
df_per48 = df_per48.fillna(0)

with all_players:
    col1, col2 = st.columns(2)
    with col1:
        mpg_slider = st.slider('MPG:', 0.0, 48.0, (0.0,48.0))       
    with col2:
        games_slider = st.slider('Min Games:', 0, 82, 0)        

    with col1:
        st.header("Stats:")  
        st.dataframe(df_all_players[(df_all_players['MPG'] <= mpg_slider[1]) & (df_all_players['MPG'] >= mpg_slider[0]) & (df_all_players['Games'] >= games_slider)].style.format(subset=['MPG','APG', 'SPG', 'RPG', 'BPG', 'TPG', 'PPG'], formatter="{:.1f}"))
    with col2:
        st.header("Stats por 48 minutos:")
        st.dataframe(df_per48[(df_per48['MPG'] <= mpg_slider[1]) & (df_per48['MPG'] >= mpg_slider[0]) & (df_per48['Games'] >= games_slider)].style.format(subset=['MPG','APG', 'SPG', 'RPG', 'BPG', 'TPG', 'PPG'], formatter="{:.1f}"))
    

with per_team:
    selecionar_time = st.selectbox(options=df_all_players.Team.unique(), label="Selecione seu time: ")
    col1, col2 = st.columns(2)    
    if selecionar_time:
        with col1:
            st.header("Stats:")      
            st.dataframe(df_all_players[(df_all_players['Team'] == selecionar_time)].style.format(subset=['MPG','APG', 'SPG', 'RPG', 'BPG', 'TPG', 'PPG'], formatter="{:.1f}")) 
        with col2:
            st.header("Stats por 48 minutos:")
            st.dataframe(df_per48[(df_per48['Team'] == selecionar_time)].style.format(subset=['MPG','APG', 'SPG', 'RPG', 'BPG', 'TPG', 'PPG'], formatter="{:.1f}")) 

    
   
