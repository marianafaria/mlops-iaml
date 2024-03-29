"""# 1 - Importando os módulos necessários"""

import os
import mlflow
import tensorflow
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, InputLayer, Dropout
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
from keras.regularizers import l1, l2

import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

import random
import numpy as np
import random as python_random


def reset_seeds():
   os.environ['PYTHONHASHSEED']=str(42)
   tf.random.set_seed(42)
   np.random.seed(42)
   random.seed(42)


def process_data():
   data = pd.read_csv('https://raw.githubusercontent.com/renansantosmendes/lectures-cdas-2023/master/fetal_health_reduced.csv')
   
   X = data.drop(["fetal_health"], axis=1)
   y = data["fetal_health"]

   columns_names = list(X.columns)
   scaler = preprocessing.StandardScaler()
   X_df = scaler.fit_transform(X)
   X_df = pd.DataFrame(X_df, columns=columns_names)

   X_train, X_test, y_train, y_test = train_test_split(X_df, y, test_size=0.3, random_state=42)

   y_train = y_train -1
   y_test = y_test - 1
   return X_train, X_test, y_train, y_test


def create_model(train_data):
   reset_seeds()

   model = Sequential()
   model.add(InputLayer(input_shape=(train_data.shape[1], )))
   model.add(Dense(10, activation='relu' ))
   model.add(Dense(10, activation='relu' ))
   model.add(Dense(3, activation='softmax' ))
   
   model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
   return model


def config_mlflow():
   MLFLOW_TRACKING_URI = 'https://dagshub.com/mariifaria/mlops-iaml.mlflow'
   MLFLOW_TRACKING_USERNAME = 'mariifaria'
   MLFLOW_TRACKING_PASSWORD = '3cbb9994863f11c83c600986df7d3fff17bae014'
   os.environ['MLFLOW_TRACKING_USERNAME'] = MLFLOW_TRACKING_USERNAME
   os.environ['MLFLOW_TRACKING_PASSWORD'] = MLFLOW_TRACKING_PASSWORD
   mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

   mlflow.tensorflow.autolog(log_models=True, log_input_examples=True, log_model_signatures=True)


def train_model(model, X_train, y_train):
   with mlflow.start_run(run_name='experiment_01') as run:
      model.fit(X_train, y_train, epochs=50, validation_split=0.2, verbose=3)


if __name__ == '__main__':
   X_train, X_test, y_train, y_test = process_data()
   model = create_model(X_train)
   config_mlflow()
   train_model(model, X_train, y_train)
