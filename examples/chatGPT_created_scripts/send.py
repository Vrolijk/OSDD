import os
import socket
from fec import Fec

## read file and get its contents
file_name = input("Enter the name of the file to read: ")
if not os.path.exists(file_name):
print("File does not exist")
else:
with open(file_name, "r") as file:
file_contents = file.readlines()

## create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

## create FEC object with desired parameters
fec = Fec(k=len(file_contents), n=len(file_contents) + 2)

encode file contents using FEC
encoded_data = fec.encode(file_contents)

## send each line of encoded data over UDP socket
for data in encoded_data:
sock.sendto(data, ("localhost", 12345))

## close the socket
sock.close()

print("File contents sent successfully!")
