from multiprocessing import Process, Lock, Array
import sysv_ipc
from multiprocessing.managers import BaseManager
import os

def string_to_list(string):
    li = list(string.split(" "))
    return li

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

    key = 121
    mq_setting_up = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

    value = os.getgid()
    message = str(value).encode()
    mq_setting_up.send(message, True, 1)

    message, t = mq_setting_up.receive(True, 2)
    value = message.decode()
    deck = string_to_list(value)
    print(deck)



