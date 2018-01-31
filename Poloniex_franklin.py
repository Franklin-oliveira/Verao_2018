def get_data(list_of_currencies, start, end, freq):
    
    ''' 
    This function downloads all available data from POLONIEX and creates one csv file for each currency 
    in the work directory.  
   
    Arguments:
    
    - list_of_currencies (list): a list of currencies negociated at Poloniex (Ex: ['BCN/BTC', 'BELA/BTC'])
    - start (string): inicial date in the format YYYY-mm-dd
    - end (string): final date in the format YYYY-mm-dd
    - freq (integer): 300 - 5min; 900 - 15min; 1800 - 30min; 7200 - 2h; 14400 - 4h; 86400 - daily.
    '''
    import datetime
    import time
    import pandas as pd
    import numpy as np
    import warnings
    warnings.filterwarnings("ignore")
    from IPython.display import clear_output
    from progressbar import ProgressBar
    pbar = ProgressBar()
    
    freq = str(freq)
    since = int(time.mktime(datetime.datetime.strptime(start, "%Y-%m-%d").timetuple()))
    until = int(time.mktime(datetime.datetime.strptime(end, "%Y-%m-%d").timetuple()))
     
  
    
    for name in pbar(list_of_currencies):
        name1=name.split('/')
        name1.reverse()
        name=str(name1[0]+'_'+name1[1])
        print('\033[0m Downloading \033[1m {} \033[0m from {}, since \033[1m {}, \033[0m until \033[1m {}.\033[0m \n'.format(name, 'Poloniex', start, end))
        
        try: 
            url = 'https://poloniex.com/public?command=returnChartData&currencyPair={}&start={}&end={}&period={}'.format(name, since, until, freq)
            data = pd.read_json(url)
            data.set_index('date', inplace=True)
            data['currency']='{}'.format(name)
            data.to_csv(name+'.csv', header=True, mode='a+')
            time.sleep(1.5)
            clear_output(True)
        
        except Exception as e:
            print('\033[91m',e,'\033[0m \n')
            time.sleep(1.5)
            #clear_output(True)
            pass
        
        except KeyError as e:
            print('\033[91m',e,'\033[0m \n')
            time.sleep(1.5)
            #clear_output(True)
            pass
        
    return print('\033[1m Download complete. Check your work directory. \033[0m')




def call_data(list_of_curr_downloaded):
    
    '''
    Read CSV files of the currencies downloaded and return one data frame
    
    p.s.: Do not run this function to read a large number of CSV files.
    
    '''
    
    import pandas as pd
    
    df = pd.DataFrame()

    for name in list_of_curr_downloaded:
        
        name1=name.split('/')
        name1.reverse()
        name=str(name1[0]+'_'+name1[1])

        df1 = pd.read_csv('..\\Verao_2018\\{}.csv'.format(name))
        dataf = pd.concat([df,df1])
        df=dataf
        
    df.set_index('date', inplace=True)
    
    return(df)



def data_to_sql(data_frame, name_of_db):
    
    ''' Reads a data frame into a SQL .db file.'''
    
    import sqlite3
    import pandas as pd
    import pandas.io.sql as psql
    from sqlite3 import Error
   
    
    connection = sqlite3.connect('{}.db'.format(name_of_db))
    
    try:
        pd.DataFrame.to_sql(self = data_frame, name = name_of_db, con = connection, index = True, if_exists = 'replace')
        
    except Exception as e:
        print('\033[91m{}\033[0m \n'.format(e))
        
    connection.close()
    
    