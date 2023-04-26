from tkinter import *
import time
from tkinter import ttk
from PIL import ImageTk, Image
import requests
import threading
import math
import os
import sys
import urllib.request
import subprocess

window = Tk()
window.title("Crexto")
window.geometry("900x450")
window.maxsize(900,450)
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

img1 = ImageTk.PhotoImage((Image.open("./loading.png")).resize((250, 250), Image.LANCZOS))

def val():
    sub.configure(state=DISABLED,text="Fetching..",bg="#87ff00",fg="BLACK")
    enty.configure(state=DISABLED)
    if enty.get().startswith('https://open.spotify.com/playlist/'):

        x = requests.post('https://spotify.zodiacthedev.repl.co/getyt', json = {'id':enty.get()[34:]}).json()
        if x["status"]: 
            urllib.request.urlretrieve(x["playlist"]["image"], os.path.join( os.path.expanduser( '~' ), 'Music', 'Spotify Music Downloader',x['token']+'.png' ))
            down(x)
        
        else:
            sub.configure(state=ACTIVE,text="Invalid Link",bg="#E00004",fg="BLACK")
            enty.configure(state=NORMAL)
            enty.delete(0, 'end')
    else:
        sub.configure(state=ACTIVE,text="Try Again",bg="#E00004",fg="BLACK")
        enty.configure(state=NORMAL)
        enty.delete(0, 'end')

logo = Label(window, image=img1)
text = Label(window, text="Crexto's Music\nDownloader",font="Bahnschrift 30 bold")
enty = Entry(window,font="Bahnschrift 10 bold",width=80,name="link")
sub = Button(window, text="Submit",font="Bahnschrift 10 bold",width=20,command=val)
footer = Label(window, text="Made by Crexto",font="Bahnschrift 10 bold")

icon = ImageTk.PhotoImage((Image.open('./loading.png').resize((180, 180), Image.LANCZOS)))

