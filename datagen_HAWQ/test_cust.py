#!/usr/local/bin/python

import sys
sys.path.append('./src')

from customer_pickle import *
import cPickle as pickle

sys.path.append('./src')
f = open('./pickles/generate_customer.pickle', 'rb')

CustomerPickle = pickle.load(f)
# with open('test_cust.txt','w') as w:
with open('test_cust_pickle.txt','w') as w:
	for _ in range(10000):
		# w.write(Customer().customer_attr_list + '\n')
		w.write(CustomerPickle().customer_attr_list + '\n')
