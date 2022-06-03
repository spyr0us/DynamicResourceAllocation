#!/usr/bin/env python3
import os
import random
import sys
import time
import requests
from  multiprocessing import dummy

IMAGES_PATH = os.getenv('IMAGES_PATH', './images/')
IMAGES = []
for (dirpath, dirnames, filenames) in os.walk(IMAGES_PATH):
     IMAGES.extend(filenames)
     break

def post_once():
     image = os.path.join(IMAGES_PATH, random.choice(IMAGES))
     print('Using image: {}'.format(image))
     a = requests.post("http://10.106.228.73:80", files={"file":
open(image, "rb")})
     # a = requests.post("http://edge-server-cv.info:80/", files={"file":open(image, "rb")})

     print(a)
#http://192.168.49.2:30796
DURATION = float(os.getenv('DURATION', '1800.0'))
REQUESTS_PER_30 = float(os.getenv('REQUESTS_PER_30', '90.0'))
POOL = dummy.Pool(16)

def main():
     start_time = time.time()
     while (time.time() - start_time) < DURATION:
         time.sleep(random.expovariate(REQUESTS_PER_30 / 30.0))
         POOL.apply_async(post_once)

if __name__ == "__main__":
     main()

