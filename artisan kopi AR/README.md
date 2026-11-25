# Artisan Kopi AR

Aplikasi buku menu interaktif berbasis Web Augmented Reality (WebAR) untuk brand fiktif Kedai Artisan Kopi. Pengunjung membuka website melalui browser smartphone, mengizinkan akses kamera, lalu memindai salah satu foto produk pada buku menu. MindAR mengenali gambar dan A-Frame menampilkan model minuman 3D dalam format GLB.

## Produk dan urutan target

| Target index | Produk | Model GLB |
|---:|---|---|
| 0 | Aren Latte | `aren-latte.glb` |
| 1 | Butterscotch Latte | `butterscotch-latte.glb` |
| 2 | Seasalt Caramel Latte | `seasalt-caramel-latte.glb` |
| 3 | Matcha Latte | `matcha-latte.glb` |
| 4 | Americano | `americano.glb` |

## Teknologi
- HTML5, CSS3 dan JavaScript untuk antarmuka dan logika aplikasi.
- MindAR Image Tracking untuk mengenali foto marker.
- A-Frame untuk memuat dan merender model GLB.
- Trimesh dan NumPy untuk membangun geometri 3D prosedural.
- JSZip untuk membaca lima foto marker dari arsip ZIP.
- GitHub Actions dan GitHub Pages untuk pembuatan aset serta publikasi melalui HTTPS.

## Model 3D
Aplikasi menggunakan lima model GLB terpisah. Setiap model menampilkan gelas bening berbentuk tumbler, badan minuman dengan gradasi warna, es batu, detail permukaan, dan aksen sirup atau foam sesuai varian. Model dibuat secara prosedural melalui script `tools/generate_models.py`, sehingga tidak memerlukan Unity atau Blender.

Palet model:
- **Aren Latte:** gradasi susu krem, gula aren keemasan dan espresso cokelat.
- **Butterscotch Latte:** susu krem, karamel hangat dan butterscotch amber.
- **Seasalt Caramel Latte:** susu, kopi karamel, foam sea salt dan drizzle karamel.
- **Matcha Latte:** susu krem dan matcha hijau.
- **Americano:** kopi cokelat gelap dengan bagian atas lebih amber.

Ukuran model dibuat ringan untuk kebutuhan demonstrasi WebAR. Model tetap perlu diperiksa pada beberapa perangkat karena kualitas transparansi dan pencahayaan dapat berbeda antar-browser.

## Cara menggunakan aplikasi
1. Buka https://dandielucky.github.io/Project/ melalui browser smartphone.
2. Tekan **Mulai pengalaman AR** dan izinkan akses kamera.
3. Arahkan kamera ke salah satu foto marker yang dicetak.
4. Setelah MindAR mengenali foto, model 3D produk terkait akan muncul.

## Kompilasi marker MindAR
File `assets/targets/targets.mind` harus tersedia sebelum image tracking berjalan. File tersebut dikompilasi dari lima foto marker pada halaman `compile-targets.html`. Urutan target harus tetap Aren Latte, Butterscotch Latte, Seasalt Caramel Latte, Matcha Latte, Americano.

## Pembuatan model
GitHub Actions menjalankan `tools/generate_models.py` saat deploy. Script membuat lima file GLB pada `assets/models/`, lalu workflow memasukkan aset tersebut ke commit dan memublikasikan website. Untuk menjalankan generator secara lokal, instal Python 3.11, NumPy dan Trimesh, lalu jalankan:

```bash
python -m pip install numpy trimesh
python "artisan kopi AR/tools/generate_models.py"
```

## Pengujian
Lakukan uji pada smartphone dengan browser modern yang mendukung WebRTC dan WebGL. Berikan izin kamera. Uji kelima marker satu per satu pada jarak dan sudut berbeda serta kondisi pencahayaan cukup. Catat perangkat, browser, keberhasilan deteksi, kestabilan tracking, tampilan model dan waktu respons. Jangan menyatakan aplikasi lulus uji sebelum pengujian langsung dilakukan.

## Struktur utama
- `index.html`: halaman menu dan pemindai WebAR.
- `styles.css`: tampilan responsif.
- `app.js`: pemuatan foto menu, validasi aset, dan pengendalian kamera.
- `tools/generate_models.py`: generator lima model GLB.
- `assets/models/`: lima model minuman 3D.
- `compile-targets.html`: kompilasi lima foto menjadi file target MindAR.
- `assets/markers/marker-reference-photos.zip`: paket lima foto marker.
- `assets/targets/targets.mind`: file target hasil kompilasi.

## Metode pengembangan
Proyek menggunakan kerangka Multimedia Development Life Cycle (MDLC), yang mencakup Concept, Design, Material Collecting, Assembly, Testing dan Distribution. Tahap testing perlu diselesaikan melalui pengujian langsung pada perangkat sasaran.
