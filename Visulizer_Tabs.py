class CubeVisulaizer():
        
        # Accel Settings Visualizations
        aclVisF = tk.Frame(page_setAcl)
        aclVisF.grid(row=0, column=2)
        
        self.sc = Stripchart(aclVisF, 400, 200)
        self.sc.grid(row=0, column=0)
        
        self.visBQuit = tk.Button(page_setAcl, text="STOP")
        self.visBQuit.grid(row=1, column=2)

        visB = tk.Button(page_setAcl, text="CUBE", command=lambda: CubeVis.CubeVisInit(parent.X, parent.Y, self.visBQuit))
        visB.grid(row=1, column=0)
