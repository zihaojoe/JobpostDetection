import config
import logging
import logging.config
import yaml
import numpy as np
import pandas as pd
import FeatureEngineering as FE
import keras
from keras.layers import Dense
from keras.models import Sequential,load_model
from keras.wrappers import scikit_learn
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

def create_model(input_dim=0, optimizer='adam'):
    """ Create keras model
    Args:
        input_dim (int): Input dimension, number of features
        optimizer (str): The opimization method of the model
    Returns:
        model (keras model object): A built keras model
    """
    model = Sequential()
    model.add(Dense(units = 64 , activation = 'relu' , input_dim = input_dim))
    model.add(Dense(units = 32 , activation = 'relu'))
    model.add(Dense(units = 16 , activation = 'relu'))
    model.add(Dense(units = 4 , activation = 'relu'))
    model.add(Dense(units = 1 , activation = 'sigmoid'))
    model.compile(optimizer = optimizer , loss = 'binary_crossentropy' , metrics = ['accuracy'])
    # model.summary()
    return model

if __name__ == "__main__":
    
    logging.config.fileConfig(config.LOGGING_CONFIG)
    logger = logging.getLogger('model_training')

    data = pd.read_csv(config.PROJECT_HOME+"/data/jobposting_cleaned.csv")
    logger.info("The shape of the data is {} ".format(data.shape))

    # feature engineering
    X_train, X_test, y_train, y_test = FE.train_test_split_stratified(data)   # train test split with stratified sampling
    X_train_vec, X_test_vec = FE.FE_text_feature(X_train, X_test)   # extract text feature
    X_train_SD, X_test_SD = FE.FE_standardize(X_train_vec, X_test_vec)   # standardization
    X_train_OH, X_test_OH = FE.FE_onehot(X_train_SD, X_test_SD)   # one-hot coding

    # transform a keras model to a scikit learn model object
    model = scikit_learn.KerasClassifier(build_fn=create_model, input_dim=X_train_OH.shape[1], verbose=0)

    # get params space from model_config.yml file
    with open('model_config.yml', 'r') as f: 
        params_training = yaml.load(f)

    batch_size = params_training["model_tuning"]["batch_size"]
    epochs = params_training["model_tuning"]["epochs"]
    optimizer = params_training["model_tuning"]["optimizer"]
    scoring = params_training["model_tuning"]["scoring"]

    # grid search to find the best hyperparams combination
    param_grid = dict(optimizer=optimizer, batch_size=batch_size, epochs=epochs)
    grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring=scoring, n_jobs=1, cv=3)
    grid_result = grid.fit(X_train_OH, y_train)

    # print the result of the model
    logger.info('Best: {} using {}'.format(grid_result.best_score_, grid_result.best_params_))
    means = grid_result.cv_results_['mean_test_score']
    stds = grid_result.cv_results_['std_test_score']
    params = grid_result.cv_results_['params']
    for mean, std, param in zip(means, stds, params):
        logger.info("%f (%f) with: %r" % (mean, std, param))