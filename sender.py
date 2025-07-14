#!/usr/bin/env python3

import time
import crc16
from client_thread import ClientThread

# Setup sender targeting localhost:5005
sender = ClientThread(name='Sender', host_ip='127.0.0.1', port_addr=5005)

# Send 5 test messages
try:
    for i in range(1, 10):
        message_body = f"Hello_{i}_Sender"  # Format: content_counter_clientID
        crc = str(crc16.crc16xmodem(message_body.encode()))
        full_message = f"{message_body}*{crc}"
        sender.sendData(full_message.encode('utf-8'))
        print(f"[SENDER] Sent: {full_message}")
        time.sleep(1)

except KeyboardInterrupt:
    print("\n[SENDER] Stopped by user.")
