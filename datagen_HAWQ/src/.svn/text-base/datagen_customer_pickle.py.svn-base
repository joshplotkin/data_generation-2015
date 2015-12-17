import faker
from faker import Faker
import random
import numpy as np
import sys
import datetime
from datetime import date
from datetime import timedelta
import fileinput
import random
from collections import defaultdict
import json
import cPickle as pickle
import subprocess
import os

from main_config import MainConfig
import demographics
import profile_weights_pickle
import customer_pickle
from customer_pickle import *
from create_pickles import *

class Headers:
	'Store the headers and print to stdout to pipe into csv'
	def __init__(self):
		self.make_headers()
		self.print_headers()

	def make_headers(self):
		headers = ''
		for h in ['ssn', 'first', 'last', 'gender', 'street', \
				  'city', 'state', 'zip', 'lat', 'long', 'city_pop', \
				  'job', 'dob', 'acct_num', 'profile']:
			headers += h + '|'
		self.headers = headers[:-1]

	def print_headers(self):
		print self.headers

if __name__ == '__main__':
	# read and validate stdin
	try:
		num_cust = int(sys.argv[1])
	except:
		print 'Enter number of customers as command line argument'
		sys.exit(0)

	Customer = pickle.load(open('./pickles/generate_customer.pickle', 'rb'))
	os.chdir(os.getcwd() + '/pickles')
	for _ in range(num_cust):
		print Customer().generate_transactions()