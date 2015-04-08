python datagen_customer.py 10000 4444 main_config.json >> ~/Desktop/meetup_data/customers.csv

python datagen_transaction.py ~/Desktop/meetup_data/customers.csv ./profiles/40_60_bigger_cities.json 1-1-2013 12-31-2014 >> ~/Desktop/meetup_data/40_60_bigger_cities.csv
python datagen_transaction.py ~/Desktop/meetup_data/customers.csv ./profiles/40_60_smaller_cities.json 1-1-2013 12-31-2014 >> ~/Desktop/meetup_data/40_60_smaller_cities.csv
python datagen_transaction.py ~/Desktop/meetup_data/customers.csv ./profiles/all_60_up.json 1-1-2013 12-31-2014 >> ~/Desktop/meetup_data/all_60_up.csv
python datagen_transaction.py ~/Desktop/meetup_data/customers.csv ./profiles/female_30_40_bigger_cities.json 1-1-2013 12-31-2014 >> ~/Desktop/meetup_data/female_30_40_bigger_cities.csv
python datagen_transaction.py ~/Desktop/meetup_data/customers.csv ./profiles/female_30_40_smaller_cities.json 1-1-2013 12-31-2014 >> ~/Desktop/meetup_data/female_30_40_smaller_cities.csv
python datagen_transaction.py ~/Desktop/meetup_data/customers.csv ./profiles/leftovers.json 1-1-2013 12-31-2014 >> ~/Desktop/meetup_data/leftovers.csv
python datagen_transaction.py ~/Desktop/meetup_data/customers.csv ./profiles/male_30_40_bigger_cities.json 1-1-2013 12-31-2014 >> ~/Desktop/meetup_data/male_30_40_bigger_cities.csv
python datagen_transaction.py ~/Desktop/meetup_data/customers.csv ./profiles/male_30_40_smaller_cities.json 1-1-2013 12-31-2014 >> ~/Desktop/meetup_data/male_30_40_smaller_cities.csv
python datagen_transaction.py ~/Desktop/meetup_data/customers.csv ./profiles/millenials.json 1-1-2013 12-31-2014 >> ~/Desktop/meetup_data/millenials.csv
python datagen_transaction.py ~/Desktop/meetup_data/customers.csv ./profiles/young_adults.json 1-1-2013 12-31-2014 >> ~/Desktop/meetup_data/young_adults.csv
