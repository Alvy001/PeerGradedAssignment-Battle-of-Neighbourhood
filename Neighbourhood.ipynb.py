#!/usr/bin/env python
# coding: utf-8

# # Capstone Project — The Battle of Neighbourhoods
# 
# ## **Introduction**
# 
# **Noida**, short for **New Okhla Industrial Development Authority**, is a planned city located in Gautam Buddh Nagar district of the Indian state of Uttar Pradesh. It is a satellite city of Delhi and is a part of the National Capital Region of India. As per provisional reports of Census of India, the population of Noida in 2011 was 642,381. 
# The official language of Noida and the one that is most widely spoken is Hindi.
# With its diverse culture, comes diverse food items. There are many restaurants in Noida, each belonging to different categories like Chinese, Italian, French etc. So as part of this project, we will list and visualise all major parts of Noida.
# 
# **Questions that can be asked using the above-mentioned datasets**
# 
#  - Which places In Noida have some of the finest Restaurants?
#  - Which Places in Noida have Restaurants with Lowest rating?
#  - Which place in Noida is suitable for a Foodie?
#  - Which place in Noida is not suitable for a Foodie?
#  - What are the best places in Noida for Chinese Restaurant?
#  - Which places in Noida have highest rated Chinese Restaurants?
# 
# ## **Data**
# 
# For this project we need the following data:
# 
# - Noida Restaurants data that contains list Locality, Restaurant name, Rating along with their  latitude and longitude.	
#      - Data Source: [zomatoKaggle](https://www.kaggle.com/shrutimehta/zomato-restaurants-data)
#      - Description: This data set contains the required information which we will use to explore various localities of Noida city.
# - Nearby places in each locality of Noida city.
#     - Data Source: [FourSquareAPI](https://developer.foursquare.com)
#     - Description: By using this API we will get all the venues in each neighbourhood.
# 
# ## **Approach**
# 
# - Collect the Noida city data from [zomatoKaggle](https://www.kaggle.com/shrutimehta/zomato-restaurants-data)
# - Using Foursquare API we will find all venues for each neighbourhoods.
# - Filter out all venues that are nearby by locality.
# - Using aggregative rating for each restaurant to find the best places.
# - Visualize the Ranking of neighbourhoods using folium library(python)
# 

# In[54]:


import pandas as pd
import numpy as np
import requests # library to handle requests
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe
# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors
# import k-means from clustering stage
from sklearn.cluster import KMeans

get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes ')
import folium # map rendering library
get_ipython().system(' pip install geocoder')
import geocoder


# 
# ## Read the zomato resturant data from csv file

# In[57]:


df = pd.read_csv('https://raw.githubusercontent.com/Alvy001/PeerGradedAssignment-Battle-of-Neighbourhood/main/zomato.csv',encoding='ISO-8859-1')
df.head()


# In[58]:


df_india = df[df['Country Code'] == 1]
df_Nda = df_india[df_india['City'] == 'Noida']
df_Nda.reset_index(drop=True, inplace=True)
df_Nda.head()


# ## Data Cleaning
# 
# Remove the unwanted columns and rows from dataset

# In[59]:


df_Res= df_Nda[df_Nda.Longitude !=0.000000][['Restaurant Name','Locality','Longitude','Latitude','Cuisines','Aggregate rating','Rating text','Votes']]


# In[60]:


df_Res = df_Res[df_Res['Aggregate rating'] !=0.0]


# In[61]:


df_Res.head()


# ## Creating Map to show the Restaurant clusters

# In[62]:


Noida_Rest = folium.Map(location=[28.60, 77.25], zoom_start=12)

X = df_Res['Latitude']
Y = df_Res['Longitude']
Z = np.stack((X, Y), axis=1)

kmeans = KMeans(n_clusters=5, random_state=0).fit(Z)

clusters = kmeans.labels_
colors = ['red', 'green', 'blue', 'yellow','orange']
df_Res ['Cluster'] = clusters

for latitude, longitude, Locality, cluster in zip(df_Res['Latitude'], df_Res['Longitude'], df_Res['Locality'], df_Res['Cluster']):
    label = folium.Popup(Locality, parse_html=True)
    folium.CircleMarker(
        [latitude, longitude],
        radius=5,
        popup=label,
        color='black',
        fill=True,
        fill_color=colors[cluster],
        fill_opacity=0.7).add_to(Noida_Rest)  

Noida_Rest


# In[63]:


