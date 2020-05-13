import config
import FeatureEngineeringPred as FEP
import pickle
import numpy as np
import pandas as pd

def predict_fake_post(input_data):
    input_data_FE = input_data.copy()

    input_data_FE = FEP.FE_text_feature_pred(input_data_FE,vec_file=config.MODEL_PATH+'vec_file.pickle')
    input_data_FE = FEP.FE_standardize_pred(input_data_FE,SD_file=config.MODEL_PATH+'SD_file.pickle')
    input_data_FE = FEP.FE_onehot_pred(input_data_FE, OH_file=config.MODEL_PATH+'OH_file.pickle')
    model = pickle.load(open(config.MODEL_PATH+'model_file.pickle', 'rb'))

    result = model.predict(input_data_FE)
    return result

if __name__ == "__main__":
    input_data = pd.read_csv(config.PROJECT_HOME+"/data/jobposting_cleaned.csv")[0:1]
    print(predict_fake_post(input_data))