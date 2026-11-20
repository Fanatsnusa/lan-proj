def receive_message(sock,max_size,buffer):
    data=buffer
    while b"\n" not in data:
        chunk=sock.recv(1024)
        if chunk == b"":
            break
        data += chunk 

        if len(data) > max_size:
            break

   
    message,separator,remainder = data.partition(b"\n")
    


    return message + separator, remainder


def receive_file(sock,size,buffer):
    file=buffer[:size]
    ost_mes=buffer[size:]
    while len(file) < size:
        chunk=sock.recv(min(1024,size-len(file)))
        if chunk == b"":
            break
        file+=chunk

    
    return file, ost_mes