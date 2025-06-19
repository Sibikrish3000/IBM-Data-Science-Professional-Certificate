import pandas as pd
df=pd.read_parquet('bike_trips_data_100k.parquet')
df_sample=df.sample(10000)
df_sample.to_parquet('bike_trips_data.parquet',engine='pyarrow', compression='snappy',index=False)