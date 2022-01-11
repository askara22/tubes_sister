# import library socket
import socket

# Menginisialisasi tujuan IP Server dan Port dari server yang akan terhubung
tcp_ip = "127.0.0.1" # Tujuan IP Server saat demo 26.236.11.200
tcp_port = 8085

# Definisikan ukuran buffer
buffer_size = 4096

# Membuat socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Melakukan koneksi pada server menggunakan parameter IP dan Port
s.connect((tcp_ip, tcp_port))

# Menerima pesan dari server dan displit ke dalam 2 variabel yaitu data1 & data2
data1, data2 = [str.encode(i) for i in s.recv(buffer_size).decode('utf-8').split('\n')]

# Menuliskan pesan yang akan diterima oleh client
print("Pemberitahuan!")
print("Jadwal Boarding dan Lokasi Transit Penumpang Lion Air Group: \n")
print(data1.decode('utf-8'))
print(data2.decode('utf-8'), "\n")

# Mengirimkan kembali pesan yang telah diterima
s.sendall(b'\n'.join([data1,data2]))

# Menuliskan pesan dari variabel data1 ke dalam boarding.txt dengan cara append
f1 = open("boarding.txt", "a")
f1.write(''.join(data1.decode()))
f1.write('\n')
f1.close()

# Menuliskan pesan dari variabel data2 ke dalam lokasi.txt dengan cara append
f2 = open("lokasi.txt","a")
f2.write(''.join(data2.decode()))
f2.write('\n')
f2.close()

# Menutup koneksi
s.close()
