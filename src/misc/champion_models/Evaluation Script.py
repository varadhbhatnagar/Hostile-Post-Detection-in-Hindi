### Order of Labels --> [Hostile,defamation,fake,hate,offensive,non-hostile]
### An example      --> [1,0,1,1,0,0]


import numpy as np
import pandas as pd
from sklearn.metrics import f1_score



def preprocess(df):
    
    df = df.dropna()
    
    df.insert(len(df.columns)-1,'Hostile', np.zeros(len(df),dtype=int))
    df.insert(len(df.columns)-1,'Defamation', np.zeros(len(df),dtype=int))
    df.insert(len(df.columns)-1,'Fake', np.zeros(len(df),dtype=int))
    df.insert(len(df.columns)-1,'Hate', np.zeros(len(df),dtype=int))
    df.insert(len(df.columns)-1,'Offensive', np.zeros(len(df),dtype=int))
    df.insert(len(df.columns)-1,'Non-Hostile', np.zeros(len(df),dtype=int))    
    
    for i in range(len(df)):
        text = df['Labels Set'][i]
        text = text.lower()
        text = text.replace('\n',"")
        text = text.replace('"',"")
        text = text.replace(" ","")
        text = text.split(',')


        for word in text:
            if word == 'defamation':
                df.at[i,'Hostile']    = 1
                df.at[i,'Defamation'] = 1
    
            if word == 'fake':
                df.at[i,'Hostile']    = 1
                df.at[i,'Fake'] = 1
    
            if word == 'hate':
                df.at[i,'Hostile']    = 1
                df.at[i,'Hate'] = 1
    
            if word == 'offensive':
                df.at[i,'Hostile']    = 1
                df.at[i,'Offensive'] = 1
    
            if word == 'non-hostile' and df['Hostile'][i]==0:
                df.at[i,'Hostile']    = 0
                df.at[i,'Non-Hostile'] = 1

    return df 
  
    



def get_scores(y_true, y_pred):
    
    hostility_true = y_true['Hostile']
    hostility_pred = y_pred['Hostile']
    
    hostility_f1 = f1_score(y_true=hostility_true, y_pred=hostility_pred, average='weighted')
    
    fine_true = y_true[['Defamation','Fake','Hate','Offensive']]
    fine_pred = y_pred[['Defamation','Fake','Hate','Offensive']]
    
    fine_f1          = f1_score(y_true=fine_true, y_pred=fine_pred, average=None)
    defame_f1        = fine_f1[0]
    fake_f1          = fine_f1[1]
    hate_f1          = fine_f1[2]
    offensive_f1     = fine_f1[3]
    weighted_fine_f1 = f1_score(y_true=fine_true, y_pred=fine_pred, average='weighted')

    return [hostility_f1, defame_f1, fake_f1, hate_f1, offensive_f1, weighted_fine_f1]




ground_truth_path      = '/home/varad/Desktop/IITB/CS626NLP/Project/src/champion_models/Validation Ground Truth.csv'
submission_file_path   = '/home/varad/Desktop/IITB/CS626NLP/Project/src/champion_models/submission.csv'


try:  
    y_true = pd.read_csv(ground_truth_path)
    y_pred = pd.read_csv(submission_file_path)
    
    y_true = preprocess(y_true)
    y_pred = preprocess(y_pred)
    team_score = get_scores(y_true,y_pred)

except:
    
    team_score = [0,0,0,0,0,0]
    
        
print("Coarse Grained F1-score: ", team_score[0])
print("Defamation F1-score:     ", team_score[1])
print("Fake F1-score:           ", team_score[2])
print("Hate F1-score:           ", team_score[3])
print("Offensive F1-score:      ", team_score[4])
print("Fine Grained F1-score:   ", team_score[5])

        












