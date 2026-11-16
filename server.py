import socket
from prot import receive_message

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("127.0.0.1",5000))
server.listen()
server.settimeout(1.0)
max_message_size = 64*1024
print("Ожидание подключения на 127.0.0.1:5000")

try:
    while True:
        try:
            connection,address = server.accept()
            print("Подключился клиент:", address)

        except socket.timeout:
            continue

        connection.settimeout(30)
        try:
            buffer=b""
            while True:
                data,buffer= receive_message(connection,max_message_size,buffer)
                if len(data) > max_message_size:
                    connection.sendall("ERROR TOO_LARGE\n".encode("utf-8"))
                    print("сообщение превышает лимит")
                    break
                elif data.endswith(b"\n"):
                    connection.sendall("OK\n".encode("utf-8"))
                    print("Получено:", data[:-1].decode("utf-8"))
                else:
                    print("Клиент отключился до конца сообщения")
                    break
        except socket.timeout:
            print("Клиент молчит")
            connection.sendall("ERROR TIMEOUT\n".encode("utf-8"))
        finally:    
            connection.close()
            print("Соединение закрыто")

except KeyboardInterrupt:
    print("Получена команда остановки")

finally:
    server.close()
    print("Сервер остановлен")