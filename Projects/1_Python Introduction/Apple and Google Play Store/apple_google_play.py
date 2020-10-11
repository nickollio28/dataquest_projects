#!/usr/bin/env python
# coding: utf-8

# # Profitable App Profiles for the App Store and Google Play Markets
# 
# For this project, we'll pretend we're working as data analysts for a company that builds Android and iOS mobile apps. We make our apps available on Google Play and the App Store.
# 
# We only build apps that are free to download and install, and our main source of revenue consists of in-app ads. This means our revenue for any given app is mostly influenced by the number of users who use our app — the more users that see and engage with the ads, the better. Our goal for this project is to analyze data to help our developers understand what type of apps are likely to attract more users.

# In[1]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# File links: 
# - [Apple Store](https://dq-content.s3.amazonaws.com/350/AppleStore.csv), [Documentation](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps)
# - [Google Play Store](https://dq-content.s3.amazonaws.com/350/googleplaystore.csv), [Documentation](https://www.kaggle.com/lava18/google-play-store-apps)
# 
# 

# In[2]:


opened_file_apple = open('AppleStore.csv', encoding = 'utf8')
opened_file_google = open('googleplaystore.csv', encoding = 'utf8')
from csv import reader
read_file_apple = reader(opened_file_apple)
read_file_google = reader(opened_file_google)
apps_data_apple = list(read_file_apple)
apps_data_google = list(read_file_google)

#split into header and data pieces
header_apple = apps_data_apple[0]
data_apple = apps_data_apple[1:]
header_google = apps_data_google[0]
data_google = apps_data_google[1:]

#display slice of data
print('Apple Data slice \n')
print(header_apple)
print('\n')
explore_data(data_apple, 0, 5, True)
print('\n \n Google Data slice \n')
print(header_google)
print('\n')
explore_data(data_google, 0, 5, True)



# 
# 
# # Data cleaning:
# [Google Play Discussion section](https://www.kaggle.com/lava18/google-play-store-apps/discussion/66015) describes error in entry 10472 - "this entry has missing 'Rating' and a column shift happened for next columns..
# 10472 Life Made WI-Fi Touchscreen Photo Frame 1.9 19.0 3.0M 1,000+ Free 0 Everyone NaN February 11, 2018 1.0.19 4.0 and up NaN"

# In[3]:


#preview entry
print(data_google[10472])


# In[4]:


#error is there - delete row
del data_google[10472]


# In[34]:


#check for other entries with missing columns
def row_check(data_set_list, store):

    selected_store = ''
    length = 0

    if store == 'google':
        selected_store, length = 'google', 13
    elif store == 'apple':
        selected_store, length = 'apple', 16
    else:
        return print('Wrong App Store Name')

    for row in data_set_list:
        if len(row) != length:
            print(row)


row_check(data_google, 'google')
row_check(data_apple, 'apple')


# All other rows correct
# 
# Check for duplicate entries

# In[36]:


def duplicate_entries_count(data,n):
    duplicate_entries=[]
    unique_entries=[]
    duplicate_entries_freq={}
    for row in data:
        name=row[n]
        if name in unique_entries:
            duplicate_entries.append(name)
        else:
            unique_entries.append(name)
    for name in duplicate_entries:    
        if name in duplicate_entries_freq:
            duplicate_entries_freq[name]+=1
        else:
            duplicate_entries_freq[name]=2
    print('length of duplicate entries:',len(duplicate_entries),'\n', 'length of unique entries:', len(unique_entries))
    print('Duplicate Entries Frequency Table:',duplicate_entries_freq)

    
print('\n','Google Dataset Duplicate Data','\n')
duplicate_entries_count(data_google,0)
print('\n','Apple Dataset Duplicate Data','\n')
duplicate_entries_count(data_apple,1)


# 1181 duplicate entries for google, 2 duplicate entries for apple
# 
# Need to remove duplicates. Duplicate entries vary in their number of reviews. Instead of randomly removing them, we will keep the entry with the highest number of reviews, since that is likely the most recent.
# 
# - Create dictionary, where key is app name and value is highest number of reviews of that app
# - Use the information stored in the dictionary and create a new data set, which will have only one entry per app, and for each app, we'll only select the entry with the highest number of reviews

# In[40]:


def max_reviews_dict(data, apple_or_google):
    reviews_max = {}
    if apple_or_google == 'Apple':
        name_id = 1
        review_id = 5
    elif apple_or_google == 'Google':
        name_id = 0
        review_id = 3
        
    for row in data:
        name = row[name_id]
        num_reviews = float(row[review_id])
        if (name in reviews_max and reviews_max[name] < num_reviews) or (name not in reviews_max):
            reviews_max[name] = num_reviews

    print('length of ', apple_or_google, ' reviews_max dictionary: ', len(reviews_max))
    
    return reviews_max

