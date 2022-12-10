import math
from six.moves import xrange


class FocalLossObjective(object):
    def calc_ders_range(self, approxes, targets, weights):
        # approxes, targets, weights are indexed containers of floats
        # (containers with only __len__ and __getitem__ defined).
        # weights parameter can be None.
        # Returns list of pairs (der1, der2)
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
def get_bin_cat(path2bin_cat):
  params = {
    'loss_function':FocalLossObjective(),
    'eval_metric':"Logloss",
}
  model_bin = cb.CatBoostClassifier(**params)
  model_bin.load_model(path2bin_cat)
  return model_bin
def get_regressors(paths):
  path2stavki, path2percent, path2participants = paths
  params = {
#     'learning_rate': 1, 
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
  model_stavki.load_model(path2stavki)
  model_percent.load_model(path2percent)
  model_participants.load_model(path2participants)
  return model_stavki, model_percent, model_participants
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
  else: return X
