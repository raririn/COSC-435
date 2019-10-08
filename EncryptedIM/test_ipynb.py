#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'EncryptedIM'))
	print(os.getcwd())
except:
	pass

from encryptedIMclient import Client, wrappedMsg
import message_pb2

from Crypto.Cipher import AES
from Crypto.Hash import HMAC
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Util.Padding import pad, unpad



#%%
k = '2'
key = Client.calHashForKeys(k)
len(key)

nickname = 'Nick'
padnick = pad(bytes(nickname, 'utf-8'), 16)

text = 'Piece of Crap'
text = bytes(text, 'utf-8')
padtext = pad(text, 16)


iv = Random.new().read(AES.block_size)
iv

cipher = AES.new(key, AES.MODE_CBC, iv)


#%%
cipher.encrypt(padtext)
#%%
mm = wrappedMsg("1", "2", key)



#%%
cipher = AES.new(key, AES.MODE_CBC, iv)
a = cipher.encrypt(padtext)
a


#%%
cipher2 = AES.new(key, AES.MODE_CBC, iv)
b = unpad(cipher2.decrypt(a), 16)
b.decode('utf-8')


#%%
m = message_pb2.BasicMsg()
m.nickname = cipher.encrypt(padnick)
m.text = cipher.encrypt(padtext)
m.iv = iv
n = m.SerializeToString()
n