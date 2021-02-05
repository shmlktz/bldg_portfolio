import pandas as pd

data_frame = {'name' : ['1'], 'email':['2'], 'phone':['3']}
df = pd.DataFrame(data=data_frame, index = ["we're on the way to success"])
print(df)
df.to_csv('contact_list_magic.csv')

#####
# import tkinter
# tkinter.messagebox.
# print(tkinter.ACTIVE)