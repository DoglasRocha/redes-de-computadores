from socket import socket, AF_INET, SOCK_STREAM
from random import randint
from time import sleep
from threading import Thread
from hashlib import md5
from typing import Any
from math import ceil
import logging
import os


logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="server.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s: %(message)s",
)

NAME = "127.0.0.1"
PORT = 8065

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((NAME, PORT))

serverSocket.listen()
logger.info(f"Socket escutando em {NAME}:{PORT}")
print(f"Socket escutando em {NAME}:{PORT}")


def send_file_part(returnSocket: socket, filename: str, part: str) -> None:
    if not os.path.exists(os.path.join("./files", filename)):
        returnSocket.send("ERROR Arquivo não encontrado".encode())
        return

    n_packets = ceil(os.path.getsize(os.path.join("./files", filename)) / 1024)

    n_digits = len(str(n_packets))
    if int(part) > n_packets - 1:
        returnSocket.send("ERROR Pacote não existe".encode())

    with open(os.path.join("./files", filename), "rb") as file:
        i = 0
        while data := file.read(1024):
            if int(part) == i:
                hash_ = md5(data).digest()
                returnSocket.send(
                    b" ".join([f"{i:{'0'}{n_digits}}".encode(), hash_, data])
                )
                break
            i += 1


def send_full_file(returnSocket: socket, filename: str) -> None:
    if not os.path.exists(os.path.join("./files", filename)):
        returnSocket.send("ERROR Arquivo não encontrado".encode())
        return

    n_packets = ceil(os.path.getsize(os.path.join("./files", filename)) / 1024)

    n_digits = len(str(n_packets))

    returnSocket.send(f"OK {n_packets} {n_digits+1+16+1+1024}".encode())
    with open(os.path.join("./files", filename), "rb") as file:
        i = 0
        while data := file.read(1024):
            hash_ = md5(data).digest()
            returnSocket.send(b" ".join([f"{i:{'0'}{n_digits}}".encode(), hash_, data]))
            i += 1

    sleep(1)
    returnSocket.send(b"END")


def handle_request(clientSocket: socket, addr_: str) -> None:
    message = clientSocket.recv(1024)

    request = message.decode()
    logger.info(f"Requisição: '{request}'")

    request = request.split()
    if len(request) <= 1:
        clientSocket.send("ERROR Má requisição".encode())
        return

    if request[0] != "GET":
        clientSocket.send("ERROR Método não permitido".encode())
        return

    filename = request[1]
    splitted_filename = filename.split("/")
    if len(splitted_filename) > 1:
        send_file_part(clientSocket, splitted_filename[0], splitted_filename[1])
    else:
        send_full_file(clientSocket, filename)

    clientSocket.close()


while True:
    clientSocket, addr = serverSocket.accept()

    thread = Thread(target=handle_request, args=(clientSocket, addr), daemon=True)
    thread.start()
