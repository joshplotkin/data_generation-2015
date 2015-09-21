#!/usr/local/bin/python

import sys
import os
import cPickle as pickle
import random
import subprocess
from subprocess import Popen, PIPE

def run(cmd, output = False):
        if output == True:
                return Popen([cmd],stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True).communicate()[0].split('\n')[:-1]
        out = Popen([cmd], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True).communicate()

sys.path.append('./src')
f = open('./pickles/generate_customer.pickle', 'rb')

customer = pickle.load(f)
alltrans = customer().generate_transactions()
print '\n'.join(['|'.join(a) for a in alltrans])
