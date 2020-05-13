import numpy as np
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Text Feature Extraction
def FE_text_feature(X_train, X_test=None,text_col="text", sav_path=None):
    """ Feature engineering: Extract text features using TfidfVectorizer for training and test set
    Args:
        X_train (`DataFrame`): Original training set 
        X_test (`DataFrame`): Original test set. Defaults to None
        text_col (`str`): Name of the text column. Defaults to "text"
        sav_path (`str`): Path to save the TfidfVectorizer. Defaults to None
    Returns:
        X_train_vec (`DataFrame`): Training set with vectorized text feature appended
        X_test_vec (`DataFrame`): Test set with vectorized text feature appended
    """
    vec = TfidfVectorizer(min_df=0.03,max_df=0.6)
    vec.fit(X_train[text_col])   # fit the text vectorizer based on the training set
    if sav_path is not None: pickle.dump(vec, open(sav_path, 'wb'))
    X_train_textfeature = vec.transform(X_train[text_col])
    if X_test is not None: X_test_textfeature = vec.transform(X_test[text_col])
    
    # create text feature DataFrame
    text_feature_train = pd.DataFrame(X_train_textfeature.A,columns=map(lambda x: 'text_feature'+str(x),range(X_train_textfeature.shape[1])))
    if X_test is not None: text_feature_test = pd.DataFrame(X_test_textfeature.A,columns=map(lambda x: 'text_feature'+str(x),range(X_test_textfeature.shape[1])))
    
    # concat text feature DataFrame with original feature DataFrame
    text_feature_train.index = X_train.index
    X_train_vec = pd.concat([X_train, text_feature_train], axis=1)
    X_train_vec.drop(['text'], axis=1, inplace=True)
    if X_test is not None:
        text_feature_test.index = X_test.index
        X_test_vec = pd.concat([X_test, text_feature_test], axis=1) 
        X_test_vec.drop(['text'], axis=1, inplace=True)
        
    if X_test is not None:
        return X_train_vec, X_test_vec
    else: 
        return X_train_vec

# Standardize   
def FE_standardize(X_train, X_test=None, sav_path=None):
    """ Feature engineering: Standardization
    Args:
        X_train (`DataFrame`): Original training set 
        X_test (`DataFrame`): Original test set. Defaults to None
        sav_path (`str`): Path to save the StandardScaler. Defaults to None
    Returns:
        X_train_SD (`DataFrame`): Training set after standardization
        X_test_SD (`DataFrame`): Test set after standardization
    """
    X_train_SD = X_train.copy()
    num_cols = X_train_SD.select_dtypes([float]).columns
    
    scaler = StandardScaler()
    scaler.fit(X_train_SD[num_cols])
    if sav_path is not None: pickle.dump(scaler, open(sav_path, 'wb'))
    
    X_train_SD.loc[:,num_cols] = scaler.transform(X_train_SD[num_cols])
    
    if X_test is not None: 
        X_test_SD = X_test.copy()
        X_test_SD.loc[:,num_cols] = scaler.transform(X_test_SD[num_cols])
    
    if X_test is not None:
        return X_train_SD, X_test_SD
    else:
        return X_train_SD

# One-hot
def FE_onehot(X_train, X_test=None, sav_path=None):
    """ Feature engineering: One-hot encoding training and test set
    Args:
        X_train (`DataFrame`): Original training set 
        X_test (`DataFrame`): Original test set. Defaults to None
        sav_path (`str`): Path to save the training set columns. Defaults to None
    Returns:
        X_train_OH (`DataFrame`): Training set after one-hot encoding
        X_test_OH (`DataFrame`): Test set after one-hot encoding
    """    
    # get dummy variables for both training and test set
    X_train_OH = X_train.copy()
    if X_test is not None: X_test_OH = X_test.copy()
    cat_cols = X_train_OH.select_dtypes(object).columns
    if len(cat_cols) > 0:
        dummy_train = pd.get_dummies(X_train_OH[cat_cols])
        X_train_OH = pd.concat([dummy_train,X_train_OH], axis=1)    
        X_train_OH.drop(cat_cols, axis=1, inplace=True)
    
    if X_test is not None:
        cat_cols = X_test_OH.select_dtypes(object).columns
        if len(cat_cols) > 0:
            dummy_test = pd.get_dummies(X_test_OH[cat_cols])
            X_test_OH = pd.concat([dummy_test, X_test_OH], axis=1)    
            X_test_OH.drop(cat_cols, axis=1, inplace=True)

    if X_test is not None:
        # add missing dummy columns for test set
        miss_columns = set(X_train_OH.columns) - set(X_test_OH.columns)
        for col in miss_columns:
            X_test_OH[col] = 0

        # delete adundant columns
        add_columns = set(X_test_OH.columns) - set(X_train_OH.columns)
        X_test_OH.drop(list(add_columns), axis=1, inplace=True)      

        # sort the columns to match training and test set
        X_test_OH = X_test_OH[X_train_OH.columns]
    
    if sav_path is not None: pickle.dump(X_train_OH.columns, open(sav_path, 'wb'))
    
    if X_test is not None:
        return X_train_OH, X_test_OH
    else:
        return X_train_OH

# Stratified train test split
def train_test_split_stratified(data, test_size=0.3, random_state=666, label="fraudulent"):
    """ Feature engineering: One-hot encoding training and test set
    Args:
        data (`DataFrame`): Original data set to be split
        test_size (`float`): test set size over all data size
        random_state (`int`): random seed
        label (`str`): the name of the target column in the dataset
    Returns:
        X_train (`DataFrame`): Training set without target
        X_test (`DataFrame`): Test set without target
        y_train (`DataFrame`): Training set target
        y_test (`DataFrame`): Test set target
    """   
    data_real = data[data[label]==0]
    data_fake = data[data[label]==1]

    y_real = data_real[label].copy()
    X_real = data_real.drop([label], axis=1)

    y_fake = data_fake[label].copy()
    X_fake = data_fake.drop([label], axis=1)

    X_real_train, X_real_test, y_real_train, y_real_test = train_test_split(X_real, y_real, test_size=test_size, random_state=random_state)
    X_fake_train, X_fake_test, y_fake_train, y_fake_test = train_test_split(X_fake, y_fake, test_size=test_size, random_state=random_state)
    
    X_train = pd.concat([X_real_train, X_fake_train])
    y_train = pd.concat([y_real_train, y_fake_train])

    X_test = pd.concat([X_real_test, X_fake_test])
    y_test = pd.concat([y_real_test, y_fake_test])
    
    return X_train, X_test, y_train, y_test