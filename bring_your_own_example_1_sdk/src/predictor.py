# This is the file that implements a flask server to do inferences.
# It's the file that you will modify to implement the scoring for your own algorithm.

from __future__ import print_function

import os
import json

#import StringIO
from io import StringIO
import sys
import signal
import traceback

import flask
from flask import json

import pandas as pd
import numpy as np

from pathlib import Path
from gluonts.model.predictor import Predictor

import config as cf
import model as mdl
import utils as ut


config_file = "dev.yml"
config = cf.ProgramConfiguration(config_file, "functional.yml")

model_path = '/opt/ml/model'

# A singleton for holding the model. This simply loads the model and holds it.
# It has a predict function that does a prediction based on the model and the input data.

class ScoringService(object):
    model = None   # Where we keep the model when it's loaded
    @classmethod
    def get_model(cls):
        """Get the model object for this instance, loading it if it's not already loaded."""
        if cls.model == None:
            model = Predictor.deserialize(Path(model_path))
            cls.model = model
        return cls.model

    @classmethod
    def predict(cls, input):
        """For the input, do the predictions and return them.

        Args:
            input (a pandas dataframe): The data on which to do the predictions. There will be
                one prediction per row in the dataframe"""
        clf = cls.get_model()
        
        forecasts = list(clf.predict(dataset=input))
        output = np.array([x.quantile(0.5).round().astype(int) for x in forecasts]).flatten()
        
        return output

    
# The flask app for serving predictions
app = flask.Flask(__name__)


@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    health = ScoringService.get_model() is not None  # You can insert a health check here
    
    status = 200 if health else 404
    return flask.Response(response='\n', status=status, mimetype='application/json')


@app.route('/invocations', methods=['POST'])
def transformation():
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    data = None

    # Convert from CSV to pandas
    if flask.request.content_type == 'text/csv':
        data = flask.request.data.decode('utf-8')
        #s = StringIO.StringIO(data)
        s = StringIO(data)
        df = pd.read_csv(s) #, header=None
    else:
        return flask.Response(response='This predictor only supports CSV data',
                              status=415, mimetype='text/plain')
    
    # Read file path from input
    bucket = df.loc[0, 'bucket']
    s3_file_path = df.loc[0, 'file_path']
    pred_file_path = 'gluonts_ds.pkl' #os.environ['SM_CHANNEL_PRED']
    
    #print('==================>', bucket, s3_file_path)
    
    # Download s3 pred file
    try:
        print('Inside try...')
        ut.download_file_from_S3(bucket, s3_file_path, pred_file_path)
    except:
        print('Inside pass...')
        pass
    
    print('current dir:', os.listdir("."))
    print('model', os.listdir(model_path))  
    
    # Read into a gluonts dataset
    # pp.format_cutoff_train_data(pred_dir, cutoff_week, config)
    pred_ds = mdl.train_input_fn(pred_file_path)
    
    # Do the prediction
    predictions = ScoringService.predict(pred_ds)

    # Convert from numpy back to CSV
    #out = StringIO.StringIO()
    out = StringIO()
    pd.DataFrame({'results':predictions}).to_csv(out, header=False, index=False)
    result = out.getvalue()

    return flask.Response(response=result, status=200, mimetype='text/csv')
