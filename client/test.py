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
s = sched.scheduler(time.time, time.sleep)

results = []
size_set = [1<<10,10<<10,100<<10,500<<10,1<<20,5<<20,10<<20]
size_max = 10<<20

def create_file_if_not_exit(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def get_actual_size(size):
    if size > size_max :
        return size_max
    else:
        for actual_size in size_set:
            if size <= actual_size :
                return actual_size

def get_url(actul_size):
    #return "https://www.baidu.com/"
    return "http://192.168.100.100/objects/"+str(actul_size)


def do_request(seq, size, sip = "0.0.0.0", observpoint = "default"):
    actual_size = get_actual_size(size)
    url = get_url(actual_size)
    start_time = time.time()
    response = requests.get(url)
    latency = (time.time() - start_time)
    print("[" +seq+"] " + " start_time:"+str(start_time)+" Size:"+ str(size) + " actual_size:"+str(actual_size)+" Latency:" + str(latency) + " elapsed:" + str(response.elapsed))
    
    
    results.append(seq+", "+str(start_time)+", "+ str(size) +", "+str(actual_size)+", "+str(latency) +", "+str(response.elapsed))


def main():
    time_start = time.time()
    print("time_start:",time_start)
    with open('cdn_requests_10M.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        data = data[:10]
        row_count = len(data)
        print("request_num:",row_count)
        time_first_request = int(data[0][1])
        time_last_request = 0
        pri = 0
        for row in data:
            print(row)
            print(row[0]+" scheduling")
            time_this_request = int(row[1])
            if time_this_request == time_last_request:
                pri += 1
            else:
                pri=0
            time_last_request = time_this_request
            s.enter((time_this_request-time_first_request)/1000,pri,do_request,argument=(row[0],int(row[3]),))
            print(row[0]+" scheduled: "+ str((time_this_request-time_first_request)/1000)+","+str(pri)+","+str(int(row[3])))
    
    print("time_run:",time.time())
    s.run()

    print(results)

    res = "res/cdn_requests_10M_res.csv"
    create_file_if_not_exit(res)
    f = open(res, "w+")
    for line in results:
        f.write(line + "\n")
    f.flush()
    f.close()

'''
    with open('cdn_requests_10M_res.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile,delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #writer.writerows(results)
        for row in results:
            data = list(row)
            writer.writerow(data);
'''
if __name__== "__main__":
    #print(size_set)
    main()