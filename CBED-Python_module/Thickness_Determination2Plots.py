# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 10:29:11 2021

@author: chhe
"""

from CBED_Thickness import make_si, get_thickness_plot



###################################################
###################################################
########### Predefined Constants###################
###################################################
#wavelength: https://advanced-microscopy.utah.edu/education/electron-micro/
wavelength_TEM_200kV = 0.0251*10**-10 #m 

#Latice spacing pure AL taken from Williams and Carter
d_Al_200 = 2.021*10**-10 #m Lattice spacing
d_Al_220 = 1.432 * 10**-10
##################################################




###################################################
###################################################
#############TEM Session- Measured Values##########
###################################################
###################################################
#thetai in a.u.
theta1 = 0.405
theta2 = 0.934
theta3 = 1.432
theta4 = 0
theta5 = 0
# 2* Theta_B in a.u.
d_kik = 6.91 #um

#Amount of measured KM finges
theta_list = [theta1, theta2, theta3]
###################################################






si_list = make_si(theta_list,d_kik,d_Al_220, wavelength_TEM_200kV)

thickness_fig, rsquares, thickness = get_thickness_plot(si_list, kStart = 1, kstop = 5 )
print('Thickness: ', thickness)

