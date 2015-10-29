import cPickle as pickle
import faker
from faker import Faker
import numpy as np
import sys
import os

dir = os.getcwd()

sys.path.append(dir + '/src')
sys.path.append(dir)
os.chdir(dir)

# not currently working: repeatable data set
# if repeat.lower() != 'False':
# 	np.random.seed(seed)

customer = pickle.load(open('generate_customer.pickle', 'rb'))
alltrans = customer(np.random.random()).generate_transactions()

print alltrans