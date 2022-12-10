import pandas as pd
import streamlit as st

from handler import Solution, process_data
from utils import PAGE_ICON, PAGE_TITLE, df2data, data_styler
from time import perf_counter

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

file = st.file_uploader("Загрузите входные данные:", type={'csv', 'txt', 'xlsx'})
sol = Solution()

if file:
    tic = perf_counter()
    df = pd.read_excel(file)
    output_data = sol.process(data_processed=process_data(data_frame=df))
    toc = perf_counter()
    print(f'Calculation time is {toc - tic} sec.')
    
    tic = perf_counter()
    st.dataframe(data_styler(output_data))
    toc = perf_counter()
    print(f'Print time is {toc - tic} sec.')

    st.download_button(
        label="Скачать таблицу",
        data=df2data(df),
        file_name='output_data.csv',
        mime='text/csv',
    )