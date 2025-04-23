import urllib.parse
from cryptography.fernet import Fernet

#key = Fernet.generate_key() #매번 실행때 마다 새키를 발급 하면 에러....
key = b'aW8wmBIBdB61OF3duw-qZwtH_Qp7UIifgkYydgCBs_8=' #키값은 고정 
cipher = Fernet(key)

def encryt(param : str):
    enc_encode = urllib.parse.quote(param)
    enc_pass = cipher.encrypt(enc_encode.encode())
    return enc_pass

def decryt(param : str):
    dec_pass = cipher.decrypt(param.encode()).decode()
    return dec_pass