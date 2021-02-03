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
optional_date = ""

print("\n\nHello and welcome to the Stock Market Data Supplier\n")
users_name = input("First, what is your name? ")
api_key_q = input(f"\nHi {users_name}, please understand that results will vary based on the account type,\n\
Do you have an API access_key from MarketStack? ('y' or 'n') ")
if (api_key_q == "y") or (api_key_q == "Y"):
  user_api_key = input("\nPlease enter your API access_key (NOTE: if you mistype it, the program will not run properly) ")
  ms_access_key = user_api_key
else:
  print("\nNo worries, we'll supply the house code")
  

ticker = input(f"\n{users_name}, which ticker symbol(s) would you like to get data on?\
\n-Please type the exact symbol and just the symbol i.e. 'aapl'\n\
-For multiple ticker symbols please add a comma between tickers and do not add spaces, i.e. 'amzn,tsla,aapl,emms'\n") #^^ will need to data validate ^^ #maybe need to do a try and except block? #Want to make sure the ticker symbol entry desn't cause a great crash
#will need to validate ^

cat = input("Which category of stock data are you looking for, end-of-day or intraday?\n\
['eod' or 'intraday'] ") #^^ Will also need to data validate!

pagination_limitation = input(f"\nHow many results would you like to see back?\n(MarketStack claims 1000 is the maximum) ") 

set_date = input(f"\n{users_name}, would you like to\n\
(1) let it run it's normal course of recent dates\
(2) be specific about the dates it pulls\n\
(3) soley pull the latest date?\n\
(Choose '1', '2' or '3') ")
if set_date == '1':
  pass
elif set_date == '3':
  optional_date = '/latest'
elif set_date == '2':
  print("Dates that are not returned in the data are most likely weekends or holidays")
  print("You are going to be prompted to endter a starting and ending date\n\
  You may enter: both a starting and ending date, only a starting date")
  date_from = input("\nWhat is the starting date? (YYYY-MM-DD or ISO-8601\
  format (e.g. 2020-05-21T00:00:00+0000) ")
  date_to = input("\nWhat is the ending date? (YYYY-MM-DD or ISO-8601\
  format (e.g. 2020-05-21T00:00:00+0000) ")
# date = input("Please input a date in YYYY-MM-DD or ISO-8601\
# format (e.g. 2020-05-21T00:00:00+0000), or leave blank ")

params = {
  'access_key': f'{ms_access_key}',
  'symbols' : f'{ticker}',
  'limit' : {pagination_limitation},
  'date_from' : f'{date_from}',
  'date_to' : f'{date_to}'


}

##Requesting the data from MarketStack's API##

#api_result = requests.get(f'http://api.marketstack.com/v1/tickers/{ticker}/{cat}', params)
#api_response = api_result.json() #run to json the api_result

test_r_o = requests.get(f'http://api.marketstack.com/v1/{cat}{optional_date}', params)
test_json = test_r_o.json()

print("\n**Checking Status**")
print("response object status:", test_r_o)

#Achieved a custom intraday URL: http://api.marketstack.com/v1/intraday/2020-07-25?access_key=3fe199c40e9ae83814d59ae34e9e80d1&symbols=amzn
if str(test_r_o) != "<Response [200]>":
  print("Result: Assuming an error\nPrinting the JSON object for troubleshooting purposes:\n"+str(test_json),"\n\n")
else:
  print("Result: Assuming (based on the response of '200' which means 'OK') the API request has successfully gone through & returned data\n\
  NOTE: returning a blank set of results will not necessarily result in an error")

###Setting the dataframe###

df = pd.io.json.json_normalize(test_json["data"])
# df_2 = pd.DataFrame.from_dict(test_r_o.json()["data"]["eod"])

print(df, "\n\nPrinted above is the DataFrame (df)")

host = "localhost"
db = "this_base"
user = "root"
pw = input(f"\nPlease enter the {host} password \
for the database to send and receive data: ")

##Create SQLAlchemy engine to connect to MySQL Database
engine = create_engine(f"mysql+pymysql://{user}:{pw}@{host}/{db}")

def df_to_sql():
  ####Setting up the Pandas DataFrame to MySQL exchange####
  
  global table_name
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
  df.to_sql(f"{table_name}", engine, if_exists = f"{fail_replace_append}", index = True) #schema = None, if_exists = "fail", index = True, index_label = "index_label_test" ## ,chunksize=None, dtype= None, method = None)
  print("Completed data push attempt. Please check the MySQL server for results")
  #return engine#, host, db, user, pw

if (input("\nDo you want to push this data to MySQL? ('y' or 'n') ") == "y"):
  df_to_sql()
else:
  print("\nOK, data not being pushed.")

global d
d = {}

def sql_to_df():
  #engine = df_to_sql()
  #print('reading and printing the table just created')
  data_pulls = int(input(f"\n{users_name}, how many tables would you like to pull from MySQL? "))
  for pull in range(data_pulls):
    new_df_name = "df__"+str(pull)
    pull_table = input("From which table to pull from? ")
    current_pulling_df = pd.read_sql_query(f'SELECT * FROM {pull_table}', con= engine)
    #new_df = pd.read_sql_query(f'SELECT * FROM {table_name}', con= engine)
    print()
    d[f"df_{pull}"] = current_pulling_df
    print(current_pulling_df)
  print("\nHere is a dictionary of the data frames you've pulled:\n")
  print(d)

if (input("\nDo you want to pull tables from MySQL? ('y' or 'n') ") == "y"):
  sql_to_df()
else:
  print("\nOK, data not being pulled.")


###Extra Features##
##feature blocks###

##__no remaining extra features or feature blocks - congrats!__##


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