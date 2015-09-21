* required directories:
 * profiles (with main_config.json and other profile json files)
 * demographic_data with age_gender_demographics.csv and locations_partitions.csv
 * pickles directory
* run 'python create_pickles.py'

TODO:
* create_pickles doesn't run if the number of years doesn't match the profile inputs
* work on making datasets repeatable via random seed
* script to replace hashbang with `which python`
* script to replace hard links
