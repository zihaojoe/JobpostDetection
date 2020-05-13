import numpy as np
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler

# Text Feature Extraction
def FE_text_feature_pred(X_predict, text_col="text", vec_file=None):
    """ Feature engineering: Extract text features for prediction data set using pre-trained model 
    Args:
        X_predict (`DataFrame`): Original prediction set
        text_col (`str`): Name of the text column. Defaults to "text"
        vec_file (`str`): Path of the TfidfVectorizer. Defaults to None
    Returns:
        X_predict_vec (`DataFrame`): Prediction data set with vectorized text feature appended
    """
    vec = pickle.load(open(vec_file, 'rb'))
    X_predict_textfeature = vec.transform(X_predict[text_col])
    text_feature_predict = pd.DataFrame(X_predict_textfeature.A,columns=map(lambda x: 'text_feature'+str(x),range(X_predict_textfeature.shape[1])))
    text_feature_predict.index = text_feature_predict.index
    X_predict_vec = pd.concat([X_predict, text_feature_predict], axis=1) 
    X_predict_vec.drop(['text'], axis=1, inplace=True)
    return X_predict_vec

# Standardize   
def FE_standardize_pred(X_predict, SD_file=None):
    """ Feature engineering: Standardization for prediction data set using pre-trained model 
    Args:
        X_predict (`DataFrame`): Original prediction set
        SD_file (`str`): Path of the StandardScaler. Defaults to None
    Returns:
        X_predict_SD (`DataFrame`): Prediction data set after standardization
    """
    scaler = pickle.load(open(SD_file, 'rb'))
    num_cols = X_predict.select_dtypes([float]).columns
    
    X_predict_SD = X_predict.copy()
    X_predict_SD.loc[:,num_cols] = scaler.transform(X_predict_SD[num_cols])
    
    return X_predict_SD

# One-hot
def FE_onehot_pred(X_predict, OH_file=None):
    """ Feature engineering: One-hot encoding for prediction data set using pre-trained model 
    Args:
        X_predict (`DataFrame`): Original prediction set
        OH_file (`str`): Path of the file containing training set column names. Defaults to None
    Returns:
        X_predict_OH (`DataFrame`): Prediction data set after one-hot encoding
    """   
    # get dummy variables for prediction set
    train_cols = pickle.load(open(OH_file, 'rb'))
    X_predict_OH = X_predict.copy()
    X_predict = X_predict.copy()
    cat_cols = X_predict.select_dtypes(object).columns
    if len(cat_cols) > 0:
        dummy_predict = pd.get_dummies(X_predict_OH[cat_cols])
        X_predict_OH = pd.concat([dummy_predict,X_predict_OH], axis=1)    
        X_predict_OH.drop(cat_cols, axis=1, inplace=True)

     # add missing dummy columns for prediction set
    miss_columns = set(train_cols) - set(X_predict_OH.columns)
    for col in miss_columns:
        X_predict_OH[col] = 0

    # delete adundant columns
    add_columns = set(X_predict_OH.columns) - set(train_cols)
    X_predict_OH.drop(list(add_columns), axis=1, inplace=True)      

    # sort the columns to match training set
    X_predict_OH = X_predict_OH[train_cols]
    
    return X_predict_OH


