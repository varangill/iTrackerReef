###imports
import cv2
import sys
import socket
import math
import time
import serial
import numpy as np
import Tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox
from tkinter import ttk
import serial.tools.list_ports
from playsound import playsound
from gtts import gTTS
import webbrowser
import os
import subprocess

# --------------------------------------------------------

###GUI
window = tk.Tk()  # Makes main window
window.withdraw()


webbrowser.register('chrome',
	None,
	webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))

imageFrame = tk.Frame(window, width=640, height=480)
#imageFrame.grid(row=0, column=0, padx=5, pady=5)

imageFrame = Label(imageFrame)
#imageFrame.grid(row=20, column=20)



root = tk.Tk()
root.wm_title("App")
c = tk.Canvas(root, width=1000, height=500, bg='#1E5878')
#root.attributes('-topmost',True)
c.pack()

display = tk.Frame(root, bg='white')
display.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
# --------------------------------------------------------


###CAM properties
cam_width = 640
cam_height = 480
cam_fps = 30

# Default value for cropping (eg. no cropping)
cropping_width_def_val = cam_width
cropping_height_def_val = cam_height
cropping_pos_x_def_val = 0
cropping_pos_y_def_val = 0

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

camera = cv2.VideoCapture(0)
# Give some time for the camera to start
time.sleep(1)

if (camera.isOpened()):
    print ("Camera opened")

# Set camera resolution and frame/sec if possible
camera.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)
camera.set(cv2.CAP_PROP_FPS, cam_fps)
# --------------------------------------------------------
underlineposition = 1
pagenumber = 1

### Head Tracking parameters
HeadMinSize_def_val = 80
HeadMaxSize_def_val = 600
minNeighbors_def_val = 10
scaleFactor_def_val = 1.02

Socket_val = BooleanVar()
Serial_val = BooleanVar()

HeadMinSize_val = HeadMinSize_def_val
HeadMaxSize_val = HeadMaxSize_def_val
minNeighbors_val = minNeighbors_def_val
scaleFactor_val = scaleFactor_def_val

samples = 0
sum_x = 0
sum_y = 0
X_HeadPos = 999
Y_HeadPos = 999

X_HeadPos_val = IntVar(value=X_HeadPos)
Y_HeadPos_val = IntVar(value=Y_HeadPos)

EB_color = (255, 100, 50)
Head_color = (255, 255, 255)
Overlay1_color = (200, 200, 200)
Overlay2_color = (220, 220, 220)
# --------------------------------------------------------


###Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port on the server given by the caller
server_address = ('localhost', 10001)
print (sys.stderr, 'connecting to %s port %s' % server_address)

try:
    sock.connect(server_address)
    print (sys.stderr, 'connected to %s port %s' % server_address)
# except socket.timeout:
except:
    # print >>sys.stderr, 'connection timeout on %s port %s' % server_address
    print ("Socket connection exception")
    sock.close()


# --------------------------------------------------------


def saveData(data,number,type):
    if (number > 0 & number < 19):
        dataLoc = number - 1
    else:
        print("num out of bounds")
    newData= [];
    filepath = 'data.txt'
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            newData.append(line.strip() + "\n")
            line = fp.readline()
    if (type == "cm"):
        newData[dataLoc] = "CM: " + data + " \n"
    elif (type == "yt"):
        newData[dataLoc] = "YT: " + data + " \n"
    fileWriter = open("data.txt", "w")
    fileWriter.writelines(newData)
    fileWriter.close()



def clicked3():
   h1.place_forget()
   h2.place_forget()
   h3.place_forget()
   h4.place_forget()
   h5.place_forget()
   h6.place_forget()
   one.place_forget()
   two.place_forget()
   three.place_forget()
   four.place_forget()
   five.place_forget()
   six.place_forget()
   h7.place(x=4, y=0)
   h8.place(x=404, y=0)
   h9.place(x=4, y=136)
   h10.place(x=404, y=136)
   h11.place(x=4, y=272)
   h12.place(x=404, y=272)
   seven.place(x=10, y=100)
   eight.place(x=410, y=100)
   nine.place(x=10, y=236)
   ten.place(x=410, y=236)
   eleven.place(x=10, y=372)
   twelve.place(x=410, y=372)
   b3.pack_forget()
   b4.pack()
   global pagenumber
   pagenumber=2

def clicked4():
   h7.place_forget()
   h8.place_forget()
   h9.place_forget()
   h10.place_forget()
   h11.place_forget()
   h12.place_forget()
   h6.place_forget()
   seven.place_forget()
   eight.place_forget()
   nine.place_forget()
   ten.place_forget()
   eleven.place_forget()
   twelve.place_forget()
   h13.place(x=4, y=0)
   h14.place(x=404, y=0)
   h15.place(x=4, y=136)
   h16.place(x=404, y=136)
   h17.place(x=4, y=272)
   h18.place(x=404, y=272)
   thirteen.place(x=10, y=100)
   fourteen.place(x=410, y=100)
   fifteen.place(x=10, y=236)
   sixteen.place(x=410, y=236)
   seventeen.place(x=10, y=372)
   eighteen.place(x=410, y=372)
   b4.pack_forget()
   b5.pack()
   b6.pack()
   global pagenumber
   pagenumber=3

