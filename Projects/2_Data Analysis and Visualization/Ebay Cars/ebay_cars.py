#!/usr/bin/env python
# coding: utf-8

# # Exploring Ebay Car Sales Data
# 
# Data from eBay Kleinanzeigen, a classifieds section of German eBay site
# Dataset found [here](https://www.kaggle.com/orgesleka/used-cars-database/data)
#     - data is clean - it has been modified to more closely resemble a scraped dataset
# I will clean the data and analyse the used car listings using panda

# In[97]:


import pandas as pd
import numpy as np
autos = pd.read_csv('autos.csv', encoding = 'Latin-1')


# In[98]:


autos


# In[99]:


autos.info()
autos.head()


# Autos dataset contains 20 columns, most of which are strings
# Some columns have null values, but none have > 20% null values
# Column names use camelcase instead of snakecase - cannot replace spaces with underscores
# 
# 1) convert camelcase to snakecase and reword some of the column names to be more descriptive based on the data dictionary
# 

# In[100]:


autos.columns


# In[101]:


new_cols = ['date_crawled', 'name', 'seller', 'offer_type', 'price', 'abtest',
       'vehicle_type', 'registration_year', 'gearbox', 'power_ps', 'model',
       'odometer', 'registration_month', 'fuel_type', 'brand',
       'unrepaired_damage', 'ad_created', 'nr_of_pictures', 'postal_code',
       'last_seen']
autos.columns = new_cols
autos.columns


# Column names changed
# 
# Now, explore data to see if more cleaning needed
# 
# 2) Look for:
#     - text columns where (almost) all the values are the same - not useful for analysis
#     - examples of numeric data stored as text which can be cleaned and converted

# In[102]:


autos.describe(include = 'all')


# columns with potentially mostly one value - 2 unique and 49999 freq:
#     - seller
#     - offer_type
#     

# In[103]:


autos['seller'].value_counts()


# In[104]:


autos.drop('seller', axis=1, inplace=True)


# In[105]:


autos['offer_type'].value_counts()


# In[106]:


autos.drop('offer_type', axis=1, inplace=True)


# new dataframe:

# In[107]:


autos.describe(include='all')


# In[108]:


autos


# clean price and odometer columns because they have numeric data stored as text

# In[109]:


autos['price'] = autos['price'].str.replace('$','').str.replace(',','').astype(int)
autos.rename(columns={'price':'price_$'}, inplace=True)


# In[110]:


autos['odometer']=autos['odometer'].str.replace('km', '').str.replace(',','').astype(int)
autos.rename(columns={'odometer':'odometer_km'}, inplace=True)


# In[111]:


autos['price_$'].head()


# In[112]:


autos['odometer_km'].head()


# analyze odometer and price columns to look for outliers

# In[113]:


autos['odometer_km'].value_counts().sort_index(ascending=False)


# no max outliers for odometer

# In[114]:


autos['odometer_km'].value_counts().sort_index()


# no min outliers for odometer

# In[115]:


autos['price_$'].describe()


# In[116]:


autos['price_$'].value_counts().sort_index(ascending=False).head(50)


# some cars have abnormally high prices in the millions of dollars. These should be removed.
# 
# $350,000 is still high but I will remove all cars priced higher than this to start and check the description

# In[117]:


autos[autos['price_$'] > 350000]


# In[118]:


autos[~(autos['price_$'] > 350000)].shape[0]


# In[119]:


autos = autos[~(autos['price_$'] > 350000)]


# In[120]:


autos.shape[0]


# In[121]:


autos['price_$'].describe()


# In[122]:


autos['price_$'].value_counts().sort_index(ascending=False).head(50)


# In[123]:


autos[autos['price_$'] > 70000].shape[0]


# 82 cars over $70,000, will check to see if worth deleting 

# In[124]:


autos_check = autos[~(autos['price_$'] > 70000)]


# In[125]:


autos_check.shape[0]


# In[126]:


autos_check['price_$'].describe()


# barely changed the mean, changed std deviation by ~2,000. Will not remove cars over 1k

# In[127]:


autos['price_$'].value_counts().sort_index().head(50)


# will remove cars at 0 but keep cars at price >= 1

# In[128]:


