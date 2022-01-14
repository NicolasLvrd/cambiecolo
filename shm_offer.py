from multiprocessing.managers import BaseManager
from multiprocessing import Lock


class MyRemoteClass:
    def __init__(self):
        self.value = ()
        self.lock = Lock()

    def get_list(self):
        return self.value

    def put_list(self, pushed_list):
        self.value = pushed_list

    def aquire(self):
        self.lock.aquire()

    def release(self):
        self.lock.release()


class MyManager(BaseManager):
    pass


remote = MyRemoteClass()
MyManager.register("offer_list", callable=lambda: remote)
m = MyManager(address=("127.0.0.2", 8888), authkey=b'bb')
s = m.get_server()
s.serve_forever()