def clicked5():
    h13.place_forget()
    h14.place_forget()
    h15.place_forget()
    h16.place_forget()
    h17.place_forget()
    h18.place_forget()
    h19.place_forget()
    h20.place_forget()
    thirteen.place_forget()
    fourteen.place_forget()
    fifteen.place_forget()
    sixteen.place_forget()
    seventeen.place_forget()
    eighteen.place_forget()
    b5.pack_forget()
    b6.pack_forget()
    entry1.place_forget()
    entry2.place_forget()
    h1.place(x=4, y=0)
    h2.place(x=404, y=0)
    h3.place(x=4, y=136)
    h4.place(x=404, y=136)
    h5.place(x=4, y=272)
    h6.place(x=404, y=272)
    one.place(x=10, y=100)
    two.place(x=410, y=100)
    three.place(x=10, y=236)
    four.place(x=410, y=236)
    five.place(x=10, y=372)
    six.place(x=410, y=372)
    b3.pack()
    global pagenumber
    pagenumber = 1
    resetall()
    global underlineposition
    underlineposition=0
    underlinelocation()


def clicked6():
    h13.place_forget()
    h14.place_forget()
    h15.place_forget()
    h16.place_forget()
    h17.place_forget()
    h18.place_forget()
    b6.pack_forget()
    thirteen.place_forget()
    fourteen.place_forget()
    fifteen.place_forget()
    sixteen.place_forget()
    seventeen.place_forget()
    eighteen.place_forget()
    h19.place(x=4,y=5)
    h20.place(x=404,y=5)
    entry1.place(x=4,y=325)
    entry2.place(x=304, y=325)
    global pagenumber
    pagenumber=4

def clicked7(): #this activates CM save
    saveData(entry1.get(), int(entry2.get()), "cm")
    updateData()

def clicked8(): #this leads to YT name entering. entry1 is youtube URL or the CM
    saveData(entry1.get(), int(entry2.get()),"yt")
    updateData()


global data
data = []
#Receive data from text file

#Head Clicking
def clicker():
    global underlineposition
    global pagenumber
    if(underlineposition==1):#
        if ((data[0] == "Blank")!=True):
            playsound("sounds/cm0.mp3")
    elif(underlineposition==2):#
        if ((data[1] == "Blank") != True):
            playsound("sounds/cm1.mp3")
    elif(underlineposition==3):#
        if ((data[2] == "Blank") != True):
            playsound("sounds/cm2.mp3")
    elif(underlineposition==4):#
        if ((data[3] == "Blank")!=True):
            playsound("sounds/cm3.mp3")
    elif(underlineposition==5):#
        if ((data[4] == "Blank") != True):
            playsound("sounds/cm4.mp3")
    elif(underlineposition==6):#
        if ((data[5] == "Blank") != True):
            playsound("sounds/cm5.mp3")
    elif(underlineposition==7):#Next (b3)
        clicked3()
        underlineposition = 8
        pagenumber=2
        b3.configure(font=("Arial Bold", 10), fg='black')
        h7.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')
    elif(underlineposition==8):
        if ((data[6] == "Blank") != True):
            playsound("sounds/cm6.mp3")
    elif(underlineposition==9):
        if ((data[7] == "Blank") != True):
            playsound("sounds/cm7.mp3")
    elif(underlineposition==10):
        if ((data[8] == "Blank") != True):
            playsound("sounds/cm8.mp3")
    elif(underlineposition==11):
        if ((data[9] == "Blank") != True):
            playsound("sounds/cm9.mp3")
    elif(underlineposition==12):
        if ((data[10] == "Blank") != True):
            playsound("sounds/cm10.mp3")
    elif(underlineposition==13):
        if ((data[11] == "Blank") != True):
            playsound("sounds/cm11.mp3")
    elif(underlineposition==14):#Next (b4)
        clicked4()
        underlineposition = 15
        pagenumber=3
        b4.configure(font=("Arial Bold", 10), fg='black')
        h13.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')
    elif(underlineposition==15):
        if ((data[12] == "Blank")!=True):
            webbrowser.get('chrome').open(data[12])
    elif(underlineposition==16):
        if ((data[13] == "Blank")!=True):
            webbrowser.get('chrome').open(data[13])
    elif(underlineposition==17):
        if ((data[14] == "Blank")!=True):
            webbrowser.get('chrome').open(data[14])
    elif(underlineposition==18):
        if ((data[15] == "Blank")!=True):
            webbrowser.get('chrome').open(data[15])
    elif(underlineposition==19):
        if ((data[16] == "Blank")!=True):
            webbrowser.get('chrome').open(data[16])
    elif(underlineposition==20):
        if ((data[17] == "Blank")!=True):
            webbrowser.get('chrome').open(data[17])
    elif(underlineposition==21):#Home (b5)
        clicked5()
        underlineposition=1
        pagenumber=1
        b5.configure(font=("Arial Bold", 10), fg='black')
        h1.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')







