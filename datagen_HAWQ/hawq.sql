select now();

DROP TYPE IF EXISTS transaction CASCADE;
CREATE TYPE transaction AS (
ssn text,
first text,
last text,
gender text,
street text,
city text,
state text,
zip text,
lat float8,
long float8,
city_pop integer,
job text,
dob date,
acct_num bigint,
profile text,
transnum integer,
transdate date,
category text,
amt float8);

DROP TABLE IF EXISTS trans_fact CASCADE;
CREATE TABLE trans_fact (
ssn text,
first text,
last text,
gender text,
street text,
city text,
state text,
zip text,
lat float8,
long float8,
city_pop integer,
job text,
dob date,
acct_num bigint,
profile text,
transnum integer,
transdate date,
category text,
amt float8)
DISTRIBUTED RANDOMLY;

DROP FUNCTION IF EXISTS customer(integer, text) CASCADE;
CREATE OR REPLACE FUNCTION customer(repeat text)
	RETURNS SETOF transaction
AS
$$  
	import cPickle as pickle
	import faker
	from faker import Faker
	import numpy as np
	import sys
	import os

	sys.path.append('/demo/103_datagen_HAWQ/datagen_HAWQ/src')
	sys.path.append('/demo/103_datagen_HAWQ/datagen_HAWQ')
	os.chdir('/demo/103_datagen_HAWQ/datagen_HAWQ')

	# not currently working: repeatable data set
	# if repeat.lower() != 'False':
	# 	np.random.seed(seed)

	customer = pickle.load(open('generate_customer.pickle', 'rb'))
	alltrans = customer(np.random.random()).generate_transactions()

	# see what's faster
	#for a in alltrans:
	#	yield(a)
	return [a for a in alltrans]
$$ 
LANGUAGE PLPYTHONU;

-- [pivhdsne:datagen_HAWQ]$ time psql -f hawq.sql -v customers=2
CREATE TEMPORARY TABLE numbers(n integer) DISTRIBUTED RANDOMLY;
INSERT INTO numbers
SELECT generate_series(1, :customers);

-- TODO: look into seed
INSERT INTO trans_fact
SELECT (t).* 
FROM 
	(SELECT (customer('False')) as t
	FROM (
		SELECT n 
		FROM numbers 
		)q
	)q2;

CREATE VIEW spending AS (
SELECT ssn, age, gender, count(*) as num_trans, 
	sum(food_dining) as food_dining, 
	sum(utilities) as utilities, 
	sum(grocery_net) as grocery_net, 
	sum(home) as home, 
	sum(pharmacy) as pharmacy, 
	sum(shopping_pos) as shopping_pos, 
	sum(kids_pets) as kids_pets, 
	sum(personal_care) as personal_care, 
	sum(misc_pos) as misc_pos, 
	sum(gas_transport) as gas_transport, 
	sum(misc_net) as misc_net, 
	sum(health_fitness) as health_fitness, 
	sum(shopping_net) as shopping_net, 
	sum(travel) as travel
	FROM(
	-- create case statements
	SELECT ssn as ssn, extract(years from age(NOW(),dob)) as age, 
	case when gender = 'M' then 0 else 1 end as gender,
	case when category = 'food_dining' then (amt) else 0 end as food_dining,
	case when category = 'utilities' then (amt) else 0 end as utilities, 
	case when category = 'grocery_net' then (amt) else 0 end as grocery_net, 
	case when category = 'home' then (amt) else 0 end as home, 
	case when category = 'pharmacy' then (amt) else 0 end as pharmacy, 
	case when category = 'shopping_pos' then (amt) else 0 end as shopping_pos, 
	case when category = 'kids_pets' then (amt) else 0 end as kids_pets, 
	case when category = 'personal_care' then (amt) else 0 end as personal_care, 
	case when category = 'misc_pos' then (amt) else 0 end as misc_pos, 
	case when category = 'gas_transport' then (amt) else 0 end as gas_transport, 
	case when category = 'misc_net' then (amt) else 0 end as misc_net, 
	case when category = 'health_fitness' then (amt) else 0 end as health_fitness, 
	case when category = 'shopping_net' then (amt) else 0 end as shopping_net, 
	case when category = 'travel' then (amt) else 0 end as travel

	FROM trans_fact) GROUPED
	GROUP BY ssn, age, gender
);

VACUUM ANALYZE trans_fact;

SELECT nspname || '.' || relname AS "relation",
	pg_size_pretty(pg_relation_size(C.oid)) AS "size"
  FROM pg_class C
  LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
  WHERE nspname NOT IN ('pg_catalog', 'information_schema') and relname = 'trans_fact'
  ORDER BY pg_relation_size(C.oid) DESC
  LIMIT 20;

select now();