def remove_duplicates(data, apple_or_google):
    if apple_or_google == 'Apple':
        name_id = 1
        review_id = 5
    elif apple_or_google == 'Google':
        name_id = 0
        review_id = 3
    
    reviews_dict = max_reviews_dict(data, apple_or_google)
    clean = []
    already_added = []
    for row in data:
        name = row[name_id]
        num_reviews = float(row[review_id])
        if num_reviews == reviews_dict[name] and name not in already_added:
            clean.append(row)
            already_added.append(name)
    
    print('length of ', apple_or_google, ' unique list: ', len(clean))
    
    return clean
        
        
data_apple_unique = remove_duplicates(data_apple, 'Apple')
data_google_unique = remove_duplicates(data_google, 'Google')


# new unique list has correct number of entries - duplicates removed
# 
# Now remove apps that are not directed at English speaking audience:
# - if entries have > 3 letters outside english language (> ASCII 0 - 127), remove it
#     - some entries may have trademark logo, emojis, etc. so only remove if > 3 letters not 0-127
# 

# In[42]:


def check_non_english(name):
    i = 0
    for letter in name:
        if ord(letter) > 127:
            i += 1
    if i > 3:
        return False
    else:
        return True


def remove_non_english(data, n):
    data_english = []
    for row in data:
        name = row[n]
        if check_non_english(name) == True:
            data_english.append(row)
    return data_english

data_apple_en = remove_non_english(data_apple_unique, 1)
data_google_en = remove_non_english(data_google_unique, 0)
        

print('length of unique english apple data: ', len(data_apple_en))
print('length of unique english google data: ', len(data_google_en))


    


# So far, have removed:
# - inaccuracte data
# - duplicate entries
# - non-English apps
# 
# As mentioned in intro, we only build apps that are free to download
# - isolate only the free apps

# In[50]:


def remove_paid(data, apple_or_google):        
    data_free = []    
    for row in data:
        if apple_or_google == 'Apple':
            price_id = 4
            price = float(row[price_id])
        elif apple_or_google == 'Google':
            price_id = 6
            if row[price_id] == 'Free':
                price = 0.0
            else:
                price = 1.0
        if price == 0.0:
            data_free.append(row)
    return data_free

data_apple_clean = remove_paid(data_apple_en, 'Apple')
data_google_clean = remove_paid(data_google_en, 'Google')

print('Length of cleaned Apple data: ', len(data_apple_clean))
print('Length of cleaned Google data: ', len(data_google_clean))


# Finished cleaning data
# 
# Now time to analyze:
# - find app profile that is successful on both iOS and Android
#     - strategy for app idea:
#         - build minimal android version of app and add it to Google Play Store
#         - if app has good response, develop it further
#         - if app profitable after 6 months, build iOS version and add it to App Store
# - start by finding what most common genres are for each market
#     - build frequency tables for a few columns of data sets

# In[52]:


print(header_apple, '\n\n', header_google)


# categories to use: 
# - apple: prime_genre (11)
# - google: Category (1), Genres (9)
# 
# other useful categories:
# - appple: track_name (1), rating_count_tot (5), user_rating (7), prime_genre (11)
# - google: App (0), Category (1), Rating (2), Reviews (3), Installs (4)
# 
# 
# build two functions to analyse frequency tables:
# - function to generate freq tables that show percentages
# - function to display percentages in descending order
#     - transform dictionary into list of tuples, each tuple contains key and value
#         - value first, key second so sortig works
# 

# In[58]:


def freq_table(dataset, index):
    frequency_table = {}
    frequency_table_percent = {}
    for row in dataset:
        name = row[index]
        if name in frequency_table:
            frequency_table[name] += 1
        else:
            frequency_table[name] = 1
    total = 0        
    for name in frequency_table:
        total += frequency_table[name]
    
    for name in frequency_table:
        frequency_table_percent[name] = frequency_table[name] / total * 100
    
    return frequency_table_percent
    
def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', round(entry[0], 2), '%')
        
print('Apple prime_genre frequency table: ', '\n')
display_table(data_apple_clean, 11)
print('\n','Google Category frequency table: ', '\n')
display_table(data_google_clean, 1)
print('\n','Google Genres frequency table: ', '\n')
display_table(data_google_clean, 9)


