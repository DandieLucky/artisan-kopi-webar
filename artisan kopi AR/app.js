const overlay = document.querySelector("#arOverlay");
const status = document.querySelector("#status");
const arStatus = document.querySelector("#arStatus");
const scene = document.querySelector("#arScene");
const start = document.querySelector("#startAR");
const close = document.querySelector("#closeAR");

let arSystem = null;
const labels = [
  "Aren Latte",
  "Butterscotch Latte",
  "Seasalt Caramel Latte",
  "Matcha Latte",
  "Americano"
];

const models = [...document.querySelectorAll(".drink-model")];
let loadedModels = 0;

models.forEach((model, index) => {
  model.addEventListener("model-loaded", () => {
    loadedModels += 1;
    console.info(labels[index] + " GLB berhasil dimuat.");
    if (loadedModels === models.length) {
      status.textContent = "Lima model 3D siap. Anda dapat memulai pemindaian AR.";
    }
  });
  model.addEventListener("model-error", (event) => {
    console.error("Model GLB gagal dimuat:", labels[index], event.detail);
    status.textContent = "Model " + labels[index] + " gagal dimuat. Muat ulang halaman atau periksa koneksi.";
  });
});

async function loadMenuPhotos() {
  try {
    const response = await fetch("./assets/markers/marker-reference-photos.zip", { cache: "no-store" });
    if (!response.ok) throw new Error("Paket foto marker belum tersedia.");
    const zip = await JSZip.loadAsync(await response.arrayBuffer());
    const names = [
      "aren_latte.jpg",
      "butterscotch_latte.jpg",
      "seasalt_caramel_latte.jpg",
      "matcha_latte.jpg",
      "americano.jpg"
    ];

    await Promise.all(names.map(async (name, index) => {
      const file = zip.file(name);
      if (!file) throw new Error("Foto " + name + " tidak ditemukan.");
      const blob = await file.async("blob");
      const url = URL.createObjectURL(blob);
      const image = document.querySelector('[data-marker-photo="' + index + '"]');
      if (image) image.src = url;
    }));
  } catch (error) {
    console.warn("Foto marker tidak dapat dimuat:", error);
    status.textContent = "Foto marker belum termuat. Periksa koneksi internet.";
  }
}
loadMenuPhotos();

async function stopAR() {
  try {
    if (arSystem) await arSystem.stop();
  } catch (error) {
    console.warn("AR stop:", error);
  }
  arSystem = null;
}

start.addEventListener("click", async () => {
  overlay.hidden = false;
  arStatus.textContent = "Memeriksa aset 3D dan menyiapkan kamera…";

  try {
    if (!window.isSecureContext) {
      throw new Error("Kamera memerlukan HTTPS. Buka aplikasi melalui GitHub Pages.");
    }

    const targetResponse = await fetch("./assets/targets/targets.mind", { method: "HEAD", cache: "no-store" });
    if (!targetResponse.ok) {
      throw new Error("File targets.mind belum tersedia pada server.");
    }

    const modelPaths = [
      "./assets/models/aren-latte.glb",
      "./assets/models/butterscotch-latte.glb",
      "./assets/models/seasalt-caramel-latte.glb",
      "./assets/models/matcha-latte.glb",
      "./assets/models/americano.glb"
    ];
    const checks = await Promise.all(modelPaths.map(path => fetch(path, { method: "HEAD", cache: "no-store" })));
    const missing = checks.findIndex(response => !response.ok);
    if (missing !== -1) {
      throw new Error("Aset GLB " + labels[missing] + " belum tersedia. Tunggu proses publikasi GitHub Pages selesai.");
    }

    if (!scene.hasLoaded) {
      await new Promise(resolve => scene.addEventListener("loaded", resolve, { once: true }));
    }

    await new Promise(resolve => requestAnimationFrame(resolve));
    if (typeof scene.resize === "function") scene.resize();

    arSystem = scene.systems["mindar-image-system"];
    if (!arSystem) throw new Error("MindAR belum siap. Muat ulang halaman dan coba lagi.");

    await arSystem.start();
    arStatus.textContent = "Kamera aktif · arahkan ke salah satu foto menu";
    status.textContent = "Kamera aktif. Arahkan ke salah satu foto marker.";
  } catch (error) {
    console.error(error);
    arStatus.textContent = error.message;
    status.textContent = error.message;
  }
});

close.addEventListener("click", async () => {
  await stopAR();
  overlay.hidden = true;
  status.textContent = "Pemindaian ditutup. Anda dapat memulai kembali.";
});

scene.addEventListener("arReady", () => {
  arStatus.textContent = "Kamera aktif · cari salah satu marker";
});

scene.addEventListener("arError", event => {
  arStatus.textContent = "AR gagal dimulai. Periksa izin kamera, koneksi internet, dan file target.";
  console.error("MindAR error:", event);
});

document.querySelectorAll("[mindar-image-target]").forEach((target, index) => {
  target.addEventListener("targetFound", () => {
    arStatus.textContent = labels[index] + " terdeteksi";
  });
  target.addEventListener("targetLost", () => {
    arStatus.textContent = "Marker tidak terlihat · arahkan kembali kamera";
  });
});
