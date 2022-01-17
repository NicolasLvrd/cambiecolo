import queue
import random
import threading
import time
import sysv_ipc
from multiprocessing.managers import BaseManager
import os
import sys

from sysv_ipc import BusyError


def add_input(input_queue):
    while True:
        input_queue.put(sys.stdin.readline())


def string_to_list(string):
    li = list(string.split(" "))
    return li


def display_offers(offers):
    print("current offers : ", end="")
    for offer in offers:
        print(len(offer), " ", end="")
    print("")


def offer_validity(acronyms, deck):
    if len(acronyms) > 3:
        return False,

    for char in acronyms:
        if not isinstance(char, str):
            return False,

    first_char = acronyms[0]
    for char in acronyms:
        if char is not first_char:
            return False,

    my_offer = []
    for char in acronyms:
        available = False
        for card in deck:
            if char == card[0]:
                available = True
                my_offer.append(card)
                deck.remove(card)
                break
        if not available:
            return False,
    return True, my_offer, deck


def receive_validity(offers, input, my_offer):
    print(offers)
    print(input)
    print(my_offer)
    if len(input) != 1:
        return False
    try:
        player_number = int(input[0])
    except ValueError:
        return False
    if len(offers[player_number]) is not len(my_offer):
        return False
    return True


if __name__ == "__main__":

    class MyManager(BaseManager):
        pass


    MyManager.register('pid_list')
    pid = MyManager(address=("127.0.5.11", 8888), authkey=b'aa')
    pid.connect()

    MyManager.register('offer_list')
    offer = MyManager(address=("127.0.5.12", 8888), authkey=b'bb')
    offer.connect()

    MyManager.register('flag_list')
    flag = MyManager(address=("127.0.5.13", 8888), authkey=b'cc')
    flag.connect()

    key1 = 121
    mq_setting_up = sysv_ipc.MessageQueue(key1, sysv_ipc.IPC_CREAT)

    key2 = 256
    mq_communication = sysv_ipc.MessageQueue(key2, sysv_ipc.IPC_CREAT)

    # my_pid = os.getgid()
    my_pid = random.randint(0, 9999)
    print("MY PID IS ", my_pid)
    message = str(my_pid).encode()
    mq_setting_up.send(message, True, 1)

    message, t = mq_setting_up.receive(True, 2)
    value = message.decode()
    deck = string_to_list(value)

    # trouver son numéro de joueur
    pid_list = pid.pid_list()
    pid_list.acquire()
    tab = pid_list.get_list()
    pid_list.release()
    for idx, i in enumerate(tab):
        if i == my_pid:
            my_player_number = idx

    input_queue = queue.Queue()

    input_thread = threading.Thread(target=add_input, args=(input_queue,))
    input_thread.daemon = True
    input_thread.start()

    clear = lambda: os.system('clear')

    old_offers = []

    err_message = ""

    my_offer = []

    while True:
        time.sleep(1)

        offer_list = offer.offer_list()
        offer_list.acquire()
        new_offers = offer_list.get_list()
        offer_list.release()

        if new_offers != old_offers:
            #clear()
            print(err_message)
            print("")
            print("MY PLAYER NUMBER :", my_player_number)
            display_offers(new_offers)
            print("YOUR DECK : ", deck)
            print("YOUR OFFER (N°", my_player_number, ") :", my_offer)
            print("(to make a new offer, type \"o:\" and first letters of cards)")
            print("(to accept an offer, type \"a:\" and its number)")

        if not input_queue.empty():
            flag_list = flag.flag_list()
            flag_list.acquire()
            flags = flag_list.get_list()
            if flags[my_player_number]:  # si un échange n'est pas en cours avec moi
                flags[my_player_number] = False
                offer_list = offer.offer_list()
                offer_list.acquire()
                old_offers = offer_list.get_list()

                input = input_queue.get()
                input = input[:-1]
                if input[0] + input[1] == "o:":
                    valid_offer = offer_validity(input[2:], deck)

                    if valid_offer[0]:
                        print("VALIDE")
                        my_offer = valid_offer[1]
                        deck = valid_offer[2]

                        # offer_list = offer.offer_list()
                        # offer_list.acquire()
                        # old_offers = offer_list.get_list()
                        my_old_offer = old_offers[my_player_number]
                        new_offers = old_offers
                        new_offers[my_player_number] = my_offer
                        offer_list.put_list(new_offers)
                        # offer_list.release()
                        deck = deck + my_old_offer
                    else:
                        err_message = "invalid offer or old offer accepted"

                    # flag_list.acquire()
                    # flags = flag_list.get_list()
                    flags[my_player_number] = True
                    # flag_list.put_list(flags)
                    # flag_list.release()

                elif input[0] + input[1] == "a:":
                    # offer_list = offer.offer_list()
                    # offer_list.acquire()
                    # old_offers = offer_list.get_list()
                    if receive_validity(old_offers, input[2:], my_offer):
                        if flags[int(input[2])]:
                            deck = deck + old_offers[int(input[2])]
                            old_offers[int(input[2])] = []
                            my_offer = []
                            new_offers = old_offers
                            message = str(my_player_number).encode()
                            mq_setting_up.send(message, True, int(input[2]) + 3)  # +3 car type 1 et 2 déjà utilisés
                            # offer_list.release()
                            # flag_list.release()
                        else:
                            err_message = "an exchange is already in progress"
                            # offer_list.release()
                            flags[int(input[2])] = True
                            flags[my_player_number] = True
                            # flag_list.release()
                            break
                    else:
                        err_message = "invalid accept"

                else:
                    err_message = "input error"
                offer_list.release()
                #clear()
                print(err_message)
                print("")
                print("MY PLAYER NUMBER :", my_player_number)
                display_offers(new_offers)
                print("YOUR DECK : ", deck)
                print("YOUR OFFER (N°", my_player_number, ") :", my_offer)
                print("(to make a new offer, type \"o:\" and first letters of cards)")
                print("(to accept an offer, type \"a:\" and its number)")
            else:
                err_message = "an exchange is already in progress"
            flag_list.release()

        try:
            message, t = mq_communication.receive(False, my_player_number + 3)
            print("GOOOTCHA")
            value = message.decode()
            value = int(value)
            flag_list = flag.flag_list()
            flag_list.acquire()
            flags = flag_list.get_list()
            deck = deck + new_offers[value]
            new_offers[value] = []
            my_offer = []
            flags[my_player_number] = True
            flags[value] = True
            flag_list.put_list(flags)
            flag_list.release()
        except BusyError:
            a=1

        old_offers = new_offers
