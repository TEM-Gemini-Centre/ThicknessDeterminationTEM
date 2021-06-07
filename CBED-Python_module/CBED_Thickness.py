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


def get_thickness_plot(SI_list, kStart = 1, kstop = 4, D_EXCT= None, version = '3 Plots'):
    """
    

    Parameters
    ----------
    SI_list : TYPE
        DESCRIPTION.
    kStart : TYPE, optional
        DESCRIPTION. The default is 1.
    kstop : TYPE, optional
        DESCRIPTION. The default is 6.
    D_EXCT : TYPE, optional
        DESCRIPTION. The default is None.
    version : R-Values, 3 Plots
        Chooses which value should be used.Std-Error: tries to optimize the thickness by finding the best fiting iterators (not recommended), 3 Plots: shows 3 Plots with n = 1, n = 2, n= 3 and the user has to choose which of those plots one uses
        if 3 Plots is chosen kstop =3 by default
    Returns
    -------
    fig : TYPE
        DESCRIPTION.
    STD_ERROR : TYPE
        DESCRIPTION.
    Best_THICKNESS : TYPE
        DESCRIPTION.

    """
    D_EXCT_list = []
    STD_ERROR = []
    DATA_list = [] #Saving interesting stuff per Iteration to make plots [SLOPE, Yintercept, T, D_EXCT_G,np.abs(RSQUARE), SIsquared_over_NKsquared, ONE_over_NKsquared]
    plt.rcParams.update({'font.size': 18})
    fig_size = (20,7)
    if version == 'Std-Error':
        for i in range(kstop):
          
            #while STD_ERROR[-1]>STD_ERROR[-2]:
            NK_list = np.arange(start=kStart, stop= len(SI_list)+kStart, step=1) #creating the necessary n_k
            SIsquared_over_NKsquared= np.array([S**2/N**2 for (S,N) in zip(SI_list,NK_list)]) #creating Yvalues
            ONE_over_NKsquared = np.array([1/N**2 for N in NK_list]) #creating Xvalues
            SLOPE, Yintercept, RSQUARE, p_value, std_err = linregress(ONE_over_NKsquared, SIsquared_over_NKsquared) #Getting all the necessary Data
            
            # Getting Extinction length and Thickness T
            D_EXCT_G = np.sqrt(np.abs(1/SLOPE)) * 10**9 # in nm
            T = np.sqrt(1/Yintercept)*10**9 # in nm  
            D_EXCT_list.append(D_EXCT_G)
            ############
            #### Saving Results
            STD_ERROR.append(std_err)
            DATA_list.append([SLOPE, Yintercept, T, D_EXCT_G,std_err, SIsquared_over_NKsquared, ONE_over_NKsquared])
            kStart+=1
        ###############
        # Comparing Measured Exctinction length with a given one
        """
        if D_EXCT != None:
            print(D_EXCT_G)
            print(D_EXCT_G/D_EXCT)
        """
        ############
        ############
        #  Plotting
      

        fig, (ax1, ax2) = plt.subplots(1,2,figsize=fig_size)
        #ax1.set_aspect(aspect=0.5)  # Doing Kelly's Plot
        BEST_fittedITERATION= (STD_ERROR.index(min(STD_ERROR)))
        Best_THICKNESS = DATA_list[BEST_fittedITERATION][2]
        Best_SLOPE =DATA_list[BEST_fittedITERATION][0]
        #print(type(Best_SLOPE))
        ax1.scatter(DATA_list[BEST_fittedITERATION][-1],DATA_list[BEST_fittedITERATION][-2], c= 'r', s = 24)#, label=r'Thickness= '+str(round(Best_THICKNESS,2))+' nm \n Standard Error: '+str(round(DATA_list[BEST_fittedITERATION][4],4)))
        ax1.plot(DATA_list[BEST_fittedITERATION][-1],DATA_list[BEST_fittedITERATION][1] + DATA_list[BEST_fittedITERATION][0]* DATA_list[BEST_fittedITERATION][-1], c='g', lw=3, alpha= 0.4, label= 'Linear Fit')
        ax1.legend(loc= 'upper right', title = r'Thickness= '+str(round(Best_THICKNESS,2))+' nm')
        ax1.set_xlabel(r'$\frac{1}{n_k^2}$')
        y_label= ax1.set_ylabel(r'$\frac{s_i^2}{n_k^2}$')
        y_label.set_rotation(0)
        ax1.set_yticklabels([])
        ax1.set_xticklabels([])
        if Best_SLOPE >0:
            ax1.text(.5,.5,'Wrong Slope',size = 100, bbox=dict(boxstyle="round",ec=(1., 0.5, 0.5),fc=(1., 0.8, 0.8)))
        #ax2.set_aspect(aspect= 1)   # Plotting the Rsquared
        ax2.scatter(np.arange(start= 1, stop=len(STD_ERROR)+1,step=1, dtype= int), STD_ERROR, marker= '+',s = 200)
        ax2.scatter(BEST_fittedITERATION+1, DATA_list[BEST_fittedITERATION][4], s= 200, facecolors = 'none', edgecolors= 'r',linewidth= 3)
        ax2.set_xlim([0,kstop+1])
        #ax2.set_xticklabels(np.arange( 0, kstop, dtype= int))
        ax2.set_xlabel('Number of Iterations')
        ylabel = ax2.set_ylabel(r'Standard Error')
        ylabel.set_rotation(90)
        plt.show()

        return fig, STD_ERROR, Best_THICKNESS
    
    if version== '3 Plots':
        kstop = 3
        for i in range(kstop):
          
            #while STD_ERROR[-1]>STD_ERROR[-2]:
            NK_list = np.arange(start=kStart, stop= len(SI_list)+kStart, step=1) #creating the necessary n_k
            SIsquared_over_NKsquared= np.array([S**2/N**2 for (S,N) in zip(SI_list,NK_list)]) #creating Yvalues
            ONE_over_NKsquared = np.array([1/N**2 for N in NK_list]) #creating Xvalues
            SLOPE, Yintercept, RSQUARE, p_value, std_err = linregress(ONE_over_NKsquared, SIsquared_over_NKsquared) #Getting all the necessary Data
            
            # Getting Extinction length and Thickness T
            D_EXCT_G = np.sqrt(np.abs(1/SLOPE)) * 10**9 # in nm
            T = np.sqrt(1/Yintercept)*10**9 # in nm  
            D_EXCT_list.append(D_EXCT_G)
    
            ############
            #### Saving Results
            #STD_ERROR.append(np.abs(RSQUARE))
            DATA_list.append([SLOPE, Yintercept, T, D_EXCT_G,std_err, SIsquared_over_NKsquared, ONE_over_NKsquared])
            kStart+=1
                
        ############
        ############
        #  Plotting
      
        plt.rcParams.update({'font.size': 18})
        fig, (ax1, ax2, ax3) = plt.subplots(1,3,figsize=((25,10)))
        #print(DATA_list)
        #BEST_fittedITERATION= (STD_ERROR.index(max(STD_ERROR)))
        #Best_THICKNESS = DATA_list[BEST_fittedITERATION][2]
        #Best_SLOPE =DATA_list[BEST_fittedITERATION][0]
        ax1.scatter(DATA_list[0][-1],DATA_list[0][-2], c= 'r', s = 24, label=r'Thickness= '+str(round(DATA_list[0][2],2))+' nm \n'+r'$\xi_e$= {} nm'.format(DATA_list[1][3])) # \n $R^2= $'+str(round(DATA_list[0][4],4))+'
        ax1.plot(DATA_list[0][-1],DATA_list[0][1] + DATA_list[0][0]* DATA_list[0][-1], c='g', lw=3, alpha= 0.4, label= 'Linear Fit')
        ax2.scatter(DATA_list[1][-1],DATA_list[1][-2], c= 'r', s = 24, label=r'Thickness= '+str(round(DATA_list[1][2],2))+' nm \n'+r'$\xi_e$= {} nm'.format(DATA_list[2][2])) #\n $R^2= $'+str(round(DATA_list[1][4],4))+'
        ax2.plot(DATA_list[1][-1],DATA_list[1][1] + DATA_list[1][0]* DATA_list[1][-1], c='g', lw=3, alpha= 0.4, label= 'Linear Fit')
        ax3.scatter(DATA_list[2][-1],DATA_list[2][-2], c= 'r', s = 24, label=r'Thickness= '+str(round(DATA_list[2][2],2))+' nm \n'+r'$\xi_e$= {} nm'.format(DATA_list[2][3])) #\n $R^2= $'+str(round(DATA_list[2][4],4))+'
        ax3.plot(DATA_list[2][-1],DATA_list[2][1] + DATA_list[2][0]* DATA_list[2][-1], c='g', lw=3, alpha= 0.4, label= 'Linear Fit')
        ax1.set_title = ('n=1')
        ax2.set_title = ('n=2')
        ax3.set_title = ('n=3')
        titles= [r'${n_k}= 1$',r'${n_k}= 2$',r'${n_k}= 3$']
        for i, ax in enumerate([ax1,ax2,ax3]):
            ax.legend(loc= 'upper right', title =titles[i])#, handlelength = 0, handletextpad = 0, fancybox = True)
            ax.set_xlabel(r'$\frac{1}{n_k^2}$')
            y_label= ax.set_ylabel(r'$\frac{s_i^2}{n_k^2}$')
            y_label.set_rotation(0)
            ax.set_yticklabels([])
            ax.set_xticklabels([])

        
        plt.show()

        return fig#, STD_ERROR, Best_THICKNESS

          
    

if __name__ == '__main__':
    #thetai in px
    theta1 = 52
    theta2 = 119
    theta3 = 187
    theta4 = 251
    
    # 2* Theta_B in px
    d_kik = 446
    
    si_list = make_si([52,119,187],D_KIK=446, D_HKL= 0.2021*10**-9, WAVELENGTH_TEM=0.0251*10**-10)
    get_thickness_plot(si_list, kStart=1, kstop=4, version='Std-Error')
