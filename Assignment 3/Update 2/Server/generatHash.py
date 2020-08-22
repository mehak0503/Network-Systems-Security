import os
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
import sys
from base64 import b64encode, b64decode

originalFile = sys.argv[1]
hashFile = sys.argv[2]
#originalFile = "IN-12201901.json"
#hashFile = "IN-12201901.txt"

hash = "SHA-512"

def createHash(message):
   
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
	return digest


try:
	line = open(originalFile, "r").read().rstrip('\n')
	print(line)
	hashvalue = createHash(line)
	print hashvalue
	with open(hashFile, "w") as f:
		f.write(str(hashvalue.digest()))
	
	
except:
	print("file not exist")
	



