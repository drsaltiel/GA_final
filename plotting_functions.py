'''
assorted functions for plotting from yelp academic data set 
for general assembly data science final project
'''

import matplotlib.pyplot as plt


def make_bins(category, num_bins, city):
    '''
    returns bins of number of businesses and number of businesses in category
    '''
    max_lat, min_lat, max_lon, min_lon = city_edges(city)
    dlon = (max_lon - min_lon) / num_bins
    dlat = (max_lat - min_lat) / num_bins
    
    matrix_category = [list([0]*num_bins) for x in range(num_bins)]
    matrix_total = [list([0]*num_bins) for x in range(num_bins)]
    
    for i, bus in city['categories'].iteritems():
        lat = city['latitude'][i]
        lon = city['longitude'][i]
        j=0
        while j<=num_bins:
            found_flag = False
            k=0
            while k<=num_bins:
                if (j*dlat)+min_lat < lat < (((j+1)*dlat)+min_lat) and \
                       ((k*dlon)+min_lon) < lon < (((k+1)*dlon)+min_lon):
                    matrix_total [j][k] +=1
                    if category in bus:
                        matrix_category[j][k]+=1
                    found_flag = True
                    break
                else: 
                    k+=1
            if found_flag == True:
                break
            j+=1
    return matrix_category, matrix_total

def city_edges(city):
    '''
    returns max latitude, min latitude, max longitude, min longitude
    '''
    lat_set = []
    lon_set = []
    for k, l in city['latitude'].iteritems():
        lat_set.append( city['latitude'][k] )
        lon_set.append( city['longitude'][k] )
    return max(lat_set), min(lat_set), max(lon_set), min(lon_set)

def plot_bins(category,num_bins, city):
    '''
    takes a category and city and plots the bins for it
    '''
    a, b = make_bins(category, num_bins, city)
    c = []
    max_ratio = 0
    for i in xrange(len(a)):
        c.append([])
        for j in xrange(len(a[i])):
            try: 
                ratio = a[i][j]/float(b[i][j])
                c[i].append(ratio)
                if ratio > max_ratio: 
                    max_ratio = ratio
#                     print i,j,max_ratio
            except ZeroDivisionError:
                c[i].append('NA')
#     print c
    
    for i in xrange(len(c)):
        for j in xrange(len(c[i])):
            if c[i][j] == 'NA':
                c[i][j] = max_ratio
                
    plt.imshow(c, interpolation='none', alpha = 1)

    max_lat, min_lat, max_lon, min_lon = city_edges(city)
    plt.xticks([0,len(c[0])-1],[min_lon, max_lon])
    plt.yticks([0,len(c)-1],[min_lat, max_lat])

    plt.jet()
    cb = plt.colorbar() #make color bar
    cb.set_ticks([max_ratio, 0])   #two ticks
    cb.set_ticklabels(['high concentration', 'low concentration'])  # put text labels on them

def bin_by_review_count(category, num_bins, city):
    '''
    returns bins of total reviews for businesses of category in city
    '''
    max_lat, min_lat, max_lon, min_lon = city_edges(city)
    dlon = (max_lon - min_lon) / num_bins
    dlat = (max_lat - min_lat) / num_bins
    
    matrix_category_reviews = [list([0]*num_bins) for x in range(num_bins)]
    matrix_total_reviews = [list([0]*num_bins) for x in range(num_bins)]
    
    for i, bus in city['categories'].iteritems():
        lat = city['latitude'][i]
        lon = city['longitude'][i]
        j=0
        while j<=num_bins:
            found_flag = False
            k=0
            while k<=num_bins:
                if (j*dlat)+min_lat < lat < (((j+1)*dlat)+min_lat) and \
                       ((k*dlon)+min_lon) < lon < (((k+1)*dlon)+min_lon):
                    matrix_total_reviews [j][k] +=city['review_count'][i]
                    if category in bus:
                        matrix_category_reviews[j][k]+=city['review_count'][i]
                    found_flag = True
                    break
                else: 
                    k+=1
            if found_flag == True:
                break
            j+=1
    return matrix_category_reviews, matrix_total_reviews

def plot_percent_traffic(category, num_bins, city):
    '''
    plots percent traffic (review_counts) of category in bin
    '''
    a, b =bin_by_review_count(category, num_bins, city)
    c = []
    max_ratio = 0
    for i in xrange(len(a)):
        c.append([])
        for j in xrange(len(a[i])):
            try: 
                ratio = a[i][j]/float(b[i][j])
                c[i].append(ratio)
                if ratio > max_ratio: 
                    max_ratio = ratio
#                     print i,j,max_ratio
            except ZeroDivisionError:
                c[i].append('NA')
#     print c
    
    for i in xrange(len(c)):
        for j in xrange(len(c[i])):
            if c[i][j] == 'NA':
                c[i][j] = 0
                
    plt.imshow(c, interpolation='none', alpha = 1)

    max_lat, min_lat, max_lon, min_lon = city_edges(city)
    plt.xticks([0,len(c[0])-1],[min_lon, max_lon])
    plt.yticks([0,len(c)-1],[min_lat, max_lat])

    plt.jet()
    cb = plt.colorbar() #make color bar
    cb.set_ticks([0,max_ratio])   #two ticks
    cb.set_ticklabels(['low traffic','lots of traffic'])  # put text labels on them

from matplotlib import collections  as mc
def plot_nearest(category, city_data):
    '''
    plots businessess of given category in given city with lines connecting every business to the closest of the same type
    '''
    category_businesses = city_data[[category in j for i, j in city_data['categories'].iteritems()]]
    category_bus_coordinates = []
    for k, l in category_businesses['latitude'].iteritems():
        category_bus_coordinates.append((category_businesses['longitude'][k], category_businesses['latitude'][k]))
    lines = []
    for coord in category_bus_coordinates:
        min_coord = float('inf')
        min_distance = float('inf')
        for cat_bus in category_bus_coordinates:
            if cat_bus!= coord:
                dist = coord_distance(coord, cat_bus)
                if dist < min_distance:
                    min_distance = dist
                    min_coord = cat_bus
        lines.append([coord, min_coord])
#     return lines
    lc = mc.LineCollection(lines)
    plt.figure()
    ax = plt.subplot(111)
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)

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