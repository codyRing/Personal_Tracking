Create View budget_discretionary as 
Select
t.transdate
,t.description
,t.originaldescription
,t.amount
,t.TransactionType
,t.category
,t.AccountName
,t.Labels
,t.Notes
,t.id
from txn t
    join budget b
        on t.category = b.category
where 
    b.discretionary = 1
    -- and t.transdate >= (last_Day(now()) + interval 1 day+ interval -1 year)



# Beginning of next month - 1 year
d = datetime.today() + pd.offsets.MonthBegin(1)
d = d - relativedelta(years=1)
data = data.loc[data.index >= d]