#Every Page
coordinatesx = tk.Text(root,font=("Arial", 10, 'bold'), fg='Black', bg='#C9E2F0', height = 1, width= 6)
coordinatesy = tk.Text(root, font=("Arial", 10, 'bold'), fg='Black', bg='#C9E2F0', height = 1, width= 6)
coordinatesx.place(x= 400, y= 10)
coordinatesy.place(x= 450, y=10)
coordinatesx.insert(INSERT,"x: 0")
coordinatesy.insert(INSERT,"y: 0")



#Page 1
h1 = tk.Button(display, text='', font=("Arial", 10, 'bold', 'underline'), fg='red', bg='#C9E2F0',
                height=7, width=48)
one = tk.Text(display, font=("Arial", 10, 'bold'), fg='Black', bg='#C9E2F0', height = 1, width= 1)
one.insert(INSERT,"1")
h2 = tk.Button(display, text='', font=("Arial Bold", 10), fg='black', bg='#C9E2F0',
                   height=7, width=48)
two = tk.Text(display, font=("Arial", 10, 'bold'), fg='Black', bg='#C9E2F0', height = 1, width= 1)
two.insert(INSERT,"2")
h3 = tk.Button(display, text='', font=("Arial Bold", 10), fg='black', bg='#C9E2F0',
                   height=7, width=48)
three = tk.Text(display, font=("Arial", 10, 'bold'), fg='Black', bg='#C9E2F0', height = 1, width= 1)
three.insert(INSERT,"3")
h4 = tk.Button(display, text='', font=("Arial Bold", 10), fg='black', bg='#C9E2F0',
                   height=7, width=48)
four = tk.Text(display, font=("Arial", 10, 'bold'), fg='Black', bg='#C9E2F0', height = 1, width= 1)
four.insert(INSERT,"4")
h5 = tk.Button(display, text='', font=("Arial Bold", 10), fg='black', bg='#C9E2F0',
                   height=7, width=48)
five = tk.Text(display, font=("Arial", 10, 'bold'), fg='Black', bg='#C9E2F0', height = 1, width= 1)
five.insert(INSERT,"5")
h6 = tk.Button(display, text='', font=("Arial Bold", 10), fg='black', bg='#C9E2F0',
                   height=7, width=48)
six = tk.Text(display, font=("Arial", 10, 'bold'), fg='Black', bg='#C9E2F0', height = 1, width= 1)
six.insert(INSERT,"6")


b3 = tk.Button(root, text='Next', padx=10, pady=5, fg='white', bg='#1E5878', command=clicked3)
h1.place(x=4, y=0)
h2.place(x=404, y=0)
h3.place(x=4, y=136)
h4.place(x=404, y=136)
h5.place(x=4, y=272)
h6.place(x=404, y=272)
one.place(x=10, y=100)
two.place(x=410, y=100)
three.place(x=10, y=236)
four.place(x=410, y=236)
five.place(x=10, y=372)
six.place(x=410, y=372)
b3.pack()



#Page 2
h7 = tk.Button(display, text='', font=("Arial Bold", 10), fg='black', bg='#C9E2F0', command=clicked3,
              height=7, width=48)
h8 = tk.Button(display, text='', font=("Arial Bold", 10), fg='black', bg='#C9E2F0', command=clicked3,
              height=7, width=48)
h9 = tk.Button(display, text='', font=("Arial Bold", 10), fg='black', bg='#C9E2F0', command=clicked3,
              height=7, width=48)
h10 = tk.Button(display, text='', font=("Arial Bold", 10), fg='black', bg='#C9E2F0', command=clicked3,
              height=7, width=48)
h11 = tk.Button(display, text='', font=("Arial Bold", 10), fg='black', bg='#C9E2F0', command=clicked3,
              height=7, width=48)
h12 = tk.Button(display, text='', font=("Arial Bold", 10), fg='black', bg='#C9E2F0', command=clicked3,
              height=7, width=48)
