# -*- coding:utf-8 -*-
import os
import json
import csv
import numpy as np
import errno
import requests
import time
import copy

url_satellite = "starfront.satellite.com/objects/";
url_cloud = "starfront.cloud.com/objects/";

def fetch_object(url, times):
    result_list = url;
    for i in range(times):
        start_time = time.time();
        response = requests.get(url)
        print(response.headers);
        print(response.content);
        print(response.elapsed);
        print((time.time() - start_time));
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
    results.append(copy.deepcopy(fetch_object(url, 1000)))

    url = url_satellite + "random_10K.data"
    results.append(copy.deepcopy(fetch_object(url, 1000)))

    url = url_satellite + "random_100K.data"
    results.append(copy.deepcopy(fetch_object(url, 1000)))

    url = url_satellite + "random_1M.data"
    results.append(copy.deepcopy(fetch_object(url, 1000)))

    # save logs
    log = "log.csv"
    create_file_if_not_exit(log)
    f = open(log, "w+")
    for line in results:
        f.write(line + "\n")
    f.flush()
    f.close()




if __name__== "__main__":
    main();