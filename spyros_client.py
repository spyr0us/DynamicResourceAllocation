#!/usr/bin/env python3
from  multiprocessing import dummy
import os
import random
import sys
import time
import requests
import pandas as pd


IMAGES_PATH = os.getenv('IMAGES_PATH', './images/')

IMAGES = []
for (dirpath, dirnames, filenames) in os.walk(IMAGES_PATH):
    IMAGES.extend(filenames)
    break

def post_once():
    image = os.path.join(IMAGES_PATH, random.choice(IMAGES))
    # print('Using image: {}'.format(image))
    try:
        response = requests.post('http://10.106.228.73:80', files={"file": open(image, "rb")}) # 8000 port for web with /tasks endpoint
    except requests.exceptions.ConnectionError as err:
        print('Error while trying to post once: {}'.format(err))
    # print (response)


DURATION = float(os.getenv('DURATION', '10000.0'))
POOL = dummy.Pool(16)

def main():
    traffic = pd.read_csv('sleep_times_below_13.csv')
    traffic.head()
    traffic.columns = ['Traffic']
    total_counter =0 

    for i in range((traffic.index[-1])):
        # print (traffic.values[i])
        time.sleep(traffic.values[i][0])
        # print("sleep time: ", sleep_time)
        POOL.apply_async(post_once)
        total_counter += 1

    
    print ("sum requests", total_counter)

if __name__ == "__main__": 
    main()