seven = tk.Text(display, font=("Arial", 10, 'bold'), fg='Black', bg='#C9E2F0', height = 1, width= 1)
seven.insert(INSERT,"7")
eight = tk.Text(display, font=("Arial", 10, 'bold'), fg='Black', bg='#C9E2F0', height = 1, width= 1)
eight.insert(INSERT,"8")
nine = tk.Text(display, font=("Arial", 10, 'bold'), fg='Black', bg='#C9E2F0', height = 1, width= 1)
nine.insert(INSERT,"9")
ten = tk.Text(display, font=("Arial", 10, 'bold'), fg='Black', bg='#C9E2F0', height = 1, width= 2)
ten.insert(INSERT,"10")
eleven = tk.Text(display, font=("Arial", 10, 'bold'), fg='Black', bg='#C9E2F0', height = 1, width= 2)
eleven.insert(INSERT,"11")
twelve = tk.Text(display, font=("Arial", 10, 'bold'), fg='Black', bg='#C9E2F0', height = 1, width= 2)
twelve.insert(INSERT,"12")

b4 = tk.Button(root, text='Next', padx=10, pady=5, fg='white', bg='#1E5878', command=clicked4)


#Page 3
h13 = tk.Button(display, text='', font=("Arial Bold", 10), fg='black', bg='#C9E2F0', command=clicked4,
              height=7, width=48)
h14 = tk.Button(display, text='', font=("Arial Bold", 10), fg='black', bg='#C9E2F0', command=clicked4,
              height=7, width=48)
h15 = tk.Button(display, text='', font=("Arial Bold", 10), fg='black', bg='#C9E2F0', command=clicked4,
              height=7, width=48)
h16 = tk.Button(display, text='', font=("Arial Bold", 10), fg='black', bg='#C9E2F0', command=clicked4,
              height=7, width=48)
h17 = tk.Button(display, text='', font=("Arial Bold", 10), fg='black', bg='#C9E2F0', command=clicked4,
              height=7, width=48)
h18 = tk.Button(display, text='', font=("Arial Bold", 10), fg='black', bg='#C9E2F0', command=clicked4,
              height=7, width=48)


thirteen = tk.Text(display, font=("Arial", 10, 'bold'), fg='Black', bg='#C9E2F0', height = 1, width= 2)
thirteen.insert(INSERT,"13")
fourteen = tk.Text(display, font=("Arial", 10, 'bold'), fg='Black', bg='#C9E2F0', height = 1, width= 2)
fourteen.insert(INSERT,"14")
fifteen = tk.Text(display, font=("Arial", 10, 'bold'), fg='Black', bg='#C9E2F0', height = 1, width= 2)
fifteen.insert(INSERT,"15")
sixteen = tk.Text(display, font=("Arial", 10, 'bold'), fg='Black', bg='#C9E2F0', height = 1, width= 2)
sixteen.insert(INSERT,"16")
seventeen = tk.Text(display, font=("Arial", 10, 'bold'), fg='Black', bg='#C9E2F0', height = 1, width= 2)
seventeen.insert(INSERT,"17")
eighteen = tk.Text(display, font=("Arial", 10, 'bold'), fg='Black', bg='#C9E2F0', height = 1, width= 2)
eighteen.insert(INSERT,"18")

b5 = tk.Button(root, text='Home', padx=10, pady=5, fg='white', bg='#1E5878', command=clicked5)
b6 = tk.Button(root, text='Personal Input', padx= 25, pady= 5, fg='white', bg='#1E5878', command= clicked6)


#Page 4
h19 = tk.Button(display, text='Canned Message', font=("Arial Bold", 10), fg='black', bg='#C9E2F0', command=clicked7,
              height=15, width=48)
h20 = tk.Button(display, text='Youtube Link', font=("Arial Bold", 10), fg='black', bg='#C9E2F0', command=clicked8,
              height=15, width=48)
entry1 = Entry(display,width= 45)
entry1.insert(0,"Enter in FULL YouTube URL or canned message...")
entry2 = Entry(display,width=45)
entry2.insert(0,"What box number would you like to replace")


def updateButtons(dataArray): #need to fix this so the button text updates automatically
    h1.configure(text=dataArray[0])
    h2.configure(text=dataArray[1])
    h3.configure(text=dataArray[2])
    h4.configure(text=dataArray[3])
    h5.configure(text=dataArray[4])
    h6.configure(text=dataArray[5])
    h7.configure(text=dataArray[6])
    h8.configure(text=dataArray[7])
    h9.configure(text=dataArray[8])
    h10.configure(text=dataArray[9])
    h11.configure(text=dataArray[10])
    h12.configure(text=dataArray[11])
    h13.configure(text=dataArray[12])
    h14.configure(text=dataArray[13])
    h15.configure(text=dataArray[14])
    h16.configure(text=dataArray[15])
    h17.configure(text=dataArray[16])
    h18.configure(text=dataArray[17])

