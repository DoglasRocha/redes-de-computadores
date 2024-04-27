from socket import socket, AF_INET, SOCK_STREAM
from random import randint
from time import sleep
from threading import Thread
from hashlib import md5
from typing import Any
from math import ceil, floor
import logging
import os


logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="server.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s: %(message)s",
)


def chat(client_socket: socket, addr_: str) -> None:
    client_socket.send(b"OK")

    print("\n")
    client_message_bytes: bytes = client_socket.recv(1024)
    print(f"{addr_} diz:\n\t> {client_message_bytes.decode()}")

    response = input("O que você deseja dizer ao cliente?\n\t> ")
    client_socket.send(response.encode())
    print("\n")


def get_file_checksum(filename: str) -> str:
    checksum = md5()
    with open(os.path.join("./files", filename), "rb") as file:
        while data := file.read(8192):
            checksum.update(data)

    return checksum.hexdigest()


def send_full_file(returnSocket: socket, filename: str, addr_: str) -> None:
    if not os.path.isfile(os.path.join("./files", filename)):
        returnSocket.send("ERROR Arquivo não encontrado".encode())
        return

    logger.info(f"Mandando arquivo {filename} para {addr_}")
    n_packets: int = ceil(os.path.getsize(os.path.join("./files", filename)) / 1024)
    n_digits: int = len(str(n_packets))
    checksum: str = get_file_checksum(filename)

    returnSocket.send(
        f"OK {n_packets} {n_digits+1+16+1+1024} {filename} {checksum}".encode()
    )
    confirmation: bytes = returnSocket.recv(1024)

    with open(os.path.join("./files", filename), "rb") as file:
        i = 0
        while data := file.read(1024):
            hash_ = md5(data).digest()
            returnSocket.send(b" ".join([f"{i:{'0'}{n_digits}}".encode(), hash_, data]))
            while returnSocket.recv(1024) == b"NOK":
                returnSocket.send(
                    b" ".join([f"{i:{'0'}{n_digits}}".encode(), hash_, data])
                )
            i += 1


def send_file(clientSocket: socket, addr_: str) -> bool:
    logger.info(f"Mandando arquivo para {addr_}")
    available_files: list[str] = os.listdir("./files")

    # sends file names
    long_string: str = "".join(
        f"{index}) {name}\n" for index, name in enumerate(available_files)
    )

    # sends packet count
    n_packets: int = ceil(len(long_string) / 1024)
    clientSocket.send(f"{n_packets}".encode())

    # waits confirmation
    confirmation: bytes = clientSocket.recv(1024)
    if confirmation != b"OK":
        return close_connection(clientSocket, addr_)

    for i in range(n_packets):
        clientSocket.send(long_string[1024 * i : 1024 * (i + 1)].encode())

    # gets desired file from client
    file_request: bytes = clientSocket.recv(1024)

    n_file = int(file_request.decode().split(" ")[-1])
    send_full_file(
        clientSocket,
        (
            ""
            if n_file >= len(available_files) or n_file < 0
            else available_files[n_file]
        ),
        addr_,
    )


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
            "ARQUIVO": send_file,
            "CHAT": chat,
        }
        if operation not in operation_opts.keys():
            clientSocket.send("ERROR Método não permitido".encode())
            clientSocket.send(b"FECHADO")
            clientSocket.close()
            return

        if operation_opts[operation](clientSocket, addr_):
            return


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
