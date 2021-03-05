import tkinter as tk
import os
import random
import webbrowser
#custom_keys_building

button_list = [
['Evernote: Love','evernote:///view/21614375/s192/10b4247b-5f09-4b66-953d-02e5f27aac3c/10b4247b-5f09-4b66-953d-02e5f27aac3c/'],
['Trello: עכשיו', 'trello://trello.com/b/kGXNJK3x/עכשיו'],
['Trello: Web','https://trello.com/c/Ljfh6gZq'],
['Trello: Specfic','trello://trello.com/c/Ljfh6gZq'],
['Spotify: Shabbat','https://open.spotify.com/track/2gI9RfuSwulsBujm7hbOFv?si=891addaca9524eaf']
]

window = tk.Tk()
topFrame = tk.Frame(master = window, relief = "sunken", borderwidth = 10)
topFrame.pack()
bottomFrame = tk.Frame(master = window, relief = "raised", borderwidth = 10)
bottomFrame.pack()

def runLink(): #avalue <-- argument
    #choose = avalue
    #choose = input("what number? ")
    choose = 'sucess_is_coming'
    if choose == 0:
        this = webbrowser.open('evernote:///view/21614375/s192/10b4247b-5f09-4b66-953d-02e5f27aac3c/10b4247b-5f09-4b66-953d-02e5f27aac3c/')
    elif choose == 1:
        that = webbrowser.open('trello://trello.com/b/kGXNJK3x/עכשיו')
    elif choose == 2:
        webbrowser.open('https://trello.com/c/Ljfh6gZq')
    elif choose == 3:
        webbrowser.open('trello://trello.com/c/Ljfh6gZq')
    elif choose == 4:
        webbrowser.open('https://open.spotify.com/track/2gI9RfuSwulsBujm7hbOFv?si=891addaca9524eaf')

for i in range(len(button_list)):
    b = tk.Button(text =f"{button_list[i][0]}", master = topFrame, width = 16, height = 5, command = lambda: runLink()) #command = helloCallBack)
    b.pack(side = "left")
window.mainloop()

for i in range(2):
    b = tk.Button(text ="[A Key]", master = topFrame, width = 16, height = 5, command = runLink) #command = helloCallBack)
    b.pack(side = "left")
    ##Taking a jump at binding keys
    #b.bind('a', lambda event: runLink())
    #
    b = tk.Button(text ="[B Key]", master = bottomFrame, width = 16, height = 5, command = runLink) #command = helloCallBack)
    b.pack(side = "left")
    #
    b = tk.Button(text ="[A Key]", master = topFrame, width = 16, height = 5, command = runLink) #command = helloCallBack)
    b.pack(side = "left")
    #
    b = tk.Button(text ="[B Key]", master = bottomFrame, width = 16, height = 5, command = runLink) #command = helloCallBack)
    b.pack(side = "left")
window.mainloop()  

new_evernote_button = input("Please paste the Evenote link (the 'Copy Note Link' from a right-click): \n")
new_list = new_evernote_button.split("/")
for i,item in enumerate(new_list):
    if item == "":
        new_list.remove(item)
    #i is here for fun, because I thought I might have needed it

#building an evernote link to open the desktop a
new_desktop_evernote_link = "evernote:///view/"+new_list[5]+"/"+new_list[3]+"/"+new_list[6]+"/"+new_list[6]+"/"
webbrowser.open(new_desktop_evernote_link)
