const overlay=document.querySelector("#arOverlay");
const status=document.querySelector("#status");
const arStatus=document.querySelector("#arStatus");
const scene=document.querySelector("#arScene");
const start=document.querySelector("#startAR");
let arSystem=null;
let cameraStream=null;

const products={
  aren:{layers:[["#6b351d",0.24,0.22],["#e8d5b9",0.49,0.28],["#8a4b2b",0.74,0.16]],foam:"#ead9c2",sauce:"#a35c2c",ice:"#fff4e4"},
  butterscotch:{layers:[["#b8793d",0.28,0.30],["#e5c49a",0.57,0.34],["#c58b4b",0.82,0.18]],foam:"#f3e2c7",sauce:"#d69b50",ice:"#fff5e5"},
  seasalt:{layers:[["#a45e31",0.27,0.28],["#e0c29b",0.57,0.34],["#f1e6d5",0.82,0.16]],foam:"#fff2df",sauce:"#bd793e",ice:"#fff6e9"},
  matcha:{layers:[["#e9dfc8",0.30,0.32],["#8a9d5a",0.64,0.38]],foam:"#e9e3cf",sauce:"#82934e",ice:"#f6f4e9"},
  americano:{layers:[["#3a2118",0.42,0.55],["#55301e",0.77,0.22]],foam:null,sauce:"#70432b",ice:"#fff0df"}
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
 add(root,"a-cylinder",{position:"0 0.015 0",radius:"0.37",height:"0.045",color:"#b99a78",material:"roughness:0.82"});
 add(root,"a-cylinder",{position:"0 0.73 0",radius:"0.285",height:"1.28",color:"#e9e1d5",opacity:"0.22",material:"transparent:true;roughness:0.12;metalness:0.04;side:double"});
 p.layers.forEach(([color,y,height])=>add(root,"a-cylinder",{position:`0 ${y} 0`,radius:"0.245",height:String(height),color,material:"roughness:0.24"}));
 if(p.foam) add(root,"a-cylinder",{position:"0 0.94 0",radius:"0.245",height:"0.07",color:p.foam,material:"roughness:0.62"});
 add(root,"a-torus",{position:"0 1.38 0",rotation:"90 0 0",radius:"0.265",radiusTubular:"0.018",color:"#f5eadd",material:"transparent:true;opacity:0.72"});
 add(root,"a-cylinder",{position:"0 0.08 0",radius:"0.31",height:"0.025",color:"#f4e9da",opacity:"0.45",material:"transparent:true"});
 const icePositions=[[-.10,.99,.07],[.10,1.02,-.05],[-.04,1.08,-.12],[.12,.94,.10]];
 icePositions.forEach(([x,y,z],i)=>add(root,"a-box",{position:`${x} ${y} ${z}`,rotation:`${12+i*8} ${i*31} ${18-i*5}`,width:"0.115",height:"0.12",depth:"0.105",color:p.ice,opacity:"0.84",material:"transparent:true;roughness:0.08"}));
 if(key==="seasalt"||key==="butterscotch"||key==="aren"){
  add(root,"a-torus",{position:"0 1.04 0",rotation:"90 0 0",radius:"0.17",radiusTubular:"0.025",color:p.sauce});
  add(root,"a-sphere",{position:"0 1.00 0",scale:"0.16 0.035 0.16",color:p.foam||"#ead9bd",material:"roughness:0.5"});
 }
 if(key==="matcha"){
  add(root,"a-sphere",{position:"0 1.01 0",scale:"0.20 0.035 0.20",color:"#9cab70",material:"roughness:0.7"});
 }
 const droplets=[[-.24,.42,.10],[-.22,.72,-.06],[.22,.52,.10],[.21,.84,-.08],[-.13,.24,-.18],[.13,.32,.18]];
 droplets.forEach(([x,y,z])=>add(root,"a-sphere",{position:`${x} ${y} ${z}`,scale:"0.012 0.018 0.012",color:"#ffffff",opacity:"0.55",material:"transparent:true;roughness:0.1"}));
}

document.querySelectorAll(".drink-model").forEach(el=>makeDrink(el,el.dataset.drink));

async function loadMenuPhotos(){
 try{
  const response=await fetch("./assets/markers/marker-reference-photos.zip");
  if(!response.ok) return;
  const zip=await JSZip.loadAsync(await response.arrayBuffer());
  const names=["aren_latte.jpg","butterscotch_latte.jpg","seasalt_caramel_latte.jpg","matcha_latte.jpg","americano.jpg"];
  names.forEach(async(name,index)=>{
   const file=zip.file(name); if(!file)return;
   const blob=await file.async("blob");
   const url=URL.createObjectURL(blob);
   const img=document.querySelector(`[data-marker-photo="${index}"]`);
   if(img) img.src=url;
  });
 }catch(error){console.warn("Foto menu belum dapat dimuat.",error);}
}
loadMenuPhotos();

async function stopAR(){
 try{if(arSystem) await arSystem.stop();}catch(error){console.warn(error);}
 if(cameraStream){cameraStream.getTracks().forEach(track=>track.stop());cameraStream=null;}
}
start.addEventListener("click",async()=>{
 overlay.hidden=false;
 arStatus.textContent="Memeriksa kamera…";
 try{
  if(!window.isSecureContext) throw new Error("Kamera memerlukan HTTPS. Buka aplikasi melalui GitHub Pages.");
  if(!navigator.mediaDevices?.getUserMedia) throw new Error("Browser ini tidak mendukung akses kamera.");
  cameraStream=await navigator.mediaDevices.getUserMedia({audio:false,video:{facingMode:{ideal:"environment"}}});
  cameraStream.getTracks().forEach(track=>track.stop()); cameraStream=null;
  if(!scene.hasLoaded) await new Promise(resolve=>scene.addEventListener("loaded",resolve,{once:true}));
  arSystem=scene.systems["mindar-image-system"];
  if(!arSystem) throw new Error("MindAR belum siap. Muat ulang halaman dan coba lagi.");
  await arSystem.start();
  arStatus.textContent="Kamera aktif · arahkan ke salah satu foto menu";
 }catch(error){
  console.error(error);
  arStatus.textContent=error.message;
  status.textContent=error.message;
 }
});
document.querySelector("#closeAR").addEventListener("click",async()=>{
 await stopAR(); overlay.hidden=true;
 status.textContent="Pemindaian ditutup. Anda dapat memulai kembali.";
});
scene.addEventListener("arReady",()=>arStatus.textContent="Kamera aktif · cari salah satu marker");
scene.addEventListener("arError",event=>{arStatus.textContent="AR gagal dimulai. Periksa izin kamera dan file target.";console.error(event);});
document.querySelectorAll("[mindar-image-target]").forEach((target,index)=>{
 target.addEventListener("targetFound",()=>arStatus.textContent=labels[index]+" terdeteksi");
 target.addEventListener("targetLost",()=>arStatus.textContent="Marker tidak terlihat · arahkan kembali kamera");
});
