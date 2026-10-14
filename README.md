# 🎛️ HafzAnyaDashboard — Android Stream Deck

**HafzAnaDashboard** adalah proyek aplikasi Android yang mengubah smartphone atau tablet menjadi **Stream Deck virtual** untuk mengontrol PC melalui jaringan lokal.

Aplikasi Android berfungsi sebagai *client* yang menyediakan antarmuka tombol interaktif, sedangkan server berbasis Python yang berjalan di PC bertugas menerima perintah dan menjalankan aksi yang telah dikonfigurasi.

Proyek ini cocok untuk streamer, content creator, maupun pengguna yang ingin mengontrol aplikasi dan menjalankan shortcut PC langsung dari layar sentuh Android.

## ✨ Fitur Utama

- 🎛️ **Virtual Stream Deck** — Antarmuka berupa grid tombol interaktif untuk mengirimkan perintah ke PC.
- 🖥️ **Python PC Server** — Server Python untuk menerima dan memproses perintah dari perangkat Android.
- 🚀 **Eksekusi Perintah** — Mendukung berbagai aksi yang dikonfigurasi, seperti membuka aplikasi dan menjalankan script.
- ⌨️ **Shortcut dan Macro** — Memungkinkan integrasi shortcut keyboard atau macro sesuai implementasi server.
- 🎮 **Integrasi Aplikasi PC** — Berpotensi digunakan untuk mengontrol OBS Studio, Spotify, editor kode, browser, dan aplikasi lainnya.
- 📡 **Komunikasi Jaringan Lokal** — Menghubungkan perangkat Android dan PC melalui Wi-Fi atau LAN.

> Ketersediaan setiap fitur bergantung pada implementasi kode aplikasi Android dan server Python.

## 🏗️ Arsitektur Sistem

HafzAnyaDashboard menggunakan arsitektur **Client–Server**. Aplikasi Android mengirimkan perintah, kemudian server Python memproses permintaan tersebut di PC.

```text
┌────────────────────────┐
│      HP ANDROID        │
│      Kotlin App        │
│                        │
│  • Antarmuka pengguna  │
│  • Grid tombol         │
│  • Pengiriman perintah │
└───────────┬────────────┘
            │
            │  Perintah
            │  Socket / HTTP
            ▼
┌────────────────────────┐
│       PC SERVER        │
│        Python          │
│                        │
│  • Menerima permintaan │
│  • Memproses perintah  │
│  • Menjalankan aksi    │
└───────────┬────────────┘
            │
            │  Respons / Status
            └──────────────────► Android
```

### Komponen Sistem

- **Android Client:** Menampilkan antarmuka Stream Deck dan mengirimkan perintah ke server.
- **Python Server:** Menerima permintaan dari client dan menjalankan aksi yang diizinkan di PC.
- **Protokol Komunikasi:** Menggunakan socket atau HTTP, sesuai protokol yang diterapkan dalam kode proyek.

## 🛠️ Teknologi yang Digunakan

| Komponen | Teknologi | Fungsi |
|---|---|---|
| Aplikasi Android | Kotlin | Logika aplikasi mobile |
| Antarmuka Android | Jetpack Compose | Membangun antarmuka pengguna |
| PC Server | Python | Memproses perintah dari Android |
| Komunikasi | Socket / HTTP | Pertukaran data antara client dan server |
| Build System | Gradle Kotlin DSL | Mengelola proses build Android |
| IDE | Android Studio | Pengembangan dan pengujian aplikasi |


## 📂 Struktur Proyek

```text
HafzAnaDashboard/
├── app/                  # Kode sumber aplikasi Android
├── HafzDashboardPC/      # Server Python untuk PC
├── gradle/               # Konfigurasi Gradle Wrapper
├── build.gradle.kts      # Konfigurasi build utama
├── settings.gradle.kts   # Pengaturan modul proyek
└── README.md             # Dokumentasi proyek
```


## ⚙️ Cara Menjalankan Proyek

### 1. Persiapan

Pastikan perangkat pengembangan memiliki:

- Python yang sesuai dengan kebutuhan server.
- Android Studio.
- Android SDK dan komponen build yang dibutuhkan proyek.
- Git.
- Smartphone Android dan PC yang dapat terhubung melalui jaringan lokal.

### 2. Menjalankan Server Python

**Langkah 1 — Masuk ke direktori server**

Buka terminal di direktori utama proyek, lalu jalankan:

```bash
cd HafzDashboardPC
```

**Langkah 2 — Buat virtual environment (opsional)**

Untuk Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

Untuk Linux atau macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

**Langkah 3 — Instal dependensi**

Jika repositori menyediakan file `requirements.txt`, jalankan:

