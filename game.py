import queue
import random
import threading
from multiprocessing.managers import BaseManager
import sysv_ipc
import signal
import sys
import os
import subprocess


def list_to_string(list):
    str = ' '.join(list)
    return str


clear = lambda: os.system('clear')

def add_input(input_queue):
    while True:
        input_queue.put(sys.stdin.readline())

def handler(sig, frame):
    if sig == signal.SIGUSR1:
        print("exit")

if __name__ == "__main__":

    players_number = int(sys.argv[1])

    # mq pour gérer la mise en place du jeu
    key1 = 121
    mq_setting_up = sysv_ipc.MessageQueue(key1, sysv_ipc.IPC_CREAT)

    # mq pour gérer la mise en place du jeu
    key2 = 256
    mq_communication = sysv_ipc.MessageQueue(key2, sysv_ipc.IPC_CREAT)

    class MyManager(BaseManager):
        pass


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
    print("waiting for ", players_number - current_players_number, "players...")
    while current_players_number != players_number:
        clear()
        print("waiting for ", players_number-current_players_number, "players...")
        message, t = mq_setting_up.receive(True, 1)
        value = message.decode()
        value = int(value)

        current_players_number += 1

        pid_list = pid.pid_list()
        pid_list.acquire()
        tab = pid_list.get_list()
        tab.append(value)
        pid_list.put_list(tab)
        pid_list.release()

        offer_list = offer.offer_list()
        offer_list.acquire()
        tab = offer_list.get_list()
        initial_offer = []
        tab.append(initial_offer)
        offer_list.put_list(tab)
        offer_list.release()

        flag_list = flag.flag_list()
        flag_list.acquire()
        tab = flag_list.get_list()
        tab.append(True)
        print(tab)
        flag_list.put_list(tab)
        flag_list.release()

    '''
    for i in range(players_number):
        message = "0".encode()
        mq_setting_up.send(message)
    '''

    # création du deck (jeu de carte pour cette partie)
    cards = ("airplane", "car", "train", "bike", "shoes")
    deck = []
    for i in range(players_number):
        for j in range(5):
            deck.append(cards[i])

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

    # mise en place d'une saisie non bloquante pour quitter le jeu en cours
    input_queue = queue.Queue()
    input_thread = threading.Thread(target=add_input, args=(input_queue,))
    input_thread.daemon = True
    input_thread.start()

    old_offers = []
    while True:

        offer_list = offer.offer_list()
        offer_list.acquire()
        new_offers = offer_list.get_list()
        offer_list.release()
        if new_offers != old_offers:
            pid_list = pid.pid_list()
            flag_list = flag.flag_list()
            pid_list.acquire()
            flag_list.acquire()
            tab_pid = pid_list.get_list()
            tab_flag = flag_list.get_list()
            pid_list.release()
            flag_list.release()
            clear()
            for idx, i in enumerate(tab_pid):
                print(tab_pid[idx], new_offers[idx], tab_flag[idx])
            print("")
            print("type q to quit")

        if not input_queue.empty():
            input = input_queue.get()
            if input[0] == "q":
                break
        old_offers = new_offers

    mq_setting_up.remove()
    mq_communication.remove()
