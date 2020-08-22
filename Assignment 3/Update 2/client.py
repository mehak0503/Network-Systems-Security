import socket
import os
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode
import Crypto.PublicKey.DSA as DSA
import datetime
import time

hash = "SHA-512"

my_id = "PoliceA"
print "WELCOME TO ID VERIFICATION SYSTEM !!"
print "Press q to quit."

def generate_timestamp():
    return int(time.time())


def con_server():
	skt = socket.socket()
	skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	skt.bind(('127.0.0.1',38552))
	skt.connect(('127.0.0.1',38559))
	return skt

def encrypt(msg,key):
     cipher = PKCS1_OAEP.new(key)
     return cipher.encrypt(msg) 

def decrypt(msg,key):
     cipher = PKCS1_OAEP.new(key)
     return cipher.decrypt(msg) 

def pos_rqst(msg,rqst):
    return msg.find(rqst)

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

def digest(message):
	global hash
	#hash = hashAlg
	#signer = PKCS1_v1_5.new(priv_key)
   
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
	#return signer.sign(digest)
	return str(digest.digest())

def gen_keys():
	key = RSA.generate(4096)
	f = open(my_id+'pri.pem', 'wb')
	f.write(key.exportKey('PEM'))
	f.close()
	f = open(my_id+'pub.pem', 'wb')
	f.write(key.publickey().exportKey('PEM'))
	f.close()

#gen_keys()
print "----Keys generated successfully----"
f = open(my_id+'pri.pem', 'rb')
my_key =  RSA.importKey(f.read())
f.close()
f = open('key_server_pub.pem', 'rb')
server_key =  RSA.importKey(f.read())
f.close()
f = open('key_server_pri.pem', 'rb')
server_p_key =  RSA.importKey(f.read())
f.close()


idd = raw_input("Please enter your id number : ")

while idd!="q":
	f_name = "./"+ str(idd) + ".txt"
	if os.path.isfile(f_name):
		f_ptr = open(f_name,"r")
		expiry = f_ptr.readlines()[2]
		f_ptr.close()
		today = datetime.datetime.now()
		expiry_date = datetime.datetime.strptime((expiry.split(":")[1]).split("\n")[0], '%d-%m-%Y').strftime('%Y-%m-%d %H:%M:%S')
		skt = con_server()	
		#f_ptr = open(f_name,"r")
		#file_txt = f_ptr.read()
		#f_ptr.close()	
		file_txt = open(f_name, "r").read().rstrip('\n')
		#hashh = sign(file_txt,server_p_key)
		hashh = digest(file_txt)
		rqst = my_id + "||" + idd +"||" + hashh
		rqst_en = encrypt(rqst,server_key)		
		skt.send(rqst_en)
		resp = skt.recv(4096)
		msg = decrypt(resp,server_p_key)
		time_sr = msg[pos_rqst(msg,"##")+2:]
		st = datetime.datetime.fromtimestamp(float(time_sr)).strftime('%Y-%m-%d %H:%M:%S')
		print st
		print expiry_date
		msgg = msg[0:pos_rqst(msg,"##")]
		msg = msgg[0:pos_rqst(msgg,"!!")]
		c = msgg[pos_rqst(msgg,"!!")+2:]
		print "Response sent by Server: "
		print msg

		if c=="0" and st<expiry_date:
			print "License verified !!"
		elif c=="0":
			print "License expired !!"
		skt.close()


	else:
		print "Id number not found!!\nPlease enter a valid id number.\n"
	idd = raw_input("Please enter your id number : ")


