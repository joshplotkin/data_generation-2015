import random
import pandas as pd
from pandas import *
import json
import numpy as pd
import sys
import datetime
from datetime import timedelta
import math

# day of week category

def date_mapping(start_date):
    # DAY OF WEEK OF START DATE: 
    # when pulling a day of week,
    # convert so that 0 is this 
    # start day
    date_map = {'monday': 0,
                'tuesday': 1,
                'wednesday': 2,
                'thursday': 3,
                'friday': 4,
                'saturday': 5,
                'sunday': 6}

    for d in date_map:
        date_map[d] = (date_map[d] - start_date.weekday() + 7)%7
    return date_map

def convert_week(weeks):
    default_weight = weeks['other']['weight']
    weeks_weights = {}
    for i in range(52):
        weeks_weights[i] = default_weight
    for w in weeks:
        # 'other' has already been set
        # to default
        if w != 'other':
            start = weeks[w]['start_week_num']
            end = weeks[w]['end_week_num']
            curr_weight = weeks[w]['weight']
            # change from default weights to user-defined
            # weights
            for week_num in range(start, end + 1):
                weeks_weights[week_num] = curr_weight
    return weeks_weights

def pct_dict(weights, date_type = False):
    # date_type is only used to convert
    # to week of year
    if date_type == 'week_of_year':
        weights = convert_week(weights)
    
    wsum = sum(weights.values())
        
    for w in weights:
        weights[w] = float(weights[w])/float(wsum)

    wsum = 0
    for w in weights:
        wsum += weights[w]
        weights[w] = wsum
    return weights

def pick_from_weights(weights):    
    inverted = {}
    for w in weights:
        inverted[weights[w]] = w 

    num = random.random()
    for w in sorted(inverted.keys()):
        if num <= w:
            return inverted[w]
    'ERROR PICKING FROM WEIGHTS'
    sys.exit(0)
    
# given a list of day, month, year, and start, return a date
def pick_transaction_date(date_weights, date_map, start_date):
    dates = []
    for date_type in ['day_of_week', 'week_of_year', 'year']:
        dates.append(pick_from_weights(date_weights[date_type]))
    # map the day of week to a 0-6
    # integer based on first day 
    # of date range
    dates[0] = date_map[dates[0]]
    # the offset adds days to the start date
    offset = int(dates[0]) + int(dates[1])*7 + int(dates[2])*52*7
    return start_date + timedelta(days = offset) 

# choose a weight, given weight/error
def choose_weight(err, weight):
    lower_bound = weight*(1-err)
    upper_bound = weight*(1+err)
    
    return (upper_bound - lower_bound)*random.random() + lower_bound

# number of transactions
def choose_num_transactions(json_dict, start_date, end_date):
    # fetch the bounds from the json
    lower_bound = json_dict['transactions']['lower']
    upper_bound = json_dict['transactions']['upper']
    # total number of days
    total_days = (end_date - start_date).days
    # uniform random draw from [lower, upper]
    trans_per_day = (upper_bound - lower_bound)*random.random() + lower_bound
    # round and cast as int
    return int(round(trans_per_day*float(total_days)))

def get_amount(mean, stdev):
	while True:
	    amount = float("{:.2f}".format(np.random.normal\
	                            (mean, stdev, 1)[0]))
	    if amount > 0:
	        break
	return amount

# take a birthdate and return age
def return_age(person_dict):
    age = datetime.date(int(person_dict['dob_year']), 
                        int(person_dict['dob_month']), 
                        int(person_dict['dob_day']))
    now = datetime.datetime.now()
    days_old = (datetime.date(now.year, now.month, now.day) - age).days
    years_old = float(days_old)/float(365.25)
    return years_old


########################################################
#### PERFORM THESE FOR ALL CUSTOMERS ###################
########################################################
def get_transaction_data(json_dict, start_date, end_date, date_map, date_weights, \
						cat_weight_error, amt_weight_error, person_dict):

	##############################################
	### pick # of categories #####################
	##############################################
	num_transactions = choose_num_transactions(json_dict, start_date, end_date)

	start_dict = person_dict.copy()
	person_list = []
	for i in range(num_transactions):
		person_dict = start_dict.copy()
		person_dict['trans_num'] = i
		##############################################
		### pick date for transaction ################
		##############################################
		t_date = pick_transaction_date(date_weights, date_map, start_date)
		person_dict['trans_year'] = t_date.year
		person_dict['trans_month'] = t_date.month
		person_dict['trans_day'] = t_date.day

		##############################################
		### pick a category ##########################
		##############################################
		categories_weights = {}
		for c in json_dict['categories_wt']:
		    if c != 'categories_wt_error':
		        categories_weights[c] = choose_weight(cat_weight_error, \
		                                json_dict['categories_wt'][c])
		cat_pct = pct_dict(categories_weights)
		person_dict['category'] = pick_from_weights(cat_pct)
		##############################################
		### pick a $$ amount, given a category #######
		##############################################
		cat_amounts = {}
		cat_amounts['mean'] = choose_weight(amt_weight_error, \
		                    json_dict['categories_amt'][person_dict['category']]['mean'])
		cat_amounts['stdev'] = choose_weight(amt_weight_error, \
		                    json_dict['categories_amt'][person_dict['category']]['stdev'])
		person_dict['amt'] = get_amount(cat_amounts['mean'], cat_amounts['stdev'])

		# append to list of person's transactions
		person_list.append(person_dict)

	del(start_dict)
	del(person_dict)
	return person_list

