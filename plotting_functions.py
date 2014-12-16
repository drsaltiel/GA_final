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