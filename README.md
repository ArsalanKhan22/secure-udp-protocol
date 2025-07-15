# 🔐 Secure UDP Communication (AES + CRC16)

A lightweight Python-based communication module using **AES-GCM encryption** and **CRC16 checksum validation** over **UDP sockets**. This project includes both a sender and receiver implementation and can be used as a library for secure communication between devices or processes.

## 📦 Features

- 🔒 AES-GCM encryption for confidentiality and integrity
- ✅ CRC16-XMODEM checksum validation
- 📡 UDP socket support with optional broadcasting
- 🔄 Threaded receiver with non-blocking design
- 🧱 Designed as a reusable class for library-style usage
- 📩 EventEmitter-based message callback system

---

## 🚀 Getting Started

### 📁 Clone the Repository

```bash
git clone https://github.com/arsalankhan22/secure-udp-comm.git
cd secure-udp-comm
```

### 🐍 Install Dependencies
pip install pycryptodomex pymitter scrypt crc16


### 🔄 Example Message Format

Each message has the format:

```bash
<content>_<counter>_<senderID>*<crc16>
```

### 📚 How to Use as a Library

```bash
from client_thread import ClientThread

def on_message(msg):
    print("Received:", msg)

receiver = ClientThread(name="Receiver", host_ip='127.0.0.1', port_addr=5005)
receiver.recieveEvent.on("recieve_packet", on_message)
receiver.start()
```
