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

hash = "SHA-256"

my_id = "Police"
print "WELCOME TO ID VERIFICATION SYSTEM !!"
print "Press q to quit."

def generate_timestamp():
    return int(time.time())


def con_server():
	skt = socket.socket()
	skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	skt.bind(('127.0.0.1',38552))
	skt.connect(('127.0.0.1',38556))
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

f = open('key_server_pub.pem', 'rb')
server_key =  RSA.importKey(f.read())
f.close()
f = open('key_client_pri.pem', 'rb')
client_pri_key = RSA.importKey(f.read())
f.close()

idd = raw_input("Please enter your id number : ")

while idd!="q":
	f_name = "./"+ str(idd) + ".txt"
	if os.path.isfile(f_name):
		f_ptr = open(f_name,"r")
		expiry = f_ptr.readlines()[2]
		f_ptr.close()
		today = datetime.datetime.now()
		expiry_date = datetime.datetime.strptime((expiry.split(":")[1]).split("\n")[0], '%d-%m-%Y')
		if today>expiry_date:
			print "License has expired !!"
		else:
			skt = con_server()		
			rqst = my_id + "||" + idd
			rqst_en = encrypt(rqst,server_key)
			time_st= generate_timestamp()
			skt.send(rqst_en)
			resp = skt.recv(4096)
			#resp = decrypt(resp,client_pri_key)
			signn = resp[pos_rqst(resp,"||")+2:]
			msg = resp[0:pos_rqst(resp,"||")]
			ver_f = verify(msg,signn,server_key)
			time_sr = msg[pos_rqst(msg,"##")+2:]
			msg = resp[0:pos_rqst(resp,"##")]
			print "Response sent by Server: "
			print msg
			time_sr = datetime.datetime.fromtimestamp(float(time_sr)).date()
			time_st = datetime.datetime.fromtimestamp(float(time_st)).date()			
			if ver_f:
				f_ptr = open(f_name,"r")
				file_txt = f_ptr.read()
				f_ptr.close()
				print "License produced by driver: "
				print file_txt
				if time_sr == time_st:
					if file_txt==msg:
						print "License verified !!"
					else:
						print "License tampering found !!"
				else:	
					print "Replay attack found !! Try again."
			else:
				print "Hash not verified!! Try again!"
			skt.close()


	else:
		print "Id number not found!!\nPlease enter a valid id number.\n"
	idd = raw_input("Please enter your id number : ")


