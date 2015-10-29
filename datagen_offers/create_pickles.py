import sys
sys.path.append('./src')

from main_config import MainConfig
import demographics
import profile_weights_pickle
import customer_pickle
from customer_pickle import *
from create_pickles import *
import subprocess
import datetime
from datetime import date


def validate():
	def convert_date(d):
		for char in ['/', '-', '_', ' ']:
			if char in d:
				d = d.split(char)
				try:
					return date(int(d[2]), int(d[0]), int(d[1]))
				except:
					error_msg(2)
		error_msg(2)

	def print_err(n):
		if n == 1:
			print 'Error: invalid or missing profiles directory'
		elif n == 2:
			print 'Error: main_config.json missing from profiles directory'
		elif n == 3:
			print 'Error: individual profiles missing from profiles directory'
		elif n == 4:
			print 'Error: invalid date'

		output = '\nENTER:\n (1) Transaction start date (MM-DD-YYYY)\n '
		output += '(2) Transaction end date (MM-DD-YYYY)'

		print output
		sys.exit(0)		           

	try:
		profiles = subprocess.Popen(['ls','profiles'], stdout=subprocess.PIPE)\
							 .communicate()[0].split('\n')
		profiles = [p for p in profiles if p.split('.')[-1] == 'json']
		if 'main_config.json' not in profiles:
			print_err(2)
		else:
			if len(profiles) == 1:
				print_err(3)
	except:
		print_err(1)
	try:
		start = convert_date(sys.argv[1])
		end = convert_date(sys.argv[2])
	except:
		print_err(4)
	
	return ['./profiles/' + p for p in profiles], start, end


class CreatePickles:
	'generates the .pickle files for: Customer object, cities/age_gender dicts, \
	main_config, and individual profiles'
	def __init__(self, profiles, start, end):

		self.profiles = profiles
		self.start = start
		self.end = end

		self.pickle_demographics()
		self.pickle_profiles()
		self.pickle_customer()

	def pickle_profiles(self):
		# turn all profiles into dicts to work with
		main = [p for p in self.profiles if 'main_config.json' in p][0]
		main = open(main, 'r').read()

		# pickle the main_config.json
		main_config = MainConfig(main).config
		with open('./pickles/all_profiles.pickle', 'wb') as output:
		    pickle.dump(main_config, output, pickle.HIGHEST_PROTOCOL)

		# pickle the profiles
		individual_profiles = [p for p in self.profiles if 'main_config.json' not in p]
		for p, pro in [(p, open(p, 'r').read()) for p in individual_profiles]:
			profile = profile_weights_pickle.Profile(pro, self.start, self.end)
			# skip pickling the template
			if p.split('/')[-1].split('.')[0] == 'template':
				pass
			else:
				with open(p.replace('.json','.profile').\
							replace('/profiles/','/pickles/'), \
							'wb') as output:
				    pickle.dump(profile, output, pickle.HIGHEST_PROTOCOL)

	def pickle_demographics(self):
		cities = demographics.make_cities()
		age_gender = demographics.make_age_gender_dict()
		with open('./pickles/cities.pickle', 'wb') as output:
		    pickle.dump(cities, output, pickle.HIGHEST_PROTOCOL)
		with open('./pickles/age_gender.pickle', 'wb') as output:
		    pickle.dump(age_gender, output, pickle.HIGHEST_PROTOCOL)

	def pickle_customer(self):
		with open('./pickles/generate_customer.pickle', 'wb') as output:
		    pickle.dump(Customer, output, pickle.HIGHEST_PROTOCOL)

# THIS PROGRAM CREATES THE PICKLES FROM THE PROFILES
if __name__ == '__main__':
	# read and validate stdin
	profiles, start, end = validate()
	CreatePickles(profiles, start, end)
