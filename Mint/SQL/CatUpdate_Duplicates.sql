Start Transaction ;
Select * from (
	SELECT
		row_number() OVER (
			PARTITION BY Amount ,TransDate ,OriginalDescription
            ORDER BY RowDate desc
			) AS indx
         , t.*
	FROM TXN t

	WHERE 
        Labels not like '%ND%'  and
		transdate >= '2011-01-01'
) x where indx >1;

-- ^View original ^----------------------


-- Delete all indx 2 records 

Delete from txn
where id in(

Select x.id from (
	SELECT
		row_number() OVER (
			PARTITION BY Amount ,TransDate ,OriginalDescription
            ORDER BY RowDate desc
			) AS indx
         , t.*
	FROM TXN t

	WHERE 
        Labels not like '%ND%'  and
		transdate >= '2011-01-01'
) x where indx >1
);



Commit  


