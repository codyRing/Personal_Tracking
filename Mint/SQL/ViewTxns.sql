use mint;
Select
row_number() over (partition by t.category order by transdate desc)
,t.TransDate,t.Description,t.category, t.amount,t.notes,t.id
From txn t
    left join budget_discretionary bd
        on t.id = bd.id
where bd.id is not  null
and t.transdate between '2020-08-01' and '2020-08-31'
and t.TransactionType like 'debit'
-- order by transdate desc
