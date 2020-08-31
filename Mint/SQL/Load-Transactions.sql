use mint;
-- drop table notduplicates;
-- Drop table txn;


-- Create table Txn(
-- TransDate date,
-- Description varchar(250),
-- OriginalDescription varchar(250),
-- Amount Decimal(18,2),
-- TransactionType varchar(250),
-- Category varchar(250),
-- AccountName varchar(250),
-- Labels varchar(250),
-- Notes varchar(250),
-- id INT AUTO_INCREMENT PRIMARY KEY,
-- RowDate datetime ,
-- KEY `SECONDARY` (`TransDate`),
-- index TdateAsc(TransDate desc)
-- );


-- CREATE TABLE `notduplicates` (
--   `id` int DEFAULT NULL,
-- Foreign Key(id)
-- references txn(id)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Load Data Infile 'C:\\Users\\User\\Source\\Personal_Tracking\\Data\\Mint\\transactions.csv' 
Truncate table TXN_Stage;

Load Data Infile 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\transactions.csv'
into table TXN_Stage
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 rows
(@d,Description,OriginalDescription,Amount,TransactionType,Category,AccountName,Labels,Notes)
set TransDate = STR_To_Date(@d,'%m/%d/%Y') ;

Insert into TXN(TransDate,Description,OriginalDescription,Amount,TransactionType,Category,AccountName,Labels,Notes,RowDate)
Select
s.TransDate
,S.Description
,S.OriginalDescription
,s.Amount
,S.transactionType
,S.Category
,S.AccountName
,S.Labels
,S.notes
,now() 

from TXN_Stage s
	left join TXN t
		on 
        s.transDate = t.TransDate and
        s.amount = t.amount and
        s.transactiontype = t.transactiontype and
        s.category = t.category and
        s.AccountName = t.accountName and
        s.Description = t.description
where 
	s.category not in('Credit Card Payment','Transfer') and -- These are all Duplicated. Debit from Chase and credit to BOA. Transfer less exact but very close to $0
    s.accountname not in ('PayPal Account') and -- also mostly duplcated by chase payments
	t.id is null
order by s.TransDate Asc


        
