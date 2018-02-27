## Initialisation
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import math
from geopy.geocoders import Nominatim
from datetime import datetime


geolocator = Nominatim()

"""@num_dis     : number of dispatchers
   @orders      : list of orders
   @return(dic) : dictionary of {dispatcher:[orders]}"""
def k_means_clustering(num_dis,orders):
    dic = {}
    #num_dis = len(dispatchers)
    locations = []               # list of (order number,geoinfo,address)
    cal_locs = []                # used to be clutstered [(lat,lng)]            
    
    for order in orders:
        locations.append((order.order_number,geolocator.\
            geocode(order.address,timeout=20),order.address))

    for (num,info,ad) in locations:
        cal_locs.append([info.latitude,info.longitude])

    #colmap = {1: 'r', 2: 'g', 3: 'b'}
    cols = ['x','y']
    df = pd.DataFrame(cal_locs, columns=cols)
    
    kmeans = KMeans(n_clusters=num_dis,init='random')
    kmeans.fit(df)
    labels = kmeans.predict(df)
    centroids = kmeans.cluster_centers_
    n = 0
    for item in labels:
        order = find_order_by_id(locations[n][0],orders)
        if item in dic:
            # add data to corresponding key
            dic[item].append(order)
        else:
            # create new key:[value]
            dic[item] = [order]
        n +=1

    # for item in dic:
    #     print "\nCluster ", item
    #     for i in dic[item]:
    #         print i
    
    return dic

if __name__ == "__main__":
    db = Orders_database(file_order)
    k_means_clustering(3,db.orders_all)

    
    
    
    