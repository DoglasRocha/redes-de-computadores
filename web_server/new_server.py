from app import App
from socket import socket

server = App()


@server.set_route("/", "GET")
def index():
    with open("./files/page1.html", "rb") as file:
        while data := file.read(1024):
            yield data


@server.set_route("/oi", "GET")
def oi(socket: socket):
    pass


@server.set_route("kkk", "POST")
def kkk(socket: socket):
    pass


server.run()