# Analyze:
# - Apple:
#     - most common genre: Games
#     - second most common genre: Entertainment
#     - most popular genres are for entertainment purposes (games, entertainment, photo and video, social networking, sports, music)
#     - apps for practical purposes (education, shopping, utilities, productivity, lifestyle) not as common
#     - even though a genre is very common doesn't mean it has large number of users
#         - games most popular, and would be hard to break into
#         - most users still use less common genres such as social networking, photo & video, and music - would be easier to get a user base
#        
# - Google Play:
#     - most common category: Family
#     - second most common category: Game
#     
#     - most common genre: Tools
#     - second most common genre: Entertainment
#     - most common categories and genres are for practical purposes (education, shopping, utilities, productivity, lifestyle)
#     - on Android, you can customize your phone with apps much more than with iPhone
#         - many practical apps on Android may not be able to cross over to iOS
#             - can still be profitable on Android
#         - games not as common - can release game on Android where it has higher chance of gaining popularity
#             - transfer over to iOS once its already popular, and it can compete with their large population of gaming apps
#             
# 
# 
# Proportions of apps are useful, but we will need to see which apps have most users as well
#     - Google: Installs (5)
#     - Apple: rating_count_total (5)
#     
# Apple App Store - calculate average number of user ratings per genre
#     - isolate apps of each genre
#     - sum up user ratings for apps of that genre
#     - divide sum by number of apps in that genre
#     
#     
#     

# In[65]:


frequency_table = freq_table(data_apple_clean, 11)
freq_table_ratings = {}
for genre in frequency_table:
    total = 0
    len_genre = 0
    for row in data_apple_clean:
        genre_app = row[11]
        if genre_app == genre:
            num_ratings = float(row[5])
            total += num_ratings
            len_genre += 1
    avg_num_ratings = round(total / len_genre, 2)
    freq_table_ratings[genre] = avg_num_ratings

table_display = []
for key in freq_table_ratings:
        key_val_as_tuple = (freq_table_ratings[key], key)
        table_display.append(key_val_as_tuple)

table_sorted = sorted(table_display, reverse = True)
for entry in table_sorted:
    print(entry[1], ':', round(entry[0], 2))            


# In Apple App Store, navigation seems to be the most commonly used, with reference and social networking following closely behind.
# - Navigation takes up only 0.19% of apple store apps, but is the most reviewed. This suggests that many users use a small amount of navigation apps. This seems like a good candidate for an app because there will be a large potential customer base with a small amount of competition
# - Reference is similar, though it will have over twice the competition (makes up 0.56% of app store) and approx. 13% lower customer base than navigation
#     - However, users may be more likely to download a new reference app than a navigation app. Many users may be uninterested in switching up their navigation apps, but may be interested in obtaining a new reference app.
# - Social networking and music also have large customer bases, however they take up a larger portion of the app store so there will be much more competition as well
# 
# 
# 
# 
# Google's Installs column may be a more accurate metric than Apple's number of ratings, however this metric is not very precise because it contains open-ended values (100+, 1000+, 5000+, etc.). This should work well enough to get an accurate picture, though. We will assume that 100,000+ will be 100,000, 10,000+ will be 10,000, etc.
# 
# - will need to take out commas and plus signs
# 
#     
#     
# 

# In[70]:


frequency_table = freq_table(data_google_clean, 1)
freq_table_installs = {}
for category in frequency_table:
    total = 0
    len_category = 0
    for row in data_google_clean:
        category_app = row[1]
        if category_app == category:
            num_installs = row[5]
            num_installs = num_installs.replace('+', '')
            num_installs = num_installs.replace(',', '')
            num_installs = float(num_installs)
            total += num_installs
            len_category += 1
    avg_num_installs = round(total / len_category, 2)
    freq_table_installs[category] = avg_num_installs

table_display = []
for key in freq_table_installs:
        key_val_as_tuple = (freq_table_installs[key], key)
        table_display.append(key_val_as_tuple)

table_sorted = sorted(table_display, reverse = True)
for entry in table_sorted:
    print(entry[1], ':', round(entry[0], 2))  


# In the Google Play Store, communication is by far the most commonly installed. This category makes up 3.24% of the Google Play Store, which is not very high but not very low either. It may be difficult to get people to switch to new modes of communication, and it may be difficult to make money off ads from communication apps because users would be annoyed with ads when theyre trying to message. 
# 
# Video players and social media have the second and third most installs and make up 1.79% and 2.66% of the Google Play Store, respectively. These may be better suited for our profit motive because ads are very common on these platforms, and they have a lot of potential users with a relatively small amount of competition. Video players and social media will also transfer over to iOS better than many of the common apps on the google play store such as productivity apps, as they don't require any special permissions that users are able to give on android but not iOS.
# 
# 
# # Summary
# Overall, I would recommend creating a video player or social media app. They will give us a large potential customer base, and have a relatively small amount of competition. These genres are also well suited for ads.
# 
# Games are also a genre to consider, however the Apple App Store has a large amount of competition and it may be tough to gain a large enough user base to become profitable.

# In[ ]:




