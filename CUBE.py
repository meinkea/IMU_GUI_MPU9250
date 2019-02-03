import tkinter as tk

import pygame as pyG
import pygame.locals as pyG_L

import OpenGL.GL as oglGL
import OpenGL.GLU as oglGLU
#This has OpenGL.GL and OpenGL.GLU

import sys
import os

import time
import math

import spidev as spidev

import threading

class cubeData:
    def __init__(self):
        self.verticies = (( 1, -1, -1),
                          ( 1,  1, -1),
                          (-1,  1, -1),
                          (-1, -1, -1),
                          ( 1, -1,  1),
                          ( 1,  1,  1),
                          (-1, -1,  1),
                          (-1,  1,  1))
        
        self.edges = ((0,1),
                      (0,3),
                      (0,4),
                      (2,1),
                      (2,3),
                      (2,7),
                      (6,3),
                      (6,4),
                      (6,7),
                      (5,1),
                      (5,4),
                      (5,7))
        
        self.surfaces = ((0,1,2,3),
                         (3,2,7,6),
                         (6,7,5,4),
                         (4,5,1,0),
                         (1,5,7,2),
                         (4,0,3,6))

        self.colors = ((1,0,0),
                       (0,1,0),
                       (0,0,1),
                       (0,1,0),
                       (1,1,1),
                       (0,1,1),
                       (1,0,0),
                       (0,1,0),
                       (0,0,1),
                       (0,1,0),
                       (1,1,1),
                       (0,1,1))

