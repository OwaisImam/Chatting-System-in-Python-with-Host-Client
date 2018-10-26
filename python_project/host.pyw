import threading
from ChatFns import *
import win32com.client as stephen
import speech_recognition as sr
r = sr.Recognizer()

speak = stephen.Dispatch("SAPI.SpVoice")


#---------------------------------------------------#
#---------INITIALIZE CONNECTION VARIABLES-----------#
#---------------------------------------------------#
#Initiate socket and bind port to host PC
WindowTitle = 'JChat v0.1 - Host'
s = socket(AF_INET, SOCK_STREAM)
HOST = '192.168.0.106'
PORT = 8011
conn = ''
s.bind((HOST, PORT))



#---------------------------------------------------#
#------------------ MOUSE EVENTS -------------------#
#---------------------------------------------------#
def ClickAction():
    #Write message to chat window
    EntryText = FilteredMessage(EntryBox.get("0.0",END))
    LoadMyEntry(ChatLog, EntryText)

    #Scroll to the bottom of chat windows
    ChatLog.yview(END)

    #Erace previous message in Entry Box
    EntryBox.delete("0.0",END)
            
    #Send my mesage to all others
    conn.sendall(bytes(EntryText.encode("UTF-8")))

def VoiceAction():
        # Write message to chat window
        with sr.Microphone() as source:
            print('Say Something!')
            audio = r.listen(source)
        try:
            EntryText = r.recognize_google(audio)
            EntryBox.insert("0.0", EntryText)
        except:
            pass

	
#---------------------------------------------------#
#----------------- KEYBOARD EVENTS -----------------#
#---------------------------------------------------#
def PressAction(event):
	EntryBox.config(state=NORMAL)
	ClickAction()
def DisableEntry(event):
	EntryBox.config(state=DISABLED)

    


#---------------------------------------------------#
#-----------------GRAPHICS MANAGEMENT---------------#
#---------------------------------------------------#

#Create a window
base = Tk()
base.title(WindowTitle)
base.geometry("500x500")
base.resizable(width=FALSE, height=FALSE)

#Create a Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.insert(END, "Waiting for your partner to connect..\n")
ChatLog.config(state=DISABLED)

#Bind a scrollbar to the Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create the Button to send message
SendButton = Button(base, font=30, text="Send", width="12", height=5,
                    bd=0, bg="#FFBF00", activebackground="#FACC2E",
                    command=ClickAction)
#Create the Voice Button to send message
VoiceButton = Button(base, font=30, text="Voice", width="10", height=5,
                    bd=0, bg="#FF0000", activebackground="#FF4d4d",
                    command=VoiceAction)

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
EntryBox.bind("<Return>", DisableEntry)
EntryBox.bind("<KeyRelease-Return>", PressAction)

#Place all components on the screen
scrollbar.place(x=476,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=470)
EntryBox.place(x=203, y=401, height=90, width=290)
SendButton.place(x=6, y=401, height=90)
VoiceButton.place(x=100, y=401, height=90)


#---------------------------------------------------#
#----------------CONNECTION MANAGEMENT--------------#
#---------------------------------------------------#
def GetConnected():
    s.listen(1)
    global conn
    conn, addr = s.accept()
    LoadConnectionInfo(ChatLog, 'Connected with: ' + str(addr)+'\n---------------------------------------------------------------')
    
    while 1:
        try:
            data = conn.recv(1024)
            LoadOtherEntry(ChatLog, data)
            if base.focus_get() == None:
                FlashMyWindow(WindowTitle)
                playsound('notif.wav')
        except:
            LoadConnectionInfo(ChatLog, '\n [ Your partner has disconnected ]\n [ Waiting for him to connect..] \n  ')
            GetConnected()

    conn.close()
    
threading._start_new_thread(GetConnected,())

base.mainloop()

