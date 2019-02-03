import tkinter as tk
import threading as thr
import time as time
import math, random, threading, time


# Wrapper frame for Stripchart widget (To allow placement like any other tk widget)
class Stripchart(tk.Frame):
    def __init__(self, parent, sw, h):
        tk.Frame.__init__(self, parent) # Set up frame stuff
        self.mech = StripChart_mech(self, sw, h) # Create Strip Chart
        self.mech.pack(side="top", fill="both", expand=True) # Pack Strip Chart in Frame Container

#Components and mechanisms for the actual strip chart
class StripChart_mech(tk.Frame):

        def __init__(self, parent, sw, h):
            tk.Frame.__init__(self, parent)
            self.lock = thr.Lock()
            self.gf = self.makeGraph(parent, sw, h)
            self.cf = self.makeControls(parent)
            self.gf.pack()
            self.cf.pack()
            self.x = 0
            self.t = 0
            self.data = 0
            self.bg = '#001'
            
        def makeGraph(self, frame, sw, h):
            self.sw = sw
            self.h = h
            self.top = 1
            graph = tk.Canvas(frame, width=self.sw, height=self.h, bg="#002", bd=0, highlightthickness=0)
            graph.p = tk.PhotoImage(width=2*self.sw, height=self.h)
            self.image_obj_ref = graph.create_image(-self.top, self.top, image=graph.p, anchor=tk.NW)
            return(graph)
            

        def makeControls(self, frame):
            # Control Frame
            controlFrame = tk.Frame(frame, borderwidth=1, relief="raised")
            
            # Run
            self.runB = tk.Button(controlFrame, text="Run", command=self.Run)
            self.runB.grid(column=2, row=2)
            # Stop
            self.stopB = tk.Button(controlFrame, text="Stop", command=self.Stop)
            self.stopB.grid(column=4, row=2)
            # Reset
            self.resetB = tk.Button(controlFrame, text="Reset", command=self.Reset)
            self.resetB.grid(column=6, row=2)
            
            # Preformance Indicator
            self.fps = tk.Label(controlFrame, text="0 fps")
            self.fps.grid(column=2, row=4, columnspan=5)
            
            # Return Frame
            return(controlFrame)


        def Run(self):
            with self.lock:
                self.go = True
                check = 0
                for t in threading.enumerate():
                    print(t)
                    if t.name == "_run_":
                        check = 1
                if check == 1:
                    print("already running")
                else:
                    threading.Thread(target=self.do_start, name="_run_").start()
                

        def do_start(self):
            t = 0
            y2 = 0
            tx = time.time()
            with self.lock:
                while self.go:
                    t = time.time()
                    y1 = 0.2*math.sin(0.5*math.pi*t)
                    y2 = 0.9*y2 + 0.1*(random.random()-0.5)
                    #print("Jello" + str(y1+0.25))
                    self.x = (self.x + 1) % self.sw               # x = double buffer position

                    p = self.gf.p
                    data = (0.25+y1,   0.25, 0.7+y2,   0.6,     0.7,   0.8)
                    colors = ( '#ff4', '#f40', '#4af', '#080', '#0f0', '#080')
                    bar="" if t % 65 else "#002"
                    
                    bg = bar if bar else self.bg
                    p.tk.call(p, 'put', bg, '-to', self.x, 0, self.x+1, self.h)
                    p.tk.call(p, 'put', bg, '-to', self.x+self.sw, 0, self.x+self.sw+1, self.h)
                    self.gf.coords(self.image_obj_ref, -1-self.x, self.top)  # scroll to just-written column
                    #print(p)
                    #print(data)
                    if not self.data:
                        self.data = data
                    for d in range(len(data)):
                        y0 = int((self.h-1) * (1.0-data[d]))   # plot all the data points
                        y1 = int((self.h-1) * (1.0-self.data[d]))
                        ya, yb = sorted((y0, y1))
                        for y in range(ya, yb+1):                   # connect the dots
                            p.put(colors[d], (self.x,y))    
                            p.put(colors[d], (self.x+self.sw,y))
                    self.data = data            # save for next call
                    time.sleep(.01)
                    #print("scroll end")
                        #self.scrollstrip(self.gf.p,(0.25+y1,0.25,0.7+y2,0.6,0.7,0.8),('#ff4','#f40','#4af','#080','#0f0','#080'),"" if t % 65 else "#088")

        
        def Stop(self):
            
            print("stopcheck 1!")
            self.go = False
            check = 0
            for t in threading.enumerate():
                if t.name == "_run_":
                    check = 1
                    print("\n\n --- Stopping: {:s}\n\n".format(t.name))
            if check == 1:
                print("Thread has Stopped")
            else:
                print("Already Stopped")


        def Reset(self):
            self.Stop()
            self.Stop()
            print("RESET GRAPH")
            time.sleep(0.5)
            self.clearstrip(self.gf.p, '#345')


        def clearstrip(self, p, color):
            self.bg = "#005"
            self.data = None
            self.x = 0
            print((p['width']))
            p.tk.call(p, 'put', "#005", '-to', 0, 0, self.gf.p['width'], self.gf.p['height'])


        def nanoTime(self):
            return int(round(time.time() * 1000000))


        def do_start2(self):
            t = 0
            y2 = 0


                
            t += 1
            if not t % 100: # Means IF (t%100 == 100):
                tx2 = time.time()
                self.fps.config(text='%d fps' % int(100/(tx2 - tx)))# Update FPS indicator
                tx = tx2

        def scrollstrip(self, p, data, colors, bar=""):
            self.x = (self.x + 1) % self.sw               # x = double buffer position
            bg = bar if bar else self.bg
            p.tk.call(p, 'put', bg, '-to', self.x, 0, self.x+1, self.h)
            p.tk.call(p, 'put', bg, '-to', self.x+self.sw, 0, self.x+self.sw+1, self.h)
            self.gf.coords(self.image_obj_ref, -1-self.x, self.top)  # scroll to just-written column
            print(p)
            print(data)
            if not self.data:
                self.data = data
            for d in range(len(data)):
                y0 = int((self.h-1) * (1.0-data[d]))   # plot all the data points
                y1 = int((self.h-1) * (1.0-self.data[d]))
                ya, yb = sorted((y0, y1))
                for y in range(ya, yb+1):                   # connect the dots
                    p.put(colors[d], (self.x,y))    
                    p.put(colors[d], (self.x+self.sw,y))
            self.data = data            # save for next call
            print("scroll end")
