from __future__  import division
import json
import sys
import datetime
from datetime import date
from datetime import timedelta
import random
import numpy as np
import math
from scipy.stats import rv_discrete


class Profile:
    def __init__(self, pro, start, end):
        self.profile = pro
        self.start = start
        self.end = end
        # form profile so it can be sampled from
        self.make_weights()

    def json_to_dict(self):
        self.profile = json.loads(json.dumps(self.profile, separators = (', ', ': ')).\
                    replace('\\n','').\
                    replace('\\t','').\
                    replace('\\','').\
                    replace('"{','{').\
                    replace('}"','}'))

    # turn dict into cumulative sum key
    # with entry value so we can sample
    def weight_to_cumsum(self, cat):
        wt_tot = sum(self.profile[cat].values())
        cumsum = 0
        for k in self.profile[cat]:
            cumsum += self.profile[cat][k]/float(wt_tot)
            self.profile[cat][k] = cumsum
        # invert
        self.profile[cat] = dict((self.profile[cat][k],k) for k in self.profile[cat])

    def weight_to_prop(self, profile_cat):
        wt_tot = sum(profile_cat.values())
        return dict((k, profile_cat[k]/float(wt_tot)) for k in profile_cat.keys())


    # ensures all weekdays are covered,
    # converts weekday names to ints 0-6
    # and turns from weights to log probabilities
    def prep_weekday(self):
        day_map = {'monday': 0, 'tuesday': 1, 'wednesday': 2,
                   'thursday': 3, 'friday': 4, 'saturday': 5,
                   'sunday': 6}
        # create dict of day:weight using integer day values
        weekdays = dict((day_map[day], self.profile['date_wt']['day_of_week'][day]) \
                for day in self.profile['date_wt']['day_of_week'].keys())
        # replace any missing weekdays with 100
        for d in [day_map[day] for day in day_map.keys() \
                if day not in self.profile['date_wt']['day_of_week'].keys()]:
            weekdays[d] = 100

        self.profile['date_wt']['day_of_week'] = self.weight_to_prop(weekdays)

    # take the time_of_year entries and turn into date tuples
    def date_tuple(self):
        holidays = self.profile['date_wt']['time_of_year']
        date_tuples = []
        for hol in holidays:
            start = None
            end = None
            weight = None
            for k in holidays[hol].keys():
                if 'start' in k:
                    curr_date = holidays[hol][k].split('-')
                    start = date(2000, int(curr_date[0]), int(curr_date[1]))
                elif 'end' in k:
                    curr_date = holidays[hol][k].split('-')
                    end = date(2000, int(curr_date[0]), int(curr_date[1]))
                elif 'weight' in k:
                    weight = holidays[hol][k]
            if start == None or end == None or weight == None:
                sys.stderr.write('Start or end date not found for time_of_year: ' + str(hol) + '\n')
                sys.exit(0)
            elif start > end:
                sys.stderr.write('Start date after end date for time_of_year: ' + str(hol) + '\n')
                sys.exit(0)
            date_tuples.append({'start':start, 'end':end, 'weight':weight})
        return date_tuples

    def prep_holidays(self):
        days = {}
        # all month/day combos (including leap day)
        init = date(2000, 1, 1)
        # initialize all to 100
        for i in range(366):
            curr = init + timedelta(days = i)
            days[(curr.month, curr.day)] = 100
        # change weights for holidays
        holidays = self.date_tuple()
        for h in holidays:
            while h['start'] <= h['end']:
                days[(h['start'].month, h['start'].day)] = h['weight']
                h['start'] += timedelta(days=1)

        # need separate weights for non-leap years
        days_nonleap = dict((k, days[k]) for k in days.keys() if k != (2,29))
        # get proportions for all month/day combos
        self.profile['date_wt']['time_of_year'] = self.weight_to_prop(days_nonleap)
        self.profile['date_wt']['time_of_year_leap'] = self.weight_to_prop(days)

    # checks number of years and converts
    # to proportions
    def prep_years(self):
        final_year = {}
        # extract years to have transactions for
        years = [y for y in range(self.start.year, self.end.year+1)]
        years.sort()
        # extract years provided in profile
        years_wt = ([y for y in self.profile['date_wt']['year'].keys()])
        years_wt.sort()
        # sync weights to extracted years
        for i, y in enumerate(years):
            if years_wt[i] in self.profile['date_wt']['year']:
                final_year[y] = self.profile['date_wt']['year'][years_wt[i]]
            # if not enough years provided, make it 100
            else:
                final_year[y] = 100
        self.profile['date_wt']['year'] = self.weight_to_prop(final_year)

    def combine_date_params(self):
        new_date_weights = {}
        weights = self.profile['date_wt']
        curr = self.start
        while curr <= self.end:
            # leap year:
            if curr.year%4 == 0:
                time_name = 'time_of_year_leap'
            else:
                time_name = 'time_of_year'

            date_wt = weights['year'][curr.year]*\
                      weights[time_name][(curr.month,curr.day)]*\
                      weights['day_of_week'][curr.weekday()]

            new_date_weights[curr] = date_wt
            curr += timedelta(days=1)
        # re-weight to get proportions
        self.profile['date_wt'] = self.weight_to_prop(new_date_weights)

    def date_weights(self):
        self.prep_weekday()
        self.prep_holidays()
        self.prep_years()
        self.combine_date_params()
        self.weight_to_cumsum('date_wt')
             
    # convert dates from weights to %
    def make_weights(self):
        # convert profile to a dict
        self.json_to_dict()
        # convert weights to proportions and use 
        # the cumsum as the key from which to sample
        self.weight_to_cumsum('categories_wt')
        self.date_weights()

    def closest_rand(self, pro, num):
        k = np.array(pro.keys(), dtype=float)
        # smallest positive number
        return pro[k[(k[np.where( k > num )]).argmin()]]

    def sample_amt(self, category):
        shape = self.profile['categories_amt'][category]['mean']**2/ \
                self.profile['categories_amt'][category]['stdev']**2
        scale = self.profile['categories_amt'][category]['stdev']**2/ \
                self.profile['categories_amt'][category]['mean']
        while True:
            amt = np.random.gamma(shape, scale, 1)[0]
            if amt > 0.20:
                return round(amt, 2)

    def sample_from(self):
        # randomly sample number of transactions
        num_trans = int((self.end - self.start).days * \
                np.random.uniform(self.profile['avg_transactions_per_day']['min'],\
                                  self.profile['avg_transactions_per_day']['max']))

        output = []
        rand_date = np.random.random(num_trans)
        rand_cat = np.random.random(num_trans)
        for i, num in enumerate(rand_date):
            chosen_date = self.closest_rand(self.profile['date_wt'], num)
            chosen_cat = self.closest_rand(self.profile['categories_wt'], rand_cat[i])
            chosen_amt = self.sample_amt(chosen_cat)
            output.append('|'.join([str(i), str(chosen_date), str(chosen_cat), str(chosen_amt)]))
            # output.append([str(i), str(chosen_date), str(chosen_cat), str(chosen_amt)])

        return output

