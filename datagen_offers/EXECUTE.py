#!/usr/local/bin/python

import sys
import os
import cPickle as pickle

sys.path.append('./src')
f = open('./pickles/generate_customer.pickle', 'rb')

customer = pickle.load(f)
alltrans = customer().generate_transactions()
print '\n'.join(['|'.join(a) for a in alltrans])
