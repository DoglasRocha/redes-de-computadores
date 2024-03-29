from socket import socket, AF_INET, SOCK_DGRAM
import os

NAME = ""
PORT = 8065

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((NAME, PORT))
# serverSocket.listen(1)

while True:
    message, addr = serverSocket.recvfrom(1024)
    request = message.decode().split()

    if len(request) <= 1:
        serverSocket.sendto("ERROR-|-Má requisição".encode(), addr)
        continue

    if request[0] != "GET":
        serverSocket.sendto("ERROR-|-Método não permitido".encode(), addr)
        continue

    filename = request[1]
    if not os.path.exists(os.path.join("./files", filename)):
        serverSocket.sendto("ERROR-|-Arquivo não encontrado".encode(), addr)
        continue

    with open(os.path.join("./files", filename), "rb") as file:
        data = file.read()

    data_length = len(data)
    n_packets = data_length // 1024 + 1

    n_digits = len(str(n_packets))

    serverSocket.sendto(f"OK-|-{n_packets}-|-{n_digits+3+1024}".encode(), addr)
    for i in range(n_packets):
        serverSocket.sendto(
            f"{i:{'0'}{n_digits}}-|-{data[i * 1024 : (i + 1) * 1024]}".encode(), addr
        )
