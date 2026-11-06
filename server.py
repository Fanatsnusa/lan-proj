import socket

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("127.0.0.1",5000))
server.listen()
server.settimeout(1.0)
max_message_size = 64*1024

try:
    while True:
        try:
            connection,address = server.accept()
            print("подключился клиент:", address)

        except socket.timeout:
            continue

        connection.settimeout(30)
        try:
            data = b""
            while not data.endswith(b"\n"):
                chunk= connection.recv(1024)

                if chunk == b"":
                    break
                data += chunk
                if len(data) > max_message_size:
                    break
            if len(data) > max_message_size:
                print("сообщение превышает лимит")
            elif data.endswith(b"\n"):
                connection.sendall("Получил".encode("utf-8"))
                print("Получено:", data[:-1].decode("utf-8"))
            else:
                print("Клиент отключился до конца сообщения")
        except socket.timeout:
            print("Клиент молчит")
        finally:    
            connection.close()

except KeyboardInterrupt:
    print("server stop")

finally:
    server.close()