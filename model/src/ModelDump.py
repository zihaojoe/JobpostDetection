import pickle
import config
import numpy as np
import pandas as pd
import FeatureEngineering as FE
import ModelTraining as MT
from keras.models import Sequential,load_model
from keras.wrappers import scikit_learn

data = pd.read_csv(config.PROJECT_HOME+"/data/jobposting_cleaned.csv")

y = data['fraudulent'].copy()
X = data.drop(['fraudulent'], axis=1)

X = FE.FE_text_feature(X, sav_path=(config.MODEL_PATH+'vec_file.pickle'))   # extract text feature
X = FE.FE_standardize(X, sav_path=(config.MODEL_PATH+'SD_file.pickle'))   # standardization
X = FE.FE_onehot(X, sav_path=(config.MODEL_PATH+'OH_file.pickle'))   # one-hot coding

model = scikit_learn.KerasClassifier(build_fn=MT.create_model, input_dim=X.shape[1], verbose=0)
model.fit(X, y)
pickle.dump(model, open(config.MODEL_PATH+'model_file.pickle', 'wb'))