class cube(threading.Thread):
    
    
    def __init__(self, Xp, Yp, w=300, h=300, name='_cube_'):
        threading.Thread.__init__(self, name=name)
        self.threadStop = threading.Event()

        self.position = (Xp,Yp)
        self.display = (w,h)
        self.halfScale = 2**16/2
        self.Scale = 2**16
        print(self.display)
        self.cD = cubeData()
        print("Initialized")
    
    
    def Rectify(self, y):
        self.halfScale
        self.Scale
        if y > self.halfScale:
            y=y-self.Scale
        return y
    
    
    def update(self, dt):
        for event in pyG.event.get():
            if event.type == pyG.QUIT:
                pyG.quit()
                sys.exit()
                
            if event.type == pyG.KEYDOWN:
                if event.key == pyG.K_LEFT:
                    oglGL.glTranslateF(-0.5, 0.0, 0.0)
                if event.key == pyG.K_LEFT:
                    oglGL.glTranslateF( 0.5, 0.0, 0.0)
                if event.key == pyG.K_LEFT:
                    oglGL.glTranslateF( 0.0, 1.0, 0.0)
                if event.key == pyG.K_LEFT:
                    oglGL.glTranslateF( 0.0,-1.0, 0.0)
                    
            if event.type == pyG.MOUSEBUTTONDOWN:
                if event.button == 4:
                    oglGL.glTranslateF( 0.0, 0.0, 1.0)
                if event.button == 5:
                    oglGL.glTranslateF( 0.0, 0.0,-1.0)
                    
        if self.threadStop.is_set():
            pyG.quit()
            sys.exit()
    
    
    def CubeStop(self, button):
        button.config(command = None)
        self.threadStop.set()
        print("Stopping Cube...")
    
    
    def run(self):
        print("running main function RUN!...\n")
        
        print("I ran \n")
        
        self.y1c = []
        self.y2c = []
        self.y3c = []
        
        spi = spidev.SpiDev()
        spi.open(0, 0)
        spi.max_speed_hz = 1000000
        spi.mode = 3
        spi.cshigh = False
        try:
            for i in range (0,10000):
                
                Lc = [195, 196, 197, 198, 199, 201, 202]
                lc = spi.xfer(Lc)
                
                y1 = (lc[1]<<8) + (lc[2])
                y1 = self.Rectify(y1)
                y1 = y1*0.00381475547/2
                self.y1c.append(y1)
                
                y2 = (lc[3]<<8) + (lc[4])
                y2 = self.Rectify(y2)
                y2 = y2*0.00381475547/2
                self.y2c.append(y2)
                
                y3 = (lc[5]<<8) + (lc[6])
                y3 = self.Rectify(y3)
                y3 = y3*0.00381475547/2
                self.y3c.append(y3)

        except:
            print("Calibration Failed!...")
        finally:
            spi.close()

        
        
        #print(y1c)
        
        self.y1offset = 0
        for i in range(0, len(self.y1c)):
            self.y1offset = self.y1offset + self.y1c[i]

        self.y2offset = 0
        for i in range(0, len(self.y2c)):
            self.y2offset = self.y2offset + self.y2c[i]
        
        self.y3offset = 0
        for i in range(0, len(self.y3c)):
            self.y3offset = self.y3offset + self.y3c[i]
            
        self.y1offset = self.y1offset/len(self.y1c)
        self.y2offset = self.y2offset/len(self.y2c)
        self.y3offset = self.y3offset/len(self.y3c)

        print(self.y1offset)
        print(self.y2offset)
        print(self.y3offset)
                
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % self.position
        
        pyG.init()
        
        screen = pyG.display.set_mode(self.display, pyG_L.DOUBLEBUF|pyG_L.OPENGL|pyG_L.NOFRAME)
        
        fps = 20.0
        fpsClock = pyG.time.Clock()
        dt = 1/fps # For Velocity calculations

        oglGLU.gluPerspective(45, (self.display[0]/self.display[1]), 1.2, 50.0)
        oglGL.glTranslatef(0.0, 0.0, -5)
        oglGL.glRotatef(0, 0, 0, 0)
        
        while True:
            self.update(dt)
            
            dt = fpsClock.tick(fps)
            
            spi.open(0, 0)
            spi.max_speed_hz = 1000000
            spi.mode = 3
            spi.cshigh = False
            
            L = [195, 196, 197, 198, 199, 201, 202]
            spi.xfer(L)
            spi.close()
            
            y1 = (L[1]<<8) + (L[2])
            y1 = self.Rectify(y1)
            y2 = (L[3]<<8) + (L[4])
            y2 = self.Rectify(y2)
            y3 = (L[5]<<8) + (L[6])
            y3 = self.Rectify(y3)
            #print("{0:b}".format(y1))
            
            y1 = y1*0.00381475547/2 - self.y1offset
            y2 = y2*0.00381475547/2 - self.y2offset
            y3 = y3*0.00381475547/2 - self.y3offset
            #print("{0:f}".format(y1))
            mag = math.sqrt(y1*y1+y2*y2+y3*y3)/5
            y1n = y1/mag
            y2n = y2/mag
            y3n = y3/mag
            
            oglGL.glRotatef(mag, y1n, y2n, y3n)

            oglGL.glClear(oglGL.GL_COLOR_BUFFER_BIT|oglGL.GL_DEPTH_BUFFER_BIT)
            
            # Draw Wire Edges
            oglGL.glBegin(oglGL.GL_LINES)
            for edge in self.cD.edges:
                for vertex in edge:
                    oglGL.glVertex3fv(self.cD.verticies[vertex])
            oglGL.glEnd()

            # Draw Surfaces
            oglGL.glBegin(oglGL.GL_QUADS)
            #x=0 - face coloring
            for surface in self.cD.surfaces:
                #x+=1 - face coloring
                #oglGL.glColor3fv((0,1,0))
                x=0
                for vertex in surface:
                    x+=1
                    oglGL.glColor3fv(self.cD.colors[x])    
                    oglGL.glVertex3fv (self.cD.verticies[vertex])
            oglGL.glEnd()

            
            
            pyG.display.flip()
        print("Cube Stopped!")
            

    '''
    def pause(self):
        self.display = "1x1+50+50"

    def move(self):
        return 0

    def start(self):
        return 0
    '''


cubeW = 0
def CubeVisInit(x, y, button):
    #if __name__ == '__main__':

    print("x_offset : {0} | y_offset : {1}".format(x, y))

    global cubeW
    cubeW = cube(Xp=395+x, Yp=95+y, w=300, h=300, name='_cube_')
    button.config(command=lambda: cubeW.CubeStop(button))
    
    cubeW.start()
    print("running cubeW.start()...")



    


#main3D = threading.Thread(target=main)
#main3D.start()

    
