import socket
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS
import uuid
import time

idd = "Client B"

def generate_timestamp():
    return str(int(time.time()))

def generate_nonce():
    return uuid.uuid4().hex

def decrypt(msg,key):
     cipher = PKCS1_OAEP.new(key)
     return cipher.decrypt(msg) 

def encrypt(msg,key):
     cipher = PKCS1_OAEP.new(RSA.importKey(key))
     return cipher.encrypt(msg) 


def create_recv_socket():
    skt = socket.socket()
    skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    skt.bind(('127.0.0.1',38558))
    skt.connect(('127.0.0.1',38556))
    return skt

def create_peer_socket():
    skt = socket.socket()
    skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    skt.bind(('127.0.0.1',38558))
    skt.connect(('127.0.0.1',38557))
    return skt

def create_peer_socket1():
    skt = socket.socket()
    skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    skt.bind(('127.0.0.1',38559))
    skt.listen(5)
    return skt

def nonces():
    return generate_nonce(),generate_nonce()

def pos_rqst(msg,rqst):
    return msg.find(rqst)

def pos_rqst_after(msg,rqst):
    return (len(msg) - msg.find(rqst))

print "My id: ",idd

#Reading keys
f = open('key_PKDA.pem', 'rb')
pkda_pub_key = RSA.importKey(f.read())
f.close()
f = open('key_B.pem', 'rb')
pri_key = RSA.importKey(f.read())
pub_key =  pri_key.publickey().exportKey('PEM')
f.close()

#Receive rqst from client
msg_de = ""
skt_A = create_peer_socket1()
while True:
    cli_con,cli_addr = skt_A.accept()
    msg = cli_con.recv(1024)
    print "Message received from A (encrypted): ",msg
    msg_de = decrypt(msg,pri_key)
    print "Message received from A (decrypted): ",msg_de
    cli_con.close()
    skt_A.close()
    break

#Communication with PKDA
skt_recv = create_recv_socket()
timestamp = generate_timestamp()
rqst = idd + " || Client A || " + str(timestamp)
rqst_en = rqst.encode(encoding='base64',errors='strict')
skt_recv.send(rqst_en)
print "Sending request to PKDA (original): ",rqst
print "Sending request to PKDA (encoded): ",rqst_en
response = ""
res = skt_recv.recv(2048)
print "Response from PKDA (encrypted): ",res
response = decrypt(res,pkda_pub_key)
print "Response from PKDA (decrypted): ",response
key_A = response[0:pos_rqst(response,rqst)]
skt_recv.close()

#Conversation between clients
skt_B = create_peer_socket()
nonce2 = generate_nonce()
nonce1 =  msg_de[pos_rqst(msg_de,"||")+2:]
msg = str(nonce1)+"||"+str(nonce2)
print "Message sent to A (original): ",msg
msg_en = encrypt(msg,key_A)
print "Message sent to A (encrypted): ",msg_en
skt_B.send(msg_en)
msg = skt_B.recv(1024)
print "Message received from A (encrypted): ",msg
msg_de = decrypt(msg,pri_key)
print "Message received from A (decrypted): ",msg_de
print "\n\nEnter q to quit"

msg = ""
while msg!="q":
    msg = skt_B.recv(1024)
    print "Message received from A (encrypted): ",msg
    msg_de = decrypt(msg,pri_key)
    print "Message received from A (decrypted): ",msg_de
    if msg_de=="q":
	break
    msg = raw_input("B:")
    print "Message sent to A (original): ",msg
    msg_en = encrypt(msg,key_A)
    print "Message sent to A (encrypted): ",msg_en
    skt_B.send(msg_en)

skt_B.close()
        


