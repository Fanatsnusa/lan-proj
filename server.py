import socket
from pathlib import Path
from prot import receive_message,receive_file

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("127.0.0.1",5000))
server.listen()
server.settimeout(1.0)
max_message_size = 64*1024
print("Ожидание подключения на 127.0.0.1:5000")

shared_dir= Path(__file__).resolve().parent / "shared"
shared_dir.mkdir(exist_ok=True)

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
                if data == b"":
                    print("Клиент завершил соединение")
                    break
                if len(data) > max_message_size:
                    connection.sendall("ERROR TOO_LARGE\n".encode("utf-8"))
                    print("сообщение превышает лимит")
                    break
                elif data.endswith(b"\n"):
                    try:
                        enddata= data[:-1].decode("utf-8")
                    except UnicodeDecodeError:
                        print("Error decoding")
                        connection.sendall("Error invalid_utf8\n".encode("utf-8"))
                        continue
                    parts=enddata.split()
                    if len(parts)==3 and parts[0] == "FILE" and parts[1].isdigit() and parts[1].isascii():
                        size=int(parts[1])
                        extension = parts[2]
                        print("Пользователь хочет отправить файл весом: ",size)
                        connection.sendall("Ok File_header\n".encode("utf-8"))
                        file,buffer=receive_file(connection,size,buffer)
                        if len(file) < size:
                            print("Файл битый")
                            break
                        accepted= shared_dir / f"received{extension}"
                        written= accepted.write_bytes(file)
                        connection.sendall("OK FILE SAVED\n".encode("utf-8"))
                        print("File accepted")
                        continue
                    connection.sendall("OK\n".encode("utf-8"))
                    print("Получено:", enddata)
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