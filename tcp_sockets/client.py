from socket import socket, AF_INET, SOCK_STREAM
from hashlib import md5

# filename = input("Qual o nome do arquivo que você deseja receber? ")
# # try:

# clientSocket.send(f"GET {filename}".encode())

# brute_response = clientSocket.recv(1024)
# message = brute_response

# n_packets = None
# if message[0:5] == b"ERROR":
#     response = message.decode().split(" ")
#     print("Aconteceu um erro: ", " ".join(response[1:]))

# else:
#     if message[0:2] == b"OK":

#         response = message.decode().split(" ")
#         n_packets = response[1]
#         buffer_size = response[2]
#         buffer = []
#         lost = []

#         brute_response = clientSocket.recv(int(buffer_size))

#         for i in range(0, int(n_packets)):
#             message = brute_response
#             if message[0:3] == b"END":
#                 break

#             buffer.append(message)

#             brute_response = clientSocket.recv(int(buffer_size))

#     if n_packets is not None:
#         file_array = [None for i in range(int(n_packets))]

#         n_digits = len(str(n_packets))
#         hash_init = n_digits + 1
#         hash_end = hash_init + 16
#         for packet in buffer:
#             header = packet[0:n_digits]
#             hash_ = packet[hash_init:hash_end]
#             data = packet[hash_end + 1 :]

#             if md5(data).digest() == hash_:
#                 file_array[int(header)] = data

#         file = open(filename, "wb")
#         for index, segment in enumerate(file_array):
#             if segment is not None:
#                 file.write(segment)
#             else:
#                 data = b"dkjasbda"
#                 hash_ = b"dasjbadskd"
#                 while md5(data).digest() != hash_:
#                     clientSocket.send(f"GET {filename}/{index}".encode())
#                     message = clientSocket.recv(int(buffer_size))
#                     hash_ = message[hash_init:hash_end]
#                     data = message[hash_end + 1 :]
#                 file.write(data)
#         file.close()
#         print("Arquivo transferido com sucesso!")

# clientSocket.close()


def close_connection(client_socket: socket) -> None:
    client_socket.send(b"SAIR")
    response = client_socket.recv(1024)
    if response == b"FECHADO":
        print("Conexão com servidor fechada.")
        return

    print("Erro ao fechar conexão.")


def run_ops(client_socket: socket) -> None:
    option = input(
        "\n\nO que você deseja fazer?\n"
        + "1) Sair\n"
        + "2) Receber arquivo\n"
        + "3) Chat\n"
    )

    match option:
        case "1":
            close_connection(client_socket)

        case "2":
            run_ops(client_socket)

        case "3":
            run_ops(client_socket)

        case _:
            print("\nOpção inválida!!!!")
            run_ops(client_socket)


def run_client() -> None:
    SERVERNAME: str = "127.0.0.1"
    PORT: int = 8065
    ADDR: tuple[str, int] = (SERVERNAME, PORT)

    client_socket: socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)

    run_ops(client_socket)


if __name__ == "__main__":
    run_client()

# except TimeoutError:
#     print(
#         "Houve um erro de comunicação entre o servidor e o cliente. Tente novamente mais tarde."
#     )
# except Exception as e:
#     print(f"Erro! {e}")
