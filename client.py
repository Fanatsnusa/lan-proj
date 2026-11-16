import socket
import time
from prot import receive_message

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.settimeout(10)
    print("Подключаемся к серверу")
    client.connect(("127.0.0.1",5000))
    print ("Соединение установлено")

    message_max_size=64*1024
    buffer=b""

    while True:
        message = input("Введи сообщение: ")
        if message == "/exit":
            break

        text= message + "\n"
        data= text.encode("utf-8")

        started= time.perf_counter()
        client.sendall(data)

        data,buffer=receive_message(client,message_max_size,buffer)
        elapsed_ms=(time.perf_counter()-started)*1000
        print(f"[Время запроса]{elapsed_ms:.1f} мс")

        if len(data) > message_max_size:
            print("Сообщение от сервера слишком большое")
            break
        elif data.endswith(b"\n"):
            print(data[:-1].decode("utf-8"))
        else:
            print("Сервер закрыл соединение до конца ответа")
            break
except socket.timeout:
    print("Сервер не ответил вовремя")

except ConnectionRefusedError:
    print("Не удалось подключиться")

except ConnectionResetError:
    print("Соденинение оборвано")

finally:
    client.close()
    print("Сокет закрыт")