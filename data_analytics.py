import pandas as pd


df_analytics = pd.read_excel('data\TenderHack_Москва_train_data.xlsx')
df_analytics = df_analytics.loc[(df_analytics['Статус'] == 'Завершена') | (df_analytics['Статус'] == 'Не состоялась')]
df_analytics.loc[df_analytics['Статус'] == 'Завершена', 'Статус'] = 1
df_analytics.loc[df_analytics['Статус'] == 'Не состоялась', 'Статус'] = 0

def get_stats_per_inn(inn: int) -> float:
    vec = df_analytics.loc[df_analytics['ИНН'] == inn, 'Статус']
    try:
        part_norm = vec.sum() / vec.size
    except ZeroDivisionError:
        return None
    return part_norm