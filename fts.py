import re
from nltk.corpus import stopwords
import pandas as pd


# def parse_code(code):
#     return str(code).split(';')[0]

# def clean_stopwords(st, stopwords=stopwords.words('russian')):
#     ns = ''
#     for word in st.split():
#         if word not in stopwords:
#             ns += " " + word
#     return ns

# def set_time(time_tmp):
#     _, m, d = time_tmp.split('-')
#     d = d[:2]
#     return int(m)*30 + int(d)

def get_fts4train(paths):
    patt1 = re.compile(r'[A-Za-z0-9]')
    patt2 = re.compile(r'[!"#$%&\'()*+,-./:;<=>?@][\\^_`}{|~]')
    path2kpgz, path2train, path2okpd, path2kpgz2okpd = paths
    kpgz = pd.read_excel(path2kpgz)
    train = pd.read_excel(path2train)
    okpd = pd.read_excel(path2okpd, skiprows=6)
    kpgz2okpd = pd.read_csv(path2kpgz2okpd)
    temp_kpgz = kpgz[['Код КПГЗ', 'Наименование классификации предметов государственного заказа (КПГЗ)', "Описание КПГЗ"]]
    kpgz2okpd = kpgz2okpd.rename(columns=
        {
            'Код ОКПД-2 (ОКПД2014)':"Код ОКПД2"
        }
    )

    kpgz2okpd = kpgz2okpd[['Код КПГЗ', "Код ОКПД2"]]
    okpd = okpd.rename(columns=
        {
            'Код':'Код ОКПД2'
        }
    )

    train = train.rename(columns=
        {
            'ОКПД 2':'Код ОКПД2',
            "КПГЗ":"Код КПГЗ"
        }
    )
    
    train['Код ОКПД2'] = train['Код ОКПД2'].apply(parse_code)
    train['Код КПГЗ'] = train['Код КПГЗ'].apply(parse_code)
    train = pd.merge(train, kpgz2okpd, on='Код КПГЗ', how='left')
    train['temp'] = train['Код ОКПД2_x'].apply(str) + ';' + train['Код ОКПД2_y'].apply(str)
    train['ОКПД2'] = train['temp'].apply(lambda x: x.split(';')[0] if x.split(';')[0] !='nan' and len(x.split(';')) > 1 else x.split(';')[1])
    train = train.drop('Код ОКПД2_x' , axis=1)
    train = train.drop('Код ОКПД2_y' , axis=1)
    train = train.drop('temp', axis=1)
    train['Наименование КС'] = train['Наименование КС'].apply(lambda x: patt1.sub('', x.lower())).apply(lambda x: patt2.sub('', x)).apply(clean_stopwords)
    train = pd.merge(train, temp_kpgz, on='Код КПГЗ', how='left')
    inn_info = pd.read_csv('./data/inn_info.csv')
    train = pd.merge(train, inn_info, on='ИНН', how='left')
    prepared_train = train.drop(["ИНН", 'Описание КПГЗ'], axis=1)
    prepared_train['Дата'] = prepared_train['Дата'].apply(set_time)
    prepared_train['Наименование КС'] = prepared_train['Наименование КС'].apply(str)
    prepared_train['Наименование классификации предметов государственного заказа (КПГЗ)'] = prepared_train['Наименование классификации предметов государственного заказа (КПГЗ)'].apply(str)
    return prepared_train
