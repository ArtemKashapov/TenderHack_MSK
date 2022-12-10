import streamlit as st
import pandas as pd
from utils import highlight_style, df2data, PAGE_TITLE, PAGE_ICON
from handler import process_data, Solution


st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

file = st.file_uploader("Загрузите входные данные:", type={"csv", "txt"})
sol = Solution()

if file:
    df = pd.read_csv(file)
    df_transformed = process_data(data_frame=df)
    output_data = sol.process(data=df_transformed)

    st.dataframe(output_data.style.applymap(highlight_style, subset=['Итоговая цена', 'Участники']))
    
    st.download_button(
        label="Скачать таблицу",
        data=df2data(df),
        file_name='output_data.csv',
        mime='text/csv',
    )