import sys

def make_cities():
	cities = {}
	try:
		f = open('./demographic_data/locations_partitions.csv', 'r').read().split('\r')
	except:
		print './demographic_data/locations_partitions.csv not found'
		sys.exit(0)
	for line in f[1:]:
		pdf, output = line.replace('\n','').split(',')
		cities[output] = float(pdf)
	return cities

def make_age_gender_dict():
    gender_age = {}
    try:
    	f = open('./demographic_data/age_gender_demographics.csv', 'r').read().split('\r')
    except:
		print './demographic_data/age_gender_demographics.csv not found'
		sys.exit(0)
    for line in f[1:]:
        l = line.replace('\n','').split(',')
        gender_age[(l[2], int(l[1]))] = float(l[3])
    return gender_age	
