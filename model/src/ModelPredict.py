import config as config
import FeatureEngineeringPred as FEP
import pickle
import numpy as np
import pandas as pd
import ModelTraining as MT

def predict_fake_post(input_data):
    """ Predict based on users input
    Args:
        input_data (`DataFrame`): Input data needed to be predicted
    Returns:
        result (`Array`): Prediction
    """	

    result = None
    required_columns=['telecommuting', 'has_company_logo', 'has_questions']
    for col in required_columns:
        if col not in input_data.columns:
            return 0
            
    try:
        input_data_FE = input_data.copy()
        input_data_FE = FEP.FE_text_feature_pred(input_data_FE,vec_file=config.MODEL_PATH+'vec_file.pickle')
        input_data_FE = FEP.FE_standardize_pred(input_data_FE,SD_file=config.MODEL_PATH+'SD_file.pickle')
        input_data_FE = FEP.FE_onehot_pred(input_data_FE, OH_file=config.MODEL_PATH+'OH_file.pickle')
        # Create a new model instance
        # model = MT.create_model(1135)
        with open (config.MODEL_PATH + 'input_size.txt', 'r') as f:
            input_size = int(f.readline())
        model = MT.create_model(input_size)
        # Load the previously saved weights
        model.load_weights(config.MODEL_PATH+'model_file.ckpt')
        result = model.predict(input_data_FE)
        result = result[0]
        #result[result>=0.5] = 1
        #result[result<0.5] = 0

    except:
        pass
    return result

if __name__ == "__main__":
    input_data = pd.read_csv(config.DATA_CLEANED_PATH)[0:2]
    print(predict_fake_post(input_data))