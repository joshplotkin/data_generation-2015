## Usage:
* Locally
 * (optional) modify main_config.json and json profiles to your liking
 * run 'python create_pickles.py'

* On data nodes
 * copy datagen_HAWQ/ to the same directory location on each data node
 * ensure the following python packages are installed for the python installation indicated in greenplum_path: fake-factory (tarball included) and numpy
 * to test that the python is working, run 'python EXECUTE.py' which should output transactions for one customer 

* On HAWQ master
 * copy hawq.sql anywhere on the HAWQ master
 * currently lines 60-62 of hawq.sql have the location of datagen_HAWQ/ hard-coded. ensure that matches the directory location on your data nodes
 * run psql -f hawq.sql -v customers=N (where N is the desired number of customers -- roughly 2,000,000 per 1 TB under default configuration)

### TODO:
* provide script to install packages
* provide script to modify path on data nodes
