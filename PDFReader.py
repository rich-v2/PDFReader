from tkinter import *
from PIL import ImageTk, Image
import pyttsx3
import threading
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTFigure, LTTextBox
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser
import re
import os

root = Tk(className="pdfReader")
root.title = "PDFReader"

WIDTH, HEIGHT = 800, 500
VAR = StringVar()
VAR.set("English")

BACKGROUND_FRAME = "#660101"
BACKGROUND_BUTTON = "black"
FOREGROUND_BUTTON = "white"

class Speaking(threading.Thread):
    def __init__(self, sentence, **kw):
        super().__init__(**kw)
        sentence = " ".join(sentence.split())
        self.words = sentence.split(".")
        self.paused = False

    def run(self):
        self.running = True
        while self.words and self.running:
            if not self.paused:
                word = self.words.pop(0)
                engine.say(word)
                engine.runAndWait()
        self.running = False

    def stop(self):
        self.running = False

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

speak = None

def read():
    global speak
    if speak is None or not speak.running:
        speak = Speaking(text_box.get(1.0, END), daemon=True)
        speak.start()

def stop():
    global speak
    if speak:
        speak.stop()
        speak = None

def pause():
    if speak:
        speak.pause()

def unpause():
    if speak:
        speak.resume()

def sel_lang(var):
    voices = engine.getProperty('voices')
    for voice in voices:
        if var == "English" and re.search("English", voice.name):
            engine.setProperty('voice', voice.id)
            label_german.place_forget()
            label_english.place(relx=0,rely = 0.7, relwidth=0.25,relheight=0.25)
            break
        if var == "German" and re.search("German", voice.name):
            engine.setProperty('voice', voice.id)
            label_english.place_forget()
            label_german.place(relx=0.75,rely = 0.7, relwidth=0.25,relheight=0.25)
            break


def open_file(filename,pageNum):
    text = ""
    stack = []

    rng = pageNum.split("-")
    if len(rng) == 2:
        first,last = [int(x) for x in rng]
        first -= 1

        with open(filename + ".pdf", 'rb') as f:
            parser = PDFParser(f)
            doc = PDFDocument(parser)
            pages = list(PDFPage.create_pages(doc))[first:last]
            for p in pages:
                rsrcmgr = PDFResourceManager()
                device = PDFPageAggregator(rsrcmgr, laparams=LAParams())
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                interpreter.process_page(p)
                layout = device.get_result()

                for obj in layout:
                    if isinstance(obj, LTTextBox):
                        text += obj.get_text()

                    elif isinstance(obj, LTFigure):
                        stack += list(obj)
    
        text_box.insert(END, text)

    elif len(rng) == 1:
        try:
            pageNum = int(rng[0]) -1 

            with open(filename + ".pdf", 'rb') as f:
                parser = PDFParser(f)
                doc = PDFDocument(parser)
                page = list(PDFPage.create_pages(doc))[pageNum]
                rsrcmgr = PDFResourceManager()
                device = PDFPageAggregator(rsrcmgr, laparams=LAParams())
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                interpreter.process_page(page)
                layout = device.get_result()

                for obj in layout:
                    if isinstance(obj, LTTextBox):
                        text += obj.get_text()

                    elif isinstance(obj, LTFigure):
                        stack += list(obj)
            
            text_box.insert(END, text)
        except Exception:
            with open(filename + ".pdf", 'rb') as f:
                parser = PDFParser(f)
                doc = PDFDocument(parser)
                pages = list(PDFPage.create_pages(doc))
                for p in pages:
                    rsrcmgr = PDFResourceManager()
                    device = PDFPageAggregator(rsrcmgr, laparams=LAParams())
                    interpreter = PDFPageInterpreter(rsrcmgr, device)
                    interpreter.process_page(p)
                    layout = device.get_result()

                    for obj in layout:
                        if isinstance(obj, LTTextBox):
                            text += obj.get_text()

                        elif isinstance(obj, LTFigure):
                            stack += list(obj)
        
            text_box.insert(END, text)




engine = pyttsx3.init()

canvas = Canvas(root, width = WIDTH, height = HEIGHT)
canvas.pack()

background = ImageTk.PhotoImage(Image.open(os.path.join("Assets","library.jpg")))  # PIL solution
label_background = Label(root, image=background)
label_background.place(relx=0.5, relwidth=1,relheight=1, anchor = "n")

frame_1 = Frame(root, bg = BACKGROUND_FRAME, bd = 5)
frame_1.place(relx = 0.5, rely = 0, relwidth = 0.8, relheight = 0.6, anchor = "n")
text_box = Text(frame_1, font="consolas 14",bd=5, wrap=WORD)
text_box.insert(END, "Welcome to the library.\n\nOur employees would be happy to read something to you.\n" + \
    "You can paste text in this entry field, or use the form below to load a pdf file.\n\n" +\
        "Just locate the file in the same directory and supply the librarian with the filename " \
            "and the range of pages.\nIf you don't say anything, all will be read.\n\n" + \
        "If your desired reading material is loaded, just hit the 'Read aloud' button and listen " + \
            "to our soothing voices.")
