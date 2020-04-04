import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib import pyplot
import seaborn as sns
from datetime import datetime, timedelta
from sklearn import preprocessing


data = pd.read_csv('../Data/Mint/transactions.csv')
data['Date']=pd.to_datetime(data.Date)
data = data.set_index('Date')


# start_date='1/1/2019'
# end_date = '3/29/2020'
#
# mask = (data.index >= start_date) & (data.index <= end_date)
# data=data.loc[mask]




Spend = pd.DataFrame(data[data['Transaction Type'].str.contains('debit')])
Spend = Spend[Spend["Amount"] <= 1000]
Daily_Spend= Spend.resample('D').sum()
Daily_Spend['AVG']=Daily_Spend.Amount.rolling(7).mean()



# min_max_scaler = preprocessing.MinMaxScaler()
# x = Daily_Spend[['Amount']].values.astype(float)
# x_scaled = min_max_scaler.fit_transform(x)
# Daily_Spend_Normal = pd.DataFrame(x_scaled,index=Daily_Spend.index,columns=['Amount'])




#print(Daily_Spend.describe())

target = Daily_Spend['Amount'].mean()

d = datetime.today() - timedelta(days=45)
mask = (Daily_Spend.index >= d)
Daily_Spend=Daily_Spend.loc[mask]
#Daily_Spend_Normal=Daily_Spend_Normal.loc[mask]

#
#
# # fig, ax = plt.subplots(nrows=1, ncols=1,figsize = [14,14])
# # sns.barplot(x=Daily_Spend.index,y= Daily_Spend['Amount'],ax=ax)
# # #fig.xticks(rotation=90)
# #
# # plt.show()
#
#plt.figure(figsize=(10,5))
fig, axs = plt.subplots(ncols=1)
sns.barplot(
    x=Daily_Spend.index.strftime('%m-%d-%A'),
    y=Daily_Spend['Amount'],
    palette='Blues_d'
)

sns.lineplot(
    x=Daily_Spend.index.strftime('%m-%d-%A'),
    y=Daily_Spend['AVG']
)

# axs. (
#     rotation=45,
#     horizontalalignment='right',
#     fontweight='light',
#     fontsize='x-large'
#
# )
plt.xticks(rotation=90)
plt.show()
plt.savefig('../data/mint/Daily_Spending.png', dpi=300)


# #print(Daily_Spend.describe(),target)
# #Spend.describe()