import math, os
import numpy as np
import trimesh
from trimesh.visual.material import PBRMaterial

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,"assets","models")
os.makedirs(OUT,exist_ok=True)

def rgba(h,a=255):
    h=h.lstrip("#")
    return np.array([int(h[i:i+2],16) for i in (0,2,4)]+[a],dtype=np.uint8)

def material(name,color,alpha=1.0,rough=.3,metal=0):
    return PBRMaterial(name=name,baseColorFactor=rgba(color,int(alpha*255)).tolist(),
        metallicFactor=metal,roughnessFactor=rough,
        alphaMode="BLEND" if alpha<.999 else "OPAQUE",doubleSided=True)

def add(scene,name,mesh,mat=None):
    if mat is not None: mesh.visual.material=mat
    scene.add_geometry(mesh,geom_name=name,node_name=name)

def lathe(profile,n=96):
    v=[]; f=[]
    for r,y in profile:
        for i in range(n):
            a=2*math.pi*i/n; v.append([r*math.cos(a),y,r*math.sin(a)])
    for j in range(len(profile)):
        j2=(j+1)%len(profile)
        for i in range(n):
            i2=(i+1)%n; a=j*n+i; b=j*n+i2; c=j2*n+i2; d=j2*n+i
            f.extend([[a,b,c],[a,c,d]])
    m=trimesh.Trimesh(vertices=np.array(v),faces=np.array(f),process=True); m.fix_normals()
    return m

def solid(rings,gradient,n=96):
    v=[]; f=[]; colors=[]
    y0=min(y for r,y in rings); y1=max(y for r,y in rings)
    for r,y in rings:
        for i in range(n):
            a=2*math.pi*i/n; v.append([r*math.cos(a),y,r*math.sin(a)])
            colors.append(gradient((y-y0)/(y1-y0+1e-9)))
    for j in range(len(rings)-1):
        for i in range(n):
            i2=(i+1)%n; a=j*n+i; b=j*n+i2; c=(j+1)*n+i2; d=(j+1)*n+i
            f.extend([[a,b,c],[a,c,d]])
    bi=len(v); v.append([0,y0,0]); colors.append(gradient(0))
    ti=len(v); v.append([0,y1,0]); colors.append(gradient(1))
    for i in range(n):
        i2=(i+1)%n; f.append([bi,i2,i])
        a=(len(rings)-1)*n+i; b=(len(rings)-1)*n+i2; f.append([ti,a,b])
    m=trimesh.Trimesh(vertices=np.array(v),faces=np.array(f),process=True); m.fix_normals()
    m.visual.vertex_colors=np.array(colors,dtype=np.uint8)
    return m

def interp(stops,t):
    if t<=stops[0][0]: return rgba(stops[0][1])
    if t>=stops[-1][0]: return rgba(stops[-1][1])
    for (a,ca),(b,cb) in zip(stops[:-1],stops[1:]):
        if a<=t<=b:
            u=(t-a)/(b-a); return np.clip(rgba(ca)*(1-u)+rgba(cb)*u,0,255).astype(np.uint8)

def cyl_y(radius,height):
    m=trimesh.creation.cylinder(radius=radius,height=height,sections=96)
    m.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[1,0,0]))
    return m

def torus_y(major,minor,y,color):
    m=trimesh.creation.torus(major_radius=major,minor_radius=minor,major_sections=64,minor_sections=12)
    m.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[1,0,0]))
    m.apply_translation([0,y,0]); m.visual.face_colors=np.tile(rgba(color),(len(m.faces),1))
    return m

def ice(ext,pos,angle,tint):
    m=trimesh.creation.icosphere(subdivisions=2,radius=1)
    v=np.sign(m.vertices)*np.power(np.abs(m.vertices),.62)
    v=v/(np.max(np.abs(v),axis=1).max()+1e-9)*np.array(ext)[None,:]
    m.vertices=v
    m.apply_transform(trimesh.transformations.rotation_matrix(angle,[0,1,0]))
    m.apply_translation(pos); m.visual.face_colors=np.tile(rgba(tint,225),(len(m.faces),1))
    return m

