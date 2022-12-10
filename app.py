import pandas as pd
import streamlit as st

from handler import Solution, process_data
from utils import PAGE_ICON, PAGE_TITLE, df2data, highlight_style


st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

file = st.file_uploader("Загрузите входные данные:", type={'csv', 'txt', 'xlsx'})
sol = Solution()

if file:
    # print(file)
    df = pd.read_excel(file)
    output_data = sol.process(data=process_data(data_frame=df))

    st.dataframe(output_data.style.applymap(highlight_style, subset=['Уровень снижения', 'Участники']))
    
    st.download_button(
        label="Скачать таблицу",
        data=df2data(df),
        file_name='output_data.csv',
        mime='text/csv',
    )