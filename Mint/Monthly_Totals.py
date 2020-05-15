import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import seaborn as sns
from datetime import datetime, timedelta
from sklearn import preprocessing
from dateutil.relativedelta import relativedelta


data = pd.read_csv('../Data/Mint/transactions.csv')
#data['Date'] = pd.to_datetime(data.Date) - timedelta(days=1)
data['Date'] = pd.to_datetime(data.Date)
data = data.set_index('Date')
data = data[~data['Category'].isin(['Credit Card Payment','Transfer','Financial Advisor'])]


Spend = pd.DataFrame(data[data['Transaction Type'].str.contains('debit')])
Earn = pd.DataFrame(data[data['Transaction Type'].str.contains('credit')])

# ---------------What Values to drop from Spend?------------------------------------
# Spend = Spend[~Spend['Category'].isin(['Credit Card Payment','Transfer'])]

# Drop = Spend[Spend['Category'] == 'Mortgage & Rent'].index
# Spend.drop(Drop,inplace=True)

# Spend = Spend[Spend["Amount"] <= 1000]

# min_max_scaler = preprocessing.MinMaxScaler()
# x = Spend[['Amount']].values.astype(float)
# x_scaled = min_max_scaler.fit_transform(x)
# Spend = pd.DataFrame(x_scaled,index=Spend.index,columns=['Amount'])

# ----------------Resample--------------------------------------------------
Daily = (datetime.today() - timedelta(days=31))
Weekly = (datetime.today() - timedelta(weeks=20))
Monthly = (datetime.now() - relativedelta(years=1) + relativedelta(months =1))


# d = datetime.today() - timedelta(days=45)
# mask = (Daily_Spend.index >= d)
# Daily_Spend=Daily_Spend.loc[mask]


Daily_Spend = Spend.resample('D').sum()
Daily_Spend['Day_Num'] = Daily_Spend.index.strftime('%Y-%A')
Daily_Spend['AVG'] = Daily_Spend.Amount.rolling(7).mean()
#Daily_Spend.to_csv('../data/mint/Daily_Spend.csv')
Daily_Spend = Daily_Spend.loc[Daily_Spend.index >= Daily]

Weekly_Spend = Spend.resample('W').sum()
Weekly_Spend['Week_Num'] = Weekly_Spend.index.strftime('%Y-%U')
Weekly_Spend['AVG'] = Weekly_Spend.Amount.rolling(6).mean()
Weekly_Spend = Weekly_Spend.loc[Weekly_Spend.index >= Weekly]

Monthly_Spend = Spend.resample('M').sum()
Monthly_Spend['Month_Num'] = Monthly_Spend.index.strftime('%Y-%m')
Monthly_Spend['AVG'] = Monthly_Spend.Amount.rolling(4).mean()
Monthly_Spend = Monthly_Spend.loc[Monthly_Spend.index >= Monthly]

Monthly_Earn = Earn.resample('M').sum()
Monthly_Earn['Month_Num'] = Monthly_Earn.index.strftime('%Y-%m')
Monthly_Earn = Monthly_Earn.loc[Monthly_Earn.index >= Monthly]

# ------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=[14, 14])
sns.barplot(x=Monthly_Spend['Month_Num'], y='Amount', data=Monthly_Spend, palette="Blues_d", ax=ax1)
sns.barplot(x=Monthly_Earn['Month_Num'], y='Amount', data=Monthly_Earn, palette="Blues_d", ax=ax2)

ax1.set_title('Spending')
for p in ax1.patches:
    ax1.text(p.get_x() + p.get_width() / 2., p.get_height(), '%d' % int(p.get_height()),
             fontsize=12, color='red', ha='center', va='bottom')

ax2.set_title('Earn')
for p in ax2.patches:
    ax2.text(p.get_x() + p.get_width() / 2., p.get_height(), '%d' % int(p.get_height()),
             fontsize=12, color='Green', ha='center', va='bottom')

plt.savefig('../data/mint/Over_Under.png', dpi=300)
plt.show()

# ----------------------------------------------------------------
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[14, 7])
sns.barplot(
    x=Daily_Spend.index.strftime('%m-%d-%A'),
    y=Daily_Spend['Amount'],
    palette='Blues_d'
)

sns.lineplot(
    x=Daily_Spend.index.strftime('%m-%d-%A'),
    y=Daily_Spend['AVG']
)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width() / 2., p.get_height(), '%d' % int(p.get_height()),
             fontsize=12, color='Green', ha='center', va='bottom')

plt.xticks(rotation='vertical')
plt.subplots_adjust(bottom=0.3)
plt.savefig('../data/mint/Daily.png', dpi=300)

# ------------------------------------------------------------------
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[14, 7])
sns.barplot(
    x=Weekly_Spend.index.strftime('%m-%d-%A'),
    y=Weekly_Spend['Amount'],
    palette='Blues_d'
)

sns.lineplot(
    x=Weekly_Spend.index.strftime('%m-%d-%A'),
    y=Weekly_Spend['AVG']
)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width() / 2., p.get_height(), '%d' % int(p.get_height()),
             fontsize=12, color='Green', ha='center', va='bottom')

plt.xticks(rotation='vertical')
plt.subplots_adjust(bottom=0.3)
plt.savefig('../data/mint/Weekly.png', dpi=300)
# ------------------------------------------------------------------
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[14, 7])
sns.barplot(
    x=Monthly_Spend.index.strftime('%m-%d-%A'),
    y=Monthly_Spend['Amount'],
    palette='Blues_d'
)

sns.lineplot(
    x=Monthly_Spend.index.strftime('%m-%d-%A'),
    y=Monthly_Spend['AVG']
)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width() / 2., p.get_height(), '%d' % int(p.get_height()),
             fontsize=12, color='Green', ha='center', va='bottom')

plt.xticks(rotation='vertical')
plt.subplots_adjust(bottom=0.3)
plt.savefig('../data/mint/Monthly.png', dpi=300)
