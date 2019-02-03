import tkinter as tk
from tkinter import ttk
import tkinterExtras as tke
import CUBE


class aclSetTab(ttk.Frame):
    def __init__(self, parent, page):
        ttk.Frame.__init__(self, parent) # Parent is the Notebook
        # self -> page
        # setAcl -> Self
        
        r=0
        # Full Scale and Resolution
        r +=1
        aclFilterLab = tk.Label(self, text="FULL SCALE & RESOLUTION")
        aclFilterLab.grid(row=r, column=0, columnspan=2, sticky=tk.W)
        
        # Full Scale Select
        r +=1
        aclFSclLab = tk.Label(self, text="Scl | Res:")
        aclFSclLab.grid(row=r, column=0, sticky=tk.E)

        aclFScl_L = (' ±2g | 0.00003051804g',
                     ' ±4g | 0.00006103608g',
                     ' ±8g | 0.00012207217g',
                     '±16g | 0.00024414435g')
        aclFScl_s = tk.StringVar(page)
        aclFScl_s.set(' ±2g | 0.00003051804g')
        aclFScl_W = tk.OptionMenu(self, aclFScl_s, *aclFScl_L)
        aclFScl_W.grid(row=r, column=1, columnspan=3, sticky=tk.W)
        
        # Calibration
        r +=1
        aclFilterLab = tk.Label(self, text="FILTER")
        aclFilterLab.grid(row=r, column=0, columnspan=2, sticky=tk.W)
        
        # Filter Type
        r +=1
        aclFilTypLab = tk.Label(self, text="Type:")
        aclFilTypLab.grid(row=r, column=0, sticky=tk.E)

        aclFilTyp_L = ('DEC1', 'DEC2', 'DLPF', 'DISABLE')
        aclFilTyp_s = tk.StringVar(page)
        aclFilTyp_s.set('DLPF')
        aclFilTyp_W = tk.OptionMenu(self, aclFilTyp_s, *aclFilTyp_L)
        aclFilTyp_W.grid(row=r, column=1, columnspan=4, sticky=tk.W)
        
        # Filter Config
        r +=1
        aclFilCfgLab = tk.Label(self, text="Config:")
        aclFilCfgLab.grid(row=r, column=0, sticky=tk.E)
        aclFilCfg_L = ('1,046    |  0.503 | 300',
                       '  218.1  |  1.88  | 300',
                       '   99.0  |  2.88  | 300',
                       '   48.8  |  4.88  | 300',
                       '   21.2  |  8.87  | 300',
                       '   10.2  | 16.83  | 300',
                       '    5.05 | 32.48  | 300',
                       '  420.   |  1.38  | 300')
        aclFilCfg_s = tk.StringVar(page)
        aclFilCfg_s.set('1,046    |  0.503 | 300')
        aclFilCfg_W = tk.OptionMenu(self, aclFilCfg_s, *aclFilCfg_L)
        aclFilCfg_W.grid(row=r, column=1, columnspan=4, sticky=tk.W)
        
        # Calibration
        r +=1
        aclCalibrationLab = tk.Label(self, text="CALIBRATION")
        aclCalibrationLab.grid(row=r, column=0, columnspan=2, sticky=tk.W)
        
        # Calibration Mode
        r +=1
        aclCalMdeLab = tk.Label(self, text="Mode:")
        aclCalMdeLab.grid(row=r, column=0, sticky=tk.E)
        
        aclCalMde_L = ('Auto', 'Hybrid', 'Manual')
        aclCalMde_i = tk.IntVar(page)
        aclCalMde_i.set(1)
        aclCalMde_W = []
        for i, name in enumerate(aclCalMde_L, 0):
            aclCalMde_W.append(tk.Radiobutton(self, variable=aclCalMde_i, value=i, text=name))
            aclCalMde_W[i].config(padx=5, pady=5, width=10, selectcolor='#279989', indicatoron=0)
            aclCalMde_W[i].grid(row=r, column=i+1, sticky=tk.N+tk.S+tk.E+tk.W)
        
        # Calibrate
        r +=1
        
        aclCalibrate = tk.Button(self, text="Calibrate")
        aclCalibrate.grid(row=r, column=1)
        
        aclCalSam_L = tk.Label(self, text="Samples:")
        aclCalSam_L.grid(row=r, column=2, sticky=tk.E)
        
        aclCalParSam_i = tk.IntVar(page)
        aclCalParSam_i.set('10000')
        aclCalParSam_W = tk.Entry(self, textvariable=aclCalParSam_i)
        aclCalParSam_W.config(width=10)
        aclCalParSam_W.grid(row=r, column=3, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)
        
        # Calibration Progress Bar
        r +=1
        aclCalPrgLab = tk.Label(self, text="Progress:")
        aclCalPrgLab.grid(row=r, column=0, sticky=tk.E)
        
        aclCalPrg = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=300, mode="determinate")
        aclCalPrg.grid(row=r, column=1, columnspan=3, padx=5, pady=5)
        aclCalPrg['value']=50
        
        # Calibration AXIS Labels
        r +=1
        aclCalParALab = tk.Label(self, text='Axis:')
        aclCalParALab.grid(row=r, column=0, sticky=tk.E)
        
        aclCalAxiLbl_L = ('X', 'Y', 'Z')
        aclCalAxiLbl_W = []
        for i, name in enumerate(aclCalAxiLbl_L, 0):
            aclCalAxiLbl_W.append(tk.Label(self, text=aclCalAxiLbl_L[i]))
            aclCalAxiLbl_W[i].grid(row=r, column=i+1)
        
        # Calibration Parameters AUTO
        r +=1
        aclCalParALab = tk.Label(self, text='Auto:')
        aclCalParALab.grid(row=r, column=0, sticky=tk.E)
        
        aclCalParA_s = []
        aclCalParA_W = []
        for i, name in enumerate(aclCalAxiLbl_L, 0):
            aclCalParA_s.append(tk.StringVar(page))
            aclCalParA_s[i].set('0.0000000')
            aclCalParA_W.append(tk.Entry(self, textvariable=aclCalParA_s[i]))
            aclCalParA_W[i].config(width=10)
            aclCalParA_W[i].grid(row=r, column=i+1, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)
        
        # Calibration Parameters MANUAL
        r +=1
        aclCalParMLab = tk.Label(self, text='Man:')
        aclCalParMLab.grid(row=r, column=0, sticky=tk.E)
        
        aclCalParM_s = []
        aclCalParM_W = []
        for i, name in enumerate(aclCalAxiLbl_L, 0):
            aclCalParM_s.append(tk.StringVar(page))
            aclCalParM_s[i].set('0.0000000')
            aclCalParM_W.append(tk.Entry(self, textvariable=aclCalParM_s[i]))
            aclCalParM_W[i].config(width=10)
            aclCalParM_W[i].grid(row=r, column=i+1, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)
        
        # Apply/Reset
        r +=1
        aclCalibrate = tk.Button(self, text='APPLY')
        aclCalibrate.grid(row=r, column=1)
        aclCalibrate = tk.Button(self, text='RESET')
        aclCalibrate.grid(row=r, column=3)


class setGryTab(ttk.Frame):
    def __init__(self, parent, page):
        ttk.Frame.__init__(self, parent) # Parent is the Notebook


class setMagTab(ttk.Frame):
    def __init__(self, parent, page):
        ttk.Frame.__init__(self, parent) # Parent is the Notebook


class setGpsTab(ttk.Frame):
    def __init__(self, parent, page):
        ttk.Frame.__init__(self, parent) # Parent is the Notebook


class stripChartTab(ttk.Frame):
    def __init__(self, parent, page):
        ttk.Frame.__init__(self, parent) # Parent is the Notebook
        self.sc = tke.Stripchart(self, 350, 200)
        self.sc.pack()


class cube3DTab(ttk.Frame):
    def __init__(self, parent, page, controller):
        ttk.Frame.__init__(self, parent) # Parent is the Notebook

        spacer = tk.Canvas(self, width=300, height=300)
        spacer.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        page.visBQuit = tk.Button(self, text="STOP")
        page.visBQuit.grid(row=1, column=1)

        visB = tk.Button(self, text="CUBE", command=lambda: CUBE.CubeVisInit(controller.X, controller.Y, page.visBQuit))
        visB.grid(row=1, column=0)
