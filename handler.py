import math
import re

import catboost as cb
import pandas as pd
from nltk.corpus import stopwords
from six.moves import xrange

from utils import INN_INFO_PATH, KPGZ2OKPD, KPGZ_PATH, MODEL_PATH, OKPD_PATH, PARTICIPANTS_PATH, PERCENT_PATH, STAVKI_PATH


def parse_code(code: str) -> str:
    return str(code).split(';')[0]

def clean_stopwords(st:str, stopwords=stopwords.words('russian')) -> list:
    ns = ''
    for word in st.split():
        if word not in stopwords:
            ns += " " + word
    return ns

def set_time(time_tmp: str) -> int:
    _, m, d = time_tmp.split('-')
    d = d[:2]
    return int(m)*30 + int(d)

def process_data(data_frame: pd.DataFrame) -> pd.DataFrame:
    train = data_frame
    patt1 = re.compile(r'[A-Za-z0-9]')
    patt2 = re.compile(r'[!"#$%&\'()*+,-./:;<=>?@][\\^_`}{|~]')

    kpgz = pd.read_excel(KPGZ_PATH)
    okpd = pd.read_excel(OKPD_PATH, skiprows=6)

    kpgz2okpd = pd.read_csv(KPGZ2OKPD)
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
            'КПГЗ':'Код КПГЗ',
            'ИНН_хэш': 'ИНН'
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
    # inn_info = train.groupby('ИНН')[['Участники', 'Ставки', 'НМЦК']].agg(['std', 'count', 'median'])
    inn_info = pd.read_csv(INN_INFO_PATH)
    inn_info['ИНН'] = inn_info.index
    train = pd.merge(train, inn_info, on='ИНН', how='left')
    train['percent'] = train['НМЦК'] - train['Итоговая цена']
    train['percent'] = train['percent']/train['НМЦК']
    prepared_train = train.drop(["Итоговая цена","id", "ИНН", 'Описание КПГЗ'], axis=1)
    prepared_train = prepared_train.loc[(prepared_train['Статус'] == 'Завершена') | (prepared_train['Статус'] == 'Не состоялась')]
    prepared_train['Дата'] = prepared_train['Дата'].apply(set_time)
    prepared_train['is_normal'] = prepared_train['Статус'].apply(lambda x: 1 if x=='Завершена' else 0)
    prepared_train['Наименование КС'] = prepared_train['Наименование КС'].apply(str)
    prepared_train['Наименование классификации предметов государственного заказа (КПГЗ)'] = prepared_train['Наименование классификации предметов государственного заказа (КПГЗ)'].apply(str)

    return prepared_train

def get_prepared(data, is_train=False, task_type='bin'):
    X = data.drop(['percent', 'Участники', 'Ставки', "Статус", "is_normal"], axis=1)
    if is_train:
        if task_type == 'bin':
            return X, data['is_normal']
        elif task_type == 'stavki':
            return X, data['Ставки']
        elif task_type == 'percent':
            X['Ставки'] = data['Ставки']
            return X, data['percent']
        elif task_type == 'participants':
            X['Ставки'] = data['Ставки']
            X['percent'] = data['percent']
            return X, data['participants']
        else:
            return X, data[['percent', 'Участники', 'Ставки', "is_normal"]]
    else:
        return X

class Solution(object):
    def __init__(self) -> None:
        self.model_bin = self.get_bin_cat(MODEL_PATH)
        self.model_stavki, self.model_percent, self.model_participants = self.get_regressors()
    
    def get_bin_cat(self, path2bin_cat: str) -> object:
        params = {
                'loss_function':FocalLossObjective(),
                'eval_metric':"Logloss",
            }
        model_bin = cb.CatBoostClassifier(**params)
        model_bin.load_model(path2bin_cat)
        return model_bin

    def get_regressors(self) -> tuple[object, object, object]:
        params = {
                # 'learning_rate': 1, 
                'depth': 6, 
                'l2_leaf_reg': 3, 
                'loss_function': 'MAE', 
                'eval_metric': 'MAE', 
                'task_type': 'GPU', 
                'iterations': 1000,
                'od_type': 'Iter', 
                'boosting_type': 'Plain', 
                'bootstrap_type': 'Bernoulli', 
                'allow_const_label': True, 
            }
        model_stavki = cb.CatBoostRegressor(**params)
        model_percent = cb.CatBoostRegressor(**params)
        model_participants = cb.CatBoostRegressor(**params)
        model_stavki.load_model(STAVKI_PATH)
        model_percent.load_model(PERCENT_PATH)
        model_participants.load_model(PARTICIPANTS_PATH)
        return model_stavki, model_percent, model_participants

    def get_pool(self, X: pd.DataFrame) -> cb.Pool:
        pool = cb.Pool(
            data=X,
            cat_features=['Код КПГЗ', 'Код ОКПД2', 'Регион'],
            text_features=['Наименование КС', 'Наименование классификации предметов государственного заказа (КПГЗ)']
        )
        return pool

    def process(self, data_processed: pd.DataFrame) -> pd.DataFrame:
        pool1 = self.get_pool(data_processed)
        preds_stavki = self.model_stavki(pool1)
        data_processed['Ставки'] = preds_stavki
        pool2 = self.get_pool(data_processed)
        preds_procent = self.model_percent(pool2)
        data_processed['Уровень снижения'] = preds_procent
        pool3 = self.get_pool(data_processed)
        preds_participants = self.model_percent(pool3)
        data_processed['Участники'] = preds_participants
        return data_processed

        
        

class FocalLossObjective(object):
    def calc_ders_range(self, approxes, targets, weights):
        gamma = 2.
        # alpha = 1.
        assert len(approxes) == len(targets)
        if weights is not None:
            assert len(weights) == len(approxes)
        
        exponents = []
        for index in xrange(len(approxes)):
            exponents.append(math.exp(approxes[index]))

        result = []
        for index in xrange(len(targets)):
            p = exponents[index] / (1 + exponents[index])

            if targets[index] > 0.0:
                der1 = -((1-p)**(gamma-1))*(gamma * math.log(p) * p + p - 1)/p
                der2 = gamma*((1-p)**gamma)*((gamma*p-1)*math.log(p)+2*(p-1))
            else:
                der1 = (p**(gamma-1)) * (gamma * math.log(1 - p) - p)/(1 - p)
                der2 = p**(gamma-2)*((p*(2*gamma*(p-1)-p))/(p-1)**2 + (gamma-1)*gamma*math.log(1 - p))

            if weights is not None:
                der1 *= weights[index]
                der2 *= weights[index]

            result.append((der1, der2))

        return result
