from socket import socket, AF_INET, SOCK_DGRAM

SERVERNAME = "127.0.0.1"
PORT = 8065
ADDR = (SERVERNAME, PORT)

clientSocket = socket(AF_INET, SOCK_DGRAM)

filename = input("Qual o nome do arquivo que você deseja receber? ")
clientSocket.sendto(f"GET {filename}".encode(), ADDR)

brute_response = clientSocket.recvfrom(1024)
message, addr = brute_response
response = message.decode().split(" ")


if response[0] == "ERROR":
    print("Aconteceu um erro: ", response[1])

else:
    if response[0] == "OK":

        n_packets = response[1]
        buffer_size = response[2]
        lost = []

        brute_response = clientSocket.recvfrom(int(buffer_size))
        buffer = []
        # ...
        for i in range(0, int(n_packets)):
            message, addr = brute_response
            buffer.append(message)

            if message.decode().split()[0] == "END":
                break

            brute_response = clientSocket.recvfrom(int(buffer_size))

    file = open(filename, "wb")
    n_digits = len(str(n_packets))
    for message in buffer:
        header = message[0 : n_digits + 1]
        data = message[n_digits + 2 :]

        if i != int(header.decode()):
            print(i)
            lost.append(i)

        print(data)
        # text = " ".join(response[1:])

        # print(f"{text=}")
        # clean_text = text.replace("b'", "").replace("'", "").replace('b"', "")
        # print(f"{clean_text=}")
        file.write(data[1:-1])
        # file.write(bytes(clean_text, encoding="utf-8"))

    print(lost)
    file.close()
clientSocket.close()
