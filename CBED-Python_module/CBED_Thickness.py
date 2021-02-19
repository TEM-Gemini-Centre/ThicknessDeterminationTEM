# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 18:37:20 2020

@author: chhe
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress


def make_si(THETA_list, D_KIK, D_HKL, WAVELENGTH_TEM):
    SI_list = [(WAVELENGTH_TEM*THETA)/(D_KIK*D_HKL**2) for THETA in THETA_list]
    return np.array(SI_list)


def get_thickness_plot(SI_list, kStart = 1, kstop = 6, D_EXCT= None):
    RSQUARE_list = []
    DATA_list = [] #Saving interesting stuff per Iteration to make plots
    for i in range(kstop):
      
        #while RSQUARE_list[-1]>RSQUARE_list[-2]:
        NK_list = np.arange(start=kStart, stop= len(SI_list)+kStart, step=1) #creating the necessary n_k
        SIsquared_over_NKsquared= np.array([S**2/N**2 for (S,N) in zip(SI_list,NK_list)]) #creating Yvalues
        ONE_over_NKsquared = np.array([1/N**2 for N in NK_list]) #creating Xvalues
        SLOPE, Yintercept, RSQUARE, p_value, std_err = linregress(ONE_over_NKsquared, SIsquared_over_NKsquared) #Getting all the necessary Data
        
        # Getting Extinction length and Thickness T
        D_EXCT_G = np.sqrt(np.abs(1/SLOPE)) * 10**9 # in nm
        T = np.sqrt(1/Yintercept)*10**9 # in nm  

        ############
        #### Saving Results
        RSQUARE_list.append(np.abs(RSQUARE))
        DATA_list.append([SLOPE, Yintercept, T, D_EXCT_G,np.abs(RSQUARE), SIsquared_over_NKsquared, ONE_over_NKsquared])
        kStart+=1
    ###############
    # Comparing Measured Exctinction length with a given one
    if D_EXCT != None:
        print(D_EXCT_G)
        print(D_EXCT_G/D_EXCT)

    ############
    ############
    #  Plotting
  
    plt.rcParams.update({'font.size': 18})
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(20,5))
    #ax1.set_aspect(aspect=0.5)  # Doing Kelly's Plot
    BEST_fittedITERATION= (RSQUARE_list.index(max(RSQUARE_list)))
    Best_THICKNESS = DATA_list[BEST_fittedITERATION][2]
    Best_SLOPE =DATA_list[BEST_fittedITERATION][0]
    print(type(Best_SLOPE))
    ax1.scatter(DATA_list[BEST_fittedITERATION][-1],DATA_list[BEST_fittedITERATION][-2], c= 'r', s = 24, label=r'Thickness= '+str(round(Best_THICKNESS,2))+' nm \n $R^2= $'+str(round(DATA_list[BEST_fittedITERATION][4],4)))
    ax1.plot(DATA_list[BEST_fittedITERATION][-1],DATA_list[BEST_fittedITERATION][1] + DATA_list[BEST_fittedITERATION][0]* DATA_list[BEST_fittedITERATION][-1], c='g', lw=3, alpha= 0.4, label= 'Perfect Condition')
    ax1.legend(loc= 'upper right')
    ax1.set_xlabel(r'$\frac{1}{n_k^2}$')
    y_label= ax1.set_ylabel(r'$\frac{s_i^2}{n_k^2}$')
    y_label.set_rotation(0)
    ax1.set_yticklabels([])
    ax1.set_xticklabels([])
    if Best_SLOPE >0:
        ax1.text(.5,.5,'Wrong Slope',size = 100, bbox=dict(boxstyle="round",ec=(1., 0.5, 0.5),fc=(1., 0.8, 0.8)))
    #ax2.set_aspect(aspect= 1)   # Plotting the Rsquared
    ax2.scatter(np.arange(start= 1, stop=len(RSQUARE_list)+1,step=1, dtype= int), RSQUARE_list, marker= '+',s = 200)
    ax2.scatter(BEST_fittedITERATION+1, DATA_list[BEST_fittedITERATION][4], s= 200, facecolors = 'none', edgecolors= 'r',linewidth= 3)
    ax2.set_xlim([0,kstop+1])
    #ax2.set_xticklabels(np.arange(start= 1, stop=len(RSQUARE_list)+1,step=1, dtype= int))
    ax2.set_xlabel('Number of Iterations')
    ylabel = ax2.set_ylabel(r'$R^2$')
    ylabel.set_rotation(90)
 
    return fig, RSQUARE_list, Best_THICKNESS
      
    

