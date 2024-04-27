import logging
from socket import socket, AF_INET, SOCK_STREAM
from typing import Callable
from threading import Thread

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="server.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s: %(message)s",
)


class App:
    def __init__(self) -> None:
        self.__NAME = "127.0.0.1"
        self.__PORT = 8065

        self.__socket: socket = socket(AF_INET, SOCK_STREAM)
        self.__socket.bind((self.__NAME, self.__PORT))
        self.__methods: set = set()
        self.__routes: set = set()
        self.__binds: dict = {}

    def set_route(self, route: str, method: str) -> Callable:
        self.__routes.add(route)
        self.__methods.add(method)

        if method not in self.__binds.keys():
            self.__binds[method] = {}

        def decorator(route_handler: Callable) -> None:
            self.__binds[method][route] = route_handler

        return decorator

    def _404_handler(self) -> None:
        pass

    def method_not_allowed_handler(self) -> None:
        pass

    def handle_requests(self, client_socket: socket, addr: str) -> None:
        logger.info(f"Aceitando conexão com: {addr}")
        brute_request = client_socket.recv(1024)
        request = brute_request.decode()
        logger.info(f"Requisição de {addr}: {request}")

        tokens = request.split()
        method = tokens[0]
        route = tokens[1]

        if route not in self.__routes:
            self._404_handler()
            return

        if method not in self.__methods or route not in self.__binds[method]:
            self.method_not_allowed_handler()
            return

        header = b"HTTP/1.1 200 OK\r\nServer: oiiiikkkkk\r\n"
        client_socket.send(header)
        data = self.__binds[method][route]()
        for piece in data:
            client_socket.send(data)

    def run(self) -> None:
        # print(f"{self.__routes=}", f"{self.__methods=}", f"{self.__binds}", sep="\n")

        self.__socket.listen()
        logger.info(f"Socket escutando em {self.__NAME}:{self.__PORT}")
        print(f"Socket escutando em {self.__NAME}:{self.__PORT}")

        while True:
            client_socket, addr = self.__socket.accept()

            thread = Thread(
                target=self.handle_requests, args=(client_socket, addr), daemon=True
            )
            thread.start()
