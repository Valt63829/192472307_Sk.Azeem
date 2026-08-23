import socket
import random

HOST = "127.0.0.1"
PORT = 6000

receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver.bind((HOST, PORT))

print(f"Receiver listening on {HOST}:{PORT}")

packets = {}

while True:
    data, addr = receiver.recvfrom(1024)

    message = data.decode()

    if message == "END":
        print("\nAll packets received.")
        break

    seq, content = message.split("|", 1)
    seq = int(seq)

    # Simulate packet loss
    if random.random() < 0.2:
        print(f"Packet {seq} lost.")
        continue

    if seq in packets:
        print(f"Duplicate packet {seq} detected.")
    else:
        packets[seq] = content
        print(f"Received packet {seq}: {content}")

    # Send ACK
    receiver.sendto(f"ACK|{seq}".encode(), addr)

# Reassemble message
print("\nReassembled message:")

for seq in sorted(packets):
    print(packets[seq], end=" ")

print()

receiver.close()