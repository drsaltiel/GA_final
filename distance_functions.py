'''
assorted functions for calculating distance from yelp academic data set 
for general assembly data science final project
'''

import numpy as np
import math as math


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

def ave_min_distance(category, city_data):
    '''
    returns the average minimum distance from any given business to a business of input category
    '''
    category_businesses = city_data[[category in cats for i, cats in city_data['categories'].iteritems()]]
    category_bus_coordinates = []
    for k, l in category_businesses['latitude'].iteritems():
        category_bus_coordinates.append((category_businesses['longitude'][k], category_businesses['latitude'][k]))
    coordinates_set = []
    for k, l in city_data['latitude'].iteritems():
        coordinates_set.append((city_data['longitude'][k], city_data['latitude'][k]))
    sum_distances = 0
    num_distances = 0
    for coord in coordinates_set:
        closest_dist = min([coord_distance(coord, cat_bus) for cat_bus in category_bus_coordinates if cat_bus != coord])
        sum_distances += closest_dist
        num_distances += 1
    ave_min_distance = sum_distances / num_distances
    return(ave_min_distance)


def ave_min_distance_of_same_type(category, city_data):
    '''
    returns the average minimum distance from any given business to a business of the same type in category
    '''
    category_businesses = city_data[[category in j for i, j in city_data['categories'].iteritems()]]
    category_bus_coordinates = []
    for k, l in category_businesses['latitude'].iteritems():
        category_bus_coordinates.append((category_businesses['longitude'][k], category_businesses['latitude'][k]))
    sum_distances = 0
    num_distances = 0
    for coord in category_bus_coordinates:
        cat_other_bus = category_bus_coordinates
        closest_dist = min([coord_distance(coord, cat_bus) for cat_bus in cat_other_bus if cat_bus != coord])
        sum_distances += closest_dist
        num_distances += 1
    ave_min_distance = sum_distances / num_distances
    return(ave_min_distance)