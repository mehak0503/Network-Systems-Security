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
from base64 import b64encode
import time
import datetime

hash = "SHA-512"

def generate_timestamp():
    return str(int(time.time()))


def create_socket():
	skt = socket.socket()
	skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	skt.bind(('127.0.0.1',38559))
	skt.listen(5)
	print "Server is listening on 38559"
	return skt

def encrypt(msg,key):
     cipher = PKCS1_OAEP.new(key)
     return cipher.encrypt(msg) 

def decrypt(msg,key):
     cipher = PKCS1_OAEP.new(key)
     return cipher.decrypt(msg) 

def gen_keys():
	key = RSA.generate(5120)
	f = open('key_server_pri.pem', 'wb')
	f.write(key.exportKey('PEM'))
	f.close()
	f = open('key_server_pub.pem', 'wb')
	f.write(key.publickey().exportKey('PEM'))
	f.close()
	
def pos_rqst(msg,rqst):
    return msg.find(rqst)

def sign(message, priv_key, hashAlg="SHA-512"):
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

def verify(message, signature, pub_key):
	signer = PKCS1_v1_5.new(pub_key)
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
	return signer.verify(digest, signature)


#gen_keys()
print "----Keys generated successfully----"
f = open('key_server_pri.pem', 'rb')
server_pri_key = RSA.importKey(f.read())
f.close()
f = open('key_server_pub.pem', 'rb')
server_key = RSA.importKey(f.read())
f.close()

skt = create_socket()
while True:
	cli_con,cli_addr = skt.accept()
	print "New client connected: ",cli_addr
	resp = cli_con.recv(1024)
	resp = decrypt(resp,server_pri_key)
	police_id = resp[0:pos_rqst(resp,"||")]
	rem = resp[pos_rqst(resp,"||")+2:]
	idd = rem[0:pos_rqst(rem,"||")]
	hashh = rem[pos_rqst(rem,"||")+2:]
	print idd
	f_name = "./Server/"+ str(idd+"_hash") + ".txt"
	print f_name
	time_st= generate_timestamp()
	
	f = open(police_id+'pub.pem','rb')
	policekey = RSA.importKey(f.read())
	f.close()	

	if os.path.isfile(f_name):
		f_ptr = open(f_name,"r")
		file_txt = f_ptr.read()
		f_ptr.close()
		#hashh = decrypt(hashh,server_pri_key)		
		#ver = verify(file_txt,hashh,policekey)
		ver = (hashh==file_txt)
		print hashh
		print file_txt
		if ver:
			reply = "License verified successfully!!"+"0"
		else:
			reply = "License tampered!!"+"1"
	else:
		reply = "License tampered as no license found !!"+"2"
	
	print reply
	print time_st
	reply = reply+"##"+time_st
	msg = encrypt(reply,server_key)
	cli_con.send(msg)
	cli_con.close()

skt.close()	
	