def updateData():
    filepath = 'data.txt'
    data = []
    with open(filepath) as fp:
       line = fp.readline()
       cnt = 0
       while line:
           data.append(line.strip()[4:])
           if (len(data[cnt])==0):
               data[cnt] = "Blank"
           line = fp.readline()
           cnt += 1
    for x in range(12): #creating MP3 files for canned messages
        if (data[x] =="Blank"): #if no MP3 file, skip to save time and memory
            continue;
        filename = "sounds/cm" + str(x) + ".mp3"
        if os.path.exists(filename):
            os.remove(filename)
        myobj = gTTS(text=data[x], lang='en', slow=False)
        myobj.save(filename)
    updateButtons(data)
    return data

data = updateData()

#Underline Location
def switcher(under_loc):
    if(under_loc==1):
        b5.configure(font=("Arial Bold", 10), fg='black')
        b3.configure(font=("Arial Bold", 10), fg='black')
        h1.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')


    elif(under_loc==2):
        h1.configure(font=("Arial Bold", 10), fg='black')
        h2.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')

    elif(under_loc==3):
        h2.configure(font=("Arial Bold", 10), fg='black')
        h3.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')


    elif(under_loc==4):
        h3.configure(font=("Arial Bold", 10), fg='black')
        h4.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')

    elif(under_loc==5):
        h4.configure(font=("Arial Bold", 10), fg='black')
        h5.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')

    elif(under_loc==6):
        h5.configure(font=("Arial Bold", 10), fg='black')
        h6.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')

    elif(under_loc==7):
        h6.configure(font=("Arial Bold", 10), fg='black')
        b3.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')

    elif(under_loc==8):
        b3.configure(font=("Arial Bold", 10), fg='black')
        b4.configure(font=("Arial Bold", 10), fg='black')
        h7.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')

    elif(under_loc==9):
        h7.configure(font=("Arial Bold", 10), fg='black')
        h8.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')

    elif(under_loc==10):
        h8.configure(font=("Arial Bold", 10), fg='black')
        h9.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')

    elif(under_loc==11):
        h9.configure(font=("Arial Bold", 10), fg='black')
        h10.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')

    elif(under_loc==12):
        h10.configure(font=("Arial Bold", 10), fg='black')
        h11.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')

    elif(under_loc==13):
        h11.configure(font=("Arial Bold", 10), fg='black')
        h12.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')

    elif(under_loc==14):
        h12.configure(font=("Arial Bold", 10), fg='black')
        b4.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')

    elif(under_loc==15):
        b4.configure(font=("Arial Bold", 10), fg='black')
        b5.configure(font=("Arial Bold", 10), fg='black')
        h13.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')

    elif(under_loc==16):
        h13.configure(font=("Arial Bold", 10), fg='black')
        h14.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')

    elif(under_loc==17):
        h14.configure(font=("Arial Bold", 10), fg='black')
        h15.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')

    elif(under_loc==18):
        h15.configure(font=("Arial Bold", 10), fg='black')
        h16.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')

    elif(under_loc==19):
        h16.configure(font=("Arial Bold", 10), fg='black')
        h17.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')

    elif(under_loc==20):
        h17.configure(font=("Arial Bold", 10), fg='black')
        h18.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')

    elif(under_loc==21):
        h18.configure(font=("Arial Bold", 10), fg='black')
        b5.configure(font=('Arial', 10, 'bold', 'underline'), fg='red')



def resetall():
    h1.configure(font=("Arial Bold", 10), fg='black')
    h2.configure(font=("Arial Bold", 10), fg='black')
    h3.configure(font=("Arial Bold", 10), fg='black')
    h4.configure(font=("Arial Bold", 10), fg='black')
    h5.configure(font=("Arial Bold", 10), fg='black')
    h6.configure(font=("Arial Bold", 10), fg='black')
    h7.configure(font=("Arial Bold", 10), fg='black')
    h8.configure(font=("Arial Bold", 10), fg='black')
    h9.configure(font=("Arial Bold", 10), fg='black')
    h10.configure(font=("Arial Bold", 10), fg='black')
    h11.configure(font=("Arial Bold", 10), fg='black')
    h12.configure(font=("Arial Bold", 10), fg='black')
    h13.configure(font=("Arial Bold", 10), fg='black')
    h14.configure(font=("Arial Bold", 10), fg='black')
    h15.configure(font=("Arial Bold", 10), fg='black')
    h16.configure(font=("Arial Bold", 10), fg='black')
    h17.configure(font=("Arial Bold", 10), fg='black')
    h18.configure(font=("Arial Bold", 10), fg='black')
    b3.configure(font=("Arial Bold", 10), fg='black')
    b4.configure(font=("Arial Bold", 10), fg='black')
    b5.configure(font=("Arial Bold", 10), fg='black')


