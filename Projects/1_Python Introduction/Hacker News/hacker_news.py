#!/usr/bin/env python
# coding: utf-8

# # Exploring Hacker News Posts
# 
# I will explore data from Hacker News posts ([link](https://www.kaggle.com/hacker-news/hacker-news-posts)), especially those whos titles begin with Ask HN or Show HN. Ask HN is for users to ask a question, and Show HN is for users to show off their projects. 
# 
# I will compare Ask HN and Show HN posts to see which receives more comments on average. I will determine if posts created at a certain time receive more comments on average

# In[26]:


from csv import reader
hn = list(reader(open('hacker_news.csv')))
header = hn[0]
hn = hn[1:]
print(header)
print('\n')
for row in hn[0:5]:
    print(row)
    print('\n')
    


# In[36]:


# create lists for ask hn, show hn, and other

ask_posts = []
show_posts = []
other_posts = []

for row in hn:
    title = row[1]
    if title.lower().startswith('ask hn'):
        ask_posts.append(row)
    elif title.lower().startswith('show hn'):
        show_posts.append(row)
    else:
        other_posts.append(row)
        
print("length of ask_posts: ", len(ask_posts))
print("length of show_posts: ", len(show_posts))
print("length of other_posts: ", len(other_posts))


# In[33]:


total_ask_comments = 0
for row in ask_posts:
    total_ask_comments += int(row[4])
avg_ask_comments = round(total_ask_comments / len(ask_posts), 2)

total_show_comments = 0
for row in show_posts:
    total_show_comments += int(row[4])
avg_show_comments = round(total_show_comments / len(ask_posts), 2)

print("Average ask comments: ", avg_ask_comments)
print("Average show comments: ", avg_show_comments)


# Ask posts receive more than double the comments on average. 
# - this may be due to the fact that people are more willing to comment if they know the answer to someone's question than they are willing to comment on someone else's project where the poster isn't specifically looking for comments
# 
# Since ask posts receive more comments, we will focus on these.
# 
# Determine if posts created at a certain time are more likely to attract comments
#     - calculate amount of ask posts created in each hour of the day, along with number of comments received
#     - calculate average number of comments ask posts receive by hour created

# In[59]:


import datetime as dt
result_list = []
for row in ask_posts:
    created_at = row[6]
    num_comments = int(row[4])
    result_list.append([row[6], int(row[4])])

counts_by_hour = {}
comments_per_hour = {}
for row in result_list:
    date_time = dt.datetime.strptime(row[0], "%m/%d/%Y %H:%M")
    hour = dt.datetime.strftime(date_time, '%H')
    if hour not in counts_by_hour:
        counts_by_hour[hour] = 1
        comments_per_hour[hour] = row[1]
    else:
        counts_by_hour[hour] += 1
        comments_per_hour[hour] += row[1]
        
        
# use counts_by_hour and comments_per_hour to calculate average number of comments for post at each hour

avg_by_hour = []
for hour in comments_per_hour:
    avg_by_hour.append([hour, comments_per_hour[hour] / counts_by_hour[hour]])

from operator import itemgetter #sort
avg_by_hour.sort(key=lambda x: x[0])

print("Average comments per post, by hour: \n")
template = "{hour} - {comments} average comments"
for row in avg_by_hour:
    hour_e = dt.datetime.strptime(row[0],'%H')
    hour = dt.datetime.strftime(hour_e,'%H:%M')
    comments = round(row[1], 2)
    print(template.format(hour=hour, comments=comments))
    
    
avg_by_hour.sort(key=lambda x: x[1], reverse=True)    
print("\n\nTop 5 hours for Ask HN comments: \n")
for row in avg_by_hour[:5]:
    hour_e = dt.datetime.strptime(row[0],'%H')
    hour = dt.datetime.strftime(hour_e,'%H:%M')
    comments = round(row[1], 2)
    print(template.format(hour=hour, comments=comments))
    


# The [documentation](https://www.kaggle.com/hacker-news/hacker-news-posts) shows that these times are on EST
# 
# If you wanted to create a post that would get the most comments, your best bet is between 3:00 and 4:00 PM EST
# If you are a night owl, the second best time to receive comments would be between 2:00 and 3:00 AM EST
