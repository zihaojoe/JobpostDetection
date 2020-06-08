import numpy as np
import pandas as pd
import re
import string
import nltk   # natural language toolkit
from nltk import pos_tag
from nltk.stem import LancasterStemmer,WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
import os
import config
nltk.data.path.append(config.PROJECT_HOME+'/model/nltk_data/')

data = pd.read_csv(config.PROJECT_HOME+"/model/data/jobposting.csv")
data.drop(['job_id','department'],axis=1,inplace=True)

#-------------------#
# country
#-------------------#
# create a new column - country_US, containing one of the 3 values: 'US', 'Other', and na
country = [np.nan if type(ls)==float else ls[0] for ls in data['location'].str.split(',')]
data['country'] = country
data.loc[(data['country']!='US')&(~data['country'].isna()),['country']] = 'Other'
data.loc[data['country'].isna(),['country']] = 'Unknown'
data.drop(['location'],axis=1,inplace=True)

#---------------------------------------------------------------------------------#
# employment_type, required_experience, required_education, function, industry
#---------------------------------------------------------------------------------#
# fillna of ['employment_type', 'required_experience', 'required_education','industry','function']
fillna_cols = ['required_education','employment_type','required_experience','industry','function']
for col in fillna_cols:
    data[col].fillna('Unspecified',inplace=True)

# combining minorities of required_education
edu_higher = ('Master\'s Degree','Doctorate')
data.loc[data['required_education'].isin(edu_higher),'required_education'] = 'Master or higher'
edu_bachelor = ('Bachelor\'s Degree','Some College Coursework Completed')
data.loc[data['required_education'].isin(edu_bachelor),'required_education'] = 'Bachelor'
edu_other = ('Vocational','Vocational - Degree','Vocational - HS Diploma',
             'Professional','Some High School Coursework')
data.loc[data['required_education'].isin(edu_other),'required_education'] = 'Other'

# combining minorities of required_experience
data.loc[data['required_experience']=='Not Applicable','required_experience'] = 'Unspecified'

# industry
# combining minorities of industry, counts < 500
tmp = data['industry'].value_counts()
data.loc[data['industry'].isin(tmp[(tmp<500)].index),'industry'] = 'Other'

# function
# combining minorities of function, counts < 300
tmp = data['function'].value_counts()
data.loc[data['function'].isin(tmp[(tmp<300)].index),'function'] = 'Other'

#-------------------#
# salary
#-------------------#
# salary range
# clean salary column
salary = data['salary_range'].str.split('-')
drop_ix = []
for ix in salary[-salary.isna()].index:
    try:
        float(salary[ix][1])
        float(salary[ix][0])
    except:
        drop_ix.append(ix)
data.drop(drop_ix,axis=0,inplace=True)

# split into low and high columns
salary = data['salary_range'].str.split('-')
salary_low = [np.nan if (type(ls)!=list) else float(ls[0]) for ls in salary]
salary_high = [np.nan if (type(ls)!=list) else float(ls[1]) for ls in salary]
data['salary_low'] = salary_low
data['salary_high'] = salary_high
data.drop('salary_range',axis=1,inplace=True)

# fillna
data['salary_low'].fillna(0,inplace=True)
data['salary_high'].fillna(0,inplace=True)

#-----------------------------------------#
# Text columns create and clean
#-----------------------------------------#
# create text column: combining ['title','company_profile', 'description', 'requirements', 'benefits']
text_cols = ['title','company_profile', 'description', 'requirements', 'benefits']
for col in text_cols:
    data[col].fillna(' ', inplace=True)

data['text'] = data[text_cols].apply(lambda x: ' '.join(x), axis=1)
data.drop(text_cols, axis=1, inplace=True)

# remove unuseful characters 
# pos_tag search path: /Users/JoeCheung/nltk_data
def text_clean(text):
    """ Delete punctuation, links and make words all lower case
    Args:
        text (`str`): Text before cleaning
    Returns:
        text (`str`): Text after cleaning
    """
    text = text.lower()   # transform to lowercase
    text = re.sub('http.?://\S+|www\.\S+', '', text)   # remove links
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)   # delete punctuation
    text = re.sub('\n', '', text)   # remove carriage return
    return text

data['text'] = data['text'].apply(lambda x: text_clean(x))

def get_word_type(tag):
    """Get the part of speech of the word from its tag
    Args:
        tag (`str`): A string indicating the tag of the word 
    Returns:
        word_type (`char`): A char reflecting the wordnet word type(part of speech)
    """
    if tag.startswith('J'):
        word_type = wordnet.ADJ
    elif tag.startswith('V'):
        word_type = wordnet.VERB
    elif tag.startswith('N'):
        word_type = wordnet.NOUN
    elif tag.startswith('R'):
        word_type = wordnet.ADV
    else:
        word_type = wordnet.NOUN
    return word_type

def text_lemmatize(text):
    """Lemmatize the text and remove stop words
    Args:
        text (`str`): Original text made up of English words
    Returns:
        text_lemmatized (`str`): Lemmatized text
    """
    lemmatizer = WordNetLemmatizer()   # tranform a word to original form by specifying its word type
    text_lemmatized = []
    
    for word in text.split():
        word_strip = word.strip()
        if word_strip not in stopwords.words('english'):
            word_tag = pos_tag([word_strip])
            word_lemmatized = lemmatizer.lemmatize(word_strip,get_word_type(word_tag[0][1]))
            text_lemmatized.append(word_lemmatized)
    return " ".join(text_lemmatized)  

# data['text'] = data['text'].apply(lambda x: text_lemmatize(x))
for i in range(len(data)):
    try:
        data.loc[i,'text'] = text_lemmatize(data.loc[i,'text'])
    except Exception as e:
        print(i)
        continue

data.to_csv(config.PROJECT_HOME+"model/data/jobposting_cleaned.csv",index=False)