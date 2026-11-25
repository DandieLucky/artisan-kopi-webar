const overlay=document.querySelector("#arOverlay");
const status=document.querySelector("#status");
const arStatus=document.querySelector("#arStatus");
const scene=document.querySelector("#arScene");
const start=document.querySelector("#startAR");
let arSystem=null;

const products={
  aren:{layers:[["#5b2c19",0.18,0.18],["#ead8bd",0.43,0.27],["#8c4a2a",0.72,0.22]],foam:"#eadbc8",syrup:"#9b5429",ice:"#fff5e8"},
  butterscotch:{layers:[["#a9612f",0.19,0.18],["#e6c69e",0.46,0.31],["#c17b3e",0.75,0.25]],foam:"#f2e1c9",syrup:"#d79b52",ice:"#fff4e3"},
  seasalt:{layers:[["#a65d32",0.18,0.18],["#e3c9a8",0.45,0.30],["#f0e5d4",0.76,0.26]],foam:"#fff0dd",syrup:"#b96e35",ice:"#fff5e8"},
  matcha:{layers:[["#e9dfc9",0.20,0.20],["#8b9c5c",0.55,0.42]],foam:"#e8e4d3",syrup:"#879a50",ice:"#f5f4e9"},
  americano:{layers:[["#2b1711",0.30,0.38],["#4b2a1b",0.68,0.30]],foam:null,syrup:"#70432b",ice:"#fff0df"}
};
const labels=["Aren Latte","Butterscotch Latte","Seasalt Caramel Latte","Matcha Latte","Americano"];

function add(parent,tag,attrs){
 const el=document.createElement(tag);
 for(const [key,value] of Object.entries(attrs)) el.setAttribute(key,value);
 parent.appendChild(el);
 return el;
}
function makeDrink(root,key){
 const p=products[key];
 root.innerHTML="";
 root.setAttribute("scale","0.72 0.72 0.72");

 // Coaster and tapered transparent glass.
 add(root,"a-cylinder",{position:"0 -0.035 0",radius:"0.34",height:"0.055",color:"#8e694b",material:"roughness:0.88"});
 add(root,"a-cone",{position:"0 0.65 0",radiusBottom:"0.245",radiusTop:"0.30",height:"1.30",color:"#f5eee4",opacity:"0.20",material:"transparent:true;roughness:0.08;metalness:0.04;side:double"});
 add(root,"a-cylinder",{position:"0 0.025 0",radius:"0.245",height:"0.045",color:"#e8dfd3",opacity:"0.32",material:"transparent:true;roughness:0.12"});

 // Distinct liquid layers for each signature drink.
 p.layers.forEach(([color,y,height],i)=>{
   const radiusBottom=key==="americano" ? 0.225 : 0.218;
   const radiusTop=key==="americano" ? 0.245 : 0.235;
   add(root,"a-cone",{position:`0 ${y} 0`,radiusBottom:String(radiusBottom),radiusTop:String(radiusTop),height:String(height),color,material:"roughness:0.28"});
 });

 // Glass rim and subtle reflections.
 add(root,"a-torus",{position:"0 1.305 0",rotation:"90 0 0",radius:"0.294",radiusTubular:"0.014",color:"#fff9ef",opacity:"0.82",material:"transparent:true;roughness:0.08"});
 add(root,"a-torus",{position:"0 0.025 0",rotation:"90 0 0",radius:"0.235",radiusTubular:"0.012",color:"#fff9ef",opacity:"0.55",material:"transparent:true"});
 add(root,"a-cylinder",{position:"-0.205 0.67 0.145",radius:"0.012",height:"0.92",color:"#ffffff",opacity:"0.40",material:"transparent:true;roughness:0.08"});
 add(root,"a-cylinder",{position:"0.218 0.66 0.105",radius:"0.008",height:"0.76",color:"#ffffff",opacity:"0.24",material:"transparent:true;roughness:0.08"});

 // Ice cubes, foam and topping.
 const icePositions=[[-.105,1.02,.07],[.105,1.045,-.055],[-.035,1.105,-.12],[.135,.99,.10]];
 icePositions.forEach(([x,y,z],i)=>add(root,"a-box",{position:`${x} ${y} ${z}`,rotation:`${12+i*8} ${i*31} ${18-i*5}`,width:"0.12",height:"0.12",depth:"0.105",color:p.ice,opacity:"0.88",material:"transparent:true;roughness:0.10"}));
 if(p.foam){
   add(root,"a-sphere",{position:"0 1.055 0",scale:"0.215 0.055 0.215",color:p.foam,material:"roughness:0.68"});
 }
 if(["seasalt","butterscotch","aren"].includes(key)){
   add(root,"a-torus",{position:"0 1.075 0",rotation:"90 0 0",radius:"0.145",radiusTubular:"0.021",color:p.syrup,material:"roughness:0.36"});
   add(root,"a-sphere",{position:"0.025 1.105 0.025",scale:"0.045 0.022 0.045",color:"#f5e9d8",material:"roughness:0.8"});
 }
 if(key==="matcha"){
   add(root,"a-sphere",{position:"0 1.08 0",scale:"0.205 0.04 0.205",color:"#9eac70",material:"roughness:0.8"});
   add(root,"a-cylinder",{position:"0 1.122 0",radius:"0.075",height:"0.006",color:"#7f914b",material:"roughness:0.9"});
 }
 if(key==="americano"){
   add(root,"a-torus",{position:"0 1.045 0",rotation:"90 0 0",radius:"0.15",radiusTubular:"0.012",color:"#9b704d",opacity:"0.8",material:"transparent:true"});
 }
 const droplets=[[-.235,.40,.10],[-.225,.72,-.06],[.235,.52,.10],[.22,.85,-.08],[-.12,.24,-.18],[.13,.32,.18]];
 droplets.forEach(([x,y,z])=>add(root,"a-sphere",{position:`${x} ${y} ${z}`,scale:"0.012 0.018 0.012",color:"#ffffff",opacity:"0.52",material:"transparent:true;roughness:0.1"}));
}
document.querySelectorAll(".drink-model").forEach(el=>makeDrink(el,el.dataset.drink));

