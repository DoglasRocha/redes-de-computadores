from socket import socket, AF_INET, SOCK_DGRAM

SERVERNAME = "127.0.0.1"
PORT = 8065
ADDR = (SERVERNAME, PORT)

clientSocket = socket(AF_INET, SOCK_DGRAM)

filename = input("Qual o nome do arquivo que você deseja receber? ")
packet_to_drop = input("Qual pacote deseja jogar fora? (-1 para não jogar) ")
clientSocket.sendto(f"GET {filename}".encode(), ADDR)

brute_response = clientSocket.recvfrom(1024)
message, addr = brute_response

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

        brute_response = clientSocket.recvfrom(int(buffer_size))

        for i in range(0, int(n_packets)):
            message, addr = brute_response
            if message[0:3] == b"END":
                break

            if i != int(packet_to_drop):
                buffer.append(message)

            brute_response = clientSocket.recvfrom(int(buffer_size))

    if n_packets is not None:
        file_array = [None for i in range(int(n_packets))]

        n_digits = len(str(n_packets))
        for packet in buffer:
            header = packet[0:n_digits]
            data = packet[n_digits + 1 :]
            file_array[int(header)] = data

        file = open(filename, "wb")
        for index, segment in enumerate(file_array):
            if segment is not None:
                file.write(segment)
            else:
                clientSocket.sendto(f"GET {filename}/{index}".encode(), ADDR)
                message, addr = clientSocket.recvfrom(int(buffer_size))
                data = message[n_digits + 1 :]
                file.write(data)
        file.close()
clientSocket.close()
