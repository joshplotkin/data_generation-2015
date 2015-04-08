import faker
from faker import Faker
import random
import pandas as pd
from pandas import *
# import json
import numpy as np
import sys
import datetime
from datetime import timedelta
# import math
import fileinput
import random

## TODO:
# customizable customers

def generate_age():
    while True:
        s = np.random.normal(45, 25, 1)
        if s < 18 or s > 85:
            pass
        else:
            # return dob
            return 2014 - int(s)

# find nearest address in dataframe
def get_random_location():
    idx = (np.abs(cities.partition.values - random.random())).argmin()
    return cities.loc[idx, 'output']
    
def print_string(ssn, first, last, gender, street, addy, job, dob_day, dob_month, dob_year, account):
    return str(ssn) + '|' + first + '|' + last + '|' + gender + '|' + street + '|' + addy + '|' + job + '|' + str(dob_day) + '|' + str(dob_month) + '|' + str(dob_year) + '|' + str(account)

def return_age(person_dict):
    age = datetime.date(int(person_dict['dob_year']), 
                        int(person_dict['dob_month']), 
                        int(person_dict['dob_day']))
    now = datetime.datetime.now()
    days_old = (datetime.date(now.year, now.month, now.day) - age).days
    years_old = float(days_old)/float(365.25)
    return years_old

def get_profile(person_dict, all_profiles):
    for pf in all_profiles:
        if in_profile(person_dict, all_profiles[pf]):
            return pf
    return 'leftovers.json'

def all_profiles_dicts(main_config):
    all_profiles = {}
    for pf in main_config:
        if pf != 'leftovers.json':
            all_profiles[pf] = {}
            for qual in main_config[pf]:
                all_profiles[pf][qual] = \
                convert_config_type(main_config[pf][qual])

    return all_profiles

def in_profile(person_dict, profile_quals):
    for pq in profile_quals:
        if pq == 'age':
            if fits_qual(return_age(person_dict),\
                         profile_quals[pq]) == False:
                return False
        else:
            if fits_qual(person_dict[pq],\
                         profile_quals[pq]) == False:
                return False
    return True

# convert type to a tuple
def convert_config_type(x):
    if type(x) is dict:
        minval = float(x['min'])
        maxval = float(x['max'])
        if maxval < 0:
            return (minval, float('inf'))
        else:
            return (minval, maxval)
    else:
        return x

def fits_qual(person_val, range_tuple):
    if type(range_tuple) is list:
        # matching value in string list 
        # (e.g. ['M','F'])
        if unicode(person_val) in range_tuple or \
            str(person_val) in range_tuple:
            return True
        # doesn't match
        else:
            return False

    elif type(range_tuple) is unicode or type(range_tuple) is str:
        if unicode(person_val) == unicode(range_tuple):
            return True
        # doesn't match
        else:
            return False

    # range
    if float(person_val) >= float(range_tuple[0]) and\
        float(person_val) <= float(range_tuple[1]):
            return True
    else:
        return False

def generate_person(cols):
    # generate person
    # ssn
    ssn = fake.ssn()
    # generate gender
    if random.random() > 0.5:
        gender = 'M'
    else:
        gender = 'F'

    if gender == 'M':
        first = fake.first_name_male()
    else:
        first = fake.first_name_female()

    last = fake.last_name()

    street = fake.street_address()
    addy = get_random_location()

    # if zip is not a #, it fails
    # if addy == False:
    #     return False

    job = fake.job().replace(',','')
    # 

    # make sure the date/time works
    while True:
        dob = fake.date_time_this_century()
        dob_month = dob.month
        dob_day = dob.day
        dob_year = generate_age()
        try:
            datetime.date(dob_year, dob_month, dob_day)
            break
        except:
            # date failed
            return False

    # skipping CC for now
    # cc = fake.credit_card_full()
    email = fake.email()
    account = fake.random_number()

    output = print_string(ssn, first, last, gender, street, addy, job, dob_day, dob_month, dob_year, account)

    # -1 because profile isn't part of it yet
    if len(output.split('|')) != len(cols.split('|'))-1:
        print 'PROBLEM WITH NUMBER OF COLUMNS'
        print ssn, first, last, gender, addy, job, dob_day, dob_month, dob_year, account
        sys.exit(0)

    # make into a dict
    customer_dict = {}
    cols_split = cols.split('|')
    # don't do profile
    for col in range(len(cols_split))[:-1]:
        customer_dict[cols_split[col]] = (str(output)).split('|')[col]

    return str(output), customer_dict
################################################################
# generate people

# real US city info in partitions proportionate
# to ZIP code size
cities = read_csv('locations_partitions.csv')

try:
    num_cust = int(sys.argv[1])
except:
    print 'ENTER (1) NUMBER OF CUSTOMERS, (2) RANDOM SEED AS COMMAND LINE ARGUMENTS, (3) main_config.json'
    sys.exit(0)
try:
    seed_num = int(sys.argv[2])
except:
    print 'ENTER (1) NUMBER OF CUSTOMERS, (2) RANDOM SEED AS COMMAND LINE ARGUMENTS, (3) main_config.json'
    sys.exit(0)
try:
    m = sys.argv[3]
except:
    print 'ENTER (1) NUMBER OF CUSTOMERS, (2) RANDOM SEED AS COMMAND LINE ARGUMENTS, (3) main_config.json'
    sys.exit(0)

main = open(m, 'r').read()

main_config = json.loads(json.dumps(main).\
            replace('\\n','').\
            replace('\\t','').\
            replace('\\','').\
            replace('"{','{').\
            replace('}"','}'))


# turn all profiles into dicts to work with
all_profiles = all_profiles_dicts(main_config)

cols = 'ssn|first|last|gender|street|city|state|zip|lat|long|city_pop|job|dob_day|dob_month|dob_year|acct_num|profile'
print cols
fake = Faker()
fake.seed(seed_num)
person_list = []

i = 0
while i < num_cust:
    temp_person = generate_person(cols)
    if temp_person != False:
        gen = temp_person[0]
        customer_dict = temp_person[1]

        curr_profile = get_profile(customer_dict, all_profiles)

        # date failed
        if gen == False:
            pass
        else:
            print gen + '|' + curr_profile
            i += 1
        del(gen)


                        