from app import App
from socket import socket

server = App()


@server.set_route("/", "GET")
def index():
    with open("./pages/index.html", "rb") as file:
        while data := file.read(1024):
            yield data


@server.set_route("/spaceship", "GET")
def oi():
    with open("./pages/spaceship.html", "rb") as file:
        while data := file.read(1024):
            yield data


@server.set_route("/hireus", "GET")
def kkk():
    with open("./pages/hire_us.html", "rb") as file:
        while data := file.read(1024):
            yield data


server.run()
