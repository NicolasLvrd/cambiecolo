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

    def aquire(self):
        self.lock.acquire()

    def release(self):
        self.lock.release()


class MyManager(BaseManager):
    pass


remote = MyRemoteClass()
MyManager.register("flag_list", callable=lambda: remote)
m = MyManager(address=("127.0.5.13", 8888), authkey=b'cc')
s = m.get_server()
s.serve_forever()