def sphere(r,pos,color,scale=(1,1,1),alpha=255):
    m=trimesh.creation.icosphere(subdivisions=2,radius=r); m.apply_scale(scale); m.apply_translation(pos)
    m.visual.face_colors=np.tile(rgba(color,alpha),(len(m.faces),1)); return m

def tube(points,radius,color):
    pts=np.array(points,float); v=[]; f=[]; n=10
    for i,p in enumerate(pts):
        t=pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]; t/=np.linalg.norm(t)+1e-9
        ref=np.array([0,1,0.])
        if abs(np.dot(t,ref))>.92: ref=np.array([1,0,0.])
        a=np.cross(t,ref); a/=np.linalg.norm(a)+1e-9; b=np.cross(t,a)
        for j in range(n):
            q=2*math.pi*j/n; v.append(p+radius*(math.cos(q)*a+math.sin(q)*b))
    for i in range(len(pts)-1):
        for j in range(n):
            j2=(j+1)%n; a=i*n+j; b=i*n+j2; c=(i+1)*n+j2; d=(i+1)*n+j
            f.extend([[a,b,c],[a,c,d]])
    m=trimesh.Trimesh(vertices=np.array(v),faces=np.array(f),process=True); m.fix_normals()
    m.visual.face_colors=np.tile(rgba(color),(len(m.faces),1)); return m

ICE=[
 ((.075,.055,.070),(-.105,.965,.035),.35,"#e8e0d0"),
 ((.070,.060,.075),(.045,.982,-.075),-.35,"#f1e9d8"),
 ((.068,.050,.070),(.145,.952,.065),.65,"#e5dfd2"),
 ((.060,.050,.064),(-.015,.985,.105),-.8,"#eee7d8"),
 ((.055,.047,.060),(-.18,.945,-.055),.15,"#e9e3d7")]

SPECS={
 "aren-latte":{"label":"Aren Latte","stops":[(0,"#ead8b6"),(.28,"#dfc18f"),(.55,"#bd8247"),(.82,"#8b4c25"),(1,"#65351d")],"top":"#79401f","streaks":[(.83,.42,.1,"#8a4a25",.012),(.78,.48,2.4,"#a86732",.010)],"swirl":"#b9783d","ice":ICE[:4],"bubbles":[(-.11,.02,.018),(.12,-.07,.014),(.04,.13,.012)],"bubble":"#6d391e"},
 "butterscotch-latte":{"label":"Butterscotch Latte","stops":[(0,"#f0dfc4"),(.25,"#ead2ad"),(.52,"#c99258"),(.82,"#a9622e"),(1,"#8a4a22")],"top":"#995323","streaks":[(.90,.54,-.25,"#d79a4d",.018),(.86,.60,1.5,"#f0c27f",.013),(.82,.48,2.7,"#b66e35",.012)],"swirl":"#e2ad67","ice":ICE,"bubbles":[(-.12,.02,.016),(.10,-.09,.012),(.03,.15,.014)],"bubble":"#8b4b22"},
 "seasalt-caramel-latte":{"label":"Seasalt Caramel Latte","stops":[(0,"#eee0c9"),(.27,"#e3c8a4"),(.54,"#c38a58"),(.82,"#9c5b31"),(1,"#824522")],"top":"#a05c2f","streaks":[(.88,.53,-.5,"#c47a3b",.016),(.84,.58,1.8,"#f0d7ad",.014),(.82,.48,2.8,"#b86c32",.012)],"foam":"#f5e8d4","swirl":"#bf793b","ice":ICE[:4],"bubbles":[(-.10,.04,.014),(.12,-.06,.012)],"bubble":"#8e512e"},
 "matcha-latte":{"label":"Matcha Latte","stops":[(0,"#f0e5ce"),(.30,"#e8ddc1"),(.55,"#c3c99a"),(.82,"#81945a"),(1,"#647a3f")],"top":"#7d9150","streaks":[(.87,.49,-.35,"#9aaa69",.018),(.83,.55,1.9,"#e5e1c8",.014)],"swirl":"#e8e0c8","ice":ICE[:4],"bubbles":[],"bubble":"#647a3f"},
 "americano":{"label":"Americano","stops":[(0,"#4c2a1c"),(.28,"#512c1c"),(.58,"#65371f"),(.84,"#804523"),(1,"#a15d2d")],"top":"#a15d2d","streaks":[(.83,.57,-.4,"#7d4324",.010)],"swirl":"#c1844e","ice":ICE,"bubbles":[(-.13,.01,.018),(.12,-.08,.014),(.04,.14,.012),(-.03,-.15,.010)],"bubble":"#3d2117"}
}

