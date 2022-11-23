from google.cloud import firestore
from google.oauth2 import service_account
import pandas as pd
import streamlit as st
import numpy as np
import json




#db = firestore.Client.from_service_account_json("firestore-key.json")


@st.experimental_memo
def create_df():
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds)
    teams = db.collection("teams")
    df = pd.DataFrame()
    dfs = []
    for team in teams.stream():
        df_team = pd.DataFrame()
        doc2 = team.to_dict()   
        team_name = doc2['name']    
        players = db.collection('teams').document(f"{team_name}").collection('players').stream()
        

        players_dict = list(map(lambda x: x.to_dict(), players))
        df_team = pd.DataFrame.from_dict(players_dict)
        df_team = df_team.assign(Team=team_name)
        dfs.append(df_team)

    print('Enter')
    return dfs