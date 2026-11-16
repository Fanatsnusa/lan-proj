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

