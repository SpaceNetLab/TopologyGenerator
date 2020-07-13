# -*- coding:utf-8 -*-
import os
import json
import csv
import numpy as np
import errno
import requests
import time

def main():
    start_time = time.time();
    response = requests.get("http://www.lzq8272587.com/")
    print(response.headers);
    print(response.content);
    print(response.elapsed);
    print((time.time() - start_time));

if __name__== "__main__":
    main();