df_Res.head()


# ## Which places In Noida have some of the finest Restaurants?

# In[64]:


import matplotlib.pyplot as plt
plt.figure(figsize=(9,5), dpi = 100)
# title
plt.title('The highest rated resturant in top 10 locality of Noida')
#On x-axis

#giving a bar plot
df_Res.groupby('Locality')['Aggregate rating'].mean().nlargest(10).plot(kind='bar')

plt.xlabel('Resturant Locality in Noida')
#On y-axis
plt.ylabel('Aggregate Rating')
#displays the plot
plt.show()


# The best restarants are available in DLF Mall of India, Sector 18, Noida.
# 
# ## Which Places in Noida  have Restaurants with Lowest rating?

# In[17]:


import matplotlib.pyplot as plt
plt.figure(figsize=(9,5), dpi = 100)
# title
plt.title('The Worst rated resturant in top 10 locality of Noida')
#On x-axis

#giving a bar plot

df_Res.groupby('Locality')['Aggregate rating'].mean().nsmallest(10).plot(kind='bar')

plt.xlabel('Resturant Locality in Noida')
#On y-axis
plt.ylabel('Aggregate Rating')

#displays the plot
plt.show()


# The worst rated Restaurants is in Sector 20.
# 
# ## Which place in Noida is suitable for a Foodie?

# In[18]:


import matplotlib.pyplot as plt
plt.figure(figsize=(9,5), dpi = 100)
# title
plt.title('The highest number of Restaurant available in Locality of Noida')
#On x-axis

#giving a bar plot
df_Res.groupby('Locality')['Restaurant Name'].count().nlargest(10).plot(kind='bar')

plt.xlabel('Resturant Locality in Noida')
#On y-axis
plt.ylabel('Number of Restaurant')

#displays the plot
plt.show()


# Sector 18 is the best place for Foodie.
# 
# ## Which place in Noida is not suitable for a Foodie?

# In[19]:


import matplotlib.pyplot as plt
plt.figure(figsize=(9,5), dpi = 100)
# title
plt.title('The lowest number of Restaurant available in Locality of Noida')
#On x-axis

#giving a bar plot
df_Res.groupby('Locality')['Restaurant Name'].count().nsmallest(10).plot(kind='bar')

plt.xlabel('Resturant Locality in Noida')
#On y-axis
plt.ylabel('Number of Restaurant')

#displays the plot
plt.show()


# No Sector is bad enough for the Foodie as per the above Statistics.
# 
# ## What are the best places in Noida for Chinese Restaurant?

# In[65]:


import matplotlib.pyplot as plt
plt.figure(figsize=(9,5), dpi = 100)
# title
plt.title('The best Locality for Chinese restaurant in Noida city')
#On x-axis

#giving a bar plot
df_Res[df_Res['Cuisines'].str.startswith('Chinese')].groupby('Locality')['Restaurant Name'].count().nlargest(5).plot(kind='bar')

plt.xlabel('Resturant Locality in Noida')
#On y-axis
plt.ylabel('Number of Chinese Restaurant')

#displays the plot
plt.show()


# Sector 62 is the best place for Chinese Restaurant.
# 
# ## Which places in Noida have highest rated Chinese Restaurants?

# In[66]:


import matplotlib.pyplot as plt
plt.figure(figsize=(9,5), dpi = 100)
# title
plt.title('Places for Highest Rated Chinese restaurant in Noida city')
#On x-axis

#giving a bar plot
df_Res[df_Res['Cuisines'].str.startswith('Chinese')].groupby('Locality')['Aggregate rating'].mean().nlargest(5).plot(kind='bar')

plt.xlabel('Resturant Locality in Noida')
#On y-axis
plt.ylabel('Rating of restaurants')

#displays the plot
plt.show()


# DLF Mall of India, Sector 18, Noida has best Chinese Resturants.
# 
# ## Data transformation
# 
# Based on Locality grouping the data

# In[67]:


df_Res_Loc =  df_Res.groupby('Locality').count()['Restaurant Name'].to_frame()
df_Res_rating= df_Res.groupby('Locality')['Aggregate rating'].mean().to_frame()
d_Cuisines = df_Res.groupby(['Locality'])['Cuisines'].agg(', '.join).reset_index()
d_R = df_Res.groupby(['Locality'])['Rating text'].unique().agg(', '.join).reset_index()
d_V = df_Res.groupby(['Locality'])['Votes'].sum().to_frame()
d_Lat = df_Res.groupby('Locality').mean()['Latitude'].to_frame()
d_Lng = df_Res.groupby('Locality').mean()['Longitude'].to_frame()
df_final = pd.merge(d_Lat,d_Lng,on='Locality').merge(df_Res_Loc, on='Locality').merge(d_Cuisines, on='Locality').merge(df_Res_rating,on ='Locality').merge(d_R, on ='Locality').merge(d_V, on ='Locality')


