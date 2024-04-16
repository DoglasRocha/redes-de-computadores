from socket import socket, AF_INET, SOCK_DGRAM
from random import randint
from time import sleep
from threading import Thread
from hashlib import md5
from typing import Any
import logging
import os


logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="server.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s: %(message)s",
)

NAME = ""
PORT = 8065

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((NAME, PORT))
PORTS_IN_USE = [
    8065,
]


def send_file_part(
    returnSocket: socket, filename: str, part: str, address: Any
) -> None:
    if not os.path.exists(os.path.join("./files", filename)):
        returnSocket.sendto("ERROR Arquivo não encontrado".encode(), address)
        return

    n_packets = (os.path.getsize(os.path.join("./files", filename)) // 1024) + 1

    n_digits = len(str(n_packets))
    if int(part) > n_packets - 1:
        returnSocket.sendto("ERROR Pacote não existe".encode(), address)

    with open(os.path.join("./files", filename), "rb") as file:
        i = 0
        while data := file.read(1024):
            if int(part) == i:
                hash_ = md5(data).digest()
                returnSocket.sendto(
                    b" ".join([f"{i:{'0'}{n_digits}}".encode(), hash_, data]), address
                )
                break
            i += 1


def send_full_file(returnSocket: socket, filename: str, address: Any) -> None:
    if not os.path.exists(os.path.join("./files", filename)):
        returnSocket.sendto("ERROR Arquivo não encontrado".encode(), address)
        return

    n_packets = (os.path.getsize(os.path.join("./files", filename)) // 1024) + 1

    n_digits = len(str(n_packets))

    returnSocket.sendto(f"OK {n_packets} {n_digits+1+16+1+1024}".encode(), address)
    with open(os.path.join("./files", filename), "rb") as file:
        i = 0
        while data := file.read(1024):
            hash_ = md5(data).digest()
            returnSocket.sendto(
                b" ".join([f"{i:{'0'}{n_digits}}".encode(), hash_, data]), address
            )
            i += 1

    sleep(1)
    returnSocket.sendto(b"END", address)


def handle_request(message_: bytes, addr_: str) -> None:
    request = message_.decode().split()

    returnSocket = socket(AF_INET, SOCK_DGRAM)
    random_port = randint(PORT + 1, PORT + 6001)
    while random_port in PORTS_IN_USE:
        random_port = randint(PORT + 1, PORT + 6001)

    PORTS_IN_USE.append(random_port)
    returnSocket.bind((NAME, random_port))

    logger.info(
        f"Requisição: '{message.decode()}', socket criado na porta: {random_port}"
    )

    if len(request) <= 1:
        returnSocket.sendto("ERROR Má requisição".encode(), addr_)
        return

    if request[0] != "GET":
        returnSocket.sendto("ERROR Método não permitido".encode(), addr_)
        return

    filename = request[1]
    splitted_filename = filename.split("/")
    if len(splitted_filename) > 1:
        send_file_part(returnSocket, splitted_filename[0], splitted_filename[1], addr_)
    else:
        send_full_file(returnSocket, filename, addr_)

    PORTS_IN_USE.remove(random_port)
    returnSocket.close()


while True:
    message, addr = serverSocket.recvfrom(1024)

    thread = Thread(target=handle_request, args=(message, addr), daemon=True)
    thread.start()