scrollb = Scrollbar(frame_1, command = text_box.yview)
scrollb.place(relx = 0.975,relwidth = 0.025,relheight=1)
text_box['yscrollcommand'] = scrollb.set
text_box.place(relwidth = 0.975, relheight=1)

frame_3 = Frame(root, bg = BACKGROUND_FRAME, bd = 5)
frame_3.place(relx = 0.5, rely = 0.65, relwidth = 0.5, relheight = 0.15, anchor="n")
open_button = Button(frame_3, text="Open File", bg = BACKGROUND_BUTTON, fg=FOREGROUND_BUTTON, command= lambda:open_file(entry_1.get(),entry_2.get()))
open_button.place(relx=0.6, rely = 0.5, relwidth=0.4,relheight=0.4)
label_1 = Label(frame_3, bg = BACKGROUND_BUTTON, text = "Filename", fg=FOREGROUND_BUTTON)
label_1.place(relwidth=0.2,relheight=0.4)
entry_1 = Entry(frame_3)
entry_1.place(relx=0.2,relwidth=0.8,relheight=0.4)
label_2 = Label(frame_3, text = "Pages",bg = BACKGROUND_BUTTON, fg=FOREGROUND_BUTTON)
label_2.place(relx=0, rely = 0.5, relwidth=0.2,relheight=0.4)
entry_2 = Entry(frame_3)
entry_2.place(relx=0.2, rely = 0.5, relwidth=0.2,relheight=0.4)
clear_button = Button(frame_3, text = "Clear", command=lambda: text_box.delete('1.0',END),bg = BACKGROUND_BUTTON, fg=FOREGROUND_BUTTON)
clear_button.place(relx=0.4, rely = 0.5, relwidth=0.2,relheight=0.4)

frame_2 = Frame(root, bg = "#660101", bd = 5)
frame_2.place(relx=0.5, rely = 0.8, relwidth = 0.5, relheight=0.1, anchor = "n")

read_button = Button(frame_2, text="Read aloud", command=read,bg = BACKGROUND_BUTTON, fg=FOREGROUND_BUTTON)
read_button.place(relx=0,rely=0,relwidth=0.25,relheight=1)

pause_button = Button(frame_2, text="Pause", command=pause,bg = BACKGROUND_BUTTON, fg=FOREGROUND_BUTTON)
pause_button.place(relx=0.25,rely=0,relwidth=0.25, relheight=1)

unpause_button = Button(frame_2, text="Unpause", command=unpause,bg = BACKGROUND_BUTTON, fg=FOREGROUND_BUTTON)
unpause_button.place(relx=0.5,rely=0,relwidth=0.25,relheight=1)

stop_button = Button(frame_2, text="Stop", command=stop,bg = BACKGROUND_BUTTON, fg=FOREGROUND_BUTTON)
stop_button.place(relx=0.75,rely=0,relwidth=0.25,relheight=1)

frame_4 = Frame(root, bg = BACKGROUND_FRAME, bd = 5)
frame_4.place(relx = 0.5, rely = 0.9, relwidth = 0.5, relheight = 0.1, anchor= "n")
label_3 = Label(frame_4, text = "Language",bg = BACKGROUND_BUTTON, fg=FOREGROUND_BUTTON)
label_3.place(relwidth=0.25,relheight=1)
radio_1 = Radiobutton(frame_4,text = "English", variable=VAR, value = "English")
radio_1.place(relx=0.25,relwidth=0.25,relheight=1)
radio_2 = Radiobutton(frame_4,text = "German", variable=VAR, value = "German")
radio_2.place(relx=0.5,relwidth=0.25,relheight=1)
language_button = Button(frame_4,text ="Apply", command=lambda: sel_lang(VAR.get()),bg = BACKGROUND_BUTTON, fg=FOREGROUND_BUTTON)
language_button.place(relx=0.75,relwidth=0.25,relheight=1)


german = ImageTk.PhotoImage(Image.open(os.path.join("Assets","german.jpg")))  # PIL solution
label_german = Label(root, image=german)


english = ImageTk.PhotoImage(Image.open(os.path.join("Assets","Freeman.jpg")))  # PIL solution
label_english = Label(root, image=english)

voices = engine.getProperty('voices')
for voice in voices:
    if re.search("English", voice.name):
        engine.setProperty('voice', voice.id)
        label_german.place_forget()
        label_english.place(relx=0,rely = 0.7, relwidth=0.25,relheight=0.25)
        break

if __name__== "__main__":
    mainloop()
