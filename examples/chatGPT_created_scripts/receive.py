import socket
from fec import Fec

create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

bind the socket to a port
sock.bind(("localhost", 12345))

receive encoded data from sender
data, addr = sock.recvfrom(1024)
encoded_data = []
while data:
encoded_data.append(data)
data, addr = sock.recvfrom(1024)

create FEC object with same parameters as sender
fec = Fec(k=len(encoded_data), n=len(encoded_data) + 2)

decode the received data using FEC
decoded_data = fec.decode(encoded_data)

write decoded data to file
with open("received_file.txt", "w") as file:
file.write("".join(decoded_data))

close the socket
sock.close()

print("File received and written successfully!")
