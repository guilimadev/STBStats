from google.cloud import firestore
from google.oauth2 import service_account
import pandas as pd
import streamlit as st
import numpy as np
import json
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

st.set_page_config(page_title='STB Stats', page_icon=':basketball:', layout='wide')


#db = firestore.Client.from_service_account_json("firestore-key.json")

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

    
   
