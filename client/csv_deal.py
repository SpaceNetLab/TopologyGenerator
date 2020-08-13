# -*- coding:utf-8 -*-
import os
import json
import csv
import numpy as np
import errno
import requests
import time
import copy
import sched
import random

request_min_size = 0
request_max_size = 10<<20 #10M
cycle_min = 60 #60 minites in each cycle
cycle_num = 1 #how many cycles' data to generate
cycle_request_num = 2000 #request num in each cycyle(in all observ points)
object_num = 10 # num of objects to approximate (取整)
observ_num = 7 # num of observ points

request_sized_num = 0
time_per_cycle=0
time_zoom = 0

size_set = [1<<10,10<<10,100<<10,500<<10,1<<20,5<<20,10<<20]

def get_actual_size(size):
    if size > request_max_size :
        return request_max_size
    else:
        i=-1
        for actual_size in size_set:
            i += 1
            if size <= actual_size :
                return actual_size, i


def create_file_if_not_exit(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def main():
    temp = []
    results = []

    with open('cdn_requests_sorted.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        i = 0
        time_first = int(data[0][1])
        for row in data:
            if (int(row[3]) >= request_min_size) and (int(row[3]) <= request_max_size):
                row[0] = i
                i += 1
                temp.append(row)
        request_sized_num = i

    print("request_sized_num:"+str(request_sized_num))

    for index in range(cycle_request_num):
        results.append(temp[index])
    time_per_cycle = int(results[cycle_request_num-1][1])
    already_alloc_request = cycle_request_num

    print("time_per_cycle:"+str(time_per_cycle))


    for i in range(cycle_num-1):
        max_time=(i+2)*time_per_cycle
        print("["+str(i+2)+"] max_time: "+str(max_time)+" ") 
        before = already_alloc_request
        while int(results[already_alloc_request-1][1]) <= max_time:
             results.append(temp[already_alloc_request])
             already_alloc_request += 1
        print("["+str(i+2)+"] cycyle alloc: "+str(already_alloc_request-before)+" requests")    
    print("already_alloc_request:"+str(already_alloc_request))
        
    time_zoom = cycle_min *60*1000/time_per_cycle
    print("time_zoom:"+str(time_zoom))

    for index in range(already_alloc_request):
        results[index][1] = str(int(int(results[index][1])*time_zoom))

    print("last_time:"+results[already_alloc_request-1][1])

    for index in range(already_alloc_request):
        actual_size,seq = get_actual_size(int(results[index][3]))
        results[index][2] = str(actual_size)
        results[index][3] = str(seq)
    
    print("object approximated")

    for index in range(already_alloc_request):
        results[index][4] = str(random.randint(0,observ_num-1))
    
    print("observ point assigned")

    

    print("output...")
    
    output = "cdn_requests_"+str(cycle_num)+"cycle_"+str(observ_num)+"observ_"+str(cycle_request_num)+".csv"
    with open(output, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in results:
            writer.writerow(row);

    print("output finished. Exit...")
    #log = "cdn_requests_<10M.csv"
    #create_file_if_not_exit(log)
    


if __name__== "__main__":
    main()
    
