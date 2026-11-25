# Artisan Kopi AR
Buku menu interaktif Kedai Artisan Kopi berbasis WebAR. Aplikasi menggunakan MindAR Image Tracking dan A-Frame untuk menampilkan visualisasi 3D minuman pada marker menu.

## Produk
1. Aren Latte
2. Butterscotch Latte
3. Seasalt Caramel Latte
4. Matcha Latte
5. Americano

## Jalankan
1. Aktifkan GitHub Pages pada repository, atau jalankan server lokal seperti `npx serve .`.
2. Buka folder `artisan kopi AR` melalui HTTPS. Kamera memerlukan secure context (HTTPS atau localhost).
3. Buka `compile-targets.html`, unggah kelima marker SVG dari folder `assets/markers`, lalu unduh hasil `targets.mind`.
4. Simpan file tersebut di `assets/targets/targets.mind`. GitHub Pages dapat meng-host file ini.
5. Buka `index.html` dari server HTTPS, izinkan akses kamera, lalu arahkan kamera ke salah satu marker.

## Struktur
- `index.html`: aplikasi WebAR.
- `styles.css`: antarmuka responsif.
- `app.js`: konfigurasi image tracking dan visualisasi 3D A-Frame.
- `compile-targets.html`: alat lokal untuk mengompilasi marker menjadi file MindAR.
- `assets/markers/`: lima marker SVG yang dapat dicetak.
- `assets/targets/`: lokasi file `targets.mind` hasil kompilasi.

## Catatan teknis
File `targets.mind` tidak dapat dibuat hanya dengan menyalin gambar. MindAR harus mengompilasi image target menjadi descriptor tracking. Karena itu, gunakan halaman `compile-targets.html` satu kali setelah mengunduh atau mengkloning proyek. Marker harus dicetak dengan ukuran dan rasio asli, tidak dipotong, dan tidak diberi filter.

Visualisasi minuman saat ini tersusun dari geometri 3D A-Frame (gelas, cairan, es, foam, dan garnish), bukan file GLB eksternal. Struktur aplikasi disiapkan agar model GLB dapat menggantikan visualisasi tersebut kemudian.

## Pengujian
Uji di Chrome Android atau Safari iOS melalui HTTPS. Pastikan pencahayaan cukup, marker tercetak tajam, dan kamera memiliki izin.
