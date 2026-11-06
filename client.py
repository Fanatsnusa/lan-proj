import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1",5000))
print ("Подключился к серверу ")

message = input("Введи сообщение: ")

text= message + "\n"
data= text.encode("utf-8")

client.sendall(data)

data =client.recv(1024)

print(data.decode("utf-8"))

client.close()