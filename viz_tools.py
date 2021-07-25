"""
File with several visualization functions intended to be used 
with results from 1D Burgers' equation simulation
"""

############## MODULES IMPORTATION ###############

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from scipy import meshgrid
import os

##################################################

def plot_a_frame_1D(x, y, xmin, xmax, ymin, ymax, titre = "MON TITRE", type = "-", ion = False):
    """
     Plot a random 1D solution with its plot window.
    
    (x:np.ndarray (format 1D), y:np.ndarray (format 1D), xmin:float, xmax:float, ymin:float, ymax:float, titre:str, type:str, ion:bool) -> plot
    """
    plt.axis([xmin,xmax,ymin,ymax])
    plt.plot(x,y, type , color = "black")
    if ion:
        plt.ion()
    plt.title(titre)
    plt.xlabel("$x \ [\mathrm{m}]$.3")
    plt.ylabel("$u \ [\mathrm{m}]$")
    plt.show()

##################################################

def plot_spatio_temp_3D(x,t,z):
    """
    Plot a 2 two parameters function z = f(x,t) where x-axis is spatial and y-axis is time.
    
    (x:np.ndarray (format 1D), y:np.ndarray (format 1D), z:np.ndarray (format 1D)) -> plot
    """
    fig = plt.figure(figsize = (10,9))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('$x \ [\mathrm{m}]$', fontsize = 16)
    ax.set_ylabel('$t \ [\mathrm{s}]$', fontsize = 16)
    ax.set_zlabel('$u \ [\mathrm{m}]$', fontsize = 16)
    ax.view_init(elev = 15, azim = 120)
    
    SX,ST = meshgrid(t,x)
    p = ax.plot_surface(ST,SX,z,cmap = plt.cm.viridis)
    plt.show()      


##################################################


def plot_spatio_temp_flat(x,y,t):
    V = y[::-1, :]
    plt.figure(figsize=(6,5))
    plt.imshow(V, extent=[0,x[y.shape[1] - 1],0,t[y.shape[0] - 1]])
    cbar = plt.colorbar()
    cbar.set_label('hight $[m]$')
    plt.xlabel('$x \ [\mathrm{m}]$')
    plt.ylabel('$t \ [\mathrm{s}]$')
    plt.axis('normal')
    plt.show()
    

##################################################


def plot_sequence(x,y):
    fig = plt.figure(figsize = (8,7))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('$x$ [$\mathrm{m}$]')
    ax.set_ylabel('Time points')
    ax.set_zlabel('$z \ [\mathrm{m}]$')
    ax.view_init(70, -90)
    y_plot = y[0:-1:20,:]
    for j in range(y_plot.shape[0]):
        ys = j*np.ones(y_plot.shape[1])
        ax.plot(x,ys, y_plot[j,:], color = plt.cm.brg(20*j))
    
    plt.show()
    
##################################################


def anim_1D(x,y, pas_de_temps, pas_d_images, save = False, myxlim = (0, 4) , myylim = (-4,4)):
    """
  Function allowing to display an annimation based on calculation result with a given time step. This function can be used to save the images sequence in the current directory.
    
    The y parameter is a list containing several functions to display : y = [ [f_1(x)], ... , [f_n(x)] ].
    
    (x:np.ndarray (format 1D), y:np.ndarray (format 2D), pas_de_temps:float , pas_d_images:int, save:bool , myxlim:tuple , myylim:tuple) -> plot (+ .mp4)
    """
    
    fig = plt.figure()
    ax = plt.axes(xlim= myxlim , ylim= myylim)
    line, = ax.plot([], [])
    ax.set_title("Wave form $u(x,t)$ after t = 0 seconds",fontsize = 14)
    ax.set_xlabel("$x \ [\mathrm{m}]$",fontsize = 14)
    ax.set_ylabel("$u \ [\mathrm{m}]$",fontsize = 14)
    def init():
        line.set_data([],[])
        return line,
    
    # animation function.  This is called sequentially
    def animate(i):
        line.set_data(x, y[:,pas_d_images*i])
        ax.set_title("Wave form $u(x,t)$ after t = {:.2f} seconds".format(np.round(i*pas_d_images*pas_de_temps, 2)), fontsize = 14)
        return line,
        
    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=y.shape[1]//pas_d_images, interval=10, blit=True)

    if save:
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=25, metadata=dict(artist='Me'), bitrate=10000)

        anim.save('lines.mp4', writer=writer)

    return anim

