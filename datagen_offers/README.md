### Usage:
* modify main_config.json and json profiles to your liking
* run 'python create_pickles.py <transaction start date MM-DD-YYYY> <end date>' (number of years be consistent with number of years in the profiles, which is 3 by default)
* install fake-factory (tarball included) and numpy. you can use `pip install <package>` or unzip the package tarballs and run `python setup.py build; python setup.py install` in the package directory.
* to test usage, run 'python EXECUTE.py' for to generate 1 customer's transactions
* to create a dataset trans_fact.csv, run 'sh GENERATE_DATASET.sh N' where N is the desired number of customers
* to run in HAWQ, enter "psql -f hawq.sql -v customers=<# of customers desired> dir=<location of datagen_HAWQ dir on each segment host>

### TODO:
* break offers into a config json and pickle/load during run
* improved offers
