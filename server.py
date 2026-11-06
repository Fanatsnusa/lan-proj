import socket

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(("127.0.0.1",5000))

server.listen()

print("Server prinimaet")

connection,address = server.accept()

data = connection.recv(1024)

connection.sendall('Получил'.encode("utf-8"))

print("Получено:", data.decode("utf-8"))

print("подключился клиент:", address)

input("Enter — завершить сервер")