from socket import *
import sys
import zlib

unReliPort = int(sys.argv[1])

divider = b'x  x'

# computes checksum
def checksum(byte):
    return zlib.crc32(byte)

# create a socket
bobSocket = socket(AF_INET, SOCK_DGRAM)
bobSocket.bind(('', unReliPort))

# ack of previous packet
prev_ack = b''

while True:
    # wait from packet from UnReliNET
    message, senderAddress = bobSocket.recvfrom(64)

    # if no message is received, break the loop
    if (len(message) == 0):
        break

    # message <- divided into seq, checksum, content
    ack_pos = message.find(divider)
    ack = message[:ack_pos]

    message = message[ack_pos + len(divider):]

    checksum_pos = message.find(divider)
    checksumValue = int.from_bytes(message[:checksum_pos], "big")

    # content
    message = message[checksum_pos + len(divider):]

    # first check if the packet is corrupt
    if checksum(message) == checksumValue:
        # check if the packet is a duplicate
        if ack != prev_ack:
            # if not a duplicate packet, print the content and update prev_ack
            sys.stdout.buffer.write(message)
            sys.stdout.buffer.flush()    
            prev_ack = ack

        bobSocket.sendto(checksum(ack).to_bytes(4, "big") + divider + ack, senderAddress)
    else:
        bobSocket.sendto(checksum(prev_ack).to_bytes(4, "big") + divider + prev_ack, senderAddress)

# close socket after all the message has been written to standard out
bobSocket.close()

