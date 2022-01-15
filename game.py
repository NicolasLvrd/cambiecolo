import random
from multiprocessing import Process, Lock
from multiprocessing.managers import BaseManager
import sysv_ipc
import signal
import sys
import time
import os
import subprocess

def list_to_string(list):
    str = ' '.join(list)
    return str

if __name__ == "__main__":

    players_number = int(sys.argv[1])

    # mq pour gérer la mise en place du jeu
    key = 121
    mq_setting_up = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

    # lancement des shared memories
    #shm_pid = subprocess.Popen(["python", "shm_pid.py"])
    #shm_offer = subprocess.Popen(["python", "shm_offer.py"])
    #shm_flag = subprocess.Popen(["python", "shm_flag.py"])

    class MyManager(BaseManager): pass

    # connection aux shared memories
    MyManager.register('pid_list')
    pid = MyManager(address=("127.0.5.11", 8888), authkey=b'aa')
    pid.connect()

    MyManager.register('offer_list')
    offer = MyManager(address=("127.0.5.12", 8888), authkey=b'bb')
    offer.connect()

    MyManager.register('flag_list')
    flag = MyManager(address=("127.0.5.13", 8888), authkey=b'cc')
    flag.connect()

    # on attend que tous les players rejoignent la partie
    current_players_number = 0

    while current_players_number != players_number:
        message, t = mq_setting_up.receive(True, 1)
        value = message.decode()
        value = int(value)

        current_players_number += 1

        pid_list = pid.pid_list()
        pid_list.aquire()
        tab = pid_list.get_list()
        tab.append(value)
        pid_list.put_list(tab)
        pid_list.release()

    print("All players joined")

    for i in range(players_number):
        message = "0".encode()
        mq_setting_up.send(message)

    # création du deck (jeu de carte pour cette partie)
    cards = ("airplane", "car", "train", "bike", "shoes")
    deck = []
    for i in range(players_number):
        for j in range(5):
            deck.append(cards[j])

    # distribution des cartes
    for i in range(players_number):
        player_deck = []
        for j in range(5):
            card = random.choice(deck)
            player_deck.append(card)
            deck.remove(card)
        print(list_to_string(player_deck))
        message = list_to_string(player_deck).encode()
        mq_setting_up.send(message, True, 2)

    i = input("")
    mq_setting_up.remove()

