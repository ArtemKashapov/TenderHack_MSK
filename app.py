from time import perf_counter

import pandas as pd
import streamlit as st

from handler import Solution, process_data
from utils import PAGE_ICON, PAGE_TITLE, data_styler, df2data, data2download


st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, initial_sidebar_state="collapsed")

file = st.file_uploader("Загрузите входные данные:", type={'csv', 'txt', 'xlsx'})
sol = Solution()

if file:
    tic = perf_counter()
    df = pd.read_excel(file)
    df = df.rename(columns={'id':'Unnamed: 0', 'ИНН': 'ИНН_хэш'})
    output_data = sol.process(data_processed=process_data(data_frame=df))
    toc = perf_counter()
    st.write(f'Время расчета предсказанй составило {(toc - tic):.2f} сек.')
    st.download_button(
        label="Скачать таблицу",
        data=df2data(data2download(output_data, in_data=df)),
        file_name='output_data.csv',
        mime='text/csv',
    )
    
    st.write(data_styler(output_data.iloc[:3000, :], in_data=df).to_html(escape=False, index=False), unsafe_allow_html=True)
