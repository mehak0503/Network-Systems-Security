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
import sys
import os,binascii

def create_peer_socket():
    skt = socket.socket()
    skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    skt.bind(('127.0.0.1',38559))
    skt.listen(5)
    return skt

def gcd(a, b): 
    if a < b: 
        return gcd(b, a) 
    elif a % b == 0: 
        return b; 
    else: 
        return gcd(b, a % b) 

def power(a, b, c): 
    x = 1
    y = a 
  
    while b > 0: 
        if b % 2 == 0: 
            x = (x * y) % c; 
        y = (y * y) % c 
        b = int(b / 2) 
  
    return x % c 

def gen_key(q): 
  
    key = random.randint(pow(10, 20), q) 
    while gcd(q, key) != 1: 
        key = random.randint(pow(10, 20), q)   
    return key 

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

skt = create_peer_socket()

while True:
	cli_con,cli_addr = skt.accept()
	secret = cli_con.recv(2048)	
	q = cli_con.recv(2048)
	alpha = cli_con.recv(2048)
	print "secret ",secret 
	print "q ",q
	print "alpha ",alpha
	q = long(q)
	alpha = long(alpha)
	xa = gen_key(q)
	ya = power(alpha,xa,q)
	h_ya = h_comp(secret,str(ya))
	cli_con.send(str(ya)+"||"+h_ya)
	print "a^XA mod q = ",str(ya)
	print "Message sent to B "+str(ya)+"||"+h_ya 
		
	msg_de = ""
	
	while msg_de!="q":
		
		resp = cli_con.recv(2048)
		print "\n\nMessage received from B "+resp 	
		msg = resp[0:pos_elem(resp,"||")]	
		rr = resp[pos_elem(resp,"||")+2:]
		yb = rr[0:pos_elem(rr,"||")]	
		r_yb = rr[pos_elem(rr,"||")+2:]
		print "a^XB mod q = ",str(yb)
		h_yb = h_comp(secret,yb)
		print "YB ",yb
		yb = long(yb)
		ver = hmac.compare_digest(r_yb,h_yb)
		key = power(yb,xa,q)
		if ver:
			print "a^(XA*XB) mod q = ",str(key)
			msg = msg.split("#")
			msg = map(long,msg)
			msg_de = decrypt(msg,key)
			msg_de = "".join(msg_de)
			print "Message received from B (decrypted): ",msg_de
		
		else:
			print "MITM Attack detected!"
			sys.exit()

	
	cli_con.close()
	break

skt.close()
