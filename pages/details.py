import streamlit as st

from data_analytics import get_stats_per_inn


st.set_page_config(initial_sidebar_state="collapsed")

params = st.experimental_get_query_params()
if params:
    st.title(f'Аналитика по сессии ID={params["ID"][0]}')
    st.experimental_set_query_params()

    hist_stat = get_stats_per_inn(params['INN'][0])
    if hist_stat:
        st.write(f'Закачик с переданным ИНН имеет {hist_stat*100:.2f} % завершенных сессий.')
    else:
        st.write('Статистика по переданному ИНН не доступна.')

