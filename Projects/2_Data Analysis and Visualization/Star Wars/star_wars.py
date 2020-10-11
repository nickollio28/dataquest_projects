#!/usr/bin/env python
# coding: utf-8

# # Star Wars Survey
# 
# The team at FiveThirtyEight collected data to answer the question "Does the rest of America realize that "The Empire Strikes Back" is clearly the best of the bunch?"
# 
# To answer this question, the team surveyed Star Wars fans using SurveyMonkey, and received 835 total responses, which is available on their [GitHub repository](https://github.com/fivethirtyeight/data/tree/master/star-wars-survey).
# 
# In this project, I will clean and explore the dataset to answer their question.

# In[16]:


import pandas as pd
star_wars = pd.read_csv('star_wars.csv', encoding = 'ISO-8859-1')
star_wars.shape[0]


# In[17]:


star_wars.head(10)


# In[18]:


star_wars.columns


# Remove null Respondent ID's

# In[19]:


star_wars = star_wars[pd.notnull(star_wars['RespondentID'])]
star_wars.head(10)


# Changing Yes and No answers in first two questions to True and False, so they are easier to work with

# In[20]:


yes_no = {'Yes': True, 'No': False}
star_wars['Have you seen any of the 6 films in the Star Wars franchise?'] = star_wars['Have you seen any of the 6 films in the Star Wars franchise?'].map(yes_no)
star_wars['Do you consider yourself to be a fan of the Star Wars film franchise?'] = star_wars['Do you consider yourself to be a fan of the Star Wars film franchise?'].map(yes_no)
star_wars.head(10)


# The next 6 columns represent a single checkbox question about which Star Wars movies the respondents have seen. I will map the movie names to boolean values, and rename the column names to something more readable

# In[22]:


for c in star_wars.columns[3:9]:
    print(star_wars[c].value_counts())


# In[24]:


import numpy as np
name_bool = {
    'Star Wars: Episode I  The Phantom Menace': True,
    'Star Wars: Episode II  Attack of the Clones': True,
    'Star Wars: Episode III  Revenge of the Sith': True,
    'Star Wars: Episode IV  A New Hope': True,
    'Star Wars: Episode V The Empire Strikes Back': True,
    'Star Wars: Episode VI Return of the Jedi': True,
    np.NaN: False
}
for c in star_wars.columns[3:9]:
    star_wars[c] = star_wars[c].map(name_bool)
star_wars.head(10)


# In[25]:


star_wars = star_wars.rename(columns={
    "Which of the following Star Wars films have you seen? Please select all that apply.": "seen_1",
    'Unnamed: 4': 'seen_2',
    'Unnamed: 5': 'seen_3',
    'Unnamed: 6': 'seen_4',
    'Unnamed: 7': 'seen_5',
    'Unnamed: 8': 'seen_6',
})


# In[26]:


star_wars.head(10)


# The next six columns ask the respondent to rank the Star Wars movies in order of least favorite to most favorite. 1 means the film was their most favorite, and 6 means the film was their least favorite.
# 
# I will convert the values to numeric type, and rename the columns.

# In[27]:


star_wars[star_wars.columns[9:15]] = star_wars[star_wars.columns[9:15]].astype(float)


# In[31]:


star_wars = star_wars.rename(columns={
    'Please rank the Star Wars films in order of preference with 1 being your favorite film in the franchise and 6 being your least favorite film.': 'ranking_1',
    'Unnamed: 10': 'ranking_2',
    'Unnamed: 11': 'ranking_3',
    'Unnamed: 12': 'ranking_4',
    'Unnamed: 13': 'ranking_5',
    'Unnamed: 14': 'ranking_6',
})
star_wars.columns


# Now I will find the average rankings of each movie

# In[39]:


get_ipython().magic('matplotlib inline')

star_wars.iloc[:,9:15].mean().plot.bar()


# Because rank 1 is the favorite overall and 6 is the least favorite, the team at FiveThirtyEight was correct in that most people enjoyed Episode V: Revenge of the Sith the most. All of the sequal movies were ranked higher than the prequels. The lowest ranked movie was Epsiode III: Revenge of the Sith.
# 
# The respondents seemed to like each successive prequel movie less and less. For the sequel movies, they liked Episode V the most, and Episode IV (the first Star Wars movie) the least, but still more than any of the prequels.
# 
# I will now create a bar chart to show how many people have seen each of the six movies.

# In[41]:


star_wars.iloc[:,3:9].sum().plot.bar()


# The most watched Star Wars movie was also Episode V: The Empire Strikes Back. 
# 
# Out of the prequels, each successive movie was seen less and less. For the sequels, the least seen was Episode IV. I found this strange that more people saw Episodes V and VI than Episode IV, since V and VI are sequels to IV.
# 
# I will now separate the rankings into groups based on gender, and plot the rankings for each gender.

# In[44]:


males = star_wars[star_wars['Gender'] == 'Male']
females = star_wars[star_wars['Gender'] == 'Female']

males.iloc[:,9:15].mean().plot.bar(title = 'Male Rankings')


# In[45]:


females.iloc[:,9:15].mean().plot.bar(title = 'Female Rankings')


# Both genders seemed to like the sequels better than the prequels, and liked Episode V: The Empire Strikes Back the most (remember, 1 is most liked). 
# 
# Males tended to rank the sequels higher than females, though, and the rankings for the prequels are approximately equal. Males also liked Episode IV and VI approximately equally, while females preferred Episode VI over IV. Also, males ranked the prequels approximately the same, while females liked Episode I the most and Episode III the least.

# In[ ]:




