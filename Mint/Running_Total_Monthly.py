import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import seaborn as sns
from datetime import datetime, timedelta
from sklearn import preprocessing

data = pd.read_csv('../Data/Mint/transactions.csv')
data['Date'] = pd.to_datetime(data.Date) - timedelta(days=1)
data = data.set_index('Date')

Spend = pd.DataFrame(data[data['Transaction Type'].str.contains('debit')])
Earn = pd.DataFrame(data[data['Transaction Type'].str.contains('credit')])

# -------------------------------------------------------
# Spend = Spend[Spend.Category != 'Mortgage & Rent']
# Spend=Spend[~Spend.Category.str.contains("Mortgage & Rent")]
# print(Spend['Category'].value_counts())
Spend = Spend[~Spend['Category'].isin(['Auto Insurance','Mortgage & Rent','Utilities','Credit Card Payment'])]

# Spend[Spend['Category'].str.match('Alcohol & Bars')]


#indexNames = Spend[Spend['Category'] == "Alcohol & Bars"].index
#indexNames = Spend[Spend.Category != 'Alcohol & Bars'].index
#indexNames=Spend[~Spend.Category.str.contains("Alcohol & Bars")].index
#Spend.drop(indexNames, inplace=True)

# Spend = Spend[Spend['Category'].str.contains('Mortgage & Rent')]
# Spend = Spend.drop(Spend[Spend['Category'].str.contains('Mortgage & Rent')].index)
# Spend = Spend.drop(Spend[Spend['Category'] == 'Mortgage & Rent'].index)


# min_max_scaler = preprocessing.MinMaxScaler()
# x = Spend[['Amount']].values.astype(float)
# x_scaled = min_max_scaler.fit_transform(x)
# Spend = pd.DataFrame(x_scaled,index=Spend.index,columns=['Amount'])


# -------------------------------------------------------
d = (datetime.today() - timedelta(weeks=48))
Spend = Spend.loc[Spend.index >= d]

Spend_Matrix = Spend.resample('D').sum()

Spend_Matrix = pd.pivot_table(Spend_Matrix,
                              index=Spend_Matrix.index.day,
                              columns=Spend_Matrix.index.month,
                              values="Amount")

Spend_Matrix = Spend_Matrix.cumsum()
Spend_Matrix.sort_index(level=0, ascending=False, inplace=True)

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[14, 7])
sns.heatmap(Spend_Matrix, annot=True, annot_kws={"size": 7}, fmt="g", linewidths=.5, cbar=False, cmap="Blues", ax=ax)
# .savefig('../data/mint/Daily_Heat.png', dpi=300)

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[14, 7])
for i in range(1, 13):
    sns.lineplot(
        x=Spend_Matrix.index,
        y=Spend_Matrix[i],
        data=Spend_Matrix

    )
plt.show()

# sns.lineplot(
#     x=Spend_Matrix.index,
#     y=Spend_Matrix[2],
#     data=Spend_Matrix
# )
# sns.lineplot(
#     x=Spend_Matrix.index,
#     y=Spend_Matrix[3],
#     data=Spend_Matrix
# )
# sns.lineplot(
#     x=Spend_Matrix.index,
#     y=Spend_Matrix[4],
#     data=Spend_Matrix
# )
# sns.lineplot(
#     x=Spend_Matrix.index,
#     y=Spend_Matrix[5],
#     data=Spend_Matrix
# )
# sns.lineplot(
#     x=Spend_Matrix.index,
#     y=Spend_Matrix[6],
#     data=Spend_Matrix
# )
# sns.lineplot(
#     x=Spend_Matrix.index,
#     y=Spend_Matrix[7],
#     data=Spend_Matrix
# )
# sns.lineplot(
#     x=Spend_Matrix.index,
#     y=Spend_Matrix[8],
#     data=Spend_Matrix
# )
# sns.lineplot(
#     x=Spend_Matrix.index,
#     y=Spend_Matrix[9],
#     data=Spend_Matrix
# )
# sns.lineplot(
#     x=Spend_Matrix.index,
#     y=Spend_Matrix[10],
#     data=Spend_Matrix
# )
# sns.lineplot(
#     x=Spend_Matrix.index,
#     y=Spend_Matrix[11],
#     data=Spend_Matrix
# )
# sns.lineplot(
#     x=Spend_Matrix.index,
#     y=Spend_Matrix[12],
#     data=Spend_Matrix
# )
# plt.show()
