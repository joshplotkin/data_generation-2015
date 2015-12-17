import cPickle as pickle
import faker
from faker import Faker
import numpy as np

fake = Faker()
fake.seed(int(np.random.uniform(-1000000,1000000)))

Customer = pickle.load(open('generate_customer.pickle', 'rb'))

print Customer().return_customer()
