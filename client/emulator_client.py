import sys
import os
import json
import csv
import numpy as np
import errno
import requests
import threading
import time
import copy
import socket
import random
from geopy import distance

size_set = [1<<10,10<<10,100<<10,500<<10,1<<20,5<<20,10<<20]
url_satellite = "http://starfront.satellite.com/objects/"
url_cloud = "http://starfront.cloud.com/objects/"
host_satellite = "starfront.satellite.com"
host_cloud = "starfront.cloud.com"

light_of_speed_m_s = 299792458 # m / s
space_attenuation_factor = 0.8 # light travels in 2/3 speed of light in free-space
terrestrial_attenuation_factor = space_attenuation_factor * 0.63 / 1.8
light_of_speed_km_ms = light_of_speed_m_s / (10 ** 6)

RTT_random_MAX = 0.1
results=[]
arg_out_file_name = "res/cdn_requests_10M_res_bed_both.csv"
#arg_out_file_name = "res/cdn_requests_10M_res_bed_only_cloud.csv"

class node_entry:
    def __init__(self):
        self.name = ''
        self.id = 0
        self.origin_id = 0
        self.type = ''# this is a satellite/cloud/request node
        self.lat = 0
        self.lon = 0
        self.alt = 0
        self.ts = 0
        self.size = 0

def init():
    #place all the objects to the two edges
    for size in size_set:
        print(requests.get(url_satellite+str(size)).elapsed)
        print(requests.get(url_cloud+str(size)).elapsed)
    print("initial Placement Finished")
    
def load_location_data():
    cloud_nodes_data_filename = "cloudfront.json"
    satellite_nodes_data_filename = "satellite_lla_overtime.json"
    vantage_nodes_data_filename = "vantage_point.json"
    request_data_filename = "request.json"

    cloud_nodes_data = open(cloud_nodes_data_filename)
    satellite_nodes_data = open(satellite_nodes_data_filename)
    vantage_nodes_data = open(vantage_nodes_data_filename)
    request_nodes_data = open(request_data_filename)

    cloud_nodes_dict = json.load(cloud_nodes_data)
    satellite_nodes_dict = json.load(satellite_nodes_data)
    vantage_nodes_dict = json.load(vantage_nodes_data)
    request_dict = json.load(request_nodes_data)

    print("Have loaded cloud + satellite + vantage point + request data from json files.")

    return [cloud_nodes_dict, satellite_nodes_dict, vantage_nodes_dict, request_dict]

