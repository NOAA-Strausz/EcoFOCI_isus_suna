#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 15:59:56 2019

@author: strausz
"""

#for now this only works with SUNAS

import pandas as pd
import matplotlib.pyplot as plt
import argparse


parser = argparse.ArgumentParser(description='Plot ISUS/SUNA variables')
parser.add_argument('infile', metavar='infile', type=str, nargs='+', 
                    help='input file created with cat_suna_isus.py')
parser.add_argument('-m', '--mooring', nargs='?', required=True,
                    help='add mooring name')
parser.add_argument('-sn', '--serial_number', nargs='?', required=True,
                    help='add SUNA serial number')
parser.add_argument('-spec', '--spectra', action="store_true",
                    help='Make spectra plot of data')
parser.add_argument('-no3', '--nitrate', action="store_true",
                    help='Plot the nitrate concentration')
parser.add_argument('-anc', '--ancillary', action="store_true",
                    help='Plot the ancillary data')
parser.add_argument('-an', '--analysis', action="store_true",
                    help='Plot analysis data')
parser.add_argument('-av', '--average', action="store_true",
                    help='Create a new csv file from input that averages the hourly readings')

args=parser.parse_args()


filename = args.infile[0]

data = pd.read_csv(filename,header=None,parse_dates=[1])
data.set_index(data[1], inplace=True)
filename_prefix = args.mooring + '_SUNA_' + args.serial_number

#for nitrate plot
if args.ancillary:
    ancillary = data[data.columns[267:276]]
    names = ['int_temp', 'spec_temp', 'lamp_temp', 'lamp_time', 'rh', 'v_main', 'lamp_v', 'int_v', 'main_I']
    ancillary.columns = names
    
if args.nitrate:
    nitrate=data[data.columns[2]]
    #average 10 nitrate samples to once an hour:
    nitrate=nitrate.resample('H').mean()
    outfile = filename_prefix + " nitrate.png"
    title = args.mooring + " SUNA " + args.serial_number + " Nitrate"
    plt.figure(figsize=(9,4))
    plt.plot(nitrate)
    plt.ylabel('μM')
    plt.title(title)
    outfile = filename_prefix + "_nitrate.png"
    plt.savefig(outfile)
if args.spectra:
    #get just the spectra channels for spectra plot
    spectra=data[data.columns[10:266]]
    #create list with wavelengths
    wavelengths = [200]
    for x in range(1,256):
        wavelengths.append(wavelengths[-1]+.7843)
    #reduce amount of decimal places to 2 
    wavelengths = [(round(n, 2)) for n in wavelengths]
    spectra.columns=wavelengths
    #resample on hour, helps to plot faster
    spectra = spectra.resample('H').mean()
    
    #use pcolormesh to plot spectra
    plt.figure(figsize=(9,4))
    plt.pcolormesh(spectra.index, spectra.columns, spectra.T, cmap=plt.cm.plasma)
    plt.colorbar()
    title = args.mooring + " SUNA " + args.serial_number + " Spectra"
    plt.title(title)
    plt.ylabel('Y(nm)')
    outfile = filename_prefix + "_spectra.png"
    plt.savefig(outfile)
    #note that spectra is transposed, converting everying to regular numpy arrays 
    #might speed it up, but this works

if args.average:
    hourly = data.resample('H').mean()
    outfile = filename_prefix + "_hourly.csv"
    hourly.to_csv(outfile)

if args.analysis:
    def make_patch_spines_invisible(ax):
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        for sp in ax.spines.values():
            sp.set_visible(False)
    #setup multiple plots taken from
    #https://matplotlib.org/gallery/ticks_and_spines/multiple_yaxis_with_spines.html
    fig, host=plt.subplots()
    fig.subplots_adjust(right=0.75)
    #fig.subplots_adjust(left=-0.65)
    title = args.mooring + " SUNA " + args.serial_number
    fig.suptitle(title)
    fig.set_size_inches(12,6)
    
    par1 = host.twinx()
    par2 = host.twinx()
    par3 = host.twinx()
    #par3 = host.twinx()
    
    par2.spines["right"].set_position(("axes", 1.1))
    #par3.spines["right"].set_position(("axes", 1.3))
    par3.spines["right"].set_position(('axes', 1.2))
    #par3.spines["left"].set_position(("axes", 1.1))
    #make_patch_spines_invisible(par2)
    #par2.spines["right"].set_visible(True)

    
    p1, = host.plot(data[279], "blue", label="Fit RMSE")
    p2, = par1.plot(data[4], "red", label="254nm Absorbance")
    p3, = par2.plot(data[5], "orange", label="350nm Absorbance")
    p4, = par3.plot(data[72], "green", label="Max Spectra")
    
    host.set_ylim(0, .005)
    par1.set_ylim(-1, 1.0)
    par2.set_ylim(-.5, 1.0)
    
    host.set_ylabel("RMSE")
    par1.set_ylabel("Absorbance 254nm")
    par2.set_ylabel("Absorbance 350nm")
    par3.set_ylabel("Spectra counts")
    
    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    par2.yaxis.label.set_color(p3.get_color())
    par3.yaxis.label.set_color(p4.get_color())
    
    tkw = dict(size=4, width=1.5)
    host.tick_params(axis='y', colors=p1.get_color(), **tkw)
    par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
    par3.tick_params(axis='y', colors=p4.get_color(), **tkw)
    host.tick_params(axis='x', **tkw)
    
    
    lines = [p1, p2, p3, p4]

    host.legend(lines, [l.get_label() for l in lines])
    outfile = filename_prefix + "_analysis_plot.png"
    plt.savefig(outfile)

    
    
        

#make heatmap with seaborn
#ax = sns.heatmap(spectra)


    



#data['full_date'] = data.date

#data['datetime'] = pd.to_datetime(data.full_date)

