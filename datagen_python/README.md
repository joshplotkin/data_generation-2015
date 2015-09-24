### Usage:
* modify main_config.json and json profiles to your liking
* run 'python create_pickles.py <transaction start date MM-DD-YYYY> <end date>' (number of years be consistent with number of years in the profiles, which is 3 by default)
* to test usage, run 'python EXECUTE.py' for to generate 1 customer's transactions
* to create a dataset trans_fact.csv, run 'sh GENERATE_DATASET.sh N' where N is the desired number of customers
