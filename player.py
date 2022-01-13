from multiprocessing import Process, Lock, Array
import sysv_ipc
from multiprocessing import shared_memory
import numpy as np

if __name__ == "__main__":
    existing_shm_pid = shared_memory.SharedMemory(name='smh_00')
    pid_buffer = existing_shm_pid.buf
    existing_shm_offer = shared_memory.SharedMemory(name='smh_01')
    offer_buffer = existing_shm_pid.offer

    existing_shm_pid.close()
    existing_shm_offer.close()


    #key = 128
    #mq = sysv_ipc.MessageQueue(key)
