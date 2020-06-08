#!/usr/bin/env python
import pytest
import sys
import pandas as pd
sys.path.append('./src')
import ModelPredict as mp
import DataCleaning as dc

# happy path for data cleaning, all features
def test_data_cleaning_all():
	test_input = pd.read_csv("unit_test/input/jobposting.csv")
	test_output = dc.data_cleaning(test_input,output=False)
	target = pd.read_csv("unit_test/target/jobposting_cleaned.csv")
	try:   
	    result = all(test_output == target)
	except:
	    result = False
	assert result

# unhappy path for additional features
def test_data_cleaning_additional_col():
	test_input = pd.read_csv("unit_test/input/jobposting.csv")
	test_input['aaa'] = 0
	fillna_cols = ['required_education','employment_type','required_experience','industry','function','aaa']
	test_output = dc.data_cleaning(test_input,  output=False, fillna_cols=fillna_cols)
	target = pd.read_csv("unit_test/target/jobposting_cleaned.csv")
	try:   
	    result = all(test_output == target)
	except:
	    result = False
	assert result

# happy path for model prediction, all features
def test_model_prediction_all():
	test_input = pd.read_csv("unit_test/target/jobposting_cleaned.csv")[0:1]
	result = mp.predict_fake_post(test_input)
	assert result==0

# happy path for model prediction, additional features
def test_model_prediction_additional_features():
	test_input = pd.read_csv("unit_test/target/jobposting_cleaned.csv")[0:1]
	test_input['aaa'] = 0
	result = mp.predict_fake_post(test_input)
	assert result==0

# unhappy path for model prediction, missing features
def test_model_prediction_missing_features():
	test_input = pd.read_csv("unit_test/target/jobposting_cleaned.csv")[0:1]
	test_input.drop('telecommuting', axis=1, inplace=True)
	result = mp.predict_fake_post(test_input)
	assert result==None




