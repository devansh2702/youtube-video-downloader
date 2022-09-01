"""
YOUTUBE DOWNLOADER
PSC INNOVATIVE ASSIGNMENT

19BCE247 DEVANSH SHAH

"""
from tkinter import *
from tkinter import ttk

import pytube
from pytube import *
from PIL import Image,ImageTk
import requests
import io
import os

class youtube_app():
    #========================function for making GUI===========================
    def __init__(self,root):
        self.root=root
        self.root.title("YOUTUBE DOWNLOADER")
        self.root.geometry("700x650+400+100")
        self.root.config(bg="#262626")

        title= Label(self.root,text="PYTHON PROJECT :YOUTUBE DOWNLOADER FOR PSC COURSE",font=("times new roman",15,'bold'),bg="#262626",fg="white").pack(side=TOP,fill=X)

        self.var_link=StringVar()
        lbl_url=Label(self.root, text="LINK : ", font=("times new roman", 15), bg="#262626", fg="white").place(x=10, y=50)
        url=Entry(self.root,  font=("times new roman", 15),textvariable=self.var_link, bg="#626262", fg="white",width=50).place(x=150, y=50)

        self.var_ftype = StringVar()
        self.var_ftype.set("HIGH")
        lbl_ftype = Label(self.root, text="FILE QUALITY: ", font=("times new roman", 15), bg="#262626", fg="white").place(x=10, y=100)

        radio_high=Radiobutton(self.root,text="HIGH",variable=self.var_ftype,value="HIGH",font=("times new roman",15),bg="#262626",fg="white",activebackground="#626262").place(x=150,y=95)
        radio_low = Radiobutton(self.root, text="LOW", variable=self.var_ftype, value="LOW",
                                 font=("times new roman", 15), bg="#262626", fg="white",
                                 activebackground="#626262").place(x=270, y=95)
        radio_onlyaudio = Radiobutton(self.root, text="ONLY AUDIO", variable=self.var_ftype, value="ONLY AUDIO",
                                 font=("times new roman", 15), bg="#262626", fg="white",
                                 activebackground="#626262").place(x=380, y=95)

        search=Button(self.root, text="SEARCH", command=self.search ,font=("times new roman", 15), bg="#626262", fg="white").place(x=560, y=95 ,height=35)

        frame1= Frame(self.root,bd=2,relief=RIDGE,bg="#626262")
        frame1.place(x=10,y=150,width=650,height=320)

        self.v_title=Label(frame1,bg="#262626",fg="white",font=("times new roman",15),text="VIDEO TITLE")
        self.v_title.place(x=10,y=10,relwidth=0.965)

        self.v_image=Label(frame1,bg="#262626",fg="white",font=("times new roman",15),text="VIDEO \nIMAGE",bd=2,relief=RIDGE)
        self.v_image.place(x=10,y=45,width=280,height=265)

        lbl_desc = Label(frame1, bg="#626262", fg="white", font=("times new roman", 15), text="DESCRIPTION").place(x=300, y=45)
        self.v_desc = Text(frame1, bg="#626262", fg="black", font=("ariel", 10))
        self.v_desc.place(x=300, y=70, width=330, height=235)

        self.lbl_size = Label(self.root, text="TOTAL SIZE : 0 MB ", font=("times new roman", 15), bg="#262626", fg="white")
        self.lbl_size.place(x=10,y=500)

        self.lbl_percentage = Label(self.root, text="DOWNLOADING : 0 % ", font=("times new roman", 15), bg="#262626",fg="white")
        self.lbl_percentage.place(x=250, y=500)

        clear = Button(self.root, text="CLEAR",command=self.clear, font=("times new roman", 12), bg="#626262", fg="white").place(x=480,y=500,height=35)
        self.btn_download = Button(self.root, text="DOWNLOAD",command=self.download, font=("times new roman", 12), bg="#626262", fg="white")
        self.btn_download.place(x=550,y=500,height=35)

        self.progess=ttk.Progressbar(self.root,orient=HORIZONTAL,length=640,mode='determinate')
        self.progess.place(x=10,y=550)

        self.lbl_msg = Label(self.root, text="", font=("times new roman", 15), bg="#262626",fg="white")
        self.lbl_msg.place(x=10, y=580,relwidth=0.965)
        #=========making the loaction for file storage===========
        if os.path.exists("PROJECT_DOWNLOADS")==False:
            os.mkdir("PROJECT_DOWNLOADS")

