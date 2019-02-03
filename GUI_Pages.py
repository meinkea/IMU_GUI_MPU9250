import threading

import tkinter as tk
from tkinter import ttk

import hardwareSetting_TABS


class IMU_Setup(tk.Frame):  #Input parameters for simulation page
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # NB >> SETUP and SETTINGS
        Setup_NB = ttk.Notebook(self)
        Setup_NB.pack(expand=1, fill="both")
        
        # TAB >> HARDWARE SETTINGS- init
        hardware_F = ttk.Frame(Setup_NB)
        Setup_NB.add(hardware_F, text=' Hardware ')
        ###
        ### SENSOR SELECTION
        ### NB >> Sensors Type
        hardwareSet_NB = ttk.Notebook(hardware_F) # Create
        hardwareSet_NB.grid(row=0, column=0, padx=5, pady=5) # Place
        ###
        ### - for Accel
        setAcl_Tab = hardwareSetting_TABS.aclSetTab(hardwareSet_NB, self) # Create
        hardwareSet_NB.add(setAcl_Tab, text='Accelerometer') # Place
        ###
        ### - for Gyro
        setGry_Tab = ttk.Frame(hardwareSet_NB) # Create
        hardwareSet_NB.add(setGry_Tab, text='Gyroscope') # Place
        ###
        ### - for Mag
        setMag_Tab = ttk.Frame(hardwareSet_NB) # Create
        hardwareSet_NB.add(setMag_Tab, text='Magnotometer') # Place
        ###
        ### - for GPS
        setGps_Tab = ttk.Frame(hardwareSet_NB) # Create
        hardwareSet_NB.add(setGps_Tab, text='GPS') # Place
        #
        # DIVIDEOR
        setDivide = ttk.Separator(hardware_F, orient="vertical")
        setDivide.grid(row=0, column=1, sticky=tk.N+tk.S)
        #
        ### SENSOR VISULIZERS
        ### NB >> Sensors Visuals
        hardwareVis_NB = ttk.Notebook(hardware_F) # Create
        hardwareVis_NB.grid(row=0, column=2, padx=5, pady=5) # Place
        ###
        ### StripChart
        stripChart_Tab = hardwareSetting_TABS.stripChartTab(hardwareVis_NB, self) # Create
        #print("In page: ")
        #print(stripChart_Tab)
        self.sc = stripChart_Tab.sc # link
        hardwareVis_NB.add(stripChart_Tab, text='StripChart') # Add
        ###
        ### 3D Cube
        Cube3D_Tab = hardwareSetting_TABS.cube3DTab(hardwareVis_NB, self, parent) # Create
        hardwareVis_NB.add(Cube3D_Tab, text='3D Cube') # Add
        
        

class pageDiag(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        LARGE_FONT = ("Verdana", 14)
        MED_FONT = ("Verdana", 12, 'bold')

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

        

class pageBlank(tk.Frame):#Input parameters for simulation page
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

