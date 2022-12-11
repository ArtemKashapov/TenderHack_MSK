# from time import perf_counter

# import pandas as pd
# import streamlit as st

# from handler import Solution, process_data, set_time
# from utils import PAGE_ICON, PAGE_TITLE, data_styler, df2data, data2download

# from utils import (INN_INFO_PATH, KPGZ2OKPD, KPGZ_PATH, MODEL_PATH, OKPD_PATH,
#                    PARTICIPANTS_PATH, PERCENT_PATH, STAVKI_PATH)

# st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, initial_sidebar_state="collapsed")

# file = st.file_uploader("Загрузите входные данные:", type={'csv', 'txt', 'xlsx'})
# sol = Solution()

# if file:
#     tic = perf_counter()
#     df = pd.read_csv(file)
#     # df = df.rename(columns={'id':'Unnamed: 0', 'ИНН': 'ИНН_хэш'})
#     df = df.rename(columns={'ИНН': 'ИНН_хэш'})
#     df.iloc[:, 1] = df.iloc[:, 1].astype(str)
#     df.iloc[:, 2] = df.iloc[:, 2].astype(str)
#     # df.iloc[:, 3] = df.iloc[:, 3].astype(str)
#     df.iloc[:, 6] = df.iloc[:, 6].apply(set_time)

#     # inn_info = pd.read_csv(INN_INFO_PATH)
#     # output_data = sol.process(data_processed=process_data(data_frame=df))
#     # train = pd.merge(df, inn_info, on='ИНН', how='left')
#     # train = train.drop('ИНН', axis=1)
#     df.iloc[:, 7] = df.iloc[:, 7].astype(str)
#     # train.iloc[:, 8] = train.iloc[:, 8].astype(str)
#     df = df.drop('Описание КПГЗ', axis=1)
    
#     output_data = sol.process(data_processed=df)
#     toc = perf_counter()
#     st.write(f'Время расчета предсказанй составило {(toc - tic):.2f} сек.')
#     st.download_button(
#         label="Скачать таблицу",
#         data=df2data(data2download(output_data, in_data=df)),
#         file_name='output_data.csv',
#         mime='text/csv',
#     )
    
#     st.write(data_styler(output_data.iloc[:1000, :], in_data=df).to_html(escape=False, index=False), unsafe_allow_html=True)

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
