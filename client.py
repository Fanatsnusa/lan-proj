import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1",5000))

client.sendall("Privet".encode("utf-8"))

print ("Подключился к серверу ")

data =client.recv(1024)

print(data.decode("utf-8"))

input("Enter — закрыть соединение")

client.close()