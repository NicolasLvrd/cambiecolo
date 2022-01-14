import random
from multiprocessing import Process, Lock
from multiprocessing.managers import BaseManager
import sysv_ipc
import signal
import sys
import time
import os


if __name__ == "__main__":

    players_number = sys.argv[0]

    # mq pour gérer la mise en place du jeu
    key = 128
    mq_setting_up = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

    os.system("python shm_flag.py")
    os.system("python shm_offer.py")
    os.system("python shm_pid.py")

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

    # on attend que tous les players rejoignent la partie
    current_players_number = 0
    while True:
        message, t = mq_setting_up.receive()
        if message is not None:
            value = message.decode()
            current_players_number += 1
            message.remove()
        if current_players_number == players_number:
            break


    # création du deck (jeu de carte pour cette partie)
    cards = ("airplane", "car", "train", "bike", "shoes")
    deck = ()
    for i in range(players_number):
        for j in range(players_number):
            deck.append(cards[j])

    # distribution des cartes
    for i in range(players_number):
        player_deck = ()
        for j in range(players_number):
            card = random.choice(deck)
            player_deck.append(card)
            deck.remove(card)
        message = player_deck.encode()
        mq_setting_up.send(message)

    #
    key = 256
    mq_communication = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

    # dire au players qu'on start le game
    



    
    
    key = 128
    mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
    shared_memory = Array(('1','1'), 5)

