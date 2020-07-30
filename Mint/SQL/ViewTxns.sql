use mint;
Select
row_number() over (partition by category order by transdate desc)
,t.*
From txn t
    left join budget_discretionary bd
        on t.id = bd.id
where bd.id is not null
and t.transdate >= '2020-07-01'
and t.TransactionType like 'debit'