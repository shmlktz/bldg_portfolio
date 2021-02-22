import tkinter as tk

##lets make a personal customizable keyboard
window = tk.Tk()

##open links
import webbrowser
def runLink():
    this = webbrowser.open('evernote:///view/21614375/s192/10b4247b-5f09-4b66-953d-02e5f27aac3c/10b4247b-5f09-4b66-953d-02e5f27aac3c/')
#this = "evernote:///view/21614375/s192/10b4247b-5f09-4b66-953d-02e5f27aac3c/10b4247b-5f09-4b66-953d-02e5f27aac3c/"
for i in range(8):
    frame = tk.Frame(master = window, relief = "sunken", borderwidth = 10)
    frame.pack(side = "left")
    b = tk.Button(text ="[A Key]", master = frame, width = 16, height = 5, command = runLink) #command = helloCallBack)
    b.pack()
    frame_2 = tk.Frame(master = window, relief = "raised", borderwidth = 10)
    frame_2.pack(side = tk.LEFT)
    b = tk.Button(text ="[B Key]", master = frame_2, width = 16, height = 5, command = runLink) #command = helloCallBack)
    b.pack()
    # frame = tk.Frame(master = window, relief = "raised", borderwidth = 10)
    # frame.pack(side = tk.RIGHT)
    # b = tk.Button(text ="[A Key]", master = frame, width = 16, height = 5, command = runLink) #command = helloCallBack)
    # b.pack()

    # frame = tk.Frame(master = window, relief = "raised", borderwidth = 10)
    # frame.pack(side = tk.TOP)
    # b = tk.Button(text ="[A Key]", master = frame, width = 16, height = 5, command = runLink) #command = helloCallBack)
    # b.pack()

#Building a button from the components of a [Right Click and "Copy Note Link"] evernote link
#STRUCTURES###
#desktop link: evernote:///view/[userId]/[shardId]/[noteGuid]/[noteGuid]/
#web link: https://[service]/shard/[shardId]/nl/[userId]/[noteGuid]/
##############
new_evernote_button = input("Please paste the Evenote link (the 'Copy Note Link' from a right-click): \n")
new_list = new_evernote_button.split("/")
for i,item in enumerate(new_list):
    if item == "":
        new_list.remove(item)
    #i is here for fun, because I thought I might have needed it

new_desktop_evernote_link = "evernote:///view/"+new_list[5]+"/"+new_list[3]+"/"+new_list[6]+"/"+new_list[6]+"/"
webbrowser.open(new_desktop_evernote_link)

window.mainloop()



# name_entry = tk.Entry(
#     fg="white", bg="black", width = 16, master = frame ) #fg = text; bg = background
# name_entry.pack()
# name_entry.insert(0, "_name_")