def down(x):
    
    global cover

    cover = ImageTk.PhotoImage((Image.open(os.path.join( os.path.expanduser( '~' ), 'Music', 'Spotify Music Downloader',x['token']+'.png' ))).resize((224, 224), Image.LANCZOS))
    
    enty.destroy()
    sub.destroy()
    footer.destroy()
    logo.destroy()
    text.destroy()

    content = Frame(window)
    title = Label(content, text="Crexto's Music Downloader",font="Bahnschrift 30 bold")

    frame1 = Frame(content, relief=RIDGE,borderwidth=7,background="red")
    songlabel = Label(frame1, text="_ _ Tracks _ _",font="Bahnschrift 12 bold")
    songs = Listbox(frame1 ,width=55,height=12,activestyle=DOTBOX,font="Bahnschrift 10 bold")

    frame2 = Frame(content, relief=RIDGE,borderwidth=7,background="red")
    image = Label(frame2,image=cover)
    name = Label(frame2, text=x["playlist"]["name"],font="Bahnschrift 15 bold")
    owner = Label(frame2, text="by "+x["playlist"]["owner"],font="Bahnschrift 12 bold")
    desc = Label(frame2, text=x["playlist"]["desc"],font="Bahnschrift 9 bold")
    tracks = Label(frame2, text="total tracks: "+str(len(x["playlist"]["tracks"])+1),font="Bahnschrift 10 bold")
    
    frame3 = Frame(content, relief=RIDGE,borderwidth=5,background="red")
    pb = ttk.Progressbar(frame3,orient='horizontal',mode='determinate',length=600)
    info = Frame(frame3, relief=RIDGE,borderwidth=5,background='red')
    currentp = Label(info,text="Percentage: ",font="Bahnschrift 10 bold")
    currentd = Label(info,text="Currently Downloading: ",font="Bahnschrift 10 bold")
    remaining = Label(info,text="Time Remaining: ",font="Bahnschrift 10 bold")
    speeed = Label(info,text="Speed: ",font="Bahnschrift 10 bold")
    
    content.columnconfigure(0, weight=4)
    content.columnconfigure(1, weight=6)
    content.rowconfigure(0, weight=1)
    content.rowconfigure(1, weight=7)
    content.rowconfigure(2, weight=3)

    frame2.rowconfigure(0, weight=2)
    frame2.rowconfigure(1, weight=1)
    frame2.rowconfigure(2, weight=3)
    frame2.rowconfigure(3, weight=1)

    frame3.columnconfigure(1, weight=3)
    frame3.columnconfigure(2, weight=3)
    frame3.rowconfigure(0, weight=5)

    content.grid(column=0, row=0, sticky=(N, S, E, W))
    title.grid(column=0,columnspan=3,row=0,sticky=N)

    frame1.grid(column=0,columnspan=1,row=1,rowspan=2,sticky=(N,W),padx=(10,0))
    songlabel.grid(column=0,row=0)
    songs.grid(column=0,row=1)

    frame2.grid(column=1,columnspan=2,row=1,rowspan=2,sticky=(N,E,W),padx=(0,10),ipadx=8)
    image.grid(column=0,row=0,rowspan=4,sticky=W,padx=(0,8))
    name.grid(column=1,row=0,sticky=NW,pady=5,padx=(0,8))
    owner.grid(column=1,row=1,sticky=NW,pady=5,padx=(0,8))
    desc.grid(column=1,row=2,sticky=NW,pady=5,padx=(0,8))
    tracks.grid(column=1,row=3,sticky=NW,pady=5,padx=(0,8))

    frame3.grid(column=0,columnspan=3,row=2,rowspan=3,sticky=(S,E,W),padx=10,pady=(0,10))
    pb.grid(column=0,row=0,columnspan=1,sticky=(S,W,N),pady=20,padx=15)
    info.grid(column=1,row=0,columnspan=2,sticky=(N,S,E,W),ipadx=8)
    currentp.grid(column=0,row=0,sticky=W,padx=(0,8))
    currentd.grid(column=0,row=1,sticky=W,padx=(0,8))
    remaining.grid(column=0,row=2,sticky=W,padx=(0,8))
    speeed.grid(column=0,row=3,sticky=W,padx=(0,8))
    
    songs.insert(0,x["name"])
    for y in range(len(x["playlist"]["tracks"])):
        songs.insert(y+1,x["playlist"]["tracks"][y]["name"])

    def finish(a):
        content.destroy()
        window.title("Crexto's Music Downloader")
        window.geometry("450x200")
        window.maxsize(450, 200)

        finframe = Frame(window)
        ima = Label(finframe, image=icon)
        mes = Label(finframe, text="Files Have Been\nDownloaded",font="Bahnschrift 23 bold")
        ope = Button(finframe, text="Open Files",font="Bahnschrift 14 bold",command=lambda:subprocess.Popen(r'explorer /select,"C:\Users\charith\Music\Spotify Music Downloader\"'+a+".mp3"))
        exi = Button(finframe, text="Exit",font="Bahnschrift 14 bold",command=lambda:sys.exit())

        finframe.pack()
        ima.pack(side=LEFT,padx=10,pady=10)
        mes.pack(pady=(30,10))
        ope.pack(side=LEFT,padx=(35,10),anchor=N)
        exi.pack(side=RIGHT,padx=(0,40),anchor=N)


    def download(name, link, token):
        global start
    
        try:
            currentd.configure(text="Currently Downloading: "+(name if len(name)<13 else name[0:12]+".."))
            path = os.path.join( os.path.expanduser( '~' ), 'Music', 'Spotify Music Downloader' ) 
            if not(os.path.isdir(path)):
                os.mkdir(path)

            start = time.perf_counter()
            urllib.request.urlretrieve(link, path+'\\'+name+".mp3", show_progress)
            if songs.size() != 0:
                songs.delete(0)

            wa = requests.post('https://spotify.zodiacthedev.repl.co/gettracks', json={'token': token})
            if wa.text == 'finished':
                finish(name)
                os.remove(path+"\\"+token+".png")
                return
            else:
                download(wa.json()['name'], wa.json()['link'], token)
        except Exception as e:
            print(e) 

    def show_progress(block_num, block_size, total_size):
        speed = round(block_num * block_size//(time.perf_counter() -start)/ 100000,2) 
        remain = 1 if speed == 0 else round(((total_size*songs.size()) - (block_num * block_size))//(speed*100000))+1

        currentp.configure(text="Percentage: "+str(100 if (math.ceil(block_num * block_size / total_size * 100)) > 100 else (math.ceil(block_num * block_size / total_size * 100)))+"%")
        remaining.configure(text="Time Remaining: "+ (str(remain)+" seconds" if remain < 60 else str(remain//60)+" minutes "+str(remain%60)+" seconds"))
        speeed.configure(text="Speed: "+str(speed)+" Mbps")
        pb["value"] = round(block_num * block_size / total_size * 100, 2)

    threading.Thread(target=lambda:download(x["name"], x['link'], x['token'])).start()

logo.pack(pady=8)
text.pack()
enty.pack(pady=6)
sub.pack()
footer.pack(anchor=SE)

mainloop()