# In[68]:


df_final = df_final[df_final['Aggregate rating'] != 0.000000]
df_final.columns =['Locality','Lat','Lng', 'No_of_Restaurant','Cusines', 'Agg_Rating','Comments' ,'No_of_Votes']
df_final.head()


# In[69]:


df_final.shape


# ## Defining Foursquare Credentials and Version

# In[70]:


## Define Foursquare Credentials and Version
CLIENT_ID = 'ZNUQA0Y0JUXEKGWLC2HQAS1HVNDJ4UBDTZIKKUZ40DZH1EL1' # Foursquare ID
CLIENT_SECRET = 'CVQOTVVVTKJACYGLJUY1W2GVZ0UC21YS5S5W0LKOLI1UODKB' # Foursquare Secret
VERSION = '20180604' # Foursquare API version

print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)


# ## Function to analyse all localities in Noida in similar way

# In[71]:


## create Function to analyse all localities in Noida in similar way

def getNearbyVenues(names, latitudes, longitudes, radius=500,LIMIT = 50):
    
    venues_list=[]
    for name, lat, lng in zip(names, latitudes, longitudes):
        print(name)
            
        # create the API request URL
        url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
            CLIENT_ID, 
            CLIENT_SECRET, 
            VERSION, 
            lat, 
            lng, 
            radius, 
            LIMIT)
            
        # make the GET request
        results = requests.get(url).json()["response"]['groups'][0]['items']
        
        # return only relevant information for each nearby venue
        venues_list.append([(
            name, 
            lat, 
            lng, 
            v['venue']['name'], 
            v['venue']['location']['lat'], 
            v['venue']['location']['lng'],  
            v['venue']['categories'][0]['name']) for v in results])

    nearby_venues = pd.DataFrame([item for venue_list in venues_list for item in venue_list])
    nearby_venues.columns = ['Locality', 
                  'Locality Latitude', 
                  'Locality Longitude', 
                  'Venue', 
                  'Venue Latitude', 
                  'Venue Longitude', 
                  'Venue Category']
    
    return(nearby_venues)


# ## Retrieve venues for Noida Localities

# In[72]:


# Retrieve venues for Noida Localities
Noida_venues = getNearbyVenues(names=df_final['Locality'],
                                   latitudes=df_final['Lat'],
                                   longitudes=df_final['Lng']
                                  )


# In[74]:


Noida_venues.head()


# In[75]:


Noida_venues.groupby('Locality').count()


# In[76]:


print('There are {} uniques categories.'.format(len(Noida_venues['Venue Category'].unique())))


# In[77]:


## Analyze Each Locality

# one hot encoding
Noida_onehot = pd.get_dummies(Noida_venues[['Venue Category']], prefix="", prefix_sep="")

# add Locality column back to dataframe
Noida_onehot['Locality'] = Noida_venues['Locality'] 

# move Locality column to the first column
column_list = Noida_onehot.columns.tolist()
column_number = int(column_list.index('Locality'))
column_list = [column_list[column_number]] + column_list[:column_number] + column_list[column_number+1:]
Noida_onehot = Noida_onehot[column_list]

Noida_onehot.head()


# In[78]:



Noida_grouped = Noida_onehot.groupby('Locality').mean().reset_index()
Noida_grouped


# In[79]:


Noida_grouped.shape


# In[80]:


## print each Locality along with the top 5 most common venues

num_top_venues = 5

for hood in Noida_grouped['Locality']:
    print("----"+hood+"----")
    temp = Noida_grouped[Noida_grouped['Locality'] == hood].T.reset_index()
    temp.columns = ['venue','freq']
    temp = temp.iloc[1:]
    temp['freq'] = temp['freq'].astype(float)
    temp = temp.round({'freq': 2})
    print(temp.sort_values('freq', ascending=False).reset_index(drop=True).head(num_top_venues))
    print('\n')


# In[81]:


## put that into a pandas dataframe
## First, write a function to sort the venues in descending order.

