from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from dateutil.relativedelta import relativedelta
from matplotlib.colors import LinearSegmentedColormap

data = pd.read_csv('../Data/Mint/transactions.csv')
# Some transactions are delayed and others aren't. In person swipes seem to be a day off. ATM?
#data['Date'] = pd.to_datetime(data.Date) - timedelta(days=1)
data['Date'] = pd.to_datetime(data.Date)
data = data.set_index('Date')

Spend = pd.DataFrame(data[data['Transaction Type'].str.contains('debit')])
Earn = pd.DataFrame(data[data['Transaction Type'].str.contains('credit')])

# -------------------------------------------------------
# Spend = Spend[Spend.Category != 'Mortgage & Rent']
Spend = Spend[~Spend['Category'].isin(['Auto Insurance','Mortgage & Rent','Utilities','Credit Card Payment'])]

# min_max_scaler = preprocessing.MinMaxScaler()
# x = Spend[['Amount']].values.astype(float)
# x_scaled = min_max_scaler.fit_transform(x)
# Spend = pd.DataFrame(x_scaled,index=Spend.index,columns=['Amount'])


# -------------------------------------------------------
# d = (datetime.today() - timedelta(days=3*360))
d = (datetime.now() - relativedelta(years=1) + relativedelta(months =1))
Spend = Spend.loc[Spend.index >= d]

Spend_Matrix = Spend.resample('D').sum()
Spend_Matrix = pd.pivot_table(Spend_Matrix,
                              index=Spend_Matrix.index.day,
                              columns=Spend_Matrix.index.month,
                              values="Amount")

Spend_Matrix = Spend_Matrix.cumsum()
Spend_Matrix.sort_index(level=0, ascending=False, inplace=True)



fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[14, 7])
sns.heatmap(Spend_Matrix,
            annot=True,
            annot_kws={"size": 7},
            vmin=1000,
            fmt="g",
            linewidths=.5,
            cbar=False,
            cmap="Blues",
            ax=ax)
plt.savefig('../data/mint/Daily_Heat.png', dpi=300)
plt.show()

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[14, 7])
for i in range(1, 13):
    sns.lineplot(
        x=Spend_Matrix.index,
        y=Spend_Matrix[i],
        data=Spend_Matrix

    )

#plt.show()
