import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1",5000))
print ("Подключился к серверу ")

message = input("Введи сообщение: ")

message_max_size=64*1024

text= message + "\n"
data= text.encode("utf-8")

client.sendall(data)


data=b""
while not data.endswith(b"\n"):
    chunk=client.recv(1024)
    if chunk == b"":
        break
    data += chunk

if data.endswith(b"\n"):
    print(data[:-1].decode("utf-8"))
else:
    print("Сервер закрыл соединение до конца ответа")

client.close()