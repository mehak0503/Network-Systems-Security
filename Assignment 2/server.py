import socket
import math
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS
from Crypto import Random
import random
from datetime import datetime
random.seed(datetime.now())

def create_send_socket():
    skt = socket.socket()
    skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    skt.bind(('127.0.0.1',38556))
    skt.listen(5)
    print "Server is listening on 38556"
    return skt


def encrypt(msg,key):
     cipher = PKCS1_OAEP.new(RSA.importKey(key))
     return cipher.encrypt(msg) 


def gen_keys():
    key = RSA.generate(4096)
    f = open('key_PKDA.pem', 'wb')
    f.write(key.exportKey('PEM'))
    f.close()

    key = RSA.generate(1024)
    f = open('key_A.pem', 'wb')
    f.write(key.exportKey('PEM'))
    f.close()

    key = RSA.generate(1024)
    f = open('key_B.pem', 'wb')
    f.write(key.exportKey('PEM'))
    f.close()

def give_key(port):
    if port==38552:
	f = open('key_B.pem', 'rb')
	key = RSA.importKey(f.read()).publickey().exportKey('PEM')
    else:
	f = open('key_A.pem', 'rb')
	key = RSA.importKey(f.read()).publickey().exportKey('PEM')
    return key


skt = create_send_socket()
gen_keys()
print "----Keys generated successfully----"
f = open('key_PKDA.pem', 'rb')
pkda_pri_key = RSA.importKey(f.read()).publickey().exportKey('PEM')
f.close()

while True:
    cli_con,cli_addr = skt.accept()
    print "New client connected: ",cli_addr
    rqst = cli_con.recv(1024)
    print "Request received by client (encoded): ",rqst
    rqst = rqst.decode(encoding='base64',errors='strict')    
    print "Request received by client (decoded): ",rqst
    response = str(give_key(cli_addr[1]))+rqst	
    print "Response sent by PKDA (original): ",response
    res = encrypt(response,pkda_pri_key)
    print "Response sent by PKDA (encrypted): ",res
    cli_con.send(res)
    cli_con.close()
    
skt.close()




