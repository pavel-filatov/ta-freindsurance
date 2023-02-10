/*
SQL Task 2
==========
Write script for selection of the docs with such conditions:

    - Docs from the Dec 2016,
    - Results are grouped by such weeks:
        * 1 week – from 01.12.2016 to 08.12.2016
        * 2 week – from 09.12.2016 to 15.12.2016
        * 3 week – from 16.12.2016 to 22.12.2016
        * 4 week – from 23.12.2016 to 31.12.2016,
    - In each week for each good return only the last document for this week.
      Keep in mind, that in case during the last day there were few documents with one good
      – return the document with the minimum(rate) and max(s_date).

Include into results columns: WeekNum, doc id, good_name, good_group_name, s_date, amount, rate.
*/

-- 1. Get December'16 records and assign week numbers to them
WITH docs_with_weeks AS (
SELECT
	CASE 
		WHEN CAST(s_date AS DATE) BETWEEN '20161201' AND '20161208' THEN 1
		WHEN CAST(s_date AS DATE) BETWEEN '20161209' AND '20161215' THEN 2
		WHEN CAST(s_date AS DATE) BETWEEN '20161216' AND '20161222' THEN 3
		WHEN CAST(s_date AS DATE) BETWEEN '20161223' AND '20161231' THEN 4
	END AS WeekNum,
	*
FROM
	docs
WHERE
	CAST(s_date AS DATE) BETWEEN '20161201' AND '20161231'
),

-- 2. Order all records per (good, week) groups and order them ...
ordered_docs AS (
SELECT
	*,
	ROW_NUMBER() OVER (
	    PARTITION BY WeekNum, id_good
	    -- ... ordering is per DATE (not time!), rate, and then time
	    ORDER BY CAST(s_date AS DATE) DESC, rate, s_date DESC
	) AS RowNum
FROM
	docs_with_weeks
)

-- 3. Get only the first record for each group, as it represents the target condition
SELECT 
	d.id AS doc_id,
	rg.good_name AS good_name,
	rgg.good_group_name AS good_group_name,
	d.s_date AS s_date,
	d.amount AS amount,
	d.rate AS rate,
	WeekNum
FROM
	ordered_docs d
LEFT JOIN ref_goods rg ON
	d.id_good = rg.id
LEFT JOIN ref_good_groups rgg ON
	rg.id_good_group = rgg.id 
WHERE
	d.RowNum = 1
