import streamlit as st
import pandas as pd


HIGHLIGHT_COLOR = 'green'
PAGE_TITLE = 'Samurai'
PAGE_ICON = '📈'

def highlight_style(_: object) -> str:
    return f'background-color: {HIGHLIGHT_COLOR}'

@st.cache
def df2data(df: pd.DataFrame) -> bytes:
    return df.to_csv().encode('utf-8')