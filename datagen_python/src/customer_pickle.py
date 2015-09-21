import faker
from faker import Faker
import cPickle as pickle
import numpy as np
import datetime
from datetime import date
import os


class Customer:
	'generates a customer and corresponding transactions based on\
	profile'

	def __init__(self):
		self.fake = Faker()
		self.fake.seed(np.random.random())
		self.all_profiles = pickle.load(open('./pickles/all_profiles.pickle', 'rb'))
		self.cities = pickle.load(open('./pickles/cities.pickle', 'rb'))
		self.age_gender = pickle.load(open('./pickles/age_gender.pickle', 'rb'))
		
		self.customer_attr_list = self.generate_customer()

	def generate_transactions(self):
		# TODO: path lookup for pickles

		# TODO: look at more efficient way to generate the list
		profile_pickle = self.profile.replace('.json','.profile')
		# output = []
		transactions = pickle.load(open('./pickles/' + profile_pickle, 'rb')).sample_from()
		return [(self.customer_attr_list + '|' + t).split('|') for t in transactions]
		# for t in transactions:
		# 	cust = [c for c in self.customer_attr_list]
		# 	cust.extend(t)
		# 	output.append(cust)
		# return output

	def generate_customer(self):
		self.ssn = self.fake.ssn()
		self.gender, self.dob = self.generate_age_gender()
		self.first = self.get_first_name()
		self.last = self.fake.last_name()
		self.street = self.fake.street_address()
		self.addy = self.get_random_location()
		self.job = self.fake.job()

		# skipping CC for now
		# self.cc = self.fake.credit_card_full()
		self.email = self.fake.email()
		self.account = self.fake.random_number()
		self.profile = self.find_profile()
		return self.return_customer()
		# self.print_customer()

	def get_first_name(self):
		if self.gender == 'M':
			return self.fake.first_name_male()
		else:
			return self.fake.first_name_female()

	def generate_age_gender(self):
		g_a = self.age_gender[min([a for a in self.age_gender if a > np.random.random()])]

		while True:
			dob = self.fake.date_time_this_century()

			# adjust the randomized date to yield the correct age 
			start_age = (date.today() - date(dob.year, dob.month, dob.day)).days/365.
			dob_year = dob.year - int(g_a[1] - int(start_age)) 

			# since the year is adjusted, sometimes Feb 29th won't be a day
			# in the adjusted year
			try:
				# return first letter of gender and dob
			    return g_a[0][0], date(dob_year, dob.month, dob.day)
			except:
			    pass

	# find nearest city
	def get_random_location(self):
	    return self.cities[min([c for c in self.cities if c > np.random.random()])]

	def find_profile(self):
		age = (date.today() - self.dob).days/365.25
		city_pop = float(self.addy.split('|')[-1])

		match = []
		for pro in self.all_profiles:
			# -1 represents infinity
		    if self.gender in self.all_profiles[pro]['gender'] and \
		        age >= self.all_profiles[pro]['age'][0] and \
		        ( age < self.all_profiles[pro]['age'][1] or \
		        self.all_profiles[pro]['age'][1] == -1) and \
		        city_pop >= self.all_profiles[pro]['city_pop'][0] and \
		        (city_pop < self.all_profiles[pro]['city_pop'][1] or \
		        	self.all_profiles[pro]['city_pop'][1] == -1):
		            match.append(pro)
		if match == []:
		    match.append('leftovers.json')

		# found overlap -- write to log file but continue
		if len(match) > 1:
		    f = open('profile_overlap_warnings.log', 'a')
		    output = ' '.join(match) + ': ' + self.gender + ' ' +\
		    		 str(age) + ' ' + str(city_pop) + '\n'
		    f.write(output)
		    f.close()	
		return match[0]	

	def print_customer(self):
	     print str(self.ssn) + '|' +\
	     self.first + '|' +\
	     self.last + '|' +\
	     self.gender + '|' +\
	     self.street + '|' +\
	     self.addy + '|' +\
	     self.job + '|' +\
	     str(self.dob) + '|' +\
	     str(self.account)	+ '|' +\
	     self.profile	

	def return_customer(self):
	     # return [self.ssn, self.first, self.last, self.gender, \
	     # 		self.street, self.addy, self.job, str(self.dob), \
	     # 		str(self.account), self.profile]
	     return str(self.ssn) + '|' +\
	     self.first + '|' +\
	     self.last + '|' +\
	     self.gender + '|' +\
	     self.street + '|' +\
	     self.addy + '|' +\
	     self.job + '|' +\
	     str(self.dob) + '|' +\
	     str(self.account)	+ '|' +\
	     self.profile	