async function loadMenuPhotos(){
 try{
  const response=await fetch("./assets/markers/marker-reference-photos.zip");
  if(!response.ok) throw new Error("Paket foto marker belum tersedia.");
  const zip=await JSZip.loadAsync(await response.arrayBuffer());
  const names=["aren_latte.jpg","butterscotch_latte.jpg","seasalt_caramel_latte.jpg","matcha_latte.jpg","americano.jpg"];
  await Promise.all(names.map(async(name,index)=>{
   const file=zip.file(name);
   if(!file) throw new Error("Foto "+name+" tidak ditemukan dalam paket marker.");
   const blob=await file.async("blob");
   const url=URL.createObjectURL(blob);
   const img=document.querySelector(`[data-marker-photo="${index}"]`);
   if(img) img.src=url;
  }));
 }catch(error){
  console.warn("Foto menu belum dapat dimuat.",error);
  status.textContent="Foto marker belum termuat. Periksa koneksi internet lalu muat ulang halaman.";
 }
}
loadMenuPhotos();

async function stopAR(){
 try{if(arSystem) await arSystem.stop();}catch(error){console.warn(error);}
 arSystem=null;
}
start.addEventListener("click",async()=>{
 overlay.hidden=false;
 arStatus.textContent="Memeriksa file target dan menyiapkan kamera…";
 try{
  if(!window.isSecureContext) throw new Error("Kamera memerlukan HTTPS. Buka aplikasi melalui GitHub Pages.");
  const targetCheck=await fetch("./assets/targets/targets.mind",{method:"HEAD",cache:"no-store"});
  if(!targetCheck.ok) throw new Error("File target AR belum tersedia. Buka halaman Kompilasi Marker, buat targets.mind, lalu unggah ke folder assets/targets di GitHub.");
  if(!scene.hasLoaded) await new Promise(resolve=>scene.addEventListener("loaded",resolve,{once:true}));
  await new Promise(resolve=>requestAnimationFrame(resolve));
  if(typeof scene.resize==="function") scene.resize();
  arSystem=scene.systems["mindar-image-system"];
  if(!arSystem) throw new Error("MindAR belum siap. Muat ulang halaman dan coba lagi.");
  await arSystem.start();
  arStatus.textContent="Kamera aktif · arahkan ke salah satu foto menu";
  status.textContent="Kamera aktif. Arahkan ke salah satu foto marker.";
 }catch(error){
  console.error(error);
  arStatus.textContent=error.message;
  status.textContent=error.message;
 }
});
document.querySelector("#closeAR").addEventListener("click",async()=>{
 await stopAR();
 overlay.hidden=true;
 status.textContent="Pemindaian ditutup. Anda dapat memulai kembali.";
});
scene.addEventListener("arReady",()=>arStatus.textContent="Kamera aktif · cari salah satu marker");
scene.addEventListener("arError",event=>{
 arStatus.textContent="AR gagal dimulai. Periksa izin kamera, koneksi internet, dan file target.";
 console.error(event);
});
document.querySelectorAll("[mindar-image-target]").forEach((target,index)=>{
 target.addEventListener("targetFound",()=>arStatus.textContent=labels[index]+" terdeteksi");
 target.addEventListener("targetLost",()=>arStatus.textContent="Marker tidak terlihat · arahkan kembali kamera");
});
