#!/usr/bin/env python3

import time
from client_thread import ClientThread

# Setup receiver listening on port 5005
receiver = ClientThread(name='Receiver', host_ip='127.0.0.1', port_addr=5005)

# Define what to do with incoming messages
def handle_received_message(message):
    print(f"[RECEIVER] Received: {message}")

# Register event handler
receiver.recieveEvent.on("recieve_packet", handle_received_message)

# Start the receiver thread
receiver.start()

print("[RECEIVER] Listening for messages on port 5005...")

# Keep the main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[RECEIVER] Stopped by user.")
