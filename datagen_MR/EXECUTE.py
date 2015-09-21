#!/usr/local/hawq/ext/python/bin/python

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


#sys.path.append(os.getcwd())
#os.chdir('/data2/datagen_MR/')
cust_pickle = '/data2/datagen_MR/pickles/generate_customer.pickle'

f = open(cust_pickle, 'rb')

run('cp -rf /data2/datagen_MR .')
run('chmod -R 777 ./datagen_MR')

sys.path.append('/data2/datagen_MR')
sys.path.append('./datagen_MR')
sys.path.append('/usr/local/hawq/ext/python/lib/python2.6/site-packages/fake_factory-0.5.1-py2.6.egg/')
sys.path.append('/usr/local/hawq/ext/python/lib/python2.6/site-packages/importlib-1.0.3-py2.6.egg/')
sys.path.append('/usr/local/hawq/ext/python/lib/python2.6/site-packages/*')
sys.path.append('/usr/local/hawq/ext/python/lib/python2.6/site-packages/importlib-1.0.3-py2.6.egg/importlib/')
sys.path.append('/usr/local/hawq/ext/python/lib/python2.6/site-packages/importlib-1.0.3-py2.6.egg/')
sys.path.append('/usr/local/hawq/ext/python/lib/python2.6/site-packages/')


f = open('/data2/datagen_MR/pickles/generate_customer.pickle', 'rb')
print run('hostname', True), run('ls', True), sys.version, sys.executable

try:
	customer = pickle.load(f)
        alltrans = customer().generate_transactions()
	print '\n'.join(['|'.join(a) for a in alltrans])
except ImportError, e:
	print e
except IOError, e2:
	print e2
	print os.getcwd()
except:
	print sys.exc_info()

