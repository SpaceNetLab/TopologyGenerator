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



def create_file_if_not_exit(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def main():
    results = []
    with open('cdn_requests_0.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        i = 0
        for row in data:
            if int(row[3]) < 10<<20:
                row[0] = i
                i += 1
                results.append(row)
    
    with open('cdn_requests_10M.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in results:
            writer.writerow(row);

    
    #log = "cdn_requests_<10M.csv"
    #create_file_if_not_exit(log)
    


if __name__== "__main__":
    main()
    
