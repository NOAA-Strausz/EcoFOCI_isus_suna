#!/usr/bin/env python2.7

import re
import fileinput
import datetime
import matplotlib.pyplot as plt
import numpy as np

date = []
no3 = []
temp = []

for line in fileinput.input():
  if re.match("SAT\wLF", line):
    split_line = line.split(',')
    day_year = re.match('(\d{4})(\d{3})', split_line[1])
    hours = split_line[2]
    nitrate = split_line[3]
    t_lamp = split_line[10]
    day = day_year.group(2)
    year = day_year.group(1)
    hour_minutes = re.match('(\d{1,2})(\.\d+)', hours)
    hour = hour_minutes.group(1)
    minutes = int(float(hour_minutes.group(2)) * 60)
    seconds = int(((float(hour_minutes.group(2)) * 60) % 1) * 60)
    
    time_format = "%s %s %s %s %s" %(year, day, hour, minutes, seconds)
    time_datetime = datetime.datetime.strptime(time_format, "%Y %j %H %M %S")
    date.append(time_datetime)
    no3.append(nitrate)
    temp.append(t_lamp)
 
   
plt.yticks()
plt.plot_date(x=date, y=no3)

#p1.set_ylim([0,5])

#fig = plt.figure()
#ax = fig.add_subplot(111)
#plt.plot_date(x=date, y=no3)
##ax.set_ylim(0,20)
#plt.plot_date(x=date, y=no3)
#plt.savefig('test.png')
plt.show()

    

  
