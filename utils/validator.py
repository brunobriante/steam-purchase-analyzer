import streamlit as st

from utils.parser import get_soup

HEADER_VALUES = [
    # "消费历史记录",  # Simplified Chinese
    # "購買記錄",  # Traditional Chinese
    # "購入履歴",  # Japanese
    # "구매 기록",  # Korean
    # "ประวัติการสั่งซื้อ",  # Thai
    # "История на покупките",  # Bulgarian
    # "Historie nákupů",  # Czech
    # "Købshistorik",  # Danish
    # "Einkaufsverlauf",  # German
    "Purchase History",  # English
    # "Historial de compras",  # Spanish
    # "Ιστορικό αγορών",  # Greek
    # "Historique des achats",  # French
    # "Cronologia degli acquisti",  # Italian
    # "Riwayat Pembelian",  # Indonesian
    # "Vásárláselőzmény",  # Hungarian
    # "Aankoopgeschiedenis",  # Dutch
    # "Kjøpshistorikk",  # Norwegian
    # "Historia zakupów",  # Polish
    "Histórico de compras",  # Portuguese
    # "Istoricul achizițiilor",  # Romanian
    # "История покупок",  # Russian
    # "Ostotapahtumat",  # Finnish
    # "Köphistorik",  # Swedish
    # "Satın Alım Geçmişi",  # Turkish
    # "Lịch sử mua bán",  # Vietnamese
    # "Історія придбань",  # Ukrainian
]


def validate_history_file():
    soup = get_soup(st.session_state.history_file)
    try:
        breadcrumb = soup.find("span", "breadcrumb_current_page")
    except BaseException:
        st.session_state.valid_history = False
        return

    if breadcrumb is not None and breadcrumb.text in HEADER_VALUES:
        st.session_state.valid_history = True
        return

    st.session_state.valid_history = False
    return
