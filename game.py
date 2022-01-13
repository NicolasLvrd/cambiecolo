import random
from multiprocessing import Array, shared_memory
import sysv_ipc

if __name__ == "__main__":
    players_number = 5

    cards = ("airplane", "car", "train", "bike", "shoes")
    deck = ()
    for i in range(players_number):
        for j in range(players_number):
            deck.append(cards[j])

    key = 128
    mq_dispenser = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
    shared_memory = Array(('a', 'a', 'a', 'a', 'a'), players_number)
    for i in range(players_number):
        player_deck = ()
        for j in range(players_number):
            card = random.choice(deck)
            player_deck.append(card)
            deck.remove(card)
        message = player_deck.encode()
        mq_dispenser.send(message)

    
    shm_pid = shared_memory.SharedMemory(name="smh_00", create=True, size=players_number)
    shm_offer = shared_memory.SharedMemory(name="smh_01", create=True, size=players_number)

    # dire au players qu'on start le game




    shm_pid.close()
    shm_pid.unlink()
    shm_offer.close()
    shm_offer.unlink()

    '''
    key = 128
    mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
    shared_memory = Array(('1','1'), 5)
    '''
