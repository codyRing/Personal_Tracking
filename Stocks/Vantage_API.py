import matplotlib.pyplot as plt
import seaborn as sns
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
import pandas as pd


key = '3PQA2T1IFGZLL0H7'

ts = TimeSeries(key, output_format='pandas')
ti = TechIndicators(key)

# Get the data, returns a tuple
# stock_data is a pandas dataframe, stock_meta_data is a dict
stock_data, stock_meta_data = ts.get_daily(symbol='ABALX')

# stock_data.reset_index(inplace=True)
stock_data.columns=['Open','High','Low','Close','Volume']




share =[]
run=[]
d = []
price = []
for n in range(0,50):
    for i,r in stock_data.iloc[n:n+24:5].iterrows():
        price.append(r['High'])
        share.append((1200/r['High']))
        run.append(n)
        d.append(i)
        # print(1000/r['High'],i,n)
        # stock_data.loc[i,'Shares'] = (1000/r['High'])
        # stock_data.loc[i, 'Run'] = (n)

result = zip(d,share,run,price)
df = pd.DataFrame(result,columns=['d','Share','Run','Price'])
df.to_csv('./5_week.csv')
df = df.groupby(['Run']).sum()
df = df.sort_values(by='Share',ascending=False)
print(df.head())

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[14, 7])
sns.barplot(
    x=df.index,
    y=df['Share'],
    palette='Blues_d',
    data=df
)

ax.set_title('Shares')
for p in ax.patches:
    ax.text(p.get_x() + p.get_width() / 2., p.get_height(), '%d' % int(p.get_height()),
             fontsize=12, color='red', ha='center', va='bottom')

plt.savefig('./5_week')



# Visualization
# figure(num=None, figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k')
# aapl_data['4. close'].plot()
# plt.tight_layout()
# plt.grid()
# plt.show()