from create_team_stats import create_teams_df
import streamlit as st




@st.cache(show_spinner=False)
def create_teams_list():
    i = 1
    list_of_teams = []
    
    
    while i < 30:
        #st.write("Starting team: " + str(i))
        list_of_teams.append(create_teams_df(i))
        print("Finish team: " + str(i))
        i += 1
        

    return list_of_teams