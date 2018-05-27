from socket import socket
from os import getenv

ADDR = getenv("SHIFUMI_ADDRESS", "0.0.0.0")
PORT = int(getenv("SHIFUMI_PORT", 22451))
GAMES = int(getenv("SHIFUMI_GAMES", 5))

class Player:
    def __init__(self, socket, name):
        self.socket = socket
        self.name = name
        self.score = 0
        self.play = b""

def main(server):
    server.bind((ADDR, PORT))
    server.listen()
    print(f"Server listening on tcp://{ADDR}:{PORT}")

    client, info = server.accept()
    print(f"Player 1 {info} connected")
    p1 = Player(client, "Player 1")

    client, info = server.accept()
    print(f"Player 2 {info} connected")
    p2 = Player(client, "Player 2")

    p1.socket.send(b"s")
    p2.socket.send(b"s")
    print(f"Game started, first to reach {GAMES} wins")
    while (p1.score < GAMES and p2.score < GAMES):
        print(f"Waiting for {p1.name}...")
        data = p1.socket.recv(1)
        if data not in [b"p", b"r", b"s"]:
            print(f"Invalid data {data}")
            break
        print("Got", data)
        p1.play = data

        print(f"Waiting for {p2.name}...")
        data = p2.socket.recv(1)
        if data not in [b"p", b"r", b"s"]:
            print(f"Invalid data {data}")
            break
        print("Got", data)
        p2.play = data

        if p1.play == p2.play:
            print("Draw")
            p1.socket.send(b"d")
            p2.socket.send(b"d")
            continue

        winner = None
        looser = None
        if p1.play == b"s":
            if p2.play == b"p":
                winner = p1
                looser = p2
            else:
                winner = p2
                looser = p1
        elif p1.play == b"r":
            if p2.play == b"s":
                winner = p1
                looser = p2
            else:
                winner = p2
                looser = p1
        else:
            if p2.play == b"r":
                winner = p1
                looser = p2
            else:
                winner = p2
                looser = p1

        print(f"{winner.name} won !")
        winner.score += 1

        winner.socket.send(b"w")
        looser.socket.send(b"l")

    p1.socket.send(b"e")
    p1.socket.close()
    p2.socket.send(b"e")
    p2.socket.close()
    print("Match is over.")
    print(f"{p1.name} score is {p1.score}")
    print(f"{p2.name} score is {p2.score}")

if __name__ == "__main__":
    server = socket()
    try:
        main(server)
    except Exception as exc:
        print(exc)
    finally:
        server.close()

