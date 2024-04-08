from socket import socket, AF_INET, SOCK_DGRAM
from random import randint
from time import sleep
from threading import Thread
import os

NAME = ""
PORT = 8065

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((NAME, PORT))


def handle_request(message: bytes, addr: str) -> None:
    request = message.decode().split()

    returnSocket = socket(AF_INET, SOCK_DGRAM)
    returnSocket.bind((NAME, randint(PORT + 1, PORT + 6001)))

    if len(request) <= 1:
        returnSocket.sendto("ERROR-|-Má requisição".encode(), addr)
        return

    if request[0] != "GET":
        returnSocket.sendto("ERROR-|-Método não permitido".encode(), addr)
        return

    filename = request[1]
    if not os.path.exists(os.path.join("./files", filename)):
        returnSocket.sendto("ERROR-|-Arquivo não encontrado".encode(), addr)
        return

    n_packets = 0
    with open(os.path.join("./files", filename), "rb") as file:
        data = file.read(1024)
        while data:
            n_packets += 1
            data = file.read(1024)

    n_digits = len(str(n_packets))

    returnSocket.sendto(f"OK {n_packets} {n_digits+1+1024}".encode(), addr)
    with open(os.path.join("./files", filename), "rb") as file:
        i = 0
        data = file.read(1024)
        while data:
            returnSocket.sendto(
                b" ".join([f"{i:{'0'}{n_digits}}".encode(), data]), addr
            )
            i += 1

            data = file.read(1024)

    sleep(1)
    returnSocket.sendto(b"END", addr)


while True:
    message, addr = serverSocket.recvfrom(1024)

    thread = Thread(target=handle_request, args=(message, addr), daemon=True)
    thread.start()
