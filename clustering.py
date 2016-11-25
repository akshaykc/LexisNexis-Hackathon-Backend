'''
Created on Oct 13, 2016

@author: achaluv
'''

'''
import geocoder
g = geocoder.google('Intuitive Surgical, Kifer Road, Sunnyvale, California')
print g.latlng
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from geopy.distance import great_circle
from shapely.geometry import MultiPoint


f = open("addWithLatLong.txt")
latlongList=[]
with open('addWithLatLong.txt') as infile:
    for line in infile:
        if len(line.split("\t")) == 9 :
            lat = (line.split("\t")[7])
            longi = (line.split("\t")[8]).strip()
            latlongList.append([lat,longi])
            
            
df = pd.DataFrame(latlongList, columns=["Lat", "Long"])  
df.head()
#coords = df.as_matrix(columns=['lat', 'lon'])
#print coords
coords_st = df.as_matrix(columns=['Lat', 'Long'])
#print coords_st
#type(coords_st)


import numpy as np
coords = coords_st.astype(np.float)

df_num = df.astype(np.float)
df_num.head()
#coords = df.as_matrix(columns=['lat', 'lon'])
#print coords
coords_st = df_num.as_matrix(columns=['Lat', 'Long'])
#print coords_st
type(coords_st)

kms_per_radian = 6371.0088
epsilon = 30 / kms_per_radian
db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
cluster_labels = db.labels_
num_clusters = len(set(cluster_labels))
clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])
interestClusters = 0

def get_centermost_point(cluster):
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
    return tuple(centermost_point)

for elem in clusters:
    if len(elem) > 10:
        print get_centermost_point(elem)
        interestClusters +=1
print interestClusters
print('Number of clusters: {}'.format(num_clusters))


centermost_points = clusters.map(get_centermost_point)

lats, lons = zip(*centermost_points)
rep_points = pd.DataFrame({'lon':lons, 'lat':lats})
print (rep_points)



fig, ax = plt.subplots(figsize=[10, 6])

#x1,x2,y1,y2 = plt.axis()

plt.axis((-7,4,47,58))


rs_scatter = ax.scatter(rep_points['lon'], rep_points['lat'], c='#99cc99', edgecolor='None', alpha=0.7, s=120)
df_scatter = ax.scatter(df_num['Long'], df_num['Lat'], c='k', alpha=0.9, s=3)
ax.set_title('Full data set vs DBSCAN reduced set')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.legend([df_scatter, rs_scatter], ['Full set', 'Reduced set'], loc='upper right')
plt.show()






