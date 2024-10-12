Berikut adalah **README.md** versi Bahasa Indonesia yang sangat spesifik dan lengkap untuk proyek **sistem client-server P2P (Peer-to-Peer)** dengan dua server, load balancer, dan fitur monitoring.

---

# Sistem Client-Server P2P dengan Load Balancer dan Monitoring

## Ringkasan

Proyek ini mengimplementasikan sistem komunikasi **Peer-to-Peer (P2P)** menggunakan dua server, load balancer, dan client untuk mengirim serta menerima pesan atau file. Sistem ini mendukung multithreading atau asynchronous programming, mengukur waktu respon, latency, throughput, serta mencatat semua aktivitas seperti waktu koneksi, waktu pengiriman pesan, dan penerimaan balasan.

Proyek ini juga mencakup kemampuan monitoring untuk menganalisis performa sistem melalui file log.

## Fitur

- **Multithreading/Asynchronous programming**: Menangani beberapa permintaan client secara bersamaan.
- **Load Balancer**: Mendistrbusikan permintaan client ke dua server menggunakan metode round-robin.
- **Komunikasi Peer-to-Peer**: Node dapat terhubung, berbagi, dan mencari file antar node.
- **Logging**: Log rinci untuk koneksi, pengiriman pesan, dan pencarian file.
- **Monitoring**: Mencatat waktu respon, throughput, dan semua event sistem ke dalam `combined_log.txt`.

## Struktur File

```text
|-- p2p_system.py             # Skrip utama untuk sistem komunikasi P2P
|-- server1.py                # Skrip server pertama (berjalan di port 8080)
|-- server2.py                # Skrip server kedua (berjalan di port 8081)
|-- load_balancer.py          # Skrip load balancer (mendistribusikan permintaan client)
|-- client.py                 # Skrip client (mengirim pesan ke server melalui load balancer)
|-- client_manager.py         # Mengelola beberapa client, menangani permintaan secara bersamaan
|-- log_manager.py            # Mengelola log koneksi, pengiriman pesan, dan waktu respon
|-- combined_log.txt          # File log dengan aktivitas sistem dan performa
|-- contoh.txt                # File contoh yang digunakan dalam berbagi file P2P
|-- README.md                 # File readme ini
```

## Cara Menjalankan Sistem

### Langkah 1: Jalankan Server 1

Buka terminal atau terminal di VS Code, lalu jalankan:

```bash
python server1.py
```

Ini akan memulai **Server 1** di port `8080`.

### Langkah 2: Jalankan Server 2

Di terminal baru, jalankan:

```bash
python server2.py
```

Ini akan memulai **Server 2** di port `8081`.

### Langkah 3: Jalankan Load Balancer

Buka terminal baru dan jalankan:

```bash
python load_balancer.py
```

Load balancer akan mendengarkan di port `8000` dan mendistribusikan permintaan client antara **Server 1** dan **Server 2**.

### Langkah 4: Jalankan Client Manager

Untuk mensimulasikan beberapa client yang mengirim pesan atau file ke server, jalankan client manager:

```bash
python client_manager.py
```

Saat diminta, masukkan jumlah client dan pesan yang ingin dikirim. Client manager akan menangani beberapa client secara bersamaan dan menghitung metrik performa seperti waktu respon dan throughput.

### Langkah 5: Monitor Log

Semua detail koneksi, pencarian file, dan waktu respon dicatat ke dalam file `combined_log.txt`. Anda dapat membuka dan melihat file ini untuk memantau performa dan aktivitas sistem:

```bash
cat combined_log.txt
```

Contoh entri log:
```
2024-10-12 13:26:34 - Node localhost:5001 menambahkan tetangga node localhost:5002.
2024-10-12 13:26:34 - Node localhost:5002 menerima permintaan pencarian file 'contoh.txt'.
2024-10-12 13:26:35 - File 'contoh.txt' ditemukan di node localhost:5001.
2024-10-12 13:26:35 - Waktu respon pencarian file di node localhost:5001: 0.000991s.
```

## Log dan Monitoring

- **combined_log.txt**: File log ini mencatat event-event berikut:
  - **Koneksi**: Waktu saat koneksi dibuat antara node atau client.
  - **Pesan Dikirim**: Waktu dan isi pesan yang dikirim.
  - **Pesan Diterima**: Waktu dan isi balasan dari server.
  - **Waktu Respon**: Waktu yang dibutuhkan untuk memproses permintaan.
  - **Throughput**: Kecepatan transfer data yang diukur dalam bytes per detik.

### Contoh Log:
```text
2024-10-12 13:26:34 - Node localhost:5001 siap menerima koneksi...
2024-10-12 13:26:35 - File 'contoh.txt' ditemukan di node localhost:5001.
2024-10-12 13:26:35 - Waktu respon pencarian file di node localhost:5001: 0.000991s.
2024-10-12 13:26:35 - Waktu respon total: 0.003009s, throughput: 11300.922102 bytes/s.
```

## Data Contoh

File `contoh.txt` digunakan sebagai contoh file yang dibagikan antar node. Isinya sebagai berikut:

```text
INI ADALAH KOMUNIKASI P2P
```

## Metrik Performa

Sistem ini menghitung dan mencatat metrik performa berikut:

1. **Waktu Respon**: Waktu yang dibutuhkan server untuk memproses dan merespons permintaan client.
2. **Latency**: Penundaan antara pengiriman permintaan dan penerimaan byte pertama dari respons.
3. **Throughput**: Jumlah data yang ditransfer per detik.

Metrik ini tersedia di file **combined_log.txt** dan dapat digunakan untuk menganalisis performa sistem di bawah beban.

## Pengembangan Lebih Lanjut

- **Load Balancer yang Lebih Pintar**: Saat ini menggunakan round-robin, pertimbangkan untuk menambahkan metode seperti least connections atau weighted round-robin.
- **Asynchronous Programming**: Implementasikan `asyncio` untuk meningkatkan efisiensi dan concurrency.
- **Enkripsi TLS/SSL**: Untuk mengamankan komunikasi antara client dan server.
- **Logging ke Database**: Pindahkan log ke database seperti SQLite atau PostgreSQL untuk analisis terstruktur.

## Lisensi

Proyek ini dilisensikan di bawah MIT License. Lihat file `LICENSE` untuk detail lebih lanjut.

---

**Catatan:**
- Pastikan untuk menggunakan jendela terminal terpisah untuk setiap komponen (server, load balancer, dan client manager).
- Anda dapat menyesuaikan mekanisme berbagi file atau metode load balancing sesuai kebutuhan.

