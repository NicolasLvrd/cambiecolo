from multiprocessing import Process, Lock, Array
import sysv_ipc
from multiprocessing import shared_memory
import numpy as np

if __name__ == "__main__":
    existing_shm = shared_memory.SharedMemory(name='smh_00')
    buffer = existing_shm.buf
    buffer[1] = 8
    b = input("")
    existing_shm.close()


    #key = 128
    #mq = sysv_ipc.MessageQueue(key)
