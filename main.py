import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn

import os
from datetime import datetime

# Data Path
League = ["France","England","Germany","Italy","Spain"]

# Only change the 
DataPath = "/Users/tinghao/Desktop/project_data/" + League[1]

os.chdir(DataPath)

league_datasets= os.listdir()
league_datasets = sorted(league_datasets)
league_datasets.remove('Icon\r')
back_k_runs =10

team = 'Liverpool'
data = pd.read_csv(league_datasets[2])


home_data = data[data['HomeTeam']==team]
col_name = home_data.columns.tolist()  
col_name.insert(col_name.index('AwayTeam')+1,'Home_Indicator')  
home_data = home_data.reindex(columns=col_name)  
home_data['Home_Indicator'] = 1
home_data = home_data.rename(columns={'HomeTeam': 'Team', 'AwayTeam': 'Opponent'})


away_data = data[data['AwayTeam']=='Liverpool']
col_name_2 = away_data.columns.tolist()  
col_name_2.insert(col_name_2.index('AwayTeam')+1,'Home_Indicator')  
away_data = away_data.reindex(columns=col_name_2)  
away_data['Home_Indicator'] = 0
away_data = away_data.rename(columns={'AwayTeam': 'Team', 'HomeTeam': 'Opponent'})


concat_data = pd.concat([home_data, away_data])

features_lst = ['Date','Team','Opponent','Home_Indicator','FTHG','FTAG','FTR','HTHG','HTAG','HST','AST','AS','HS','HC','AC']
team_data = concat_data[features_lst]

#rename the column
rename_dict = {'FTHG':'Full_Home_Goals','FTAG':'Full_Away_Goals','FTR':'Full_Results','HTHG':'Half_Home_Goals','HTAG':'Half_Away_Goals',
               'HST':'Home_Shots_on_Target','AST':'Away_Shots_on_Target','AS':'Away_Shots','HS':'Home_Shots','HC':'Home_Corners','AC':'Away_Corners'}
team_data = team_data.rename(columns=rename_dict)

#sort by date
team_data['Date'] = [datetime.strptime(x, '%d/%m/%y') for x in team_data['Date'] ]
team_data = team_data.sort_values(by='Date')

#compute the standing until this game
col_name_3 = team_data.columns.tolist()  
col_name_3.insert(col_name_3.index('FTR')+1,'Standing')  
team_data = team_data.reindex(columns=col_name_3)

tmp = []      
for pair in zip(team_data['Home_Indicator'], team_data['FTR']):
    if (pair[0]==0 and pair[1]=='A') or (pair[0]==1 and pair[1]=='H'):
        tmp.append(3)
    elif (pair[0]==1 and pair[1]=='A') or (pair[0]==0 and pair[1]=='H'):
        tmp.append(0)
    else:
        tmp.append(1)

standing_lst = []
for i in range(len(tmp)+2):
    if i > 1:
        standing_lst.append(np.sum(tmp[:i-1]))

team_data['Standing'] = standing_lst


#compute the winning probability
col_name_4 = team_data.columns.tolist()  
col_name_4.insert(col_name_4.index('Standing')+1,'Winning_Probability')  
team_data = team_data.reindex(columns=col_name_4)

tmp_1 = []
for pair in zip(team_data['Home_Indicator'], team_data['FTR']):
    if (pair[0]==0 and pair[1]=='A') or (pair[0]==1 and pair[1]=='H'):  #win
        tmp_1.append(1)
    elif (pair[0]==1 and pair[1]=='A') or (pair[0]==0 and pair[1]=='H'): #lose
        tmp_1.append(0)
    else: #draw
        tmp_1.append(0)

win_lst = []
for i in range(len(tmp_1)+2):
    if i > 1:
        win_lst.append(np.sum(tmp_1[:i-1])/(i-1))
team_data['Winning_Probability']= win_lst


#compute the winning probability of being home/away team
home_wprob_lst = []
away_wprob_lst = []

for i in range(len(team_data)):
    tmp_data = team_data[:i+1]
    tmp_df = tmp_data[tmp_data['Home_Indicator']==1]
    if len(tmp_df)==0:
        home_wprob_lst.append(0)
    else:
        home_wprob = (len(tmp_df[tmp_df['FTR']=='H']))/len(tmp_df)
        home_wprob_lst.append(home_wprob)
    
    tmp_df1 = tmp_data[tmp_data['Home_Indicator']==0]
    if len(tmp_df1)==0:
        away_wprob_lst.append(0)
    else:
        away_wprob = (len(tmp_df1[tmp_df1['FTR']=='A']))/len(tmp_df1)
        away_wprob_lst.append(away_wprob)
        
        
col_name = team_data.columns.tolist() 
col_name.insert(col_name.index('Winning_Probability')+1,'Home_Win_Prob')
team_data = team_data.reindex(columns=col_name)
team_data['Home_Win_Prob'] = home_wprob_lst

col_name = team_data.columns.tolist() 
col_name.insert(col_name.index('Home_Win_Prob')+1,'Away_Win_Prob')
team_data = team_data.reindex(columns=col_name)
team_data['Away_Win_Prob'] = away_wprob_lst

        
# Tinghao's codes 可以这样新加column
team_data['Goals']= np.where(team_data['Home_Indicator']==1,team_data['FTHG'],team_data['FTHG'])



        
        