def underlinelocation():
    global underlineposition
    global pagenumber
    if(underlineposition == 7 and pagenumber==1):
        underlineposition = 0
    elif(underlineposition==14 and pagenumber==2):
        underlineposition=7
    elif(underlineposition==21 and pagenumber==3):
        underlineposition=14
    underlineposition = underlineposition + 1
    switcher(underlineposition)
    time.sleep(1)

def swiper(headposx,headposy):
    global pagenumber
    if(headposx>45 and headposx!=999 and pagenumber>0 and pagenumber<4): #tilt head right over 1sec
        timer = True
        time.sleep(2)
        if(headposx<35 or headposx==999):
            timer= False
        if (timer == True):
            clicker()
    elif (headposx < -45 and headposx != 999 and pagenumber>0 and pagenumber<4): #tilt head left over 1sec
        timer = True
        time.sleep(1.5)
        if (headposx > -35 or headposx == 999):
            timer = False
        if(timer == True):
            underlinelocation()
    if (headposy < -15 and pagenumber>0 and pagenumber<4 and headposx>-15 and headposx<15):
        time.sleep(2)
        os.system("taskkill /im chrome.exe /f")



### Serial Communication
def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return "#err#"


portslist = []


def serial_ports():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        portNumber = find_between(str(p), " (", ")'")
        portslist.append(portNumber)
    return portslist


ser = serial.Serial()
ser.baudrate = 115200
ser.timeout = 0


def on_select(event=None):
    ser.port = Combo.get()

    try:
        ser.open()
        print(ser.name + ' is open at ' + str(ser.baudrate))
    except:
        print ("error open serial port")
        ser.close()


def Head_Tracking(Px, Py):
    global samples
    global sum_x
    global sum_y

    # Get the serial and socket checkbutton value to send the coordinatesf
    Serial_val = Serialbutton.var.get()
    Socket_val = Socketbutton.var.get()

    # Check if the face coordinate are in range
    if ((Px != 999) & (Py != 999)):

        X_HeadPos = Px
        Y_HeadPos = Py

    else:
        X_HeadPos = 999
        Y_HeadPos = 999

    if (samples == 10):
        result_x = int(sum_x / samples)
        result_y = int(sum_y / samples)

        # Display Head position coordinate on GUI
        #X_HeadPos_val.set(int(result_x))
        #Y_HeadPos_val.set(int(result_y))

        # Output buffer
        serout = ('<%+0.3d|%+0.3d>' % (result_x, result_y))

        if (Socket_val == 1):
            try:
                sock.send(serout)
            except:
                sock.close()

        if (Serial_val == 1):
            try:
                ser.write(serout)
                print(serout)
            except Exception as e:
                print ("Write exception on serial port: " + str(e))

            time.sleep(0)

        sum_x = 0
        sum_y = 0
        samples = 0

    else:

        # Only average correct values
        if ((X_HeadPos != 999) & (Y_HeadPos != 999)):
            sum_x = sum_x + X_HeadPos
            sum_y = sum_y + Y_HeadPos
            samples = samples + 1

        sum_x = sum_x
        sum_y = sum_y

    time.sleep(0.01)


