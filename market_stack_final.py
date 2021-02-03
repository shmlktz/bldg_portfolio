# one pound sign: should be temporary. 
# two pound signs: it's here to stay, it's meant to be a descriptive note

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine
import sqlalchemy

ms_access_key = "3fe199c40e9ae83814d59ae34e9e80d1"

print("\n\nHello and welcome to the Stock Data Supplier\n")
users_name = input("First off, what is your name? ")
api_key_q = input(f"\nHi {users_name}, do you have an API access_key from MarketStack? ('y' or 'n') ")
if (api_key_q == "y") or (api_key_q == "Y"):
  user_api_key = input("\nPlease enter your API access_key (NOTE: if you mistype it, the program will not run)")
  ms_access_key = user_api_key
else:
  print("\nNo worries, we'll supply the house code")
  

ticker = input(f"\n{users_name}, which ticker symbol(s) would you like to get data on?\
\n-Please type the exact symbol and just the symbol i.e. 'aapl'\n\
-For multiple ticker symbols please add a comma between tickers and do not add spaces, i.e. 'amzn,tsla,aapl,emms'\n") #^^ will need to data validate ^^ #maybe need to do a try and except block? #Want to make sure the ticker symbol entry desn't cause a great crash
#will need to validate ^

cat = input(f"\n{users_name}, which category of stock data are you looking for, end-of-day or intraday?\n\
['eod' or 'intraday'] ") #^^ Will also need to data validate!

# date = input("Please input a date in YYYY-MM-DD or ISO-8601\
# format (e.g. 2020-05-21T00:00:00+0000), or leave blank ")

params = {
  'access_key': f'{ms_access_key}',
  'symbols' : f'{ticker}'
}

##Requesting the data from MarketStack's API##

#api_result = requests.get(f'http://api.marketstack.com/v1/tickers/{ticker}/{cat}', params)
#api_response = api_result.json() #run to json the api_result

print("\n**Housekeeping Notice** This engine is currently landing\n\n")

test_r_o = requests.get(f'http://api.marketstack.com/v1/{cat}', params)
test_json = test_r_o.json()

print("\nprinting JSON object", test_json,"\n\n")
print("\nprinting Response object:", test_r_o,"\n\n")
#Achieved a custom intraday URL: http://api.marketstack.com/v1/intraday/2020-07-25?access_key=3fe199c40e9ae83814d59ae34e9e80d1&symbols=amzn


###Setting the dataframe###

df = pd.io.json.json_normalize(test_json["data"])
# df_2 = pd.DataFrame.from_dict(test_r_o.json()["data"]["eod"])

print("\nprinting data frame\n\n", df)

def df_to_sql():
  ####Setting up the Pandas DataFrame to MySQL exchange####
  host = "localhost"
  db = "this_base"
  user = "root"
  pw = "this is parnasa"
  #pw = input(f"Please enter the {hostname} password: ")

  ##Create SQLAlchemy engine to connect to MySQL Database
  engine = create_engine(f"mysql+pymysql://{user}:{pw}@{host}/{db}")
  table_name = input("\nWhat is the name of the table you'll save this as? ")
  table_options = ['fail', 'replace', 'append']
  table_options_plus = {"fail": f"if '{table_name}' already exists, it will fail to store the data",\
  "replace": f"replaces the data from table '{table_name}', if '{table_name}' already exists",\
  "append": f"appends all data from the current data frame to the table '{table_name}'. NOTE: you cannot append eod or intraday data to a table of the other kind [the data is organized differently and SQL will fail to INSERT it.]"}
  fail_replace_append = input(f"\n{users_name}, what would you like the 'if_exists' table setting to be: '" + "' or '".join(table_options_plus.keys()) + f"'?\
  \n\nRead this dictionary for more option info: \n{str(table_options_plus)}\n\n")
  if fail_replace_append in table_options:
    pass
  else:
    fail_replace_append = "fail"
  print("\nBeginning data push..")
  df.to_sql(f"{table_name}", engine, if_exists = f"{fail_replace_append}", index = True, index_label = "#") #schema = None, if_exists = "fail", index = True, index_label = "index_label_test" ## ,chunksize=None, dtype= None, method = None)
  print("Completed data push attempt. Please check the MySQL server for results")

