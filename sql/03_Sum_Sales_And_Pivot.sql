/*
SQL Task 3
==========
Write script for selecting sum(sales) with such conditions:

    - Date begin and date end as parameters,
    - Group sum(sales) per [good_name] (which show in rows) and per dates (which are going to the column headers).
      Keep in mind, that since we can set various begin and end date as parameters for the query –
      the number of columns in the final report is unknown.


Explanations
============
Aggregating data by a set of grouping variables is a trivial task.
But in this case, the output data is presented as a "tall" table.
That means, the main task is to transpose the tall table into a wide representation.

For this, T-SQL has the PIVOT function available: one column's values become separate columns.
The only problem of this approach, it expects a predefined set of output columns
(which is, well, unknown in advance).

As a workaround, I chose the approach with dynamic script:
if we're able to create a template with placeholders for columns, that's everything needed.

The idea came from SO: https://stackoverflow.com/a/10404455
*/

-- 1. Set variables for the query and validate them
DECLARE @DateBegin DATE
DECLARE @DateEnd DATE

--- SET DESIRED VALUES HERE
SET @DateBegin = '20160101'
SET @DateEnd = '20160110'

IF @DateEnd < @DateBegin
	THROW 51000, '@DateEnd cannot be less than @DateBegin!', 1

SELECT @DateBegin AS DateBegin, @DateEnd AS DateEnd

-- 2. Declare helper variables
--- To keep dates that become columns in the end
DECLARE @DateColumns NVARCHAR(MAX)
--- To iterate over dates
DECLARE @LoopDate DATE
--- As a template of the pivotal query
DECLARE @PivotQuery NVARCHAR(MAX)


-- 3. Generate a list of date-columns by iterating from the start to the end date
SET @DateColumns = ''
SET @LoopDate = @DateBegin

WHILE @LoopDate <= @DateEnd
BEGIN
	SET @DateColumns = @DateColumns	+ QUOTENAME(@LoopDate)
	IF @LoopDate < @DateEnd
		SET @DateColumns = @DateColumns + ','
	SET @LoopDate = DATEADD(DAY, 1, @LoopDate) 
END

-- 4. Generate the query to transpose the data
--- Note that filtering is done on the pivot side not in query
SET @PivotQuery = '
	SELECT good_name, ' + @DateColumns + ' FROM (
		SELECT
        	id_good,
			good_name,
        	CAST(s_date AS DATE) AS s_date,
        	amount
        FROM
        	sales s
		JOIN
			ref_goods AS g
		    	ON s.id_good = g.id
	) base

	PIVOT (
		SUM(amount) FOR s_date IN (' + @DateColumns + ')
	) pvt

	ORDER BY pvt.id_good
' 

-- 5. Show the results!
EXECUTE (@PivotQuery)
