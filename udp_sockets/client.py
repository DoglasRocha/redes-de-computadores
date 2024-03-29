from socket import socket, AF_INET, SOCK_DGRAM

SERVERNAME = "127.0.0.1"
PORT = 8065
ADDR = (SERVERNAME, PORT)

clientSocket = socket(AF_INET, SOCK_DGRAM)

filename = input("Qual o nome do arquivo que você deseja receber? ")
clientSocket.sendto(f"GET {filename}".encode(), ADDR)

brute_response = clientSocket.recvfrom(1024)
message, addr = brute_response
response = message.decode().split("-|-")


if response[0] == "ERROR":
    print("Aconteceu um erro: ", response[1])

if response[0] == "OK":
    file = open(filename, "ab")

    n_packets = response[1]
    buffer_size = response[2]

    for i in range(int(buffer_size)):
        brute_response = clientSocket.recvfrom(1096)
        message, addr = brute_response
        response = message.decode().split("-|-")
        file.write(bytes(response[1][2:-1], encoding="utf-8"))

    file.close()

clientSocket.close()