def return_most_common_venues(row, num_top_venues):
    row_categories = row.iloc[1:]
    row_categories_sorted = row_categories.sort_values(ascending=False)
    
    return row_categories_sorted.index.values[0:num_top_venues]


# In[82]:


## create the new dataframe and display the top 10 venues for each Locality.

num_top_venues = 10

indicators = ['st', 'nd', 'rd']

# create columns according to number of top venues
columns = ['Locality']
for ind in np.arange(num_top_venues):
    try:
        columns.append('{}{} Most Common Venue'.format(ind+1, indicators[ind]))
    except:
        columns.append('{}th Most Common Venue'.format(ind+1))

# create a new dataframe
Locality_venues_sorted = pd.DataFrame(columns=columns)
Locality_venues_sorted['Locality'] = Noida_grouped['Locality']

for ind in np.arange(Noida_grouped.shape[0]):
    Locality_venues_sorted.iloc[ind, 1:] = return_most_common_venues(Noida_grouped.iloc[ind, :], num_top_venues)

Locality_venues_sorted


# In[83]:



## Cluster Locality
## Run k-means to cluster the Locality into 5 clusters.

# set number of clusters
kclusters = 5

Noida_clustering = Noida_grouped.drop('Locality', 1)

# run k-means clustering
kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(Noida_clustering)

# check cluster labels generated for each row in the dataframe
kmeans.labels_[0:10] 
kmeans.labels_.shape


# In[84]:


# add clustering labels
Noida_merged = df_final.head(76)
Noida_merged['Cluster Labels'] = kmeans.labels_

# merge Noida_grouped with df_Chinese to add latitude/longitude for each Locality
Noida_merged = Noida_merged.join(Locality_venues_sorted.set_index('Locality'), on='Locality')

Noida_merged.head()


# In[85]:


# create final map
map_clusters = folium.Map(location=[latitude, longitude], zoom_start=10)

# set color scheme for the clusters
x = np.arange(kclusters)
ys = [i+x+(i*x)**2 for i in range(kclusters)]
#colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
#rainbow = [colors.rgb2hex(i) for i in colors_array]
colors = ['red', 'green', 'blue', 'yellow','orange']

# add markers to the map
markers_colors = []
for lat, lon, poi, cluster in zip(Noida_merged['Lat'], Noida_merged['Lng'], Noida_merged['Locality'], Noida_merged['Cluster Labels']):
    label = folium.Popup(str(poi) + ' Cluster ' + str(cluster), parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        popup=label,
        color='black',
        fill=True,
        fill_color=colors[cluster],
        fill_opacity=0.7).add_to(map_clusters)
       
map_clusters


# In[86]:


## Examine Clusters

## Cluster 1
Noida_merged.loc[Noida_merged['Cluster Labels'] == 0, Noida_merged.columns[[1] + list(range(5, Noida_merged.shape[1]))]]


# In[87]:


## Examine Clusters

## Cluster 2
Noida_merged.loc[Noida_merged['Cluster Labels'] == 1, Noida_merged.columns[[1] + list(range(5, Noida_merged.shape[1]))]]


# In[88]:


## Examine Clusters

## Cluster 3
Noida_merged.loc[Noida_merged['Cluster Labels'] == 2, Noida_merged.columns[[1] + list(range(5, Noida_merged.shape[1]))]]


# In[89]:


## Examine Clusters

## Cluster 4
Noida_merged.loc[Noida_merged['Cluster Labels'] ==3 , Noida_merged.columns[[1] + list(range(5, Noida_merged.shape[1]))]]


# In[90]:


## Examine Clusters

## Cluster 5
Noida_merged.loc[Noida_merged['Cluster Labels'] == 4, Noida_merged.columns[[1] + list(range(5, Noida_merged.shape[1]))]]


# ## Conclusion
# - DLF Mall OF India are some of the best neighbourhoods for Chinese cuisine
# - Sector 62 place have the highest number of Chinese Resturant.
# - Sector 18 and Sector 32 are the best places for foodie.
# - DLF Mall OF India, Gardens Galleria have best resturants in Noida. 
# #### Cluster 1 and Cluster 5 : It is most recommended for family 
# #### Cluster 2: It is most recommended for convenient Store and Entertainment
# #### Cluster 3:  It is most recommended for restaurants
# #### Cluster 4: It is most recommended for the cafe and pizza
#  
# 
# 

# In[ ]:




