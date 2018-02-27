## Initialisation

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

from geopy.geocoders import Nominatim
geolocator = Nominatim()

sample_data = [['22','800 swanston street,3053','Rondo','0401082050','CakeType1','Making'],
               ['24312','500 swanston street,3053','Michael','0405078123','CakeType2','Arrived'],
               ['5586','melbourne central,3000','Yibo','041230123','Type3','Waiting'],
               ['12314','442 Elizabeth street,3000','Jeffery','645231321','Type4','Waiting'],
               ['54645','200 collins street,3000','David','45234123','Type0','Waiting']]
#geo code for each location
locations = []
    
new_locations = ['442 Elizabeth street,3000',
                 'melbourne central,3000',
                 '500 swanston street,3053',
                 '200 collins street,3000',
                 '710 Collins St,3001']
                 # '424 St Kilda Rd,3004',
#                  '147 Victoria Ave,3206',
#                  '167 Toorak Rd,3141',
#                  '100 Bridge Rd,3121']
for i in new_locations:
    locations.append((geolocator.geocode(i,timeout=20),i))

normalized_locs = []
data = []
for (info,address) in locations:
    normalized_locs.append([info.latitude,info.longitude,address])
    data.append([info.latitude,info.longitude])
print normalized_locs

colmap = {1: 'r', 2: 'g', 3: 'b'}
cols2 = ['x','y','address']
cols = ['x','y']
df2 = pd.DataFrame(normalized_locs, columns=cols2)
df = pd.DataFrame(data, columns=cols)


print df2


from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=2,init='k-means++')
kmeans.fit(df)
labels = kmeans.predict(df)
print labels

clusters = {}
n = 0
for item in labels:
    print item
    if item in clusters:
        clusters[item].append(new_locations[n])
    else:
        clusters[item] = [new_locations[n]]
    n +=1

for item in clusters:
    print "Cluster ", item
    for i in clusters[item]:
        print i
        
centroids = kmeans.cluster_centers_
print centroids

fig = plt.figure(figsize=(5, 5))
colors = map(lambda x: colmap[x+1], labels)

plt.scatter(df['x'], df['y'], color=colors, alpha=0.5, edgecolor='k')
for idx, centroid in enumerate(centroids):
    plt.scatter(*centroid, color=colmap[idx+1])
plt.xlim(-38,-37.6 )
plt.ylim(144.8,145.1 )
plt.show()