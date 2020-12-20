# -*- coding: utf-8 -*-

"""
Copyright (C) Zato Source s.r.o. https://zato.io

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

# stdlib
import logging
import socket
from socket import timeout as SocketTimeoutException

# Bunch
from bunch import bunchify

# Zato
from zato.common.util.api import parse_tcp_address
from zato.hl7.mllp.reader import SocketReader

# ################################################################################################################################

if 0:
    from bunch import Bunch
    from gevent._socket3 import socket

    Bunch = Bunch
    socket = socket

# ################################################################################################################################
# ################################################################################################################################

class Client:
    """ An HL7 MLLP client for sending data to remote endpoints.
    """
    __slots__ = 'config', 'name', 'address', 'max_wait_time', 'max_msg_size', 'should_log_messages', \
        'start_seq', 'end_seq', 'host', 'port', 'reader'

    def __init__(self, config):
        # type: (Bunch) -> None
        self.config = config
        self.name = config.name
        self.address = config.address
        self.max_wait_time = config.max_wait_time # type: float
        self.max_msg_size = config.max_msg_size # type: int
        self.should_log_messages = config.should_log_messages # type: bool

        self.start_seq = config.start_seq
        self.end_seq   = config.end_seq

        self.host, self.port = parse_tcp_address(self.address) # type (str, int)

        # This is used for reading responses from the server
        self.reader = SocketReader({
            'address': '<socket-reader-client-unused-address>',
            'name': self.name,
            'should_log_messages': self.should_log_messages,
            'logging_level': self.config.logging_level,
            'start_seq': self.start_seq,
            'end_seq': self.end_seq,
        })

    def send(self, data):
        # type: (bytes) -> bytes

        # Wrap the message in an MLLP envelope
        msg = self.start_seq + data + self.end_seq

        # This will auto-close the socket ..
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            # .. connect to the remote end ..
            sock.connect((self.host, self.port))

            # .. send our data ..
            sock.send(msg)

            # .. buffer that the response will be written to ..
            buffer = []

            # .. wait for response, if any ..
            self.reader.handle(
                sock,
                sock.getpeername(),
                self.max_wait_time,
                self.max_msg_size,
                self.config.read_buffer_size,
                self.config.recv_timeout,
                buffer
            )

            print(111, buffer)

# ################################################################################################################################
# ################################################################################################################################

def send_data(address, data):
    """ Sends input data to a remote address.
    """
    # type: (bytes, str) -> bytes

    config = bunchify({
        'name': 'My Client',
        'address': address,
        'start_seq': b'\x0b',
        'end_seq': b'\x1c\x0d',
        'max_wait_time': 0.5,
        'max_msg_size': 2_000_000,
        'read_buffer_size': 2048,
        'recv_timeout': 0.25,
        'logging_level': 'INFO',
        'should_log_messages': True,
    })

    client = Client(config)
    response = client.send(data)

    return response

# ################################################################################################################################
