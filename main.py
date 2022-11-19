from create_teams_list import create_teams_list

import pandas as pd
import streamlit as st
import numpy as np

st.set_page_config(page_title='STB Stats', page_icon=':basketball:', layout='wide')
teams = create_teams_list()


st.title("STB Stats by " + ':bear:')

all_players, per_48, per_team = st.tabs(["Todos jogadores","Por 48 minutos", "Por time" ])

df_all_players = pd.concat(teams)
df_all_players = df_all_players.astype({'Games': 'int'})
df_all_players.index = [''] * len(df_all_players)
df_all_players = df_all_players.fillna(0)




with all_players:
    col1, col2 = st.columns(2)
    with col1:
        mpg_slider = st.slider('MPG:', 0.0, 48.0, 48.0)
    with col2:
        games_slider = st.slider('Min Games:', 0, 82, 0)
    st.dataframe(df_all_players[(df_all_players['MPG'] <= mpg_slider) & (df_all_players['Games'] >= games_slider)].style.format(subset=['MPG','APG', 'SPG', 'RPG', 'BPG', 'TPG', 'PPG'], formatter="{:.1f}"))


with per_team:
    selecionar_time = st.selectbox(options=df_all_players.Team.unique(), label="Selecione seu time: ")
    if selecionar_time:      
        st.dataframe(df_all_players[(df_all_players['Team'] == selecionar_time)].style.format(subset=['MPG','APG', 'SPG', 'RPG', 'BPG', 'TPG', 'PPG'], formatter="{:.1f}")) 

with per_48:
    df_per48 = df_all_players
    df_per48['APG'] = df_per48['APG'] * 48 / df_per48['MPG']
    df_per48['PPG'] = df_per48['PPG'] * 48 / df_per48['MPG']
    df_per48['TPG'] = df_per48['TPG'] * 48 / df_per48['MPG']
    df_per48['BPG'] = df_per48['BPG'] * 48 / df_per48['MPG']
    df_per48['SPG'] = df_per48['SPG'] * 48 / df_per48['MPG']
    df_per48['RPG'] = df_per48['RPG'] * 48 / df_per48['MPG']
    df_per48 = df_per48.fillna(0)
    list_of_teams = np.empty(1)
    list_of_teams = np.append(list_of_teams,"Todos")
    list_of_teams = np.delete(list_of_teams, 0)
    list_of_teams = np.append(list_of_teams,df_all_players.Team.unique()) 
    
    col1, col2, col3 = st.columns(3)
    with col1:
        mpg_slider_48 = st.slider('MPG:', 0.0, 48.0, 48.0, key=2)
    with col2:
        games_slider_48 = st.slider('Min Games:', 0, 82, 0, key=3)
    with col3:
        selecionar_time_48 = st.selectbox(options=list_of_teams, label="Selecione seu time: ", key=4)

    if selecionar_time_48 == "Todos":
        st.dataframe(df_per48[(df_per48['MPG'] <= mpg_slider_48) & (df_per48['Games'] >= games_slider_48)].style.format(subset=['MPG','APG', 'SPG', 'RPG', 'BPG', 'TPG', 'PPG'], formatter="{:.1f}"))
    else:
        st.dataframe(df_per48[(df_per48['MPG'] <= mpg_slider_48) & (df_per48['Games'] >= games_slider_48) & (df_per48['Team'] == selecionar_time_48)].style.format(subset=['MPG','APG', 'SPG', 'RPG', 'BPG', 'TPG', 'PPG'], formatter="{:.1f}"))    

   
