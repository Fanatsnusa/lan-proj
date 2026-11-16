def receive_message(sock,max_size):
    data=b""
    while not data.endswith(b"\n"):
        chunk=sock.recv(1024)
        if chunk == b"":
            break
        data += chunk

        if len(data) > max_size:
            break

    return data