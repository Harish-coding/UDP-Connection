import zlib
import sys
from socket import *

# port number of UnreliNET
unReliPort = int(sys.argv[1])
unReliName = 'localhost'

MESSAGE = 0

divider = b'x  x'

# compute checksum
def checksum(byte):
    return zlib.crc32(byte)

# returns a array for bytes of appropriate size segments 
def segmentation(message):
    segments = ()
    while len(message) != 0:
        segment = message[:51]
        segments += (checksum(segment).to_bytes(4, "big") + divider + segment, )
        message = message[51:]
    return segments

# toggles  between 1 and 0
def toggle(num):
    return 1 if num == 0 else 0

# checks of the ack packet received is corrupt
def checkCorrupt(packet):
    pos = packet.find(divider)
    ack = packet[pos + len(divider):]
    checksumPacket = packet[:pos]
    return checksumPacket == checksum(ack).to_bytes(4, "big")

# obtains the ack from ack packet
def extractAck(packet):
    pos = packet.find(divider)
    ack = packet[pos + len(divider):]
    return ack

# create a socket
aliceSocket = socket(AF_INET, SOCK_DGRAM)

# read the input message
message = b''
text = sys.stdin.buffer.read1(1000)

while len(text) != 0:
    message += text
    text = sys.stdin.buffer.read1(1000)

# have to segment, and transmit
# seqNum is 1 bytes, checksum computed is 4 bytes, and 58 bytes for payload
# The sender packet format is as follows
# seqNum     -   1  byte
# divider    -   4  bytes
# checksum   -   4  bytes
# divider    -   4  bytes
# content    -   51 bytes

# sequence number of the current packet that is to be transmitted
seqNum = 0

# for each segment 
for seg in segmentation(message):

    # create a packet
    seqNumByte = seqNum.to_bytes(1, "big")
    packet = seqNumByte + divider + seg

    # indicates if the current seg is transmitted succesfully
    successful = False
    
    while not successful:
        try :
            aliceSocket.settimeout(0.05)
            aliceSocket.sendto(packet, (unReliName, unReliPort))
            ackReturn = aliceSocket.recvfrom(9)[MESSAGE]

            while not checkCorrupt(ackReturn) or extractAck(ackReturn) != seqNumByte:
                aliceSocket.settimeout(0.05)
                aliceSocket.sendto(packet, (unReliName, unReliPort))
                ackReturn = aliceSocket.recvfrom(9)[MESSAGE]

            successful = True
        
        except:
            continue

    seqNum = toggle(seqNum)

# close socket after sending message
aliceSocket.close()

