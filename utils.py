import pandas as pd
import streamlit as st


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
    # print(x.info())
    if mask[x.name] == 0:
        style_vec = [f'background-color: red'] * len_x
    else:
        style_vec = [''] * len_x
        style_vec[-2] = 'background-color: green'
        style_vec[-1] = 'background-color: green'
    return style_vec

def data_styler(data: pd.DataFrame, in_data: pd.DataFrame) -> pd.DataFrame:
    is_normal_col = data['is_normal']
    data = data[['Наименование КС', 'Ставки', 'Уровень снижения, %', 'Участники']]
    data.insert(loc=0, column='ID', value=in_data['Unnamed: 0'])
    data.insert(loc=1, column='Обзор', value=in_data['Unnamed: 0'])
    data['Участники'] = data['Участники'].apply(round)
    data['Обзор'] = in_data.apply(lambda x: f'<a target="_blank" href="http://localhost:8501/details?ID={x["Unnamed: 0"]}&INN={x["ИНН_хэш"]}&M={x["Дата"].split("-")[1]}&KPGZ={x["КПГЗ"]}">Посмотреть</a>', axis=1)
    data['Уровень снижения, %'] = data['Уровень снижения, %'] * 100
    return data.style.apply(highlight_style, mask=is_normal_col, axis=1)

def data2download(data: pd.DataFrame, in_data: pd.DataFrame) -> pd.DataFrame:
    data = data[['Наименование КС', 'Ставки', 'Уровень снижения, %', 'Участники']]
    data.insert(loc=0, column='ID', value=in_data['Unnamed: 0'])
    data.insert(loc=1, column='Обзор', value=in_data['Unnamed: 0'])
    return data

@st.cache
def df2data(df: pd.DataFrame) -> bytes:
    return df.to_csv().encode('utf-8')