from tkinter import *
from tkinter.ttk import Combobox
from tkinter.scrolledtext import ScrolledText
from tkinter import IntVar, messagebox
import calc

VERSION="0.1.0"
HEIGHT=650
WIDTH=500

MSG_ERROR='ERROR'
MSG_INFO='INFO'
MSG_WARN='WARN'
NORMAL='normal'
DISABLED='disabled'


class emfPage(Frame):
    def addY(self, y):
        return y+0.065
    def resetErrorLabel(self):
        self.info3Label.config(text="")
        self.info3Label.configure(background=self.orig_color)
    def setErrorLabel(self,errorText):
        self.info3Label.config(text=errorText)
        self.info3Label.config(bg="yellow", fg="red")           
    def calculate(self, controller):

        self.resetErrorLabel()

        try:
            pwr=controller.powerVar.get()
        except:
            self.setErrorLabel("Power value must be a number.")
            return

        try:
            fre=controller.freqVar.get()
        except:
            self.setErrorLabel("Frequency value must be a number.")
            return

        dist = calc.calculateEMF(pwr,fre)

        if dist<0:
            controller.distVar.set(0)
            if dist==-10:
                self.setErrorLabel("Enter a value of 10MHz or more")
            elif dist==-300000:
                self.setErrorLabel("Enter a value less than 300,001MHz")
                
        else:
            controller.distVar.set(dist)

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
       
        self.controller = controller
        relh = 0.05
        fontsize=16

        labelfont = ('TkDefaultFont', 12)
        titlefont = ('TkDefaultFont', 18)
        
        y=0.14
        titleLabel = Label(self, text="EMF Calculator")
        titleLabel.place(relx=0.05, relwidth=0.9,relheight=0.12)
        titleLabel.config(font=titlefont)           
        
        y=self.addY(y)

        powerLabel = Label(self, text="Tx Power EIRP (Watts)", anchor="e")
        powerLabel.place(relx=0.05, rely=y,relwidth=0.4)
        powerLabel.config(font=labelfont)           
        

        self.powerEntry = Entry(self, font=40, textvariable=controller.powerVar, justify='center')
        self.powerEntry.place(relx=0.5,rely=y, relwidth=0.48,relheight=relh)
        self.powerEntry.config(state=NORMAL)
       
        y=self.addY(y)
        
        freqLabel = Label(self, text="Frequency (MHz)", anchor="e")
        freqLabel.place(relx=0.05, rely=y,relwidth=0.4)
        freqLabel.config(font=labelfont)           
        
        self.freqEntry = Entry(self, font=40, textvariable=controller.freqVar, justify='center')
        self.freqEntry.place(relx=0.5,rely=y, relwidth=0.48,relheight=relh)
        self.freqEntry.config(state=NORMAL)
        
        y=self.addY(y)

        self.saveButton = Button(self, text="Calculate", command=lambda:self.calculate(controller), bg="white", font=30)
        self.saveButton.place(relx=0.3,rely=y,relwidth=0.48,relheight=relh)
        
        y=self.addY(y)

        distLabel = Label(self, text="Separation Distance", anchor="e")
        distLabel.place(relx=0.05, rely=y,relwidth=0.4)
        distLabel.config(font=labelfont)           
        
        self.distEntry = Entry(self, font=40, textvariable=controller.distVar, justify='center')
        self.distEntry.place(relx=0.5,rely=y, relwidth=0.48,relheight=relh)
        self.distEntry.config(state=NORMAL)
        
        y=self.addY(y)
        
        y=self.addY(y)

        infoLabel = Label(self, text="Calculation based on the", anchor="center")
        infoLabel.place(relx=0.05, rely=y,relwidth=0.9)
        infoLabel.config(font=labelfont)           
        
        y = y+0.04

        info1Label = Label(self, text="OFCOM EMF Calucation Spreadsheet v 0.1.2", anchor="center")
        info1Label.place(relx=0.05, rely=y,relwidth=0.9)
        info1Label.config(font=labelfont)           
        
        y = y+0.04

        info2Label = Label(self, text="Enter Frequency from 10MHz to 300,000MHz", anchor="center")
        info2Label.place(relx=0.05, rely=y,relwidth=0.9)
        info2Label.config(font=labelfont)           

        y = y+0.04

        self.info3Label = Label(self, text="", anchor="center")
        self.info3Label.place(relx=0.05, rely=y,relwidth=0.9)
        self.info3Label.config(font=labelfont)
        self.orig_color = self.info3Label.cget("background")

class App(Tk):
    def addY(self, y):
        return y+0.065
    
    def ask_quit(self):
            
        print('Exiting. Thanks for using EMF Calculator By M0IAX')
        self.destroy()  

    def showMessage(self, messagetype, messageString):
        if messagetype==MSG_ERROR:
            messagebox.showerror("Error", messageString)
        elif messagetype==MSG_WARN:
            messagebox.showwarning("Warning",messageString)
        elif messagetype==MSG_INFO:
            messagebox.showinfo("Information",messageString)
    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        self.geometry(str(WIDTH)+"x"+str(HEIGHT))
        self.title("EMF Calculator M0IAX v"+VERSION)
        
        self.powerVar = IntVar()
        self.freqVar = IntVar()
        self.distVar = IntVar()

        self.powerVar.set(10)
        self.freqVar.set(145)

        self.seq=1

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (emfPage, emfPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            
        self.show_frame(emfPage)

try:

    app = App()
    app.protocol("WM_DELETE_WINDOW", app.ask_quit)
    app.mainloop()
    
finally:
    print('End of line')

