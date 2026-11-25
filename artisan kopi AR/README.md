# Artisan Kopi AR
Buku menu interaktif Kedai Artisan Kopi berbasis WebAR. Aplikasi menggunakan MindAR Image Tracking dan A-Frame untuk menampilkan visualisasi 3D minuman pada marker foto produk.

## Produk dan urutan target
1. Aren Latte
2. Butterscotch Latte
3. Seasalt Caramel Latte
4. Matcha Latte
5. Americano

## Teknologi
- MindAR Image Tracking untuk mengenali foto menu.
- A-Frame untuk membangun dan merender model minuman 3D secara prosedural.
- HTML, CSS, dan JavaScript untuk antarmuka serta logika aplikasi.
- JSZip untuk membaca paket foto marker.
- GitHub Pages untuk publikasi melalui HTTPS.

## Cara menggunakan
1. Buka aplikasi melalui GitHub Pages.
2. Tekan **Mulai pengalaman AR** dan izinkan akses kamera.
3. Arahkan kamera smartphone ke salah satu foto marker yang dicetak.
4. Model 3D minuman akan muncul pada target yang dikenali.

## Kompilasi image target
1. Buka `compile-targets.html` melalui GitHub Pages.
2. Tekan **Kompilasi 5 marker**.
3. Halaman memuat lima foto dari `assets/markers/marker-reference-photos.zip`, lalu menjalankan MindAR Compiler.
4. Unduh file `targets.mind`.
5. Unggah file tersebut ke folder `assets/targets/` pada repository GitHub dan commit perubahan.
6. GitHub Actions akan memublikasikan ulang aplikasi.

Urutan foto dalam proses kompilasi harus tetap sama dengan urutan produk di atas karena aplikasi menghubungkan target index 0 sampai 4 dengan masing-masing model.

## Struktur utama
- `index.html`: halaman menu dan pemindai WebAR.
- `styles.css`: desain responsif.
- `app.js`: model 3D prosedural, pemuatan foto menu, dan pengendalian kamera.
- `compile-targets.html`: kompilasi lima foto menjadi descriptor MindAR.
- `assets/markers/marker-reference-photos.zip`: paket foto marker JPEG.
- `assets/targets/targets.mind`: file target hasil kompilasi, harus diunggah setelah proses kompilasi.

## Model 3D
Lima minuman dibentuk secara prosedural menggunakan geometri A-Frame. Model terdiri atas gelas, lapisan cairan, es, busa atau garnish, dan detail permukaan sederhana. Aplikasi versi ini tidak memerlukan Unity atau Blender dan tidak menggunakan file GLB eksternal.

## Persyaratan
- Browser modern yang mendukung WebRTC dan WebGL.
- Izin kamera.
- HTTPS (GitHub Pages) atau localhost.
- Pencahayaan yang cukup dan marker tercetak dengan jelas.

## Pengujian
Aplikasi harus diuji pada lima marker dan beberapa kondisi jarak, sudut, serta pencahayaan. Catat browser, perangkat, dan hasil aktual. Jangan menganggap semua kombinasi perangkat otomatis kompatibel.
