# Artisan Kopi AR

Aplikasi buku menu interaktif berbasis Web Augmented Reality (WebAR) untuk brand fiktif Kedai Artisan Kopi. Pengunjung membuka website melalui browser smartphone, mengizinkan akses kamera, lalu memindai salah satu foto produk pada buku menu. MindAR mengenali gambar dan A-Frame menampilkan model minuman 3D prosedural di atas marker.

## Produk dan urutan target

| Target index | Produk | Model |
|---:|---|---|
| 0 | Aren Latte | Gelas, espresso, susu, gula aren, es dan topping |
| 1 | Butterscotch Latte | Gelas, susu, lapisan butterscotch, es dan topping |
| 2 | Seasalt Caramel Latte | Gelas, susu, karamel, sea salt dan es |
| 3 | Matcha Latte | Gelas, susu, matcha dan es |
| 4 | Americano | Gelas, kopi, es dan detail permukaan |

## Teknologi
- HTML5, CSS3 dan JavaScript untuk antarmuka dan logika aplikasi.
- MindAR Image Tracking untuk mengenali foto marker.
- A-Frame untuk membangun dan merender objek 3D secara prosedural.
- JSZip untuk membaca lima foto marker dari arsip ZIP.
- GitHub Pages untuk publikasi melalui HTTPS.

## Cara menggunakan aplikasi
1. Buka https://dandielucky.github.io/Project/ melalui browser smartphone.
2. Tekan **Mulai pengalaman AR** dan izinkan akses kamera.
3. Arahkan kamera ke salah satu foto marker yang dicetak.
4. Setelah MindAR mengenali foto, model 3D produk terkait akan muncul.

## Kompilasi marker MindAR
File `targets.mind` harus dibuat dari lima foto marker. Aplikasi tidak dapat menjalankan image tracking sebelum file ini tersedia.

1. Buka https://dandielucky.github.io/Project/compile-targets.html.
2. Tekan **Kompilasi 5 marker**.
3. Tunggu proses analisis fitur visual hingga selesai. Browser akan mengunduh `targets.mind`.
4. Buka repository GitHub dan masuk ke `artisan kopi AR/assets/targets/`.
5. Unggah `targets.mind` dengan nama file persis tersebut.
6. Commit perubahan dan tunggu workflow GitHub Pages selesai.
7. Muat ulang aplikasi dan uji kelima marker.

Urutan marker harus tetap: Aren Latte, Butterscotch Latte, Seasalt Caramel Latte, Matcha Latte, Americano. Jangan mengubah urutan tanpa mengompilasi ulang file target.

## Aset foto marker
Lima foto JPEG tersedia di `assets/markers/marker-reference-photos.zip`. File tersebut menjadi sumber foto pada halaman menu dan input untuk compiler MindAR. Cetak foto dengan ukuran yang cukup, kontras dan ketajaman yang baik. Hindari melipat, memotong, atau memantulkan cahaya pada marker.

## Model 3D
Versi aplikasi saat ini membangun lima model secara prosedural menggunakan primitive geometry A-Frame melalui `app.js`. Setiap minuman memiliki lapisan warna, gelas, es dan topping sesuai karakter produk. Implementasi ini tidak memerlukan Unity atau Blender. Model masih berupa visualisasi 3D demonstrasi dan bukan hasil pemindaian produk fisik.

## Pengujian
Lakukan uji pada smartphone dengan browser modern yang mendukung WebRTC dan WebGL. Berikan izin kamera. Uji lima marker satu per satu pada jarak dan sudut berbeda serta kondisi pencahayaan cukup. Catat perangkat, browser, keberhasilan deteksi, kestabilan tracking dan waktu respons. Jangan menyatakan aplikasi lulus uji sebelum pengujian langsung dilakukan.

## Struktur utama
- `index.html`: halaman menu dan pemindai WebAR.
- `styles.css`: tampilan responsif.
- `app.js`: model 3D prosedural, pemuatan foto menu dan pengendalian kamera.
- `compile-targets.html`: kompilasi lima foto menjadi file target MindAR.
- `assets/markers/marker-reference-photos.zip`: paket lima foto marker.
- `assets/targets/targets.mind`: file target hasil kompilasi yang perlu diunggah.

## Metode pengembangan
Proyek menggunakan kerangka Multimedia Development Life Cycle (MDLC), yang mencakup Concept, Design, Material Collecting, Assembly, Testing dan Distribution. Tahap testing perlu diselesaikan melalui pengujian langsung pada perangkat sasaran.
