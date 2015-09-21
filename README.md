## Data generation using pure python, HAWQ (with PL/Python), or MapReduce (streaming via python)

TODO:
* location of locations_partitions.csv is hardcoded (fixed?)
* come up with a realistic template so numbers aren't out of whack
* script to calculate expected outputs based on profiles
* for transactions, give the option to provide either a folder of all profiles to iterate through or just one json (automatic checking)
* user input to generate config files

* test output against profiles
* add shell scripts to install python packages
* add shell scripts to fix hard coding for HAWQ and MR
* clean up HAWQ and MR code
* add more/better data

* improve performance of MapReduce
* Spark streaming?

* create_pickles doesn't run if the number of years doesn't match the profile inputs
* work on making datasets repeatable via random seed
* script to replace hashbang with `which python`
* script to replace hard links