def build(key,s):
    scene=trimesh.Scene()
    glass=lathe([(.218,.025),(.226,.055),(.295,1.125),(.302,1.155),(.289,1.155),(.281,1.125),(.211,.075),(.205,.055)])
    add(scene,"Clear tapered glass body",glass,material("clear glass","#eef6f5",.20,.08,.02))
    base=cyl_y(.218,.035); base.apply_translation([0,.035,0])
    add(scene,"Thick clear glass base",base,material("glass base","#edf5f5",.28,.08,.02))
    add(scene,"Polished glass rim",torus_y(.294,.012,1.145,"#f7f2e8"))
    add(scene,"Glass base highlight",torus_y(.216,.008,.065,"#f3f4ed"))
    grad=lambda t: interp(s["stops"],t)
    liquid=solid([(.195,.105),(.202,.15),(.216,.38),(.236,.66),(.258,.88),(.262,.91)],grad)
    add(scene,"Drink liquid gradient",liquid)
    top=cyl_y(.259,.008); top.apply_translation([0,.909,0])
    add(scene,"Drink meniscus",top,material("drink surface",s["top"],1,.23))
    for i,(ys,ye,theta,color,width) in enumerate(s.get("streaks",[])):
        pts=[]
        for k in range(16):
            t=k/15; y=ys+(ye-ys)*t; th=theta+.22*math.sin(t*math.pi*1.4+i)
            r=.238+(y-.5)*.025; pts.append([r*math.cos(th),y,r*math.sin(th)])
        add(scene,"Internal syrup ribbon "+str(i+1),tube(pts,width,color))
    if s.get("foam"):
        foam=cyl_y(.252,.035); foam.apply_translation([0,.925,0])
        add(scene,"Sea salt cream foam",foam,material("cream foam",s["foam"],1,.62))
    for i,(ext,pos,angle,tint) in enumerate(s["ice"]):
        add(scene,"Ice cube "+str(i+1),ice(ext,pos,angle,tint),material("ice "+str(i+1),tint,.64,.12))
        if i in (0,2):
            h=sphere(.025,[pos[0]-.012,pos[1]+.008,pos[2]+.012],"#ffffff",(1.25,.55,.7),135)
            add(scene,"Ice highlight "+str(i+1),h,material("ice glint","#ffffff",.42,.08))
    if s.get("swirl"):
        pts=[]
        for i in range(65):
            t=i/64; a=2*math.pi*2.15*t+.35; r=.025+.17*t
            pts.append([r*math.cos(a),.952+.008*math.sin(a*2),r*math.sin(a)])
        add(scene,"Surface syrup swirl",tube(pts,.009,s["swirl"]))
    for i,(x,z,r) in enumerate(s.get("bubbles",[])):
        b=sphere(r,[x,.924,z],s["bubble"],(1,.35,1),225)
        add(scene,"Coffee bubble "+str(i+1),b,material("coffee bubble",s["bubble"],1,.35))
    for i,(x,y,z,r) in enumerate([(-.20,.36,.115,.009),(.205,.49,.105,.008),(-.16,.72,.18,.007),(.16,.82,.17,.008),(.03,.28,.20,.006)]):
        d=sphere(r,[x,y,z],"#ffffff",(.75,1.4,.55),180)
        add(scene,"Condensation droplet "+str(i+1),d,material("condensation","#ffffff",.48,.08))
    scene.metadata={"product":s["label"],"brand":"Kedai Artisan Kopi","model":"Procedural iced coffee glass"}
    return scene

for key,spec in SPECS.items():
    scene=build(key,spec)
    out=os.path.join(OUT,key+".glb")
    with open(out,"wb") as f: f.write(scene.export(file_type="glb"))
    check=trimesh.load(out,force="scene")
    assert len(check.geometry)>=18 and check.bounds[1][1]>1.1
    print("Built",out,os.path.getsize(out),"bytes",len(check.geometry),"meshes")
