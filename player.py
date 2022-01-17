import queue
import threading
import time
import sysv_ipc
from multiprocessing.managers import BaseManager
import os
import sys


def add_input(input_queue):
    while True:
        input_queue.put(sys.stdin.readline())

def string_to_list(string):
    li = list(string.split(" "))
    return li

def offers_to_numbers(offers):
    res = []
    for offer in offers:
        if offer == 0:
            res.append(0)
        else:
            res.append(len(offer))
    return res

def valid_offer(acronyms, deck):
    my_offer = []
    for char in acronyms:
        available = False
        for card in deck:
            print("comp:", char, card[0])
            if char == card[0]:
                available = True
                my_offer.append(card)
                break
        deck.remove(card)
        if not available:
            return False,
    return True, my_offer, deck


if __name__ == "__main__":

    class MyManager(BaseManager): pass

    MyManager.register('pid_list')
    pid = MyManager(address=("127.0.5.11", 8888), authkey=b'aa')
    pid.connect()

    MyManager.register('offer_list')
    offer = MyManager(address=("127.0.5.12", 8888), authkey=b'bb')
    offer.connect()

    MyManager.register('flag_list')
    flag = MyManager(address=("127.0.5.13", 8888), authkey=b'cc')
    flag.connect()

    key = 121
    mq_setting_up = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

    my_pid = os.getgid()
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

    clear = lambda : os.system('clear')

    old_offers = []

    while True:
        time.sleep(1)
        offer_list = offer.offer_list()
        offer_list.acquire()
        new_offers = offer_list.get_list()
        offer_list.release()

        if new_offers != old_offers:
            clear()
            print("current offers", offers_to_numbers(new_offers))
            print("Your deck : ", deck)
            print("to make a new offer, type \"o:\" and first letters of cards")
            print("for exemple \"o:ab\" for airplane and bike")
            print("to accept an offer, type \"a:\" and its number")

        if not input_queue.empty():
            flag_list = flag.flag_list()
            flag_list.acquire()
            flags = flag_list.get_list()

            input = input_queue.get()
            input = input[:-1]
            print("INPUT : ", input)
            print(input[0]+input[1])
            if input[0]+input[1] == "o:":
                valid_offer = valid_offer(input[2:], deck)
                print(input[2:])

                if valid_offer[0] and flags[my_player_number]:
                    print("valid offer")
                    my_offer = valid_offer[1]
                    deck = valid_offer[2]

                    offer_list = offer.offer_list()
                    offer_list.acquire()
                    old_offers = offer_list.get_list()
                    my_old_offer = old_offers[my_player_number]
                    new_offers = old_offers
                    new_offers[my_player_number] = my_offer
                    offer_list.put_list(new_offers)
                    offer_list.release()
                    deck = [*deck, *my_old_offer]
                else:
                    print("invalid offer or old offer accepted")

            elif input[0]+input[1] == "a:":
                print(" ")
            else:
                "input error"
            flag_list.release()

        old_offers = new_offers