```bash
pip install -r requirements.txt
```

Jika file tersebut tidak tersedia, periksa dokumentasi dan import pada kode server untuk mengetahui dependensi yang diperlukan.

**Langkah 4 — Jalankan server**

Jika file utama server bernama `server.py`, jalankan:

```bash
python server.py
```

Pastikan server berhasil berjalan dan mencatat port yang digunakan sebelum melanjutkan ke aplikasi Android.

### 3. Menjalankan Aplikasi Android

**Langkah 1 — Clone repositori**

```bash
git clone https://github.com/qanziz47-coder/HafzAnyaDashboard.git
```

**Langkah 2 — Buka proyek**

1. Jalankan Android Studio.
2. Pilih **Open**.
3. Pilih folder `HafzAnaDashboard` hasil clone.
4. Tunggu proses Gradle Sync selesai.

**Langkah 3 — Build dan jalankan**

1. Hubungkan smartphone Android ke komputer atau siapkan emulator.
2. Aktifkan USB debugging jika menggunakan perangkat fisik melalui USB.
3. Pilih perangkat target di Android Studio.
4. Klik **Run** untuk membangun dan menjalankan aplikasi.

### 4. Menghubungkan Android ke PC

1. Pastikan server Python berjalan di PC.
2. Hubungkan smartphone dan PC ke jaringan lokal yang sama.
3. Temukan alamat IP lokal PC.
4. Buka aplikasi HafzAnaDashboard di Android.
5. Masukkan alamat IP dan port server, jika antarmuka aplikasi menyediakan pengaturan tersebut.
6. Tekan tombol koneksi jika tersedia.
7. Uji tombol Stream Deck untuk memastikan perintah diterima dan diproses oleh server.

Contoh alamat IP lokal:

```text
192.168.1.10
```

Gunakan alamat IP dan port aktual dari PC, bukan sekadar menyalin contoh di atas.

## ⚠️ Catatan Penting

### Jaringan

Pastikan Android dan PC dapat saling berkomunikasi melalui jaringan lokal. Beberapa jaringan Wi-Fi memiliki fitur *client isolation* yang dapat mencegah perangkat saling terhubung.

### Firewall

Jika koneksi gagal, periksa pengaturan firewall PC dan izinkan koneksi masuk hanya untuk aplikasi serta port yang diperlukan.

### Keamanan

- Gunakan jaringan tepercaya.
- Jangan mengekspos server langsung ke internet tanpa perlindungan yang memadai.
- Batasi perintah yang dapat dijalankan server.
- Hindari menjalankan perintah sistem mentah dari input pengguna.
- Pertimbangkan autentikasi atau token untuk memverifikasi permintaan dari client.

## 🗺️ Rencana Pengembangan

Beberapa ide untuk pengembangan selanjutnya:

- [ ] Kustomisasi ikon, nama, dan warna tombol.
- [ ] Dukungan multi-halaman atau folder tombol.
- [ ] Integrasi OBS Studio.
- [ ] Integrasi Spotify dan Discord.
- [ ] Pembuatan shortcut keyboard dan macro kustom.
- [ ] Penyimpanan konfigurasi tombol.
- [ ] Indikator status koneksi server.
- [ ] Autentikasi dan token keamanan.
- [ ] Sistem plugin untuk memperluas fungsi aplikasi.

## 🤝 Kontribusi

Kontribusi untuk pengembangan HafzAnaDashboard sangat terbuka.

Jika ingin berkontribusi, ikuti langkah berikut:

**1. Fork repositori**

Fork repositori utama melalui GitHub.

**2. Clone repositori hasil fork**

```bash
git clone https://github.com/USERNAME/HafzAnaDashboard.git
cd HafzAnaDashboard
```

Ganti `USERNAME` dengan nama akun GitHub milikmu.

**3. Buat branch fitur**

```bash
git checkout -b fitur/FiturBaru
```

**4. Commit perubahan**

```bash
git add .
git commit -m "Menambahkan fitur baru"
```

**5. Push branch**

```bash
git push origin fitur/FiturBaru
```

**6. Buat Pull Request**

Buka repositori hasil fork di GitHub, lalu ajukan Pull Request ke repositori utama.

## 📄 Lisensi

Lisensi proyek belum ditentukan.

## 👨‍💻 Pengembang

**qanziz47-coder**

GitHub: [github.com/qanziz47-coder](https://github.com/qanziz47-coder)

Repositori: [HafzAnyaDashboard](https://github.com/qanziz47-coder/HafzAnyaDashboard)

---

*Dikembangkan untuk menghadirkan pengalaman Stream Deck virtual dari perangkat Android.*
