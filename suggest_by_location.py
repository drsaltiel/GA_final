'''
Returns the optimal business for a given location based upon surrounding businesses
within a specified radius.

possible_categories = list all possible categories divided by commas (no spaces)

Needs input of latitude and longitude and possible_categories, defaults:
radius = 1 mile
metric = combined metrics
num_results = top 10 results
city = Las Vegas
'''

import pandas as pd
import ast
import numpy as np
import math as math
import sys


def find_optimal_bus(latitude, longitude, radius, metric='combined_metric', 
                     possible_categories=None, num_results=10, city='Las Vegas'):
    '''
    takes in a coordinate location and finds what category of business 
    from possible_categories would be best there according to metric
    based on information about businesses within radius
    '''
    bus_data=pd.read_csv('yelp_academic_dataset_business.csv')
    city_data = bus_data[bus_data['city']== city]
    if possible_categories is None:
        possible_categories = []
        for i, j in city_data['categories'].iteritems():
            possible_categories+=ast.literal_eval(j)
        possible_categories=list(set(possible_categories))
    if num_results==None:
        num_results = len(possible_categories)
    
    if metric == 'combined_metric':
        results_traffic = [(cat, max_traffic_percent(latitude,longitude,cat,radius,city_data)) \
                           for cat in possible_categories]
        results_traffic.sort(key=lambda pair: pair[1], reverse=True)
        results_traffic = [cat for cat, _ in results_traffic]
        results_neighbors = [(cat, min_neighbors(latitude,longitude,cat,radius,city_data)) \
                             for cat in possible_categories]
        results_neighbors.sort(key=lambda pair: pair[1], reverse=True)
        results_neighbors = [cat for cat, _ in results_neighbors]
        results = [(cat, results_traffic.index(cat)+results_neighbors.index(cat)) \
                   for cat in possible_categories]
        results.sort(key=lambda pair: pair[1])

    else:
        results = [(cat, metric(latitude,longitude,cat,radius,city_data)) \
                   for cat in possible_categories]
        results.sort(key=lambda pair: pair[1], reverse=True)
        
    return results[:num_results]


def max_traffic_percent(lat,lon,category,radius,city):
    '''
    returns percent traffic of category surrounding lat and lon in radius
    '''
    cat_rev, total_rev = review_count_radius(lat, lon, category, radius, city)
    cat_percent = float(cat_rev) / total_rev
    return cat_percent

def min_neighbors(lat,lon,category,radius, city):
    '''
    metric of minimum number of neighbors of same category
    '''
    cat_bus, total_bus = neighbor_radius(lat,lon,category,radius,city)
    return -(float(cat_bus)/total_bus)

def neighbor_radius(lat,lon,category,radius,city):
    '''
    returns category businesses and total businesses within radius
    '''
    lat_bus = lat
    lon_bus = lon
    category_bus = 0
    total_bus = 0
    for i, bus in city['categories'].iteritems():
        lat = city['latitude'][i]
        lon = city['longitude'][i]
        
        if radius < coord_distance((lon_bus,lat_bus),(lon,lat)):
            total_bus  +=1
            if category in bus:
                category_bus+=1
    
    return category_bus, total_bus


def review_count_radius(lat, lon, category, radius, city):
    '''
    returns category businesses and total businesses reviews 
    within radius in miles
    '''
    lat_bus = lat
    lon_bus = lon
    category_reviews = 0
    total_reviews = 0
    for i, bus in city['categories'].iteritems():
        lat = city['latitude'][i]
        lon = city['longitude'][i]
        
        if radius < coord_distance((lon_bus,lat_bus),(lon,lat)):
            total_reviews  +=city['review_count'][i]
            if category in bus:
                category_reviews+=city['review_count'][i]
    
    return category_reviews, total_reviews

def coord_distance(point1, point2, scale='miles'):
    '''
    finds the distance between two coordinate locations given as
    (longitude, latitude)
    uses Haversine formula
    '''
    if len(point1) != 2 or len(point2) != 2:
        raise ValueError('Input(s) do not have correct dimensions')
    if scale == 'miles': 
        R = 3963
    elif scale == 'kilometers': 
        R = 6373
    else: 
        raise ValueError('Need valid scale (miles or kilometers)')
    dLat = (point1[1] - point2[1]) * np.pi / 180
    dLong = (point1[0] - point2[0]) * np.pi / 180
    a = np.sin(dLat / 2) * np.sin(dLat / 2) + np.cos(point1[1] * np.pi / 180) \
        * np.cos(point2[1] * np.pi / 180) * np.sin(dLong / 2) * np.sin(dLong / 2)
    c = 2 * math.atan2(np.sqrt(a), np.sqrt(1 - a))
    return R*c

def main(latitude, longitude):
    suggestions = find_optimal_bus(latitude, 
                                   longitude, 
                                   radius = 1, 
                                   metric = metric, 
                                   possible_categories=categories, 
                                   num_results=10, 
                                   city='Las Vegas')
    for element in suggestions:
        print element 

metric_map = {"max_traffic": max_traffic_percent,
              "traffic_percent": max_traffic_percent,
              "min_neighbors": min_neighbors,
              "combined": "combined_metric"}


if __name__ == '__main__':
    lat = float(sys.argv[1])
    lon = float(sys.argv[2])
    categories = sys.argv[3].split(',')
    if categories == ['None'] or categories == ['none']:
        categories = None
    try: 
        metric = metric_map[sys.argv[4]]
    except IndexError:
        metric = metric_map['combined']
    except KeyError:
        print "invalid metric entered"
        sys.exit(1)

    main(lat, lon)