def create_file_if_not_exit(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def estimate_RTT_via_location(src_node, dst_node, speed):
    src_location = (src_node.lat,src_node.lon)
    dst_location = (dst_node.lat,dst_node.lon)
    dis = distance.distance(src_location, dst_location).km
    dis = dis + abs(src_node.alt - dst_node.alt)
    estimate_RTT = 2 * (dis / speed)

    return estimate_RTT

def main(argv):
    print("main")
    #connect to two servers' link info socket

    link_s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    link_s.connect((host_satellite,9090))
    print("connected to 'satellite' link info socket")
    link_c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    link_c.connect((host_cloud,9090))
    print("connected to 'cloud' link info socket")

    #read vantage_point
    #read cloud_front
    #read satellite_lla
    #read request info(time,size,position)

    [cloud_data, satellite_data, vantage_data, request_data] = load_location_data()
    num_of_cloud = int(cloud_data['num_of_cloud'])
    num_of_vantage = int(vantage_data['num_of_vantage'])
    num_of_satellite = int(satellite_data['num_of_satellite'])
    vantage_list = vantage_data['vantage_points']


    print('Have loaded node data from json file, with %s clouds, %s vantage points and %s satellites.' % (str(num_of_cloud), str(num_of_vantage), str(num_of_satellite)))

    cloud_RTT = {}
    satellite_last_slot = {}

    #read request resolve info(the result of Algorithm)
    with open('assignment-row.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        assignment = list(reader)
        for request in request_data:
            request_seq = int(request['seq'])
            request_time = int(int(request['request_time'])/1000/60) #slot
            request_size = int(request['request_size']) # unit: byte
            request_src = vantage_list[int(request['observ_point'])]
            request_dst = assignment[request_seq][3] #1:only-cloud 3:cloud-satellite

            node = node_entry()
            node.name = "Request-from-" + str(request['observ_point']) + '-slot-' + str(request_time) + '-size-' + str(request_size)
            node.lat = float(request_src['lat'])
            node.lon = float(request_src['lon'])
            node.alt = float(request_src['alt'])
            
            RTT = 0.0
        #for every request, calculate RTT and send to the edge server
            #cloud
            if request_dst[0]=='C':
                cloud_seq = int(request_dst[1:])
                if cloud_RTT.__contains__(cloud_seq):
                    RTT = cloud_RTT[cloud_seq]
                else:
                    cloud_info = cloud_data['cities'][cloud_seq-1]
                    cloud_node = node_entry()
                    cloud_node.lat = float(cloud_info['lat'])
                    cloud_node.lon = float(cloud_info['lon'])
                    cloud_node.alt = float(cloud_info['alt'])
                    RTT = estimate_RTT_via_location(node, cloud_node, light_of_speed_km_ms * terrestrial_attenuation_factor)
                    cloud_RTT[cloud_seq] = RTT
                RTT = RTT * (1+random.uniform(0,RTT_random_MAX))
                link_info = str(request['seq'])+","+request_dst+","+str(request_time)+","+str(RTT)
                print(link_info)
                
                link_c.send(link_info.encode('utf-8')) 
                data = link_c.recv(1024)
                print('back:',data.decode())
                #send link_info
            #satellite
            elif request_dst[0]=='S':
                sat_seq = int(request_dst[1:])
                if satellite_last_slot.__contains__(sat_seq) and request_time == satellite_last_slot[sat_seq]:
                    print("no sat link update")
                else:
                    sat_info = satellite_data['snapshot_sequence'][request_time]['snapshot'][sat_seq-1]
                    sat_node = node_entry()
                    sat_node.lat = float(sat_info['lat'])
                    sat_node.lon = float(sat_info['lon'])
                    sat_node.alt = float(sat_info['alt'])
                    RTT = estimate_RTT_via_location(node, sat_node, light_of_speed_km_ms * space_attenuation_factor)
                    RTT = RTT * (1+random.uniform(0,RTT_random_MAX))
                    satellite_last_slot[sat_seq] = request_time
                    link_info = str(request['seq'])+","+request_dst+","+str(request_time)+","+str(RTT)
                    print(link_info)

                    link_s.send(link_info.encode('utf-8')) 
                    data = link_s.recv(1024)
                    print('back:',data.decode())
            else:
                print("CDN edge resolve failure")
    #send request, get result
            url=''
            if request_dst[0]=='C':
                url = url_cloud+str(request_size)
            else:
                url = url_satellite+str(request_size)
            
            start_time = time.time()
            response = requests.get(url)
            latency = (time.time() - start_time)
            #print("[" +seq+"] " + " start_time:"+str(start_time)+" Size:"+ str(size) + " actual_size:"+str(actual_size)+" Latency:" + str(latency) + " elapsed:" + str(response.elapsed))
            
            results.append(request['seq']+", "+str(request_time)+", "+ str(request_size) +", "+ request_src['name']+", "+request_dst+","+str(latency) +", "+str(response.elapsed))
            print(results[-1])
    
    print("results output start...")

    res = arg_out_file_name
    create_file_if_not_exit(res)
    f = open(res, "w+")
    for line in results:
        f.write(line + "\n")
    f.flush()
    f.close()

    print("results output end.")
    print("exiting...")


            
            
            


    

    
        
   
    


if __name__== "__main__":
    #print(size_set)
    #init()
    main(sys.argv)
    
