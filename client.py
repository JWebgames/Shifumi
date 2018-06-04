#!/usr/bin/python3.6

from atexit import register
@register
def foo():
    input("Press ENTER to quit")

from argparse import ArgumentParser
from socket import socket
from os import getenv

parser = ArgumentParser()
parser.add_argument("-a", "--addr",
                    default=getenv("SHIFUMI_ADDRESS", "localhost"),
                    help="Shifumi server address")
parser.add_argument("-p", "--port",
                    type=int,
                    default=int(getenv("SHIFUMI_PORT", 22451)),
                    help="Shifumi server port")
config = parser.parse_args()

def main():
    server = socket()
    server.connect((config.addr, config.port))
    print("Connected, waiting start signal...")
    server.recv(1)

    my_score = 0
    his_score = 0
    while True:
        print(f"Me: {my_score}, Him: {his_score}")
        while True:
            play = input("[P]aper, [R]ock, [S]cisor ? ").casefold()
            if play in ["p", "r", "s"]:
                server.send(play.encode())
                break
            print("Nop.")
        data = server.recv(1)
        if data == b"w":
            print("Won !")
            my_score += 1
        elif data == b"l":
            print("Lost.")
            his_score += 1
        elif data == b"d":
            print("Draw !")
        else:
            print("Error !!!")
            break

        if my_score == 5 or his_score == 5:
            print("Match is over ! You {}.".format(
                      "win" if my_score == 5 else "loose"))
            server.recv(1)
            break

    server.close()

if __name__ == "__main__":
    main()

