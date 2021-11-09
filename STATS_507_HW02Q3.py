#!/usr/bin/env python
# coding: utf-8

# a.

# In[ ]:


# reshape demographic data and combine them
import pandas as pd
df_Demo_11_12 = pd.read_sas('DEMO_G_11_12.XPT', format='xport')
df_Demo_13_14 = pd.read_sas('DEMO_H_13_14.XPT', format='xport')
df_Demo_15_16 = pd.read_sas('DEMO_I_15_16.XPT', format='xport')
df_Demo_17_18 = pd.read_sas('DEMO_J_17_18.XPT', format='xport')

# reshape each data frame above to contain the unique ids (SEQN), 
# age (RIDAGEYR), race and ethnicity (RIDRETH3), education (DMDEDUC2), and marital status (DMDMARTL)
# variables related to the survey weighting: (RIDSTATR, SDMVPSU, SDMVSTRA, WTMEC2YR, WTINT2YR) 

col_name_lis = ['SEQN', 'RIDAGEYR', 'RIAGENDR', 'RIDRETH3', 'DMDEDUC2', 'DMDMARTL', 
                'RIDSTATR', 'SDMVPSU', 'SDMVSTRA', 'WTMEC2YR', 'WTINT2YR']
df_Demo_11_12_reshape = (df_Demo_11_12[col_name_lis]).assign(COHORT=['2011 - 2012'] * len(df_Demo_11_12))
df_Demo_13_14_reshape = (df_Demo_13_14[col_name_lis]).assign(COHORT=['2013 - 2014'] * len(df_Demo_13_14))
df_Demo_15_16_reshape = (df_Demo_15_16[col_name_lis]).assign(COHORT=['2015 - 2016'] * len(df_Demo_15_16))
df_Demo_17_18_reshape = (df_Demo_17_18[col_name_lis]).assign(COHORT=['2017 - 2018'] * len(df_Demo_17_18))
df_Demo_11_18_reshape = pd.concat([df_Demo_11_12_reshape, df_Demo_13_14_reshape, 
                                   df_Demo_15_16_reshape, df_Demo_17_18_reshape])
# change column names
new_clo_name_lis = ['unique ids', 'age', 'gender', 'race and ethnicity', 'education',
                   'marital status', 'interview/examination status', 'masked variance pseudo-PSU', 
                    'masked variance pseudo-stratum', 'full sample 2 year MEC exam weight',
                   'full sample 2 year interview weight', 'data year']
df_Demo_11_18_reshape.set_axis(new_clo_name_lis, axis=1, inplace=True)

# briefly check first ten rows
df_Demo_11_18_reshape.head(10)


# In[ ]:


# replace numerical data with coresponding categorical data
df_Demo_11_18_reshape['race and ethnicity'].replace([1.0, 2.0, 3.0, 4.0, 6.0, 7.0, '.'],
                                                    ['Mexican American','Other Hispanic', 'Non-Hispanic White', 'Non-Hispanic Black',
                                                    'Non-Hispanic Asian', 'Other Race - Including Multi-Racial', 'Missing'], inplace=True)
df_Demo_11_18_reshape['education'].replace([1.0, 2.0, 3.0, 4.0, 5.0, 7.0, 9.0, '.'],
                                          ['Less than 9th grade', '9-11th grade: Includes 12th grade with no diploma',
                                          'High school graduate/GED or equivalent', 'Some college or AA degree',
                                          'College graduate or above', 'Refused',
                                          'Unkown', 'Missing'], inplace=True)
df_Demo_11_18_reshape['marital status'].replace([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 77.0, 99.0, '.'],
                                          ['Married', 'Widowed',
                                          'Divorced', 'Separated',
                                          'Never married', 'Living with partner',
                                          'Refused', 'Unknown', 'Missing'], inplace=True)
df_Demo_11_18_reshape['interview/examination status'].replace([1.0, 2.0, '.'], 
                                                              ['Interviewed only', 'Both interviewed and MEC examined',
                                                              'Missing'], inplace=True)
df_Demo_11_18_reshape['gender'].replace([1.0, 2.0, '.'], ['Male', 'Female',
                                                              'Missing'], inplace=True)


# In[ ]:


# check the first ten rows of the final version of demographic dataframe 
print(df_Demo_11_18_reshape.shape)
df_Demo_11_18_reshape.head(10)


# In[ ]:


# storing reshaped dataframe as pickle file 
df_Demo_11_18_reshape.to_pickle('CDC_Demo_11_18_df.pkl',
                               compression=None)


# b.

# In[ ]:


# Repeat part a for the oral health and dentition data (OHXDEN_*.XPT) 
# retaining the following variables: SEQN, OHDDESTS, tooth counts (OHXxxTC), and coronal cavities (OHXxxCTC)
df_Oral_Den_11_12 = pd.read_sas('OHXDEN_G.XPT', format='xport')
df_Oral_Den_13_14 = pd.read_sas('OHXDEN_H.XPT', format='xport')
df_Oral_Den_15_16 = pd.read_sas('OHXDEN_I.XPT', format='xport')
df_Oral_Den_17_18 = pd.read_sas('OHXDEN_J.XPT', format='xport')
oral_col_name_lis = ['SEQN', 'OHDDESTS', 'OHXxxTC', 'OHXxxCTC']
 