if (input("do you want to push this data to MySQL? ('y' or 'n') ") == "y"):
  df_to_sql()
else:
  print("ok, data not being pushed")

###Extra Features##
##feature blocks###

#Pull stored db information here -->
#pull_from_mysql_q = input("Would you like to pull the stock data from the db? ('y' or 'n') ")










###Notes & learning

##two ways to make a dataframe:

##way #1 to make a dataframe
# output_2 = api_result.json()["data"]["eod"]
# df = pd.DataFrame.from_dict(output_2)
##or condensed to: df = pd.DataFrame.from_dict(api_result.json()["data"]["eod"])

#df = pd.DataFrame.from_dict(test_r_o.json()["data"]["eod"])

##way #2 to make a dataframe
# df = pd.io.json.json_normalize(api_response["data"]["eod"])

#print(test_r_o)

####output = pd.json_normalize(api_response["data"]["eod"]) #found on stack exchange, but doesn't work

##dataframe to numpy
#data_df_2 = df_2.to_numpy() ##can iterate over the individual items


## unsure if worked
##variable_name = requests.get(f'http://api.marketstack.com/v1/{cat}/{date}?access_key=3fe199c40e9ae83814d59ae34e9e80d1&symbols={ticker}')


##Printing labelless data!#Just the data, I believe ((2 Options Below))
#print(df_2.to_numpy()) ##Pandas documentation suggests using .to_numpy() because of the flexibility offered by two optional parameters: 1. dtype 2. copy
#print(df_2.values) ##older and proabably used more often as a result

#print the keys to know what we're working with
#print(api_response["data"].keys())

#print(df_2.memory_usage(index = False)) #or can leave the parameter empty and Index will be returned

#displaying versions of Panda & dependencies 
#print(pd.__version__)
#pd.show_versions() #((Harvey Summers Thanks))

##checking the data type of each column
#print(df_2.dtypes)

##It is possible to modify data type ".astype()"##, check realpython dataframes pandas for that

##DF size, attributes .ndim, .size, and .shape return the number of dimensions, number of data values across each dimension, and total number of data values, respectively

##Memory usage checker (for each column): .memory_usage() (exclude the column with the row labels, pass the optional argument index=False)

##Putting the data from a df (dataframe) into a csv file
#df.to_csv("eod_data.csv")

# #Reading a csv (and printing it)
# print(pd.read_csv("eod_data.csv", index_col=0)) ##That’s how you get a Pandas DataFrame
# #from a file. In this case, index_col=0 specifies that the row labels are located in
# #the first column of the CSV file.
# #https://realpython.com/pandas-dataframe/#creating-a-pandas-dataframe-with-dictionaries

###opening and creating files to write to & read###
# f = open("api_response_.txt", "w+")
# f.write(api_response)
# f.close()

##Status Codes
# print("Status Code:", api_result.status_code)
# print("(example) Codes.","1:",requests.codes['temporary_redirect'],"2:",requests.codes.teapot)


#print("API .Text:",api_result.text)

# for stock_data in api_result:
#   print(stock_data)

#print(type(api_response))

#api_result.headers["Date"] = "now" #changing the date value
#print(api_result.headers["Date"]) #Pulling & printing the date value, from the dictionary[key]

##Creating a space to put the data into a string
##to be added to the file

# api_holding_string = ""
# for item in api_response:
#   api_holding_string += " "+item+";"

# print(api_holding_string)

# g = open(requests_1.py, "r")
# g.read

# print("\nApi Result Headers")
# for key, value in api_result.headers.items():
#   print("\n",key+" : "+value)



# for stock_data in api_response['data']:
#     print(u'Ticker %s has a day high of  %s on %s' % (
#       stock_data['symbol']
#       stock_data['high']
#       stock_data['date']
#     ))ate']
# ))

#need to add .text to end of api_result (Response object) to have something to run
# soup = BeautifulSoup(api_result, 'lxml')
# print(soup)

print("\nCOMPLETED. \nthis is the final line of code.")