#contact list reader and email printer
import pandas as pd
import tkinter as tk
#import contact_list_magic_tree.csv
contacts = open("contact_list_magic_tree.csv", "r")
print()
new = contacts.readlines()
print()
#print(new[0].splitlines())
email_list = []
phone_list = []
for i in range(len(new)):
    item = (new[i].split(","))
    email_list.append(item[2])
    phone_list.append(item[3])
print(email_list)
print("\n",new)

email_to_text = ['@vtext.com', '@message.alltel.com', '@txt.att.net', '@cingularme.com',
'@MyMetroPcs.com', '@messaging.nextel.com', '@ptel.net', '@messaging.sprintpcs.com',
'@tms.suncom.com', '@tmomail.net', '@email.uscc.net', '@vmobl.com']

phone_dictionary = {}
for phone_number in phone_list:
    phone_emails = []
    for extension in email_to_text:
        phone_emails.append(phone_number+extension)
    phone_dictionary[phone_number] = phone_emails
print("\n")
# for item in phone_dictionary.values():
#     print(item,"\n")
df = pd.DataFrame(data=phone_dictionary)
print(df)



# display_contacts = tk.Tk()
# display_contacts = tk.Label("contacts")
# display_contacts.mainloop()

#print(display_contacts)
#print(contacts)
# df = pd.DataFrame(data=contacts)
# print(df)
# for item in contacts:
#     print(item)