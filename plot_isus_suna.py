#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 15:59:56 2019

@author: strausz
"""

import pandas as pd
import matplotlib.pyplot as plt
import sys
import seaborn as sns
import numpy as np


filename = sys.argv[1]


data = pd.read_csv(filename,header=None,parse_dates=[1])
data.set_index(data[1], inplace=True)


#get just the spectra channels for spectra plot
spectra=data[data.columns[10:266]]
nitrate=data[data.columns[2]]
#average 10 nitrate samples to once an hour:
nitrate=nitrate.resample('H').mean()


#create list with wavelengths
wavelengths = [200]
for x in range(1,256):
    wavelengths.append(wavelengths[-1]+.7843)

wavelengths = [(round(n, 2)) for n in wavelengths]
spectra.columns=wavelengths

datetime = data[1]
column = ['datetime']
datetime.columns=column
spectra = spectra.resample('H').mean()

#use pcolormesh to plot spectra
plt.figure(figsize=(9,4))
plt.pcolormesh(spectra.index, spectra.columns, spectra.T, cmap=plt.cm.plasma)
plt.colorbar()
plt.title("SUNA Spectra")
plt.ylabel('Y(nm)')
plt.savefig('suna.png')
#note that spectra is transposed, converting everying to regular numpy arrays 
#might speed it up, but this works
plt.show()


#make heatmap with seaborn
#ax = sns.heatmap(spectra)


    



#data['full_date'] = data.date

#data['datetime'] = pd.to_datetime(data.full_date)

