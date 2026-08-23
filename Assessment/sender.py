import socket

SERVER = "127.0.0.1"
PORT = 6000

sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender.settimeout(2)

message = input("Enter message: ")

# Divide message into packets
packet_size = 5
packets = [
    message[i:i + packet_size]
    for i in range(0, len(message), packet_size)
]

for seq, data in enumerate(packets):
    packet = f"{seq}|{data}".encode()

    while True:
        try:
            print(f"Sending packet {seq}: {data}")

            sender.sendto(packet, (SERVER, PORT))

            ack, addr = sender.recvfrom(1024)
            ack = ack.decode()

            ack_type, ack_seq = ack.split("|")

            if ack_type == "ACK" and int(ack_seq) == seq:
                print(f"ACK received for packet {seq}\n")
                break

        except socket.timeout:
            print(f"Timeout! Retransmitting packet {seq}...\n")

# Tell receiver transmission is complete
sender.sendto(b"END", (SERVER, PORT))

print("All packets transmitted successfully.")

sender.close()