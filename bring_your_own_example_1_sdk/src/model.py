import pandas as pd
import numpy as np
import os
from pathlib import Path
import pickle

from gluonts.model.simple_feedforward import SimpleFeedForwardEstimator
from gluonts.trainer import Trainer
#from gluonts.evaluation import Evaluator
#from gluonts.evaluation.backtest import backtest_metrics

import utils as ut

def train_input_fn(train_file_path):

    with open(train_file_path, 'rb') as file:
        response = pickle.load(file)

    return response
    
    
def compute_error(res):

    # This function is necessary for the hyperop part, to enable SageMaker's hyperopt module to choose the right
    # parameters based on the WAPE
    active_sales = pd.read_parquet(os.environ["SM_DATA_DIR"] + '/active_sales')
    active_sales['date'] = pd.to_datetime(active_sales['date'])
    # Since the predictions' date column is a datetime, this step is necessary for a smooth merge right after

    res = pd.merge(res, active_sales, how="left")
    res["ae"] = np.abs(res["yhat"] - res["y"])
        
    cutoff_abs_error = res["ae"].sum()
    cutoff_target_sum = res["y"].sum()
    
    print(res.head())
    print("WAPE computed!", cutoff_abs_error, cutoff_target_sum)
    
    return cutoff_abs_error, cutoff_target_sum

    
def train_model_fn(cutoff_week_id, config, hyperparameters):

    train_ds = train_input_fn(os.environ['SM_CHANNEL_TRAIN'] + '/gluonts_ds_cutoff_' + str(cutoff_week_id) + '.pkl')
        
    nb_ts = len(train_ds)

    # New tuning
    estimator = SimpleFeedForwardEstimator(freq=config.get_prediction_freq(),
                                           prediction_length=config.get_prediction_length(),
                                           context_length=hyperparameters['context_length'],
                                           num_hidden_dimensions=[hyperparameters['len_hidden_dimensions'] for i in range(hyperparameters['num_hidden_dimensions'])],
                                           trainer=Trainer(epochs=hyperparameters['epochs'],
                                                           batch_size=hyperparameters['batch_size'],
                                                           num_batches_per_epoch=hyperparameters['num_batches_per_epoch'],
                                                           learning_rate=hyperparameters['learning_rate'])
                                           )

    predictor = estimator.train(train_ds)

    predictor.serialize(Path(os.environ['SM_MODEL_DIR']))
    
    return 0