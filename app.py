import streamlit as st

from utils.analyzer import analyze_history
from utils.validator import validate_history_file

st.markdown(
    """
<style>
    [data-testid="stFileUploaderDropzone"] {
        background: #344654;
        border-radius: 0;
    }

    [data-testid="stFileUploaderDropzone"]:focus-visible {
        box-shadow: transparent 0px 0px;
    }

    [data-testid="stBaseButton-secondary"] {
        border: 0;
        border-radius: 2px;
        background-image: radial-gradient(circle at top left, #A3CF06 0%, #6A8704 120%);
        transition: box-shadow .2s ease-out;
        box-shadow: 2px 2px 5px rgba(0,0,0,.2);
        color: #DFE3E6;
    }

    [data-testid="stBaseButton-secondary"]:hover {
        background-image: radial-gradient(circle at top left, #A3CF06 0%, #6A8704 120%);
        color: #FFFFFF;
        box-shadow: 2px 2px 15px rgba(0,0,0,.5);
    }

    [data-testid="stBaseButton-secondary"]:focus:not(:active),
    [data-testid="stBaseButton-secondary"]:focus-visible {
        color: #FFFFFF;
        box-shadow: 2px 2px 15px rgba(0,0,0,.5);
    }

</style>
""",
    unsafe_allow_html=True,
)

if "valid_history" not in st.session_state:
    st.session_state["valid_history"] = False


uploader_block = st.empty()
analysis_block = st.empty()

with uploader_block.container():
    st.title("Steam Purchase Analyzer")
    history_uploader = st.file_uploader(
        label="History HTML File",
        label_visibility="hidden",
        type=["htm", "html"],
        accept_multiple_files=False,
        key="history_file",
        on_change=validate_history_file,
    )
    if st.session_state.history_file is not None and not st.session_state.valid_history:
        st.toast(body="Invalid HTML file", icon=":material/error:")

    st.markdown("""
    ## How To
    1. Go to https://store.steampowered.com/account/history/
    2. Scroll to the bottom of the page
    3. Click on **LOAD MORE TRANSACTIONS** button
    4. Repeat 2 and 3 until the button don't show on the bottom of the page
    5. Save that page as a HTML file
    6. Upload it here to be analyzed
    """)

    if st.session_state.history_file is not None and st.session_state.valid_history:
        uploader_block.empty()
        with analysis_block.container():
            st.write(analyze_history())
