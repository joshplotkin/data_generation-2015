import sys

def make_cities():
	cities = {}
	try:
		f = open('./demographic_data/locations_partitions.csv', 'r').readlines()
	except:
		print './demographic_data/locations_partitions.csv not found'
		sys.exit(0)
	for line in f:
	    try:
	        cdf, output = line.replace('\n','').split(',')
	        cities[float(cdf)] = output
	    # header
	    except:
	        pass
	return cities

def make_age_gender_dict():
    gender_age = {}
    prev = 0
    try:
    	f = open('./demographic_data/age_gender_demographics.csv', 'r').readlines()
    except:
		print './demographic_data/age_gender_demographics.csv not found'
		sys.exit(0)
    for line in f:
        l = line.replace('\n','').split(',')
        if l[3] != 'prop':
            prev += float(l[3])
            gender_age[prev] = (l[2], float(l[1]))
    return gender_age	
