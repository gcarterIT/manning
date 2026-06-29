/****** Script for SelectTopNRows command from SSMS  ******/

SELECT count(*)
  FROM [manning_book_reviews].[dbo].[purchases]
-- 71519

-- assumptions
-- not important, delte the following:
--   [event_time]
--   [product_id]
--   [category_id]
--   [category_code]
--   [brand]
--   [price]
--   [session_id]

-- these could tie into customer db
-- those that don't should be added to total
--      ,[customer_id] <- if in customer db don't add to total
--      ,[guest_first_name] <- if these next three not in customer db add to total
--      ,[guest_surname]
--      ,[guest_postcode]

-- remove excess columns
SELECT [customer_id]
      ,[guest_first_name]
      ,[guest_surname]
      ,[guest_postcode]
into
	purch1
FROM [manning_book_reviews].[dbo].[purchases]

SELECT * FROM purch1

SELECT count(*)
  FROM purch1
-- 71519

-- assume a custome only has 1 customer id
-- remove duplicates

-- collect all non_NULL distinct customer_ids
-- we will match these against the customer_ids in the cust db
-- those that don't match will be added to the total

select distinct
	customer_id
into
	purch_cust_ids
from
	purch1
where 
	customer_id is not null
order by
	customer_id

SELECT distinct
* 
FROM purch_cust_ids
order by customer_id

SELECT count(*) 
FROM purch_cust_ids
-- 24959

-- we'll only use name when we have both last and first names and postcode
--  inspection shows none of the fields have NULLs
-- if same name appears for more than 1 post code, we'll assume those are 
--	people sharing same name
select distinct 
	guest_first_name
	,guest_surname
	,guest_postcode
	,guest_surname+guest_first_name+guest_postcode as combined
into
	purch_names_postcodes2
from
	purch1
where 
	customer_id is null

select count(*) from purch_names_postcodes2
-- 8300

select * from purch_names_postcodes2

--=============================================

-- now lets compare our new purch tables against cust
--	db to determine if purch table had custs unaccounted for

-- make copy of cust db to assure original undisturbed
select
	*
into
	cust_copy
from
	[dbo].[customer_database]

select count(*) from cust_copy
-- 23475

-- concatenate names and post codes

select
	*
	,surname+first_name+postcode as combined
into
	cust_copy2
from
	cust_copy

select count(*) from cust_copy2
-- 23475





-------------------------------------------------------

-- find which cust_ids in purch are not in cust db

select
	*
into 
	purch_cust_ids_not_in_cust
from 
	purch_cust_ids
where 
	purch_cust_ids.customer_id not in (select 
											customer_id
										from
											cust_copy2)

select count(*) from purch_cust_ids_not_in_cust
-- 3617
-- these cust_ids not in cust db
-- we will add this number to total at end


-------------------------------------------------------

-- find which cust names and post codes not in cust db

select
	*
into 
	purch_names_postcodes2_not_in_cust
from 
	purch_names_postcodes2
where 
	purch_names_postcodes2.combined not in (select 
												combined
											from
												cust_copy2)
-- 6148
-- these cust names post codes not in cust db
-- we will add this number to total at end

------------------------------------------------------------

-- add cust id from cust2

select
	customer_id,
	null as [first_name],
	null as [surname],
	null as [postcode],
	null as [age],
	null as [combined]
into
	cust_copy3
from
	purch_cust_ids_not_in_cust
union
select
	null as customer_id,
	null as [first_name],
	null as [surname],
	null as[postcode],
	null as[age],
	[combined]
from
	purch_names_postcodes2_not_in_cust
union
select 
	*
from
	cust_copy2

-- 33241
-- 23476 + 3617 + 6148 = 33241

select count(*) from cust_copy3
-- 33241

--========================================================

-- now lets do simil;ar for crm-export table


-- collect all non_NULL distinct customer_ids
-- we will match these against the customer_ids in the cust db
-- those that don't match will be added to the total

select distinct
	customer_id
into
	crm_cust_ids
from
	[dbo].[crm_export]
where 
	customer_id is not null
order by
	customer_id

SELECT distinct
* 
FROM crm_cust_ids
order by customer_id

SELECT count(*) 
FROM crm_cust_ids
-- 7825

-- find which cust_ids in crm are not in cust db

select
	*
into 
	crm_cust_ids_not_in_cust
from 
	crm_cust_ids
where 
	crm_cust_ids.customer_id not in (select 
											customer_id
										from
											cust_copy3)

select count(*) from crm_cust_ids_not_in_cust
-- 0
-- so all cust_ids in crm already accounted for in cust db

---------------------------------------------

-- now lets check name and post codes

-- find which cust names and post codes not in cust db

-- we'll only use name when we have both last and first names and postcode
--  inspection shows none of the fields have NULLs
-- if same name appears for more than 1 post code, we'll assume those are 
--	people sharing same name
select distinct 
	first_name
	,surname
	,postcode
	,surname+first_name+postcode as combined
into
	crm_names_postcodes
from
	[dbo].[crm_export]
where 
	customer_id is null

select count(*) from crm_names_postcodes
-- 0
-- so all already accounted for in cust db

--==============================================

--   Thus, total customers = 33241
