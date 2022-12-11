import pandas as pd


df_analytics = pd.read_csv('data/real_train.csv')
df_analytics = df_analytics.loc[(df_analytics['Статус'] == 'Завершена') | (df_analytics['Статус'] == 'Не состоялась')]
df_analytics.loc[df_analytics['Статус'] == 'Завершена', 'Статус'] = 1
df_analytics.loc[df_analytics['Статус'] == 'Не состоялась', 'Статус'] = 0
df_analytics['Падение цены'] = (df_analytics['НМЦК'] - df_analytics['Итоговая цена']) / df_analytics['НМЦК'] * 100 
df_analytics['month'] = df_analytics['Дата'] // 30

def get_stats_per_inn(inn: int) -> float:
    vec = df_analytics.loc[df_analytics['ИНН'] == inn, 'Статус']
    try:
        part_norm = vec.sum() / vec.size
    except ZeroDivisionError:
        return None
    return part_norm

def get_med_price_fall(kpgz, month):
    try:
        return df_analytics.loc[df_analytics['Код КПГЗ'] == kpgz].groupby('month')['Падение цены'].median()[month]
    except:
        return None

def get_med_partcpts(kpgz, month):
    try:
        return df_analytics.loc[df_analytics['Код КПГЗ'] == kpgz].groupby('month')['Участники'].median()[month]
    except:
        return None
    