df_lis_oral = [df_Oral_Den_11_12, df_Oral_Den_13_14, df_Oral_Den_15_16, df_Oral_Den_17_18]

df_Oral_Den_11_18 = pd.concat(df_lis_oral)
df_Oral_Den_11_18_sli_1 = df_Oral_Den_11_18.filter(regex='^OHX[0-9][0-9]TC$')
df_Oral_Den_11_18_sli_2 = df_Oral_Den_11_18.filter(regex='^OHX[0-9][0-9]CTC$')
df_Oral_Den_11_18_sli_1.replace([1.0, 2.0, 3.0, 4.0, 5.0, 9.0, '.'], ['primary tooth (deciduous) present', 
                                                                      'permanent tooth present',
                                                                     'dental implant',
                                                                     'tooth not present',
                                                                     'permanent dental root fragment present',
                                                                     'could not assess',
                                                                     'missing'], inplace=True)
df_Oral_Den_11_18_sli_2.replace({'b\'A\'':'Primary tooth',
                                 'b\'D\'':'Sound primary tooth', 
                                 'b\'E\'':'Missing due to dental disease',
                                'b\'F\'':'Permanent tooth with a restored surface', 
                                'b\'J\'':'Permanent root tip, no restorative replacement',
                                 'b\'K\'':'Primary tooth with a dental carious surface',
                                'b\'M\'':'Missing due to other causes',
                                 'b\'P\'':'Missing due to dental disease, replaced by a removable restoration',
                                 'b\'Q\'':'Missing due to other causes, replaced by a removable restoration',
                                'b\'R\'':'Missing due to dental disease, replaced by a fixed restoration',
                                 'b\'S\'':'Sound permanent tooth', 
                                 'b\'T\'':'Permanent root tip, a restorative replacement',
                                'b\'U\'':'Unerupted', 
                                 'b\'X\'':'Missing due to other causes, replaced by a fixed restoration',
                                 'b\'Y\'':'Tooth present, condition cannot be assessed',
                                'b\'Z\'':'Permanent tooth with a dental carious surface',
                                 'b\'\'':'Missing'}, inplace=True)

df_Oral_Den_11_18_reshape = pd.concat([df_Oral_Den_11_18[['SEQN', 'OHDDESTS']], 
                                      df_Oral_Den_11_18_sli_1,
                                      df_Oral_Den_11_18_sli_2], axis=1)

df_Oral_Den_11_18_reshape = df_Oral_Den_11_18_reshape.assign(COHORT=['2011 - 2012'] * len(df_Oral_Den_11_12) +
                                                                    ['2013 - 2014'] * len(df_Oral_Den_13_14) +
                                                                    ['2015 - 2016'] * len(df_Oral_Den_15_16) +
                                                                    ['2017 - 2018'] * len(df_Oral_Den_17_18))
df_Oral_Den_11_18_reshape.rename(columns={"SEQN": "unique ids", 
                                          "OHDDESTS": "dentition status code", 
                                          "COHORT": "data year"}, inplace=True)
num_OHXxxTC = (df_Oral_Den_11_18.filter(regex='^OHX[0-9][0-9]TC$')).shape[1]
num_OHXxxCTC = (df_Oral_Den_11_18.filter(regex='^OHX[0-9][0-9]CTC$')).shape[1]
for i in range(2, 2+num_OHXxxTC):
    if i < 10:
        df_Oral_Den_11_18_reshape.rename(columns={'OHX0' + str(i - 1) + 'TC':'tooth_count#' + str(i - 1)}, inplace=True)
    else:
        df_Oral_Den_11_18_reshape.rename(columns={'OHX' + str(i - 1) + 'TC':'tooth_count#' + str(i - 1)}, inplace=True)
        
for i in range(2+num_OHXxxTC, 2+num_OHXxxTC+num_OHXxxCTC+3):
    if i < 2 + num_OHXxxTC + 10:
        df_Oral_Den_11_18_reshape.rename(columns={'OHX0' + str(i - num_OHXxxTC - 1) + 'CTC':'coronal_caries_tooth_count#' +
                                                 str(i - num_OHXxxTC - 1)}, inplace=True)
    else:
        df_Oral_Den_11_18_reshape.rename(columns={'OHX' + str(i - num_OHXxxTC - 1) + 'CTC':'coronal_caries_tooth_count#' +
                                                 str(i - num_OHXxxTC - 1)}, inplace=True)

df_Oral_Den_11_18_reshape.head(10)


# In[ ]:


df_Oral_Den_11_18_reshape['dentition status code'].replace([1.0, 2.0, 3.0, '.'], ['Complete', 'Partial', 'Not Done', 'Missing'], inplace=True)
df_Oral_Den_11_18_reshape.head(10)


# In[ ]:


print(df_Oral_Den_11_18_reshape['tooth_count#1'].unique())


# In[ ]:


df_Oral_Den_11_18_reshape.to_pickle('CDC_Oral_Den_11_18_df.pkl',
                               compression=None)


# c.

# In[ ]:


print(len(df_Demo_11_18_reshape))
print(len(df_Oral_Den_11_18_reshape))
# report the number of cases there are in the two datasets above 

