import random
import pandas as pd
from pandas import *
import json
import numpy as pd
import sys
import datetime
from datetime import timedelta
from datetime import date
import math

import profile_weights

def get_user_input():
    # convert date to datetime object
    def convert_date(d):
        for char in ['/', '-', '_', ' ']:
            if char in d:
                d = d.split(char)
                try:    
                    return date(int(d[2]), int(d[0]), int(d[1]))
                except:
                    error_msg(3)
        error_msg(3)

    # error handling for CL inputs
    def error_msg(n):
        if n == 1:
            print 'Could not open customers file\n'
        elif n == 2:
            print 'Could not open main config json file\n'
        else:
            print 'Invalid date (MM-DD-YYYY)'
        output = 'ENTER:\n(1) Customers csv file\n'
        output += '(2) profile json file\n'
        output += '(3) Start date (MM-DD-YYYY)\n'
        output += '(4) End date (MM-DD-YYYY)\n'
        print output
        sys.exit(0)

    try:
        customers = open(sys.argv[1], 'r').readlines()
    except:
        error_msg(1)   
    try:
        pro = open(sys.argv[2], 'r').read()
        pro_name = sys.argv[2].split('/')[-1]
    except:
        error_msg(2)    
    try:
        startd = convert_date(sys.argv[3])
    except:
        error_msg(3)        
    try:
        endd = convert_date(sys.argv[4])
    except:
        error_msg(4)

    return customers, pro, pro_name, startd, endd

def create_header(line):
    headers = line.split('|')
    headers[-1] = headers[-1].replace('\n','')
    headers.extend(['trans_num', 'trans_date', 'category', 'amt'])
    print ''.join([h + '|' for h in headers])[:-1]
    return headers


class Customer:
    def __init__(self, customer, profile):
        self.customer = customer
        self.attrs = self.clean_line(self.customer)
    
    def print_trans(self, trans):
        for t in trans:
            print self.customer + '|' + t

    def clean_line(self, line):
        # separate into a list of attrs
        cols = [c.replace('\n','') for c in line.split('|')]
        # create a dict of name:value for each column
        attrs = {}
        for i in range(len(cols)):
            attrs[headers[i].replace('\n','')] = cols[i].replace('\n','')
        return attrs

if __name__ == '__main__':
    # read user input into Inputs object
    # to prepare the user inputs
    customers, pro, curr_profile, start, end = get_user_input()
    profile = profile_weights.Profile(pro, start, end)

    # takes the customers headers and appends
    # transaction headers and returns/prints
    headers = create_header(customers[0])

    # for each customer, if the customer fits this profile
    # generate appropriate number of transactions
    for line in customers[1:]:
        cust = Customer(line, profile)
        if cust.attrs['profile'] == curr_profile:
            cust.print_trans(profile.sample_from())