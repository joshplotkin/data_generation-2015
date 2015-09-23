#!/usr/local/hawq/ext/python/bin/python

import sys
import os
import cPickle as pickle
import random

from mrjob.job import MRJob


class test(MRJob):

    def mapper(self):
        yield random.random()

    # def combiner(self, word, counts):
    #     yield (word, sum(counts))

    # def reducer(self, word, counts):
    #     yield (word, sum(counts))


if __name__ == '__main__':
     test.run()









# #sys.path.append(os.getcwd())
# os.chdir('/data2/datagen_MR/pickles')

# print random.random()
# #customer = pickle.load(open(os.getcwd() + '/generate_customer.pickle', 'rb'))
# #alltrans = customer().generate_transactions()
# #print '\n'.join(['|'.join(a) for a in alltrans])