def VideoCapture():
    # Get the parameters value for face tracking from GUI
    HeadMinSize_val = HeadMinSizeScaler.get()
    HeadMaxSize_val = HeadMaxSizeScaler.get()
    minNeighbors_val = minNeighborsScaler.get()
    scaleFactor_val = scaleFactorScaler.get()

    # Get the parameters value for cropping from GUI
    CroppingWidth_val = CroppingWidthScaler.get()
    CroppingHeight_val = CroppingHeightScaler.get()
    CroppingXPos_val = cropping_pos_x_def_val
    CroppingYPos_val = cropping_pos_y_def_val

    if (camera.isOpened()):

        # Read video stream from camera
        ret, frame = camera.read()

        # Set the proper cropping value
        x1 = ((cam_width - CroppingWidth_val) / 2)
        y1 = ((cam_height - CroppingHeight_val) / 2)
        x2 = (x1 + CroppingWidth_val)
        y2 = (y1 + CroppingHeight_val)

        # Crop the video frame to the new format
        crop = frame[int(y1):int(y2), int(x1):int(x2)]

        # Use cropped frame in gray mode
        frameGray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        # Display the new resolution to work with
        #cv2.putText(crop, "{}x{}".format(CroppingWidth_val, CroppingHeight_val), (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    #(220, 220, 220), 1, cv2.LINE_AA)

        # Face detection
        face = faceCascade.detectMultiScale(
            frameGray,
            scaleFactor=scaleFactor_val,
            minNeighbors=minNeighbors_val,
            minSize=(HeadMinSize_val, HeadMinSize_val),
            maxSize=(HeadMaxSize_val, HeadMaxSize_val),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Draw a rectangle around the face - detecting only one face
        if len(face) == 1:
            for (hx, hy, hw, hh) in face:
                cv2.rectangle(crop, (hx, hy), (hx + hw, hy + hh), Head_color, 2)  # Draw rectangle around the face
                headpos_x = (hx + hh / 2) - (CroppingWidth_val / 2)  # Get the Head x coordinate
                headpos_y = (CroppingHeight_val / 2) - (hy + hw / 2)  # Get the Head y coordinate
                cv2.line(crop, (hx, hy), (hx + hw, hy + hh), Overlay1_color, 1, cv2.LINE_AA)
                cv2.line(crop, (hx + hw, hy), (hx, hy + hh), Overlay1_color, 1, cv2.LINE_AA)
        else:
            # no face detected
            headpos_x = 999
            headpos_y = 999

        # Display center lines + Head position
        #cv2.line(crop, (0, int(CroppingHeight_val / 2)), (CroppingWidth_val, int(CroppingHeight_val / 2)),
                 #Overlay1_color, 1,cv2.LINE_AA)
        #cv2.line(crop, (int(CroppingWidth_val / 2), 0), (int(CroppingWidth_val / 2), CroppingHeight_val),
                 #Overlay1_color, 1,cv2.LINE_AA)
        #cv2.putText(crop, "Head Pos : x{} y{}".format(int(headpos_x), int(headpos_y)), (5, (CroppingHeight_val - 20)),
                    #cv2.FONT_HERSHEY_SIMPLEX, 0.7, Overlay2_color, 1, cv2.LINE_AA)
        #cv2.rectangle(crop, (int(CroppingWidth_val / 2) - 10, int(CroppingHeight_val / 2) - 10),
                      #(int(CroppingWidth_val / 2) + 10, int(CroppingHeight_val / 2) + 10), Overlay1_color, 1)

        # Set back the frame to color to display on GUI
        color = cv2.cvtColor(crop, cv2.COLOR_BGR2RGBA)

        # TkInter process for displaying the video
        #img = Image.fromarray(color)
        #imgtk = ImageTk.PhotoImage(image=img)
        #display1.imgtk = imgtk
        #display1.configure(image=imgtk)

        # Process the Head position
        Head_Tracking(Px=headpos_x, Py=headpos_y)

        swiper(headpos_x,headpos_y)
        coordinatesx.delete('1.0',END)
        coordinatesy.delete('1.0',END)
        coordinatesx.insert(INSERT,"x: "+ str(headpos_x))
        coordinatesy.insert(INSERT,"y: " +str(headpos_y))

    window.after(5, VideoCapture)


def HeadResetParameters():
    HeadMinSizeScaler.set(HeadMinSize_def_val)
    HeadMaxSizeScaler.set(HeadMaxSize_def_val)
    minNeighborsScaler.set(minNeighbors_def_val)
    scaleFactorScaler.set(scaleFactor_def_val)
    CroppingWidthScaler.set(cam_width)
    CroppingHeightScaler.set(cam_height)


###Control Frame
Controls = LabelFrame(imageFrame, text='Controls', font="Consolas 11 bold")
Controls.grid(row=0, column=0, rowspan=10, ipadx=5, ipady=5, sticky='nesw')

###BlankSpace
blankspace = Label(Controls)
blankspace.grid(row=0, column=0, sticky='we')

###HitBoxFrame
HitBoxFrame = LabelFrame(Controls, text='HitBox', font="Consolas 10 bold")
HitBoxFrame.grid(row=1, column=0, sticky='nesw', ipadx=5, ipady=5, columnspan=1)
Label(HitBoxFrame, text="Min Size", font="Consolas 10").grid(row=0, column=1, sticky='ws')
HeadMinSizeScaler = Scale(HitBoxFrame, from_=20, to=200, resolution=10, orient=HORIZONTAL)
HeadMinSizeScaler.grid(row=0, column=0, sticky='w')
HeadMinSizeScaler.set(HeadMinSize_def_val)
Label(HitBoxFrame, text="Max Size", font="Consolas 10").grid(row=1, column=1, sticky='ws')
HeadMaxSizeScaler = Scale(HitBoxFrame, from_=200, to=600, resolution=10, orient=HORIZONTAL)
HeadMaxSizeScaler.grid(row=1, column=0, sticky='w')
HeadMaxSizeScaler.set(HeadMaxSize_def_val)

###Cropping Frame
CroppingFrame = LabelFrame(Controls, text='Cropping', font="Consolas 10 bold")
CroppingFrame.grid(row=2, column=0, sticky='nesw', ipadx=5, ipady=5, columnspan=1)
Label(CroppingFrame, text="Width ", font="Consolas 10").grid(row=0, column=1, sticky='ws')
CroppingWidthScaler = Scale(CroppingFrame, from_=int(cam_width / 2), to=cam_width, resolution=10, orient=HORIZONTAL)
CroppingWidthScaler.grid(row=0, column=0, sticky='w')
CroppingWidthScaler.set(cropping_width_def_val)
Label(CroppingFrame, text="Height", font="Consolas 10").grid(row=1, column=1, sticky='ws')
CroppingHeightScaler = Scale(CroppingFrame, from_=int(cam_height / 2), to=cam_height, resolution=10, orient=HORIZONTAL)
CroppingHeightScaler.grid(row=1, column=0, sticky='w')
CroppingHeightScaler.set(cropping_height_def_val)

###SpecialFrame
SpecialFrame = LabelFrame(Controls, text='Special', font="Consolas 10 bold")
SpecialFrame.grid(row=3, column=0, sticky='nesw', ipadx=5, ipady=5)
Label(SpecialFrame, text="MinNeighbors", font="Consolas 10").grid(row=0, column=1, sticky='ws')
minNeighborsScaler = Scale(SpecialFrame, from_=1, to=10, orient=HORIZONTAL)
minNeighborsScaler.grid(row=0, column=0, sticky='we')
minNeighborsScaler.set(minNeighbors_def_val)
Label(SpecialFrame, text="ScaleFactor", font="Consolas 10").grid(row=1, column=1, sticky='ws')
scaleFactorScaler = Scale(SpecialFrame, from_=1.02, to=1.6, resolution=0.02, orient=HORIZONTAL)
scaleFactorScaler.grid(row=1, column=0, sticky='we')
scaleFactorScaler.set(scaleFactor_def_val)

### HeadResetbutton
HeadResetbutton = Button(Controls, width=16, height=1, text='Reset params', font="Consolas 10", fg="red",
                         command=HeadResetParameters)
HeadResetbutton.grid(row=4, column=0, padx=2, pady=2, sticky='nesw')

###BlankSpace
blankspace = Label(Controls)
blankspace.grid(row=5, column=0, sticky='we')

###SerialComFrame
SerialComFrame = LabelFrame(Controls, text='SerialCom', font="Consolas 10 bold")
SerialComFrame.grid(row=6, column=0, sticky='nesw', ipadx=5, ipady=5, columnspan=1)
Serialbutton = Checkbutton(SerialComFrame, width=20, height=1, text='Send position', font="Consolas 10",
                           variable=Serial_val)
Serialbutton.grid(row=0, column=1, sticky='ws')
Serialbutton.var = Serial_val
Serialbutton.var.set(0)
Combo = ttk.Combobox(SerialComFrame, width=10, values=serial_ports())
Combo.grid(row=0, column=0, sticky='ws')
Combo.set("none")

###SocketFrame
SocketFrame = LabelFrame(Controls, text='SocketCom', font="Consolas 10 bold")
SocketFrame.grid(row=7, column=0, sticky='nesw', ipadx=5, ipady=5, columnspan=1)
Socketbutton = Checkbutton(SocketFrame, width=20, height=1, text='Send position', font="Consolas 10",
                           variable=Socket_val)
Socketbutton.grid(row=0, column=1, sticky='ws')
Socketbutton.var = Socket_val
Socketbutton.var.set(0)

### CameraFrame
CameraFrame = LabelFrame(imageFrame, width=cam_width, height=cam_height)
CameraFrame.grid(row=2, column=1, padx=5, pady=5, columnspan=2)
imagePreviewFrame = tk.Frame(CameraFrame, width=cam_width, height=cam_height)
imagePreviewFrame.grid(padx=5, pady=5, sticky='nesw')
imagePreviewFrame.grid_propagate(0)
display1 = tk.Label(imagePreviewFrame)
display1.grid(row=0, column=0, sticky='nesw')
display1.place(in_=imagePreviewFrame, anchor="c", relx=.5, rely=.5)

###HeadBox Frame
HeadBoxFrame = LabelFrame(imageFrame, text='HeadBox Position', font="Consolas 11 bold")
HeadBoxFrame.grid(row=0, column=1, columnspan=2, sticky='nesw')
Label(HeadBoxFrame, text=" X =", font="Consolas 12 bold").grid(row=0, column=0, sticky=W)
Label(HeadBoxFrame, text=" Y =", font="Consolas 12 bold").grid(row=1, column=0, sticky=W)
Label(HeadBoxFrame, textvariable=X_HeadPos_val, font="Consolas 12 bold").grid(row=0, column=1, sticky=W)
Label(HeadBoxFrame, textvariable=Y_HeadPos_val, font="Consolas 12 bold").grid(row=1, column=1, sticky=W)


# When closing application
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        sock.close()
        camera.release()
        time.sleep(1)
        cv2.destroyAllWindows()
        window.destroy()




Combo.bind('<<ComboboxSelected>>', on_select)
window.protocol("WM_DELETE_WINDOW", on_closing)
VideoCapture()  # Face recognition
window.mainloop()  # Starts GUI
