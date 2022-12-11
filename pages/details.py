import streamlit as st

from data_analytics import (get_med_partcpts, get_med_price_fall,
                            get_stats_per_inn)

st.set_page_config(initial_sidebar_state="collapsed")

params = st.experimental_get_query_params()
if params:
    # st.write(params)
    st.title(f'Аналитика по сессии ID={params["ID"][0]}')
    st.experimental_set_query_params()

    hist_stat_inn = get_stats_per_inn(params['INN'][0])
    hist_stat_part = get_med_partcpts(params['KPGZ'][0], int(params['M'][0]))
    hist_stat_price = get_med_price_fall(params['KPGZ'][0], int(params['M'][0]))
    if hist_stat_inn:
        st.write(f'Закачик с переданным ИНН имеет {hist_stat_inn*100:.2f} % завершенных сессий.')
    else:
        st.write('Статистика по переданному ИНН не доступна.')

    if hist_stat_part:
        st.write(f'КС при переданном КПГЗ и сезоне в среднем имеет {hist_stat_part:.1f} участников.')
    else:
        st.write('Статистика числа участников по переданному КПГЗ и сезону не доступна.')

    if hist_stat_price:
        st.write(f'КС при переданном КПГЗ и сезоне в среднем имеет {hist_stat_price:.2f} % падение цены.')
    else:
        st.write('Статистика падения цены по переданному КПГЗ и сезону не доступна.')