######################################################
#### CONFIG FILE FUNCTIONS ###########################
######################################################

# convert inputted date
def convert_start_date(d):
    if '/' in d:
        split_char = '/'
    elif '-' in d:
        split_char = '-'
    elif '_' in d:
        split_char = '_'
    elif ' ' in d:
        split_char = ' '
    else:
        print 'INVALID DATE ENTERED'
        sys.exit(0)

    d = d.split(split_char)
    return datetime.date(int(d[2]), int(d[0]), int(d[1]))



######################################################
#### CLI INPUTS ######################################
######################################################

try:
    customers = sys.argv[1]
except:
    print 'ENTER (1) INPUT CUSTOMER CSV, (2) PROFILE CONFIG (3) START DATE MM-DD-YYYY (4) END DATE MM-DD-YYYY'
    sys.exit(0)
try:
    pro = sys.argv[2]
except:
    print 'ENTER (1) INPUT CUSTOMER CSV, (2) PROFILE CONFIG (3) START DATE MM-DD-YYYY (4) END DATE MM-DD-YYYY'
    sys.exit(0)
try:
    startd = sys.argv[3]
except:
    print 'ENTER (1) INPUT CUSTOMER CSV, (2) PROFILE CONFIG (3) START DATE MM-DD-YYYY (4) END DATE MM-DD-YYYY'
    sys.exit(0)
try:
    endd = sys.argv[4]
except:
    print 'ENTER (1) INPUT CUSTOMER CSV, (2) PROFILE CONFIG (3) START DATE MM-DD-YYYY (4) END DATE MM-DD-YYYY'
    sys.exit(0)

# DATES READ FROM INPUTS
start_date = convert_start_date(startd)
end_date = convert_start_date(endd)

js = open(pro, 'r').read()
json_dict = json.loads(json.dumps(js, separators = (', ', ': ')).\
            replace('\\n','').\
            replace('\\t','').\
            replace('\\','').\
            replace('"{','{').\
            replace('}"','}'))

# based on first day of window
# map the day offset to the 
# corresponding day
date_map = date_mapping(start_date)
# convert dates from weights to %
date_weights = {}
for date_type in ['day_of_week', 'week_of_year', 'year']:
    date_weights[date_type] = pct_dict(json_dict['date_wt'][date_type], date_type)

cat_weight_error = json_dict['categories_wt']['categories_wt_error']
amt_weight_error = json_dict['categories_amt']['categories_amt_error']

#############################################################
# CHOOSE PEOPLE FROM THIS GROUP AND ADD TRANSACTION DATA ####
#############################################################

f = open(customers, 'r')
header = True
# each line is a customer
for line in f.readlines():
    person_dict = {}
    if header == True:
        header = False
        headers = line.split('|')
        headers[-1] = headers[-1].replace('\n','')

        headers.extend(['trans_num', 'trans_year', 'trans_month', \
						'trans_day', 'category', 'amt'])
        # print header to stdout
        header_string = ''
        for h in headers:
        	header_string += h + '|'
        header_string = header_string[:-1]
        print header_string
    else:
        person = line.split('|')
        person[-1] = person[-1].replace('\n','')

        
        for i in range(len(person)):
            person_dict[headers[i].replace('\n','')] = person[i].replace('\n','')
   
        curr_profile = person_dict['profile']

        if curr_profile == pro.split('/')[-1]:
			# generate transactions
            person_dict = get_transaction_data(json_dict, start_date, end_date, \
            	date_map, date_weights, cat_weight_error, amt_weight_error, person_dict)

            # print to pipe to file
            for pd in person_dict:
            	output_string = ''
            	for p in headers:
            		output_string += str(pd[p]) + '|'
            	# remove trailing pipe
            	output_string = output_string[:-1]
                print output_string

            del(person_dict)