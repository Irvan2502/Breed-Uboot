#!/usr/bin/env python3
import socket
import time
import threading
import signal
import sys
sending = None


def send_thread_func(s):
    global sending
    while sending:
        time.sleep(0.1)
        s.sendto(b'BREED:ABORT', ('255.255.255.255', 37541))


def receive_thread_func(s):
    global sending
    while sending:
        data, addr = s.recvfrom(2048)
        if data == b'BREED:ABORTED':
            print("BREED now running on {}".format(addr[0]))
            print("http://{}".format(addr[0]))
            break
    sending = False


def start_breed_enter():
    global sending
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(('0.0.0.0', 37540))

    sending = True
    receive_thread = threading.Thread(target=receive_thread_func, args=(s, ))
    send_thread = threading.Thread(target=send_thread_func, args=(s, ))

    receive_thread.daemon = True
    send_thread.daemon = True
    receive_thread.start()
    send_thread.start()

    print("Waiting breed to be discovered....")
    while sending:
        try:
            time.sleep(0.5)
        except KeyboardInterrupt:
            break

    print("QUIT")
    sys.exit(0)


def main():
    start_breed_enter()


if __name__ == '__main__':
    main()
