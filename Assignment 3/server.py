import socket
import os
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
import time
import datetime

hash = "SHA-256"

def generate_timestamp():
    return str(int(time.time()))


def create_socket():
	skt = socket.socket()
	skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	skt.bind(('127.0.0.1',38556))
	skt.listen(5)
	print "Server is listening on 38556"
	return skt

def encrypt(msg,key):
     cipher = PKCS1_OAEP.new(RSA.importKey(key))
     return cipher.encrypt(msg) 

def decrypt(msg,key):
     cipher = PKCS1_OAEP.new(key)
     return cipher.decrypt(msg) 

def gen_keys():
	key = RSA.generate(4096)
	f = open('key_server_pri.pem', 'wb')
	f.write(key.exportKey('PEM'))
	f.close()
	f = open('key_server_pub.pem', 'wb')
	f.write(key.publickey().exportKey('PEM'))
	f.close()
	key = RSA.generate(4096)
	f = open('key_client_pri.pem', 'wb')
	f.write(key.exportKey('PEM'))
	f.close()
	f = open('key_client_pub.pem', 'wb')
	f.write(key.publickey().exportKey('PEM'))
	f.close()
	
def pos_rqst(msg,rqst):
    return msg.find(rqst)

def sign(message, priv_key, hashAlg="SHA-256"):
	global hash
	hash = hashAlg
	signer = PKCS1_v1_5.new(priv_key)
   
	if (hash == "SHA-512"):
		digest = SHA512.new()
	elif (hash == "SHA-384"):
		digest = SHA384.new()
	elif (hash == "SHA-256"):
		digest = SHA256.new()
	elif (hash == "SHA-1"):
		digest = SHA.new()
	else:
		digest = MD5.new()
	digest.update(message)
	return signer.sign(digest)

gen_keys()
print "----Keys generated successfully----"
f = open('key_server_pri.pem', 'rb')
server_pri_key = RSA.importKey(f.read())
f.close()
f = open('key_client_pub.pem', 'rb')
client_pub_key = RSA.importKey(f.read())
f.close()
skt = create_socket()
while True:
	cli_con,cli_addr = skt.accept()
	print "New client connected: ",cli_addr
	resp = cli_con.recv(1024)
	resp = decrypt(resp,server_pri_key)
	idd = resp[pos_rqst(resp,"||")+2:]
	print idd
	f_name = "./Server/"+ str(idd) + ".txt"
	print f_name
	time_st= generate_timestamp()
	if os.path.isfile(f_name):
		f_ptr = open(f_name,"r")
		expiry = f_ptr.readlines()[2]
		f_ptr.close()
		today = datetime.datetime.now()
		expiry_date = datetime.datetime.strptime((expiry.split(":")[1]).split("\n")[0], '%d-%m-%Y')
		if today>expiry_date:
			reply = "License has expired (on server side)!!"
		else: 
			f_ptr = open(f_name,"r")
			reply = f_ptr.read()
			f_ptr.close()
	else:
		reply = "No license found !!"
	
	print reply
	print time_st
	reply = reply+"##"+time_st
	signn = sign(reply,server_pri_key)
	msg = reply + "||" + signn
	#msg = encrypt(msg,client_pub_key)
	cli_con.send(msg)
	cli_con.close()

skt.close()	
	

