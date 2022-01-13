from multiprocessing import Array, shared_memory
import sysv_ipc

if __name__ == "__main__":

    players_number = 5

    shm_pid = shared_memory.SharedMemory(name="smh_00", create=True, size=players_number)
    shm_offer = shared_memory.SharedMemory(name="smh_00", create=True, size=players_number)
    shm_pid.close()
    shm_pid.unlink()
    shm_offer.close()
    shm_offer.unlink()

    '''
    key = 128
    mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
    shared_memory = Array(('1','1'), 5)
    '''


