#!/usr/bin/env python3

import re
import fileinput
import datetime
import argparse

#this is a simple utility to combine the many files of an isus or suna 
#deployment into one big file


parser = argparse.ArgumentParser(description='Concatinate many SUNA output files into one')
parser.add_argument('infiles', 
    metavar='infiles', 
    nargs='*',
    help='input files, can use wildcards ie *.CSV')
parser.add_argument('-m', '--mooring', nargs=1, 
                    help='add mooring name')
parser.add_argument('-sn', '--serial_number', nargs=1,
                    help='add SUNA serial number')
args=parser.parse_args()

if args.mooring and args.serial_number:
    filename=args.mooring[0]+'_'+'suna'+'_'+args.serial_number[0]+'.csv'
    f = open(filename, 'w')
    
    for line in fileinput.input(args.infiles):
        if re.match("SAT\wLF", line):
            line.rstrip()
            prefix,yr_day,dec_time,the_rest = line.split(',', 3)
            hour = str(int(float(dec_time)))
            minutes = str(int(60*(float(dec_time) % 1)))
            seconds = str(int(60*((60*(float(dec_time) % 1))%1)))
            year = yr_day[:4]
            doy = yr_day[4:]
            full_date = year + ' ' + doy + ' ' + hour + ' ' + minutes + ' ' + seconds 
            time_datetime = datetime.datetime.strptime(full_date, "%Y %j %H %M %S" )
            time_formatted = time_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
            f.write(prefix+','+time_formatted+','+the_rest)
    f.close()
        
        
#    split_line = line.split(',')
#    day_year = re.match('(\d{4})(\d{3})', split_line[1])
#    hours = split_line[2]
#    nitrate = split_line[3]
#    t_lamp = split_line[10]
#    day = day_year.group(2)
#    year = day_year.group(1)
#    hour_minutes = re.match('(\d{1,2})(\.\d+)', hours)
#    hour = hour_minutes.group(1)
#    minutes = int(float(hour_minutes.group(2)) * 60)
#    seconds = int(((float(hour_minutes.group(2)) * 60) % 1) * 60)
#    
#    time_format = "%s %s %s %s %s" %(year, day, hour, minutes, seconds)
#    time_datetime = datetime.datetime.strptime(time_format, "%Y %j %H %M %S")
#    date.append(time_datetime)
#    no3.append(nitrate)
#    temp.append(t_lamp)
# 

    

  
