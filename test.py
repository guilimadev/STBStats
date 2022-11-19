from pathlib import Path
from threading import Thread
from streamlit.scriptrunner import add_script_run_ctx

import streamlit as st

def target():
    st.text("s")

if __name__ == '__main__':
    if not st.session_state.get("thread"):
        st.session_state["thread"] = True
        t = Thread(target=target)        
        add_script_run_ctx(t)
        t.start()