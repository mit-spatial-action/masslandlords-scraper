-- This query returns week over week eviction filings 
-- in wide format (with districts in columns).

-- This outer query is the long-to-wide pivot.
SELECT 
	week_start,
	week_end,
	COALESCE(max(n) FILTER (WHERE district = 'central'), 0) AS C_db,
	COALESCE(max(n) FILTER (WHERE district = 'eastern'), 0) AS E_db,
	COALESCE(max(n) FILTER (WHERE district = 'metrosouth'), 0) AS MS_db,
	COALESCE(max(n) FILTER (WHERE district = 'northeast'), 0) AS NE_db,
	COALESCE(max(n) FILTER (WHERE district = 'southeast'), 0) AS SE_db,
	COALESCE(max(n) FILTER (WHERE district = 'western'), 0) AS W_db
FROM (
	-- This inner query groups filings by week.
	SELECT 
		-- MassLandlords week starts on Sunday, not Monday.
		-- Thus, the INVERVAL shift.
		date_trunc('week', file_date + INTERVAL '1 day') - INTERVAL '1 day' AS week_start,
		date_trunc('week', file_date + INTERVAL '1 day') + INTERVAL '5 day' AS week_end,
		district,
		COUNT(*) AS n
	FROM filings
	GROUP BY week_start, week_end, district
	ORDER BY week_start
	) AS long
GROUP BY week_start, week_end
ORDER BY week_start, week_end;

-- This query returns week over week eviction filings 
-- ~~where we successfully pulled the address~~
-- in wide format (with districts in columns).

-- This outer query is the long-to-wide pivot.
SELECT 
	week_start,
	week_end,
	COALESCE(max(n) FILTER (WHERE district = 'central'), 0) AS C_db_add,
	COALESCE(max(n) FILTER (WHERE district = 'eastern'), 0) AS E_db_add,
	COALESCE(max(n) FILTER (WHERE district = 'metrosouth'), 0) AS MS_db_add,
	COALESCE(max(n) FILTER (WHERE district = 'northeast'), 0) AS NE_db_add,
	COALESCE(max(n) FILTER (WHERE district = 'southeast'), 0) AS SE_db_add,
	COALESCE(max(n) FILTER (WHERE district = 'western'), 0) AS W_db_add
FROM (
	-- This inner query groups filings by week.
	SELECT 
		-- MassLandlords week starts on Sunday, not Monday.
		-- Thus, the INVERVAL shift.
		date_trunc('week', file_date + INTERVAL '1 day') - INTERVAL '1 day' AS week_start,
		date_trunc('week', file_date + INTERVAL '1 day') + INTERVAL '5 day' AS week_end,
		district,
		COUNT(*) AS n
	FROM filings
	WHERE add_p IS NOT NULL
	GROUP BY week_start, week_end, district
	ORDER BY week_start
	) AS long
GROUP BY week_start, week_end
ORDER BY week_start, week_end;
