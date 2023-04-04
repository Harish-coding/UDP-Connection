# UDP Connection

## Description

There are 3 programs involved in this project - Alice, UnreliNET, and Bob. Alice will send chat messages to Bob over UDP and Bob may provide feedback as neccessary. The `UnreliNET` program is used to simulate the unreliable transmission channel in both directions, that randomly corrupt or drop packets, but always delivers packets in order.

To run UnreliNET run the folloing command:
```
java UnreliNET <P_DATA_CORRUPT> <P_DATA_LOSS> <P_ACK_CORRUPT> <P_ACK_LOSS> <UnreliNetPort> <rcvPort>
```
The first four arguments can take values between 0 and 0.3.

Alice reads a input messages that would be no larger than 5000 bytes, and pass on to UnreliNET. 

Bob receives messages from Alice via UnreliNET and prints them to standard output. It may also send feedback packets to Alice via UnreliNET. Bob only prints messages that are correctly received from Alice.

Since UDP transmission is unreliable, sequence number and checksum mechanisms are implmented and are included in the header fields. Additionaly, Alice has a timer for unacknowledged packets at 50ms.

## Testing

Make sure the programs and test folder are in the same directory, and then run the following command:

```
bash test/RunTest.sh
```

If you want to test the server manually, please select a port number greater than 1024, as OS usually restricts usage of ports lower than 1024. if you get a `BindException: Address already in use` or similar please try a differetn port number.

For convenience of testing, you can use the file redirection feature to let `Alice` read from a file rather than form keyboard input. 

```
python3 Alice.py <unreliNetPort> < input.txt
```

Similarly, you can also let `Bob` output to a file.

```
python3 Bob.py <rcvPort> > output.txt
```

Finally you can compare input.txt and output.txt as follows.

```
cmp input.txt output.txt
```

To run this, you must first launch Bob, followed by UnrelNET in the second window, and launch Alice in third window to start data transmission.


