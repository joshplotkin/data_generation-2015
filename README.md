## Data generation using pure python, HAWQ (with PL/Python), or MapReduce (streaming via python)

### Instructions are included for each of the 3. MapReduce version is in the early stages and it's not currently recommended.

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
=======
## Data generation scripts

### TODO:

* location of locations_partitions.csv is hardcoded
* parallelize so it doesn't take so long
* fix bug that generates data past user defined end date
* come up with a realistic template so numbers aren't out of whack
* allow user defined customer data, more categories, and generally more versatile
* think about analysis that can be done --> add more columns
* minor: add adds weeks to the start date so we don't get data for the final half week
* script to calculate expected outputs based on profiles
* improve shell scripts (alternatively, do the below...)
* for transactions, give the option to provide either a folder of all profiles to iterate through or just one json (automatic checking)
* user input to generate config files
>>>>>>> 40fa23f5ba0967a674a0f5cb80bc097642b41a7a
