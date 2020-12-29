#!/usr/bin/python3
from subprocess import Popen
import sys

#filename = sys.argv[1]
while True:
#    print("\n----- Starting " + filename + " -----")
#    p = Popen("python3 " + filename, shell=True)
    p = Popen("sudo nohup python3 /var/www/html/np.py &", shell=True)
    p.wait()
