import socket
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Random import random
from Crypto.PublicKey import ElGamal
from Crypto.Util.number import GCD
from Crypto.Hash import SHA
import random  
from math import pow
import hmac
import hashlib
import os,binascii
import sys

def gen_key(q): 
  
    key = random.randint(pow(10, 20), q) 
    while gcd(q, key) != 1: 
        key = random.randint(pow(10, 20), q)   
    return key 


def gcd(a, b): 
    if a < b: 
        return gcd(b, a) 
    elif a % b == 0: 
        return b; 
    else: 
        return gcd(b, a % b) 

def encrypt(msg):
	encryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
	cipher_text = encryption_suite.encrypt(msg)
	return cipher_text

def decrypt(msg):
	decryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
	plain_text = decryption_suite.decrypt(msg)
	return plain_text


def power(a, b, c): 
    x = 1
    y = a 
  
    while b > 0: 
        if b % 2 == 0: 
            x = (x * y) % c; 
        y = (y * y) % c 
        b = int(b / 2) 
  
    return x % c 

def create_peer_socket():
    skt = socket.socket()
    skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    skt.bind(('127.0.0.1',38557))
    skt.connect(('127.0.0.1',38559))
    return skt

def h_comp(secret,msg):
	h = hmac.new(secret,msg,hashlib.sha256)
	return h.hexdigest()

def pos_elem(s,x):
	return s.find(x)


def encrypt(msg,key): 
  
    en_msg = [] 
      
    for i in range(0, len(msg)): 
        en_msg.append(msg[i]) 
   
    for i in range(0, len(en_msg)): 
        en_msg[i] = key * ord(en_msg[i]) 
  
    return en_msg
  
def decrypt(en_msg,key): 
  
    dr_msg = [] 
    for i in range(0, len(en_msg)): 
        dr_msg.append(chr(int(en_msg[i]/key))) 
          
    return dr_msg 


secret = binascii.b2a_hex(os.urandom(32))
skt = create_peer_socket()
q = random.randint(pow(10,20), pow(10, 50)) 
alpha = random.randint(2,q)
print "secret ",secret 
print "q ",q
print "alpha ",alpha
skt.send(secret)
skt.send(str(q))
skt.send(str(alpha))


resp = skt.recv(2048)
print "Message received from A "+resp 	
ya = resp[0:pos_elem(resp,"||")]	
r_ya = resp[pos_elem(resp,"||")+2:]
h_ya = h_comp(secret,ya)
print "a^XA mod q = ",str(ya)
ya = long(ya)
ver = hmac.compare_digest(r_ya,h_ya)

if ver:
	print "\n\nEnter q to quit"
	msg = ""
	while msg!="q":
		xb = gen_key(q)
		yb = power(alpha,xb,q)
		h_yb = h_comp(secret,str(yb)) 
		#skt.send(str(yb)+"||"+h_yb)
		#print "Message sent to A "+str(yb)+"||"+h_yb
		print "\n\na^XB mod q = ",str(yb)
		key = power(ya,xb,q)
		print "a^(XA*XB) mod q = ",str(key)
		
		msg = raw_input("B: ")
	        print "Message sent by B (original): ",msg+"||"+str(yb)+"||"+h_yb
        	msg_en = encrypt(msg,key)
		msg_en = map(str,msg_en)
		msg_en = "#".join(msg_en)+"||"+str(yb)+"||"+h_yb
        	print "Message sent by B (encrypted): ",msg_en
        	skt.send(str(msg_en))
else:
	print "MITM Attack Detected!"
	sys.exit()

