from multiprocessing import Process, Lock, Array
import sysv_ipc
from multiprocessing.managers import BaseManager
import os

if __name__ == "__main__":

    class MyManager(BaseManager): pass

    MyManager.register('pid_list')
    pid = MyManager(address=("127.0.0.1", 8888), authkey=b'aa')
    pid.connect()

    MyManager.register('offer_list')
    offer = MyManager(address=("127.0.0.2", 8888), authkey=b'bb')
    offer.connect()

    MyManager.register('flag_list')
    flag = MyManager(address=("127.0.0.3", 8888), authkey=b'cc')
    flag.connect()



    # le player ajoute son pid dans la shm_pid
    pid_list = pid.pid_list()
    pid_list.aquire()
    tab = pid_list.get_list()
    tab.append(tab, os.pid())
    pid_list.put_list(tab)
    pid_list.release()

    '''
    key = 128
    mq_dispenser = sysv_ipc.MessageQueue(key)
    key = 256
    mq_communication = sysv_ipc.MessageQueue(key)

    '''

    '''
    for i in range(len(pid_buffer)):
        if pid_buffer[i] is None:
            if __name__ == '__main__':
                pid_buffer[i] = os.getpid()

    shm_pid.close()
    shm_offer.close()
    '''
