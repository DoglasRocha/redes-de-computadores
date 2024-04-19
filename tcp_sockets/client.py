from socket import socket, AF_INET, SOCK_STREAM
from hashlib import md5

SERVERNAME = "127.0.0.1"
PORT = 8065
ADDR = (SERVERNAME, PORT)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.settimeout(120)

filename = input("Qual o nome do arquivo que você deseja receber? ")
# try:
clientSocket.connect(ADDR)
clientSocket.send(f"GET {filename}".encode())

brute_response = clientSocket.recv(1024)
message = brute_response

n_packets = None
if message[0:5] == b"ERROR":
    response = message.decode().split(" ")
    print("Aconteceu um erro: ", " ".join(response[1:]))

else:
    if message[0:2] == b"OK":

        response = message.decode().split(" ")
        n_packets = response[1]
        buffer_size = response[2]
        buffer = []
        lost = []

        brute_response = clientSocket.recv(int(buffer_size))

        for i in range(0, int(n_packets)):
            message = brute_response
            if message[0:3] == b"END":
                break

            buffer.append(message)

            brute_response = clientSocket.recv(int(buffer_size))

    if n_packets is not None:
        file_array = [None for i in range(int(n_packets))]

        n_digits = len(str(n_packets))
        hash_init = n_digits + 1
        hash_end = hash_init + 16
        for packet in buffer:
            header = packet[0:n_digits]
            hash_ = packet[hash_init:hash_end]
            data = packet[hash_end + 1 :]

            if md5(data).digest() == hash_:
                file_array[int(header)] = data

        file = open(filename, "wb")
        for index, segment in enumerate(file_array):
            if segment is not None:
                file.write(segment)
            else:
                data = b"dkjasbda"
                hash_ = b"dasjbadskd"
                while md5(data).digest() != hash_:
                    clientSocket.send(f"GET {filename}/{index}".encode())
                    message = clientSocket.recv(int(buffer_size))
                    hash_ = message[hash_init:hash_end]
                    data = message[hash_end + 1 :]
                file.write(data)
        file.close()
        print("Arquivo transferido com sucesso!")

clientSocket.close()
# except TimeoutError:
#     print(
#         "Houve um erro de comunicação entre o servidor e o cliente. Tente novamente mais tarde."
#     )
# except Exception as e:
#     print(f"Erro! {e}")
