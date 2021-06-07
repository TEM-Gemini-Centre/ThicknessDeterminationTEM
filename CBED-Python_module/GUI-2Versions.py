# -*- coding: utf-8 -*-
"""
Spyder Editor
By Christoph Martin Hell
This is a temporary script file.
"""

from tkinter import *
from CBED_Thickness import make_si, get_thickness_plot
import matplotlib.pyplot as plt






###################################################
###################################################
########### Predefined Constants###################
###################################################
#wavelength: https://advanced-microscopy.utah.edu/education/electron-micro/
wavelength_TEM_200kV = 0.0251*10**-10 #m 

#Latice spacing pure AL taken from Williams and Carter
#d_Al_200 = 2.021e-10 #m Lattice spacing
d_Al_220 = 1.432e-10
##################################################





def run_CBEDAnalysis(event):
    theta1_variable = theta1.get()
    theta2_variable = theta2.get()
    theta3_variable = theta3.get()
    #theta4_variable = theta4.get()
    d_kik_variable = float(d_kik.get())
    version = version_variable.get()

    theta_list = [theta1_variable,theta2_variable,theta3_variable]
    theta_list= [float(entry) for entry in theta_list]


    wavelengthTEM_variable = float(wavelengthTEM.get())
    d_latticePlane_variable = float(d_latticePlane.get())


    si_list = make_si(theta_list , d_kik_variable, d_latticePlane_variable , wavelengthTEM_variable)
    thickness_fig, rsquares, thickness = get_thickness_plot(si_list, kStart = 1, kstop = 5 ,version= version)
    print('##################'+ '\n'+'##################'+ '\n'+'Thickness: '+ str(round(thickness,3))+
          '\n'+'##################'+'\n'+'##################')






root = Tk() #creates empty Window
root.title('CBED- Sicknessmeasurements')
root.geometry('400x300')
caption = Label(root, text = 'CBED- Sicknessmeasurements ', bg= 'black', fg = 'white', font = ('arial italic',20))
caption.grid(row = 0, column=0, columnspan = 2, pady = 10)


theta1_label = Label(root, text = 'Theta1:')
theta1_label.grid(row =3, column=0)
theta1 = Entry(root, width = 20)
theta1.grid(row =4, column=0)


theta2_label = Label(root, text = 'Theta2:')
theta2_label.grid(row =5, column=0)
theta2 = Entry(root, width = 20)
theta2.grid(row =6, column=0)


theta3_label = Label(root, text = 'Theta3:')
theta3_label.grid(row =7, column=0)
theta3 = Entry(root, width = 20)
theta3.bind('<Return>',run_CBEDAnalysis)
theta3.grid(row =8, column=0)


"""
theta4_label = Label(root, text = 'Theta4:')
theta4_label.pack()
theta4 = Entry(root, width = 20)
theta4.pack()
"""

d_kik_label = Label(root, text = 'Kikuchi Distance:')
d_kik_label.grid(row =1, column=0)
d_kik = Entry(root, width = 20)
d_kik.bind('<Return>',run_CBEDAnalysis)
d_kik.grid(row =2, column=0,pady = 15)




button1 = Button(root, text="Calculate Sickness", command = run_CBEDAnalysis)
button1.bind("<Button-1>", run_CBEDAnalysis)

button1.grid(row = 8, column = 1, columnspan = 1)




wavelengthTEM_label = Label(root, text = 'Wavelength [m]: ')
wavelengthTEM_label.grid(row =1, column=1)
wavelengthTEM = Entry(root, width = 20)
wavelengthTEM.insert(END, wavelength_TEM_200kV)
wavelengthTEM.grid(row =2, column=1)


d_latticePlane_label = Label(root, text = 'Latticeplane distance [m]:')
d_latticePlane_label.grid(row =3, column=1)
d_latticePlane = Entry(root, width = 20)
d_latticePlane.insert(END, d_Al_220)
d_latticePlane.grid(row =4, column=1)



version_variable= StringVar(root)
version_variable.set('3 Plots')
version = OptionMenu(root, version_variable, '3 Plots', 'Std-Error')
version.grid(row =7, column=1)
















root.mainloop() #shows Window continously

