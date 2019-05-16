#!/usr/bin/env python3

import re
import fileinput
import datetime
import argparse

#this is a simple utility to combine the many files of an isus or suna 
#deployment into one big file


parser = argparse.ArgumentParser(description='Concatinate many SUNA output files into one')
parser.add_argument('infiles', metavar='infiles', type=str, nargs='+', 
                    help='input files, can use wildcards ie *.CSV')
parser.add_argument('-m', '--mooring', nargs='?', required=True,
                    help='add mooring name')
parser.add_argument('-sn', '--serial_number', nargs='?', required=True,
                    help='add SUNA serial number')
parser.add_argument('-l', '--leave_dark', action="store_true",
                    help='Leave dark frames')
parser.add_argument('-d', '--dark', action="store_true",
                    help='Only get dark frames')
args=parser.parse_args()

if args.mooring and args.serial_number:
    filename=args.mooring+'_'+'suna'+'_'+args.serial_number+'.csv'
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

        


    

  
