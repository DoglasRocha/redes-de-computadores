from socket import socket, AF_INET, SOCK_STREAM
from hashlib import md5
from os import makedirs, path


def chat(client_socket: socket) -> None:
    client_socket.send(b"CHAT")

    # waits server reponse
    response: bytes = client_socket.recv(1024)

    # sends message
    message: str = input("O que você deseja dizer ao servidor?\n\t> ")

    client_socket.send(message[:1024].encode())

    server_response: bytes = client_socket.recv(1024)
    print(f"O servidor diz:\n\t> {server_response.decode()}")


def unpack_data_packet(
    packet: bytes, hash_init: int, hash_end: int
) -> tuple[bytes, bytes, bytes]:
    packet_number = packet[0:3]
    part_checksum = packet[hash_init:hash_end]
    data = packet[hash_end + 1 :]

    return packet_number, part_checksum, data


def receive_file(client_socket: socket) -> None:
    file_data = client_socket.recv(1024).decode().split(" ")

    n_packets = None
    if file_data[0] == "ERROR":
        print("Aconteceu um erro: ", " ".join(file_data[1:]))
        return

    if file_data[0] == "OK":
        n_packets = file_data[1]
        buffer_size = file_data[2]
        filename = file_data[3]
        checksum = file_data[4]
        client_socket.send(b"OK")

        n_digits = len(str(n_packets))
        hash_init = n_digits + 1
        hash_end = hash_init + 16

        makedirs("./destination", exist_ok=True)
        full_checksum = md5()
        with open(path.join("./destination", filename), "wb") as file:
            for i in range(0, int(n_packets)):
                packet = client_socket.recv(int(buffer_size))
                if packet[0:3] == b"END":
                    break

                packet_number, part_checksum, data = unpack_data_packet(
                    packet, hash_init, hash_end
                )

                while md5(data).digest() != part_checksum:
                    client_socket.send(b"NOK")
                    packet = client_socket.recv(int(buffer_size))
                    packet_number, part_checksum, data = unpack_data_packet(
                        packet, hash_init, hash_end
                    )

                full_checksum.update(data)
                file.write(data)
                client_socket.send(b"OK")

        if full_checksum.hexdigest() == checksum:
            print("Arquivo transferido com sucesso!")
        else:
            print("A transferência de arquivo não teve sucesso!!!")


def get_file(client_socket: socket) -> None:
    client_socket.send(b"ARQUIVO")

    resp_available_files_count: bytes = client_socket.recv(1024)

    client_socket.send(b"OK")

    print("\n")
    for i in range(int(resp_available_files_count.decode())):
        print(client_socket.recv(1024).decode())

    file_to_receive: str = input("Qual o número do arquivo que você deseja receber? ")
    client_socket.send(b" ".join([b"GET", file_to_receive.encode()]))

    receive_file(client_socket)


def close_connection(client_socket: socket) -> None:
    client_socket.send(b"SAIR")
    response: bytes = client_socket.recv(1024)
    if response == b"FECHADO":
        print("Conexão com servidor fechada.")
        return

    print("Erro ao fechar conexão.")


def run_ops(client_socket: socket) -> None:
    option: str = input(
        "\n\nO que você deseja fazer?\n"
        + "1) Sair\n"
        + "2) Receber arquivo\n"
        + "3) Chat\n"
    )

    match option:
        case "1":
            close_connection(client_socket)

        case "2":
            get_file(client_socket)
            run_ops(client_socket)

        case "3":
            chat(client_socket)
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
