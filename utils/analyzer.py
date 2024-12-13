import streamlit as st

from utils.parser import get_dataframe


def analyze_history():
    return get_dataframe(st.session_state.history_file)
