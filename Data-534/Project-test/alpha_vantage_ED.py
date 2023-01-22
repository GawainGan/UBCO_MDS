from project import *
import requests
import pandas as pd
import time
apikey = 'O6LFU5LE4ZVYXL1H'

def convert_js_to_df_monthly(data):
      df = pd.json_normalize(data['data'])
      # Convert the 'date' column into a datetime object
      df['date'] = pd.to_datetime(df['date'])
      # df['date'] = pd.DatetimeIndex(df['date']).to_period('M')
      # df['year'] = df['date'].dt.year
      # df['month'] = df['date'].dt.month
      # df = df.drop(columns=['date'])

      # Convert the 'value' column into a float
      df['value'] = pd.to_numeric(df['value'])
      # columns_order = ['date','year','month','value']
      # df = df.reindex(columns=columns_order)
      return df

def get_economic_indicators(api=apikey, interval='monthly', save_path='/Users/gawain/finance_project/dataset/'):
      CPI_url = 'https://www.alphavantage.co/query?function=CPI'+'&interval='+ interval+'&apikey='+api # monthly and semiannual are accepted.
      UNEMPLOYMENT_url = 'https://www.alphavantage.co/query?function=UNEMPLOYMENT&apikey='+api
      REAL_GDP_PER_CAPITA_url = 'https://www.alphavantage.co/query?function=REAL_GDP_PER_CAPITA&apikey='+api
      FEDERAL_FUNDS_RATE_url = 'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval='+ interval+'&apikey='+api # daily, weekly, and monthly
      RETAIL_SALE_url = 'https://www.alphavantage.co/query?function=RETAIL_SALES&apikey='+api #monthly
      DURABLES_url = 'https://www.alphavantage.co/query?function=DURABLES&apikey=' + api #monthly 日用商品
      
      indicator_dict={  'cpi':CPI_url,                        # monthly and semiannual are accepted.
                        'unemployment':UNEMPLOYMENT_url,      # monthly is accepted.
                        'gdp':REAL_GDP_PER_CAPITA_url,        # quarterly is accepted.
                        'fundrate':FEDERAL_FUNDS_RATE_url,    # daily, weekly, and monthly are accepted.
                        'retail':RETAIL_SALE_url,             # monthly is accepted.
                        'durables':DURABLES_url               # monthly is accepted.日用商品
                        }
      for i in indicator_dict:
            name = i
            url = indicator_dict[i]
            r = requests.get(url)
            data = r.json()
            df = convert_js_to_df_monthly(data)
            df.to_csv(save_path+name+'.csv')
            print(name+' csv is set')
            time.sleep(10)
            

get_economic_indicators(api=apikey)
