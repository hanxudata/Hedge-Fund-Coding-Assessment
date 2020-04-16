# load modules
import pandas as pd
import time


# log start time
start_time = time.time()

# load input data set (Python pickle file)
df = pd.read_pickle(r'px.xz') 

# datetime format
df['dt']=pd.to_datetime(df['dt'])

# get time difference group by security identifier
df['diff']=df.groupby('bbgid')['dt'].diff()-pd.Timedelta(days=1)

# get time difference length in days
df['length']=df['diff'].dt.days

# filter to get securities that have gaps
stats=df[df['length']>0].reset_index(drop=True)

# end date of gap
stats['end']=stats['dt']-pd.Timedelta(days=1)

# start date of gap
stats['start']=stats['dt']-stats['diff']

# keep fileds needed
stats=stats[['start','end','length','bbgid']]

# sort
stats=stats.sort_values(by=['length','bbgid','start'],ascending=[False,True,True]).reset_index(drop=True)

# export result to Excel
stats.iloc[0:1000].to_excel(r'px_stats.xlsx',index=False) # replace <path> with proper file path

# show execution time
print("--- %s seconds ---" % (time.time() - start_time))
