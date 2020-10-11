#!/usr/bin/env python
# coding: utf-8

# # Clean and Analyze Employee Exit Surveys
# 
# I will work with exit surveys from employees of the Deptartment of Education, Training and Employment (DETE) and the Technical and Further Education (TAFE) institute in Queensland, Austrailia. You can find the DETE survey [here](https://data.gov.au/dataset/ds-qld-fe96ff30-d157-4a81-851d-215f2a0fe26d/details?q=exit%20survey) and the TAFE surver [here](https://data.gov.au/dataset/ds-qld-89970a3b-182b-41ea-aea2-6f9f17b5907e/details?q=exit%20survey).
# 
# In this project, I will play the role of a data analyst and pretend the stockholders want to know whether employees who worked for the institutes for a short period of time resign due to some kind of dissatisfaction.
# 
# They want me to combine the results of both surveys to answer these questions. However, although both used the same survey template, one of them customized some of the answers. I will clean the data, then get to analyzing the questions.

# In[4]:


import pandas as pd
import numpy as np
dete_survey = pd.read_csv('dete_survey.csv')
tafe_survey = pd.read_csv('tafe_survey.csv')

print('DETE survey:')
dete_survey.info()
dete_survey.head()


# In[5]:


print('\nTAFE survey:')
tafe_survey.info()
tafe_survey.head()


# 1) dete_survey df contains 'Not Stated' values indicating they are missing, but aren't represented as NaN
# 
# 2) both df's contain many columns I don't need for my analysis
# 
# 3) each df contains many of the same columns, but with different column names
# 
# 4) there are multiple columns/answers that indicate an employee resigned because they were dissatisfied
# 
# _________________________________________________________________________________________________________
# 
# 1) use pandas read_csv function to specify values that should be represented as NaN
#  - use this to fix missing values first, then drop col's that are unnecessary for analysis

# In[6]:


dete_survey = pd.read_csv('dete_survey.csv', na_values='Not Stated')


# In[9]:


dete_survey_updated = dete_survey.drop(dete_survey.columns[28:49], axis=1)
tafe_survey_updated = tafe_survey.drop(tafe_survey.columns[17:66], axis=1)


# In[14]:


dete_survey_updated.info()


# In[13]:


tafe_survey_updated.info()


# missing values in dete_survey fixed, unnecessary columns from both surveys dropped, and assigned to updated df
# 
# now I will normalize the df's column names so they can eventually be combined

# In[15]:


dete_survey_updated.columns = dete_survey_updated.columns.str.lower().str.strip().str.replace(' ','_')
dete_survey_updated.columns


# In[18]:


tafe_survey_updated.columns


# In[23]:


tafe_survey_updated = tafe_survey_updated.rename(columns={'Record ID': 'id', 
                                    'CESSATION YEAR': 'cease_date', 
                                    'Reason for ceasing employment': 'separationtype',
                                    'Gender. What is your Gender?': 'gender',
                                    'CurrentAge. Current Age': 'age',
                                    'Employment Type. Employment Type': 'employment_status',
                                    'Classification. Classification': 'position',
                                    'LengthofServiceOverall. Overall Length of Service at Institute (in years)': 'institute_service',
                                    'LengthofServiceCurrent. Length of Service at current workplace (in years)': 'role_service'
                                   })


# In[21]:


dete_survey_updated.head()


# In[24]:


tafe_survey_updated.head()


# In dete survey, I changed all capitalization to lowercase, removed and trailing whitespace from the end of the strings, and replaced spaces with underscores. In tafe survey, I changed the names of columns that had equivalent columns in dete survey to those names, as well as a few others to shorter names. I left a few of the column names as is, and will handle them later.

# The end goal is to answer whether employees resigned due to some kind of dissatisfaction. So we will remove rows where the separationtype is not resigned.

# In[25]:


dete_survey_updated['separationtype'].value_counts()


# In[27]:


tafe_survey_updated['separationtype'].value_counts()


# dete survey has multiple types of resignation, and I will have to account for these so I don't unintentionally drop data

# In[28]:


dete_resignations = dete_survey_updated.copy()[(dete_survey_updated['separationtype']=='Resignation-Other reasons') | 
                                               (dete_survey_updated['separationtype']=='Resignation-Other employer') |
                                               (dete_survey_updated['separationtype']=='Resignation-Move overseas/interstate')]


# In[30]:


tafe_resignations = tafe_survey_updated.copy()[tafe_survey_updated['separationtype'] == 'Resignation']


# In[31]:


dete_resignations.head()


# In[32]:


tafe_resignations.head()


# new df's created that only contain employees who have resigned.

# Now I will verify that the data doesn't contain any major inconsistencies. 
# 
# - verify that years in cease_date and dete_start_date columns make sense
#     - both columns must have years before the current date
#     - unlikely that dete_start_date is sometime before 1940
#     
#     

# In[33]:


dete_resignations['cease_date'].value_counts()


# In[38]:


years = dete_resignations['cease_date'].str.split('/').str.get(-1).astype(float)
years.value_counts()


# In[39]:


dete_resignations['cease_date'] = years


# In[40]:


dete_resignations['cease_date'].value_counts()


# In[41]:


dete_resignations['dete_start_date'].value_counts()


# In[42]:


tafe_resignations['cease_date'].value_counts()


# All of the cease dates for both df's is in recent years. The dete start dates are all reasonable years.

# We are trying to figure out whether employees who have worked for a short time resigned due to a dissatisfaction and the same with employees who have worked for a long time. Tafe_resignations already has a column for length of time an employee worked there, institute_service, so I will create the same column for dete_resignations

# In[43]:


dete_resignations['institute_service'] = dete_resignations['cease_date'] - dete_resignations['dete_start_date']


# In[44]:


dete_resignations['institute_service'].head()


# Now that we have the institute_service column in both df's, we will identify employees who resigned because they were dissatisfied. Below are the columns we'll use to categorize employees as'dissatisfied' from each df:
# 
#     tafe_survey_updated:
#         Contributing Factors. Dissatisfaction
#         Contributing Factors. Job Dissatisfaction
#     dete_survey_updated:
#         job_dissatisfaction
#         dissatisfaction_with_the_department
#         physical_work_environment
#         lack_of_recognition
#         lack_of_job_security
#         work_location
#         employment_conditions
#         work_life_balance
#         workload
# 
# If an employee indicated any of these factors caused them to resign, mark them as disssatisfied in a new column:

# In[46]:


tafe_resignations['Contributing Factors. Dissatisfaction'].value_counts()


# In[47]:


tafe_resignations['Contributing Factors. Job Dissatisfaction'].value_counts()


# In[51]:


def update_vals(val):
    if pd.isnull(val):
        return np.nan
    elif val=='-':
        return False
    else:
        return True
    
tafe_resignations[['Contributing Factors. Dissatisfaction','Contributing Factors. Job Dissatisfaction']] = tafe_resignations[['Contributing Factors. Dissatisfaction','Contributing Factors. Job Dissatisfaction']].applymap(update_vals)


# In[58]:


tafe_resignations['dissatisfied'] = tafe_resignations[['Contributing Factors. Dissatisfaction','Contributing Factors. Job Dissatisfaction']].any(axis=1, skipna=False)


# In[60]:


ds_cols = ['job_dissatisfaction', 'dissatisfaction_with_the_department', 'physical_work_environment', 
            'lack_of_recognition', 'lack_of_job_security', 'work_location', 'employment_conditions', 
            'work_life_balance', 'workload']
dete_resignations[ds_cols] = dete_resignations[ds_cols].applymap(update_vals)


# In[68]:


dete_resignations['dissatisfaction']=dete_resignations[ds_cols].any(axis=1, skipna=False)
dete_resignations['dissatisfaction_with_the_department'].value_counts()


# In[69]:


dete_resignations[ds_cols] = dete_survey_updated[ds_cols]
dete_resignations[ds_cols].head()


# Ran update_vals on dete_resignations when values were already in T/F form, which turned them all to true. Reassigned them their values from dete_survey_updated.  Will use df.any method to create dissatisfaction column

# In[100]:


dete_resignations['dissatisfied']=dete_resignations[ds_cols].any(axis=1, skipna=False)
dete_resignations['dissatisfied'].head()


# In[101]:


dete_resignations_up = dete_resignations.copy()
tafe_resignations_up = tafe_resignations.copy()


# At this point, I have:
# - renamed columns
# - dropped any data not needed for analysis
# - verified the quality of data
# - created a new 'institute_service' column
# - cleaned the 'Contributing Factors' column
# - created a new column indicating if an employee resigned because they were dissatisfied in some way
# 
# now, it is time to combine the datasets
# 
# first, add column to each df to allow us to distinguish between the two

# In[102]:


dete_resignations_up['institute'] = 'DETE'
tafe_resignations_up['institute'] = 'TAFE'


# In[103]:


combined = pd.concat([dete_resignations_up, tafe_resignations_up])
combined.info()


# In[105]:


combined_updated = combined.dropna(thresh=500, axis=1)


# In[106]:


combined_updated.info()


# dropped columns with less than 500 non-null objects because they were not needed to complete our analysis
# 
# now, I will clean the 'institute_service' column to use new definitions:
# - new: less than 3 years at the company
# - experienced: 3-6 years at the company
# - established: 7-10 years at the company
# - veteran: 11+ years at the company

# In[107]:


combined_updated['institute_service'].value_counts()


# In[108]:


combined_updated['institute_service'] = combined_updated.copy()['institute_service'].astype('str').str.replace('Less than 1 year', '1').str.replace('More than 20 years', '20').str.split('-').str.get(-1).astype('float')
combined_updated['institute_service'].value_counts()


# In[109]:


def update_service_cat(val):
    if pd.isnull(val):
        return np.nan
    elif val < 3.0:
        return 'New'
    elif val < 6.0:
        return 'Experienced'
    elif val < 10.0:
        return 'Established'
    else:
        return 'Veteran'

combined_updated['service_cat'] = combined_updated['institute_service'].apply(update_service_cat)
combined_updated['service_cat'].value_counts()


# I have cleaned the 'institute_service' column and have now created a new column 'service_cat' that shows whether an employee is new, experiences, established, or a veteran.

# In[113]:


combined_updated['dissatisfied'].value_counts(dropna=False)


# In[115]:


combined_updated['dissatisfied'] = combined_updated['dissatisfied'].fillna(False)


# In[116]:


combined_updated['dissatisfied'].value_counts()


# In[119]:


pv_combined = combined_updated.pivot_table(index='service_cat', values='dissatisfied')
pv_combined


# since true is considered to be 1 in a pivot table, calculating the mean of dissatisfied gives the percentage of dissatisfied employeed for each category

# In[120]:


get_ipython().magic('matplotlib inline')


# In[126]:


pv_combined.plot(kind='bar')


# The shareholders question has been answered: The long term employees, those in the established or veteran categories, are the most dissatisfied, while the new employees were the least dissatisfied.

# In[ ]:




