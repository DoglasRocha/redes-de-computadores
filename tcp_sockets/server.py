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


def close_connection(clientSocket: socket, addr_: str) -> bool:
    logger.info(f"Fechando conexão com {addr_}")
    clientSocket.send(b"FECHADO")
    clientSocket.close()

    return True


def handle_request(clientSocket: socket, addr_: str) -> None:
    logger.info(f"Aceitando conexão com endereço: {addr_}")
    while True:
        message = clientSocket.recv(1024)
        request = message.decode().split()

        if len(request) <= 0:
            logger.warning(f"Má requsição de {addr_}")
            clientSocket.send("ERROR Má requisição".encode())
            clientSocket.send(b"FECHADO")
            clientSocket.close()
            return

        operation: str = request[0]
        operation_opts: dict = {
            "SAIR": close_connection,
            "ARQUIVO": lambda x: x,
            "CHAT": lambda x: x,
        }
        if operation not in operation_opts.keys():
            clientSocket.send("ERROR Método não permitido".encode())
            clientSocket.send(b"FECHADO")
            clientSocket.close()
            return

        if operation_opts[operation](clientSocket, addr_):
            return

    # filename = request[1]
    # splitted_filename = filename.split("/")
    # if len(splitted_filename) > 1:
    #     send_file_part(clientSocket, splitted_filename[0], splitted_filename[1])
    # else:
    #     send_full_file(clientSocket, filename)

    # clientSocket.close()


def run_server() -> None:
    NAME = "127.0.0.1"
    PORT = 8065

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((NAME, PORT))

    serverSocket.listen()
    logger.info(f"Socket escutando em {NAME}:{PORT}")
    print(f"Socket escutando em {NAME}:{PORT}")

    while True:
        clientSocket, addr = serverSocket.accept()

        thread = Thread(target=handle_request, args=(clientSocket, addr), daemon=True)
        thread.start()


if __name__ == "__main__":
    run_server()
