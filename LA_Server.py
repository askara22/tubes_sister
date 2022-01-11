# import library socket
import socket

#import library datetime
from datetime import datetime

# Menginisialisasi IP binding dan Port binding yang akan digunakan
tcp_ip = "127.0.0.1" # IP binding saat demo 26.236.11.200
tcp_port = 8085

# Definisikan ukuran buffer
buffer_size = 4096

# Membuat Socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Melakukan koneksi pada server menggunakan parameter IP dan Port
s.bind((tcp_ip, tcp_port))

# Server akan listen menunggu koneksi dari client
s.listen(10)

# Definisikan variabel now sebagai tanggal dan waktu saat ini
now = datetime.now()

# Menampilkan tanggal dan waktu hari ini
print ("\nTanggal dan waktu hari ini: ", str(now))

# Definisikan variabel loc sebagai list yang berisikan lokasi transit
loc = [
    "Barcelona, Spain",
    "London, England",
    "Toronto, Canada",
    "Berlin, Germany",
    "Paris, France"
]

# Definisikan variabel board sebagai list yang berisikan jadwal boarding
board = [
    datetime(2022, 2, 11, 11, 30, 00),
    datetime(2022, 2, 12, 20, 15, 00),
    datetime(2022, 2, 13, 21, 30, 00),
    datetime(2022, 2, 12, 15, 30, 00),
    datetime(2022, 2, 11, 12, 45, 00)
]

# Definisikan variabel reschedule
reschedule = False

# Membuat kondisi reschedule saat melewati waktu tertentu akan terjadi reschedule
if datetime.now() >= datetime(2021, 1, 11, 10, 47):
    reschedule = True

# Membuat kondisi saat reschedule bernilai True
if reschedule == True:
    # Menginisialisasi lokasi sesuai dengan list loc
    location = loc[3]
    # Menginisialisasi jadwal sesuai dengan list board
    date1 = board[3]
    # Menginisialisasi boarding sesuai dengan jadwal dan mengubahnya menjadi string
    boarding = date1.strftime("%B %d %Y %H:%M:%S")

# Membuat kondisi saat reschedule bernilai False
else:
    # Menginisialisasi lokasi sesuai dengan list loc
    location = loc[0]
    # Menginisialisasi jadwal sesuai dengan list board
    date2 = board[0]
    # Menginisialisasi boarding sesuai dengan jadwal dan mengubahnya menjadi string
    boarding = date2.strftime("%B %d %Y %H:%M:%S")

# Melakukan loop forever
while 1:
    # Menerima koneksi client
    conn, addr = s.accept()
    # Menampilkan alamat yang terkoneksi dengan server
    print("\nAlamat: ", addr)
	
    # Mengirim pesan kepada client yang terkoneksi berupa variabel boarding dan location
    conn.sendall(str.encode("\n".join([boarding, location])))
    
    # Menerima pesan sesuai ukuran buffer
    data = conn.recv(buffer_size)

    # Menampilkan pesan yang diterima
    print("Mengirim pesan berisi: ", data.decode())

# Menutup koneksi
conn.close()
