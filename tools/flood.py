from threading import Thread
import os
from ping3 import ping

tps=100

def do():
    while True:
        ping('192.168.1.2')

threads=[]
for i in range(tps):
    print(i)
    t=Thread(target=do)
    t.daemon=True
    threads.append(t)

for i in threads:
    i.start()

for i in threads:
    i.join()