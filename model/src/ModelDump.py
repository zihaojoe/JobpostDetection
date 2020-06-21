import pickle
import config
import numpy as np
import pandas as pd
import os
import yaml
import tensorflow as tf
import FeatureEngineering as FE
import ModelTraining as MT
from keras.models import Sequential,load_model
from keras.wrappers import scikit_learn
from keras import backend as K
from sklearn.metrics import confusion_matrix

def modeldump(df, sav_path=None):
	""" Train the best model and save to file
    Args:
        df (`DataFrame`): DataFrame used to train the momdel
        sav_path (`str`): Path to save the model. Defaults to None
    """
	np.random.seed(423)
	tf.random.set_seed(423)
	os.environ['PYTHONHASHSEED']=str(423)
	session_conf = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
	sess = tf.compat.v1.Session(graph=tf.compat.v1.get_default_graph(), config=session_conf)
	tf.compat.v1.keras.backend.set_session(sess)

	data = df.copy()

    # get params space from model_config.yml file
	with open(os.path.join(config.PROJECT_HOME, 'model','src','model_config.yml'), 'r') as f: 
		params_training = yaml.load(f)

	batch_size = params_training["model_production"]["batch_size"]
	epochs = params_training["model_production"]["epochs"]
	optimizer = params_training["model_production"]["optimizer"]

	X_train, X_test, y_train, y_test = FE.train_test_split_stratified(data)   # train test split with stratified sampling
	X_train_vec, X_test_vec = FE.FE_text_feature(X_train, X_test)   # extract text feature
	X_train_SD, X_test_SD = FE.FE_standardize(X_train_vec, X_test_vec)   # standardization
	X_train_OH, X_test_OH = FE.FE_onehot(X_train_SD, X_test_SD)   # one-hot coding
	g = tf.Graph()
	with g.as_default():
		tf.random.set_seed(423)
		model = scikit_learn.KerasClassifier(build_fn=MT.create_model, input_dim=X_train_OH.shape[1], verbose=0, optimizer=optimizer, batch_size=batch_size, epochs=epochs)
		model.fit(X_train_OH, y_train)
		y_pred = model.predict(X_test_OH)

		cm = confusion_matrix(y_test, y_pred)

		with open (sav_path+'result.txt', 'w') as f:
			f.write("Size of input: {0}\n".format(X_test_OH.shape[1]))
			f.write("The confusion matrix on the test data is as follows:\n")
			f.write(str(cm))
			f.write("\n")

		#print("Size of input:", X_test_OH.shape)
		#print("The confusion matrix on the test data is as follows:")
		#print(cm)

	y = data['fraudulent'].copy()
	X = data.drop(['fraudulent'], axis=1)

	X = FE.FE_text_feature(X, sav_path=(config.MODEL_PATH+'vec_file.pickle'))   # extract text feature
	X = FE.FE_standardize(X, sav_path=(config.MODEL_PATH+'SD_file.pickle'))   # standardization
	X = FE.FE_onehot(X, sav_path=(config.MODEL_PATH+'OH_file.pickle'))   # one-hot coding

	g = tf.Graph()
	with g.as_default():
		tf.random.set_seed(423)
		model = scikit_learn.KerasClassifier(build_fn=MT.create_model, input_dim=X.shape[1], verbose=0, optimizer=optimizer, batch_size=batch_size, epochs=epochs)
		model.fit(X, y)
		y_pred = model.predict(X)

		cm = confusion_matrix(y, y_pred)

		with open (sav_path+'result.txt', 'a') as f:
			f.write("Size of input: {0}\n".format(X.shape[1]))
			f.write("The confusion matrix on the training data is as follows:\n")
			f.write(str(cm))
			f.write("\n")

		model.model.save_weights(sav_path+'model_file.ckpt')

		with open (sav_path+'input_size.txt', 'w') as f:
			f.write(str(X.shape[1]))


		#pickle.dump(model, open(sav_path, 'wb'))

if __name__ == "__main__":

	np.random.seed(423)
	tf.random.set_seed(423)

	data = pd.read_csv(config.DATA_CLEANED_PATH)
	modeldump(data, sav_path=config.MODEL_PATH)
	print("Finished!")