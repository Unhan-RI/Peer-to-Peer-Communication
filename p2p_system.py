import socket
import threading
import time
import os

# Satu file log global untuk semua node
LOG_FILE = "combined_log.txt"

def write_log(message):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

class Node:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.neighbors = []
        self.files = {}

        # Jalankan server di thread terpisah
        self.server_thread = threading.Thread(target=self.start_server, daemon=True)
        self.server_thread.start()

    # Fungsi untuk memulai server
    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        write_log(f"Node {self.host}:{self.port} siap menerima koneksi...")
        
        while True:
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True)
            client_thread.start()

    # Menangani permintaan dari client
    def handle_client(self, client_socket):
        data = client_socket.recv(1024).decode('utf-8')
        if data.startswith("SEARCH"):
            filename = data.split()[1]
            write_log(f"Node {self.host}:{self.port} menerima permintaan pencarian file '{filename}' dari {client_socket.getpeername()}")
            self.search_file(client_socket, filename)
        elif data.startswith("GET"):
            filename = data.split()[1]
            write_log(f"Node {self.host}:{self.port} menerima permintaan pengiriman file '{filename}' dari {client_socket.getpeername()}")
            self.send_file(client_socket, filename)
        client_socket.close()

    # Fungsi untuk mencari file di node ini
    def search_file(self, client_socket, filename):
        start_time = time.time()  # Mulai pengukuran waktu respon
        if filename in self.files:
            # Kirim pesan file ditemukan ke client
            client_socket.send(f"FOUND {filename} di {self.host}:{self.port}".encode('utf-8'))
            write_log(f"File '{filename}' ditemukan di node {self.host}:{self.port}.")
            
            # Hitung waktu respon
            end_time = time.time()
            response_time = end_time - start_time
            write_log(f"Waktu respon pencarian file di node {self.host}:{self.port}: {response_time:.6f}s.")
        else:
            # Jika file tidak ditemukan di node ini, teruskan ke tetangga
            write_log(f"File '{filename}' tidak ditemukan di node {self.host}:{self.port}. Mencari di node tetangga...")
            self.forward_search(filename, start_time)

    # Meneruskan pencarian file ke tetangga
    def forward_search(self, filename, start_time):
        for neighbor in self.neighbors:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((neighbor['host'], neighbor['port']))
                client_socket.send(f"SEARCH {filename}".encode('utf-8'))
                response = client_socket.recv(1024).decode('utf-8')
                end_time = time.time()  # Akhir pengukuran waktu respon

                # Hitung waktu respon dan throughput
                response_time = end_time - start_time
                throughput = len(response.encode('utf-8')) / response_time if response_time > 0 else 0

                if response.startswith("FOUND"):
                    write_log(f"File '{filename}' ditemukan di node {neighbor['host']}:{neighbor['port']}.")
                    write_log(f"Waktu respon total: {response_time:.6f}s, throughput: {throughput:.6f} bytes/s.")
                    client_socket.close()
                    break  # Hentikan pencarian setelah file ditemukan di salah satu tetangga
                else:
                    write_log(f"File '{filename}' tidak ditemukan di node {neighbor['host']}:{neighbor['port']}.")
                client_socket.close()
            except Exception as e:
                write_log(f"Node {self.host}:{self.port} gagal terhubung ke node {neighbor['host']}:{neighbor['port']}, error: {e}")

    # Mengirim file jika ditemukan
    def send_file(self, client_socket, filename):
        start_time = time.time()  # Mulai pengukuran waktu respon
        if filename in self.files:
            with open(self.files[filename], 'rb') as f:
                data = f.read()
                client_socket.send(data)
            end_time = time.time()  # Akhir pengukuran waktu respon
            response_time = end_time - start_time
            throughput = len(data) / response_time if response_time > 0 else 0
            write_log(f"File '{filename}' dikirim dari node {self.host}:{self.port} ke {client_socket.getpeername()}")
            write_log(f"Waktu pengiriman file di node {self.host}:{self.port}: {response_time:.6f}s, throughput: {throughput:.6f} bytes/s.")
        else:
            client_socket.send(f"File {filename} tidak ditemukan".encode('utf-8'))
            write_log(f"File '{filename}' tidak ditemukan di node {self.host}:{self.port}, tidak dapat mengirim file.")

    # Menambahkan file ke node
    def add_file(self, filename, filepath):
        self.files[filename] = filepath
        write_log(f"File '{filename}' ditambahkan ke node {self.host}:{self.port}.")

    # Menambahkan tetangga ke node ini
    def add_neighbor(self, host, port):
        self.neighbors.append({'host': host, 'port': port})
        write_log(f"Node {self.host}:{self.port} menambahkan tetangga node {host}:{port}.")

# Membuat jaringan P2P
def create_network():
    node1 = Node('localhost', 5001)
    node2 = Node('localhost', 5002)
    node3 = Node('localhost', 5003)

    node1.add_neighbor('localhost', 5002)  # Node 1 tetangga Node 2
    node2.add_neighbor('localhost', 5001)  # Node 2 tetangga Node 1
    node2.add_neighbor('localhost', 5003)  # Node 2 tetangga Node 3
    node3.add_neighbor('localhost', 5002)  # Node 3 tetangga Node 2

    # Tambahkan file ke node 1
    node1.add_file("contoh.txt", "path_ke_contoh.txt")

    time.sleep(1)  # Beri waktu untuk memulai server
    search_thread = threading.Thread(target=node3.forward_search, args=("contoh.txt", time.time()))
    search_thread.start()

    search_thread.join()  # Tunggu hingga pencarian selesai

if __name__ == "__main__":
    # Hapus file log lama jika ada
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    
    create_network()