autos_check = autos[autos['price_$'] > 0]


# In[129]:


autos_check['price_$'].describe()


# In[130]:


autos = autos[autos['price_$'] > 0]


# removed free cars from dataframe

# In[131]:


autos


# 5 columns referring to dates
# from data dictionary:
#     - `date_crawled`: added by the crawler
#     - `last_seen`: added by the crawler
#     - `ad_created`: from the website
#     - `registration_month`: from the website
#     - `registration_year`: from the website
# 
# date_crawled, last_seen, and ad_created all identified as string values - need to convert to numerical representation
# resistration month and year represented as numeric values
# 
# string values all in timestamp form. We care about the date and not the time
#     - instead of using datetime we could easily estract the date using the first 10 characters
#     
# date_crawled:

# In[132]:


date_crawled = autos['date_crawled'].str[:10]


# In[133]:


date_crawled[0:5]


# In[134]:


date_crawled.value_counts(normalize=True, dropna=False).sort_index() * 100


# In[135]:


date_crawled.describe()


# In date_crawled, each date crawled approx. 3% of the total data. There are 34 total dates where data was crawled
# 
# last_seen:

# In[136]:


last_seen = autos['last_seen'].str[:10]


# In[137]:


last_seen.value_counts(normalize=True, dropna=False).sort_index() * 100


# In[138]:


last_seen.describe()


# last seen dates are the same as dates crawled because they both were added by the crawler
# the amount of cars last seen seem to increase as time goes on, which makes sense
# the top three dates for last seen were in the past last three days of crawling
# 
# ad_created:

# In[139]:


ad_created = autos['ad_created'].str[:10]


# In[140]:


ad_created.value_counts(normalize=True, dropna=False).sort_index() * 100


# In[141]:


ad_created.describe()


# ad_created contains 76 dates. it seems that more ads were created later in the year, and barely any were created earlier in the year

# In[142]:


autos['registration_year'].describe()


# In[143]:


autos['registration_year'].value_counts().sort_index()


# registration year has outliers that are impossible. I will remove them

# In[144]:


autos = autos[~((autos['registration_year'] < 1910) | (autos['registration_year'] > 2020))]


# In[147]:


autos['registration_year'].value_counts(normalize=True).sort_index() * 100


# In[146]:


autos['registration_year'].describe()


# average car registration year is around may 2003, +- 7.5 years
# 
# To analyse the brand column, I will use aggregation:

# In[172]:


brand_value_counts = autos['brand'].value_counts(normalize=True).sort_index() * 100
brand_value_counts


# In[174]:


brand_index = autos['brand'].value_counts().sort_index().index
brand_index


# will aggregate only the brands that make up > 1% of the total

# In[177]:


agg_brands = []
for brand in brand_index:
    if brand_value_counts[brand] > 1:
        agg_brands.append(brand)
print(agg_brands)


# In[196]:


brands_dict = {}
for brand in agg_brands:
    brand_prices = autos[autos['brand'] == brand]['price_$']
    brands_dict[brand] = round(brand_prices.mean(),2)
    
print(brands_dict)


# In[220]:


avg_price = pd.Series(brands_dict)
avg_price.sort_values(ascending = False)


# Of the common brands on the site, Audi is the most expensive, with Mercedes Benz and BMW following close behind. Renault, Fiat, and Opel are the three least expensive brands
# 
# Now I will compare these average brand prices to their average milages to see if there is a correlation between milage and price

# In[221]:


odometer_dict = {}
for brand in agg_brands:
    brand_odometer = autos[autos['brand'] == brand]['odometer_km']
    odometer_dict[brand] = round(brand_odometer.mean(),2)
    
print(odometer_dict)


# In[227]:


avg_miles = pd.Series(odometer_dict)
price_miles = pd.DataFrame(avg_price, columns = ['mean_price'])
price_miles['mean_miles'] = avg_miles
price_miles


# It appears that milage doesn't affect price by a whole lot. The most expensive brands have some of the highest miles in the DataFrame, and Smart car with the lowest miles is has one of the lowest average prices.
# 
# This should have been expected. People with expensive car brands with low miles tend to sell on places other than eBay, so the expensive brands will naturally have high milage. 

# In[ ]:




