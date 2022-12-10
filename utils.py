import pandas as pd
import streamlit as st


HIGHLIGHT_COLOR = 'green'
PAGE_TITLE = 'Samurai'
PAGE_ICON = '📈'

# paths
OKPD_PATH = 'data\okpd.xlsx'
KPGZ_PATH = 'data\kpgz.xls'
KPGZ2OKPD = 'data\kpgz_to_orpd.csv'
MODEL_PATH = 'data\model_bin.cb'
STAVKI_PATH = 'data\model_stavki.cb'
PERCENT_PATH = 'data\model_percent.cb'
PARTICIPANTS_PATH = 'data\model_participants.cb'
INN_INFO_PATH = 'data\inn_info.csv'

def highlight_style(_: object) -> str:
    return f'background-color: {HIGHLIGHT_COLOR}'

@st.cache
def df2data(df: pd.DataFrame) -> bytes:
    return df.to_csv().encode('utf-8')