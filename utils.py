import pandas as pd
import streamlit as st


HIGHLIGHT_COLOR_ROW = 'red'
HIGHLIGHT_COLOR_COl = 'green'
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

def highlight_style(x: object, mask: pd.Series) -> str:
    len_x = len(x)
    if mask[x['index']] == 0:
        style_vec = [f'background-color: {HIGHLIGHT_COLOR_ROW}'] * len_x
    else:
        style_vec = [''] * len_x
        style_vec[3] = f'background-color: {HIGHLIGHT_COLOR_COl}'
        style_vec[4] = f'background-color: {HIGHLIGHT_COLOR_COl}'
    return style_vec

def data_styler(data: pd.DataFrame) -> pd.DataFrame:
    is_normal_col = data['is_normal']
    data = data[['Наименование КС', 'Регион', 'Уровень снижения, %', 'Участники']].reset_index()
    data['Уровень снижения, %'] = data['Уровень снижения, %'] * 100
    return data.style.apply(highlight_style, mask=is_normal_col, axis=1)

@st.cache
def df2data(df: pd.DataFrame) -> bytes:
    return df.to_csv().encode('utf-8')