import math
import random
import socket

import numpy as np

import mido

class Typhon:
    def __init__(self, callback, host='localhost', port=11586):
        self.n_samples_per_block = 0
        self.bufsize = 0 # how much data received per block
        self.recvsize = 8 # 8 + (self.n_samples_per_block * channels * bytes-per-data)
        self.msgid = None
        self.msglen = None
        self.last_data = None
        self.first_data_packet = True
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.callback = callback()
        
    def connect(self):
        self.sock.connect((self.host, self.port))
        self.recvd = self.sock.recv(8 + len(b'EHLO') + 5 + len(b'BYE'))
        assert self.recvd[8:12] == b'EHLO', "Did not get expected response on attempted connect"
        self.bpm = float(self.recvd[12:17])
        self.recvd = b''
        
    def go(self):
        while True:
            self.recvd += self.sock.recv(self.recvsize)
            if not self.recvd:
                return 0 # broke due to connection disrupted
            # TODO refactor this into 2 functions, 1 for first packet, then it switches to different func for subsequent.
            # so we don't need to always check for bufsize and first_data_packet.
            if not self.bufsize:
                self.msgid = self.recvd[0:4]
                self.msglen = self.recvd[4:8]
                self.bufsize = int.from_bytes(self.msglen, 'little')
                self.recvsize = self.bufsize
                continue
            if self.first_data_packet:
                self.first_data_packet = False
                self.recvsize += 8
            data = np.frombuffer(self.recvd[8:-300], dtype=np.int16)
            midi_data = np.frombuffer(self.recvd[-300:], dtype=np.uint8)
            data = (data / 32768).reshape(2, -1).astype(np.float32)
            reply, midi_reply = self.callback(data, midi_data, bpm=self.bpm, chunk_size=self.chunk_size)
            reply = reply.reshape(-1)
            reply = np.clip(reply, -1, 1)
            msg2 = (reply * 32768.0).astype(np.int16).tobytes()
            #msg2 = np.zeros_like(reply).astype(np.int16).tobytes()
            msg2 += midi_reply.astype(np.uint8).tobytes()
            msg = self.msgid + self.msglen + msg2
            if len(msg) == self.recvsize:
                self.sock.send(msg)
            self.recvd = b''

def midi_parser(midi_bytes):
    """Return bytes parsed into midi messages by Midi"""
    p = mido.Parser()
    p.feed(midi_bytes)
    return p.messages