from GUI_Pages import *

import tkinter as tk
from tkinter import ttk

import CUBE

# Fonts
LARGE_FONT = ("Verdana", 14)
MED_FONT = ("Verdana", 12, 'bold')

# Global variables for window merging control
Xm = 0
Ym = 0


class EARTH(tk.Tk):  # The hackFF2E class is inheriting from the class Tk from tk (tkinter)
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        #Window Modifications
        self.wm_attributes('-type', 'splash')

        self.task_bar = tk.Frame(self)
        self.grip = tk.Label(self.task_bar, width=650, bitmap="gray25")
        self.grip.grid(row=0, column=0)
        
        self.bind("<ButtonPress-1>", self.StartMove)
        self.bind("<ButtonRelease-1>", self.StopMove)
        self.bind("<B1-Motion>", self.OnMotion)

        exitB = tk.Button(self.task_bar, text="X", command=self.destroy)
        exitB.grid(row=0, column=1)
        self.task_bar.pack(side="top", fill="x", expand=True)
        
        # --- Containment System ---
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        #container.grid()

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # This is a dictionary for all page frames
        # All pages require two parameters:
        #   1 - a widget that will be the parent of this class,
        #   2 - An object that will server as a controller
        #       (a term borrowed from the UI patter model/view/controller)

        # Populate dictionary
        for F in (pageDiag, IMU_Setup, pageBlank):  # F now represents page class on each iter
            frame = F(self.container, self) # Creates the page object from F page class
            #print(frame) 
            self.frames[F] = frame  # Save page to dictionary.  Key is F or class name
            frame.grid(row=0, column=0, sticky="nsew")  # Places page in container

        self.container.X = 0 # Main window X position (for later use)
        self.container.Y = 0 # Main window Y position (for later use)

        self.show_frame(IMU_Setup)  # StartPage
        
    
    #MAIN CONTROLLER#
    def show_frame(self, cont):  # cont is container controller
        while True:
            try:
                if cont == pageDiag:
                    theStage.geometry("300x150")
            finally:
                break
            print('resizing')
        frame = self.frames[cont]
        frame.tkraise()

    
    def StartMove(self, event):
        self.x = event.x
        self.y = event.y
        # To stop graphs
        (self.frames[IMU_Setup]).sc.mech.Stop()
        # To stop Visulizer
        for t in threading.enumerate():
            if t.getName() == '_cube_':
                global cubeW
                CUBE.cubeW.CubeStop((self.frames[IMU_Setup]).visBQuit)
        

    def StopMove(self, event):
        print(self.container.X)
        print(self.container.Y)
        self.x = None
        self.y = None


    def OnMotion(self, event):
        try:
            deltax = event.x - self.x
            deltay = event.y - self.y
            self.container.X = self.winfo_x() + deltax
            self.container.Y = self.winfo_y() + deltay
            self.geometry("+%s+%s" % (self.container.X, self.container.Y))
        except:
            print("Error occured!")
       


# Lauch GUI Thread
def mainguiTh():
    theStage = EARTH()
    theStage.tk_setPalette(background='LightSteelBlue4')#878685
    theStage.geometry("775x450+" + str(Xm) + "+" + str(Ym))
    theStage.mainloop()


mainTkTh = threading.Thread(target=mainguiTh, name='_tkMain_')
mainTkTh.start()
mainTkTh.join()

