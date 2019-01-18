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
    
    # necessary imports (it's replicated from the notebook here only for precaution)
    import datetime
    import time
    import pandas as pd
    import numpy as np
    import warnings
    warnings.filterwarnings("ignore")
    from IPython.display import clear_output
    
    
    # treating inputs
    freq = str(freq)
    since = int(time.mktime(datetime.datetime.strptime(start, "%Y-%m-%d").timetuple()))
    until = int(time.mktime(datetime.datetime.strptime(end, "%Y-%m-%d").timetuple()))
     
  
    
    for name in list_of_currencies:
        
        # Treating string to be inserted into the url
        name1=name.split('/')
        name1.reverse()
        name=str(name1[0]+'_'+name1[1])
        
        # displays which currency data is being downloaded
        print('\033[0m Downloading \033[1m {} \033[0m from {}, since \033[1m {}, \033[0m until \033[1m {}.\033[0m \n'.format(name, 'Poloniex', start, end))
        
        # fetching data with some error treatment
        try: 
            
            # creating the url
            url = 'https://poloniex.com/public?command=returnChartData&currencyPair={}&start={}&end={}&period={}'.format(name, since, until, freq)
            
            # reading data from Poloniex's (available in .json)
            data = pd.read_json(url)
            data.set_index('date', inplace=True)
            data['currency']='{}'.format(name)
            
            # stores data downloaded into a .csv file (with currency name)
            data.to_csv(name+'.csv', header=True, mode='a+')
            
            # waiting before next iteration... (Poloniex has an upper limit of data that can be downloaded by the same IP address per minute)
            time.sleep(1.5)
            clear_output(True)
        
        # passing some exceptions
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
    
    # displays that the download is complete and the process is finished.
    return print('\033[1m Download complete. Check your work directory. \033[0m')




def call_data(list_of_curr_downloaded):
    
    '''
    Read CSV files of the currencies downloaded and returns one concatenated data frame
    
    p.s.: Do not run this function to read a large number of CSV files. 
        (memmory issues. I didn't solve this because, as we're analyzing only 3 currencies, it's not reeeeeeally necessary. 
        Also, because I didn't have much time before the hand-in date was due. XD)
    
    '''
    
    import pandas as pd
    
    # variable to store the "large" data frame
    df = pd.DataFrame()

    for name in list_of_curr_downloaded:
        
        name1=name.split('/')
        name1.reverse()
        name=str(name1[0]+'_'+name1[1])
        
        # reads the .csv file
        df1 = pd.read_csv('{}.csv'.format(name))
        
        # concatenates each dataframe into a large one
        dataf = pd.concat([df,df1])
        df=dataf
        
    # sets the index to be the date     
    df.set_index('date', inplace=True)
    
    # returns the data frame that contains all the data from the .csv files
    return(df)




def data_to_sql(data_frame, name_of_db):
    
    ''' Reads a data frame into a SQL .db file.'''
    
    import sqlite3
    import pandas as pd
    import pandas.io.sql as psql
    from sqlite3 import Error
   
    # creates a connection with the database
    connection = sqlite3.connect('{}.db'.format(name_of_db))
    
    # stores a dataframe into the .db file 
    try:
        pd.DataFrame.to_sql(self = data_frame, name = name_of_db, con = connection, index = True, if_exists = 'replace')
    
    # if there's an error, it'll be displayed on the screen
    except Exception as e:
        print('\033[91m{}\033[0m \n'.format(e))
    
    # closes the connection with the database 
    connection.close()
    
    