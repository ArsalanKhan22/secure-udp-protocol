#!/usr/bin/env python3

import socket
import threading
from pymitter import EventEmitter
from Cryptodome.Cipher import AES
import scrypt
import os
import crc16
import ast


class ClientThread(threading.Thread):
    def __init__(self, name='', host_ip='', port_addr=0, *args, **kwargs):
        super().__init__()
        self.name = name
        self.host_ip = host_ip
        self.port_addr = port_addr
        self.recieveEvent = EventEmitter()
        self.password = b's3kr3t@Sw4rM_p4ssw0rd'

    def encrypt_AES_GCM(self, msg, password):
        kdfSalt = os.urandom(16)
        secretKey = scrypt.hash(password, kdfSalt, N=16384, r=8, p=1, buflen=32)
        aesCipher = AES.new(secretKey, AES.MODE_GCM)
        ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
        return (kdfSalt, ciphertext, aesCipher.nonce, authTag)

    def decrypt_AES_GCM(self, encryptedMsg, password):
        (kdfSalt, ciphertext, nonce, authTag) = encryptedMsg
        secretKey = scrypt.hash(password, kdfSalt, N=16384, r=8, p=1, buflen=32)
        aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
        plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
        return plaintext

    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.s.bind(("", self.port_addr))

        packetCounter = {}
        packetLoss = {}

        while True:
            try:
                encrpytedMsg = self.s.recv(4096)
                encrpytedMsg = encrpytedMsg.decode('utf-8')
                encrpytedMsg = ast.literal_eval(encrpytedMsg)  # Convert string to list
                msg1 = self.decrypt_AES_GCM(encrpytedMsg, self.password)
                msg1 = msg1.decode('utf-8')

                message, crc_rec = msg1.split("*")
                rec_message, rec_counter, rec_name = message.split("_")
                crc_cal = crc16.crc16xmodem(message.encode())

                if crc_cal == int(crc_rec) and rec_message:
                    if rec_name not in packetCounter:
                        packetCounter[rec_name] = 1
                        packetLoss[rec_name] = packetCounter[rec_name] - int(rec_counter)
                        if packetLoss[rec_name] < 0:
                            packetLoss[rec_name] = 0
                    else:
                        packetCounter[rec_name] += 1
                        packetLoss[rec_name] = packetCounter[rec_name] - int(rec_counter)
                        if packetLoss[rec_name] < 0:
                            packetLoss[rec_name] = 0

                    self.recieveEvent.emit("recieve_packet", rec_message)

            except Exception:
                # Fail silently or allow user to handle via subclassing or adding error event
                continue

    def sendData(self, data):
        if not hasattr(self, 's'):
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        encryptedData = self.encrypt_AES_GCM(data, self.password)
        encryptList = [i for i in encryptedData]
        encryptedData = bytearray(str(encryptList), 'utf-8')
        self.s.sendto(encryptedData, (self.host_ip, self.port_addr))
