from multiprocessing.managers import BaseManager
from multiprocessing import Lock


class MyRemoteClass:
    def __init__(self):
        self.value = []
        self.lock = Lock()

    def get_list(self):
        return self.value

    def put_list(self, pushed_list):
        self.value = pushed_list

    def acquire(self):
        self.lock.acquire()
        print("pid lock acquired")

    def release(self):
        self.lock.release()
        print("pid lock released")


class MyManager(BaseManager):
    pass

remote = MyRemoteClass()
MyManager.register('pid_list', callable=lambda:remote)
m = MyManager(address=("127.0.5.11", 8888), authkey=b'aa')
s = m.get_server()
s.serve_forever()
