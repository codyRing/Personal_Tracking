from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from dateutil.relativedelta import relativedelta
from matplotlib.colors import LinearSegmentedColormap

data = pd.read_csv('../Data/Mint/transactions.csv')
# Some transactions are delayed and others aren't. In person swipes seem to be a day off. ATM?
# data['Date'] = pd.to_datetime(data.Date) - timedelta(days=1)
data['Date'] = pd.to_datetime(data.Date)
data = data.set_index('Date')

#Beginning of next month - 1 year
d = datetime.today() + pd.offsets.MonthBegin(1)
d = d - relativedelta(years=1)
data = data.loc[data.index >= d]

Spend = pd.DataFrame(data[data['Transaction Type'].str.contains('debit')])
Earn = pd.DataFrame(data[data['Transaction Type'].str.contains('credit')])

#Use to extend index to today
new_datetime_range = pd.date_range(start=Spend.index.min(), end= datetime.today(),freq="D")


# -------------------------------------------------------
#Split out fixed and discretionary categories
Spend_Fixed = pd.DataFrame(Spend[Spend['Category'].isin([
    'Auto Insurance'
    , 'Mortgage & Rent'
    , 'Utilities'
    , 'Internet'
    , 'Subscription_Service'
    , 'Mobile Phone'
    , 'Home Insurance'
    # 'Alcohol & Bars'
    # ,'Entertainment'
])])

#Credit card transactions are duplicated. Category dropped below are payments to Bank Of America.
Spend = Spend[~Spend['Category'].isin(['Credit Card Payment','Transfer','Financial Advisor'
                                          , 'Auto Insurance'
                                          , 'Mortgage & Rent'
                                          , 'Utilities'
                                          , 'Internet'
                                          , 'Subscription_Service'
                                          , 'Mobile Phone'
                                          , 'Home Insurance'
                                       ])]

# min_max_scaler = preprocessing.MinMaxScaler()
# x = Spend[['Amount']].values.astype(float)
# x_scaled = min_max_scaler.fit_transform(x)
# Spend = pd.DataFrame(x_scaled,index=Spend.index,columns=['Amount'])


# -------------------------------------------------------
Spend_Matrix = Spend.resample('D').sum().reindex(new_datetime_range,fill_value=0)
Spend_Matrix = pd.pivot_table(Spend_Matrix,
                              index=Spend_Matrix.index.day,
                              columns=Spend_Matrix.index.month,
                              values="Amount")

Spend_Matrix = Spend_Matrix.cumsum()
Spend_Matrix.sort_index(level=0, ascending=False, inplace=True)

Spend_Matrix_Fixed = Spend_Fixed.resample('D').sum().reindex(new_datetime_range,fill_value=0)
Spend_Matrix_Fixed = pd.pivot_table(Spend_Matrix_Fixed,
                                    index=Spend_Matrix_Fixed.index.day,
                                    columns=Spend_Matrix_Fixed.index.month,
                                    values="Amount")

Spend_Matrix_Fixed = Spend_Matrix_Fixed.cumsum()
Spend_Matrix_Fixed.sort_index(level=0, ascending=False, inplace=True)
# -------------------------------------------------------
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[14, 7])
sns.heatmap(Spend_Matrix,
            annot=True,
            annot_kws={"size": 7},
            vmin=500,
            vmax=2500,
            fmt="g",
            linewidths=.5,
            cbar=False,
            cmap="Blues",
            ax=ax)
plt.title('Discretionary Spending')
ax.set_xlabel('Month')
ax.set_ylabel('Day')

plt.savefig('../data/mint/Daily_Discretionary_Heat.png', dpi=300)
plt.show()

fig1, ax1 = plt.subplots(nrows=1, ncols=1, figsize=[14, 7])
sns.heatmap(Spend_Matrix_Fixed,
            annot=True,
            annot_kws={"size": 7},
            fmt="g",
            linewidths=.5,
            vmin=2000,
            # vmax=2000,
            cbar=False,
            cmap="Blues",
            ax=ax1)
plt.title('Fixed Spending')
ax1.set_xlabel('Month')
ax1.set_ylabel('Day')

plt.show()
plt.savefig('../data/mint/Daily_Fixed_Heat.png', dpi=300)









# fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=[14, 7])
# sns.barplot(x='Category',y='Amount',data=Spend)
#
# plt.show()

# fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[14, 7])
# for i in range(1, 13):
#     sns.lineplot(
#         x=Spend_Matrix.index,
#         y=Spend_Matrix[i],
#         data=Spend_Matrix
#
#     )

# plt.show()
