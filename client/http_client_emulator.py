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

url_satellite = "http://starfront.satellite.com/objects/";
url_cloud = "http://starfront.cloud.com/objects/";
repeat = 100



def fetch_object(url, times):
    result_list = url;
    for i in range(times):
        start_time = time.time();
        response = requests.get(url)
        #print(response.headers);
        # print(response.content);
        # print(response.elapsed);
        print("Latency:" + str(time.time() - start_time) + "elapsed:" + str(response.elapsed));
        latency = (time.time() - start_time);
        #save latency sample.
        result_list = result_list + "," + str(latency)

    return result_list


def create_file_if_not_exit(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def main():
    results = [];
    # fetch 1KB/10KB/100KB/1MB object for 1000 times
    url = url_satellite + "random_1K.data"
    results.append(copy.deepcopy(fetch_object(url, repeat)))

    url = url_satellite + "random_10K.data"
    results.append(copy.deepcopy(fetch_object(url, repeat)))

    url = url_satellite + "random_100K.data"
    results.append(copy.deepcopy(fetch_object(url, repeat)))

    url = url_satellite + "random_1M.data"
    results.append(copy.deepcopy(fetch_object(url, repeat)))

    # save logs
    log = "log/log.csv"
    create_file_if_not_exit(log)
    f = open(log, "w+")
    for line in results:
        f.write(line + "\n")
    f.flush()
    f.close()




if __name__== "__main__":
    print (1)
    main()
