import spidev
import tkinter as tk


LARGE_FONT = ("Verdana", 14)
MED_FONT = ("Verdana", 12, 'bold')

class HTRAE(tk.Tk):  # The hackFF2E class is inheriting from the class Tk from tk (tkinter)
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        #container.grid()

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # This is a dictionary for all the frames
        for F in (pageDiag, pageBlank):  # Save pages to dictionary (above)
            frame = F(container, self)
            self.frames[F] = frame  # No idea, it just works
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(pageDiag)  # StartPage
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



class pageBlank(tk.Frame):#Input parameters for simulation page
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


class pageDiag(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="Address", font=LARGE_FONT, foreground='#ffffff').grid(row=0, column=0, pady=4)
        tk.Label(self, text="Data", font=LARGE_FONT, foreground='#ffffff').grid(row=0, column=1, pady=4)

        addressE = tk.Entry(self, width=10, font=LARGE_FONT, bg="#ffffff", fg="white")
        addressE.grid(row=1, column=0, padx=5, pady=5)
        
        dataE = tk.Entry(self, width=10, font=LARGE_FONT, bg="#ffffff", fg="white")
        dataE.grid(row=1, column=1, padx=5, pady=5)

        adr = tk.IntVar()
        adr.set("0")

        addressE.bind('<Return>', lambda event: runReadDATA(addressE, dataE, adr.get()))
        addressE.bind('<KP_Enter>', lambda event: runReadDATA(addressE, dataE, adr.get()))
        dataE.bind('<Return>', lambda event: runWriteDATA(addressE, dataE, adr.get()))
        dataE.bind('<KP_Enter>', lambda event: runWriteDATA(addressE, dataE, adr.get()))

        readB = tk.Button(self, text="READ", foreground='#ffffff', bg='#454444', background='#454444', command=lambda: readDATA(addressE, dataE, adr.get()))
        readB.grid(row=2, column=0, padx=5, pady=5)
        sendB = tk.Button(self, text="SEND", foreground='#ffffff', bg='#454444', background='#454444', command=lambda: writeDATA(addressE, dataE, adr.get()))
        sendB.grid(row=2, column=1, padx=5, pady=5)
       
        imuRB0 = tk.Radiobutton(self, text="IMU 0", variable=adr, value=0, font=MED_FONT, fg='SteelBlue1')
        imuRB0.grid(row=3, column=0)
        imuRB1 = tk.Radiobutton(self, text="IMU 1", variable=adr, value=1, font=MED_FONT, fg='SteelBlue1')
        imuRB1.grid(row=3, column=1)


def readDATA(addressE, dataE, adr):
    Address = int(addressE.get())
    dataE.delete(0, tk.END)
    
    spi = spidev.SpiDev()
    spi.open(0, int(adr))
    spi.max_speed_hz = 500000
    spi.mode = 3
    spi.cshigh = False
    
    readCommand = 0x80
    
    Data = []

    L = [0x80+Address, 0x80+0]
    Data = spi.xfer(L)

    print("Read Success (" + str(Address) + "): " + str(Data[1]))
    
    dataE.insert(0, "{0:08b}".format(Data[1]))
    
    spi.close()


def runReadDATA(addressE, dataE, adr):
    readDATA(addressE, dataE, adr)


def writeDATA(addressE, dataE, adr):
    wAddress = int(addressE.get())
    wData = int(dataE.get(), 2)
    #print(wData)
    
    spi = spidev.SpiDev()
    spi.open(0, int(adr))
    spi.max_speed_hz = 500000
    spi.mode = 3
    spi.cshigh = False
    
    Data = []
    l = [wAddress, wData]
    Data = spi.xfer(l)
    #print(Data)
    
    checkData = []
    checkL = [0x80+wAddress, 0x80+0]
    checkData = spi.xfer(checkL)
    #print(checkData)
    
    if wData == checkData[1]:
        print("Write Success (" + str(wAddress) + "): " + str(wData))
    else:
        print("Write Failed")
    
    spi.close()
    

def runWriteDATA(addressE, dataE):
    writeDATA(addressE, dataE)



theStage = HTRAE()
theStage.wm_title("MPU9250 Utility")
theStage.geometry("275x145")
theStage.tk_setPalette(background='LightSteelBlue4')#878685
#ani = animation.FuncAnimation(f, animate, interval=1000)#First send to figure; what to run, interval time) ~ this is for live graphs
theStage.mainloop()