#=================================functions for the code===================================

    def search(self):


        try:
            if self.var_link.get()=="":
                self.lbl_msg.config(text="URL CANNOT BE EMPTY",bg="red")
            else:
                yt = YouTube(self.var_link.get())
                #=============convert image url into image
                response= requests.get(yt.thumbnail_url)
                img_byte=io.BytesIO(response.content)
                self.img=Image.open(img_byte)
                self.img=self.img.resize((280,265),Image.ANTIALIAS)
                self.img=ImageTk.PhotoImage(self.img)
                self.v_image.config(image=self.img)
                #=========fetch the size as per user===========
                if self.var_ftype.get()=="LOW":
                    select = yt.streams.filter(progressive=True,file_extension='mp4').first()
                if self.var_ftype.get()=="HIGH":
                    select = yt.streams.filter(progressive=True, file_extension='mp4').last()
                if self.var_ftype.get()=="ONLY AUDIO":
                    select = yt.streams.filter(only_audio=True).first()

                self.size_inbytes=select.filesize
                max_size=self.size_inbytes/1024000
                self.mb=str(round(max_size,2))+ 'MB'

                #============displaying the video info=============
                self.lbl_size.config(text= "TOTAL SIZE : "+self.mb )
                self.v_title.config(text=yt.title)
                self.v_desc.delete('1.0', END)
                self.v_desc.insert(END, yt.description[:500])
                self.btn_download.config(state=NORMAL)

        except pytube.exceptions.RegexMatchError:
            self.lbl_msg.config(text="NO SUCH YOUTUBE VIDEO FOUND", bg="red")

    def progress_(self,streams,chunk,bytes_remaining):
        percentage=(float(abs(bytes_remaining-self.size_inbytes)/self.size_inbytes))*float(100)
        self.progess['value']=percentage
        self.progess.update()
        self.lbl_percentage.config(text=f"DOWNLOADING : {str(round(percentage,2))}%")

        if round(percentage,2)==100:
            self.lbl_msg.config(text="DOWNLOAD COMPLETED", bg="green")
            self.btn_download.config(state=DISABLED)

    def clear(self):
        self.var_ftype.set("HIGH")
        self.var_link.set('')
        self.progess['value']=0
        self.btn_download.config(state=DISABLED)
        self.lbl_msg.config(text='',bg="#262626")
        self.v_title.config(text='VIDEO TITLE HERE')
        self.v_image.config(image='')
        self.v_desc.delete('1.0', END)
        self.lbl_size.config(text="TOTAL SIZE : 0 MB")
        self.lbl_percentage.config(text="DOWNLOADING : 0%")

    def download(self):

        try:

            yt = YouTube(self.var_link.get(), on_progress_callback=self.progress_)
            # =========fetch the size as per user===========
            if self.var_ftype.get() == "LOW":
                select = yt.streams.filter(progressive=True, file_extension='mp4').first()
                select.download("PROJECT_DOWNLOADS/")
            if self.var_ftype.get() == "HIGH":
                select = yt.streams.filter(progressive=True, file_extension='mp4').last()
                select.download("PROJECT_DOWNLOADS/")
            if self.var_ftype.get() == "ONLY AUDIO":
                select = yt.streams.filter(only_audio=True).first()
                select.download("PROJECT_DOWNLOADS/")
        except pytube.exceptions.RegexMatchError:
            self.lbl_msg.config(text="INCORRECT URL FOUND.. CANNOT DOWNLOAD.!", bg="red")



root=Tk()
obj=youtube_app(root)
root.mainloop()