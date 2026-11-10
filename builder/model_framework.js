/* Throw Brooo / Polished Model Framework v1.0
 * Three.js r128, classic <script> compatible. Loaded before animal_models.py.
 * Zero external 3D assets; gameplay IDs, sizes, odds and income remain untouched.
 */
const POLISHED_MODEL_PROFILES = Object.freeze({
  frog:        { motion:'hop',   bob:.38, speed:1.10 },
  bunny:       { motion:'hop',   bob:.30, speed:1.05 },
  bear:        { motion:'walk',  bob:.08, speed:.65 },
  zebra:       { motion:'trot',  bob:.14, speed:1.10 },
  giraffe:     { motion:'walk',  bob:.10, speed:.60 },
  lion:        { motion:'walk',  bob:.09, speed:.72 },
  camel:       { motion:'walk',  bob:.08, speed:.60 },
  scorpion:    { motion:'scuttle', bob:.05, speed:1.20 },
  dimetrodon:  { motion:'walk',  bob:.06, speed:.50 },
  toucan:      { motion:'flap',  bob:.22, speed:1.30 },
  gorilla:     { motion:'walk',  bob:.10, speed:.65 },
  tiger:       { motion:'walk',  bob:.10, speed:.75 },
  seal:        { motion:'swim',  bob:.20, speed:.85 },
  shark:       { motion:'swim',  bob:.23, speed:.75 },
  kraken:      { motion:'float', bob:.25, speed:.66 },
  unicorn:     { motion:'trot',  bob:.14, speed:1.05 },
  phoenix:     { motion:'flap',  bob:.30, speed:1.35 },
  dragon:      { motion:'flap',  bob:.24, speed:.80 }
});

// One unit primitive per type. Per-mesh scale produces correctly sized details.
const POLISHED_GEO = {
  box: new THREE.BoxGeometry(1, 1, 1),
  orb: new THREE.IcosahedronGeometry(0.5, 1),
  cone: new THREE.ConeGeometry(0.5, 1, 6)
};
Object.values(POLISHED_GEO).forEach(geo => { geo.userData.polishedShared = true; });
const POLISHED_MATERIALS = new Map();

function polishedColor(hex, mutationId, preserve) {
  const original = new THREE.Color(hex);
  if (preserve || mutationId === 'normal') return original;
  if (mutationId === 'silver') return new THREE.Color(0xcbd5e1).lerp(original, .13);
  if (mutationId === 'golden') return new THREE.Color(0xfacc15).lerp(original, .17);
  if (mutationId === 'rainbow') {
    const hsl = { h:0, s:0, l:0 };
    original.getHSL(hsl);
    return new THREE.Color().setHSL((hsl.h + .22) % 1, .84, .58);
  }
  if (mutationId === 'cosmic') return new THREE.Color(0x8b5cf6).lerp(original, .18);
  return original;
}
function polishedMaterial(hex, mutationId, preserve, transparent, opacity, side) {
  const key = [hex, mutationId, preserve ? 1:0, transparent ? 1:0, opacity === undefined ? 1 : opacity, side === undefined ? 0 : side].join(':');
  if (POLISHED_MATERIALS.has(key)) return POLISHED_MATERIALS.get(key);
  const metal = !preserve && (mutationId === 'silver' || mutationId === 'golden');
  const cosmic = !preserve && mutationId === 'cosmic';
  const mat = new THREE.MeshStandardMaterial({
    color: polishedColor(hex, mutationId, preserve),
    roughness: metal ? .30 : .62,
    metalness: metal ? .58 : .06,
    flatShading: true,
    transparent: Boolean(transparent),
    opacity: opacity === undefined ? 1 : opacity,
    side: side === undefined ? THREE.FrontSide : side,
    emissive: cosmic ? 0x1e0d43 : 0x000000,
    emissiveIntensity: cosmic ? .30 : 0
  });
  mat.userData.polishedShared = true;
  POLISHED_MATERIALS.set(key, mat);
  return mat;
}

// Create small, re-usable parts. Coordinates are in ORIGINAL model units.
// The original animal factory already passes the final species/size/mutation scale.
function polishedKit(root, scale, mutationId) {
  const joints = root.userData || {};
  const part = (shape, parent, xyz, dims, color, opts = {}) => {
    const mesh = new THREE.Mesh(POLISHED_GEO[shape], polishedMaterial(
      color, mutationId, !!opts.preserve, !!opts.transparent, opts.opacity, opts.side
    ));
    mesh.position.set(xyz[0] * scale, xyz[1] * scale, xyz[2] * scale);
    mesh.scale.set(dims[0] * scale, dims[1] * scale, dims[2] * scale);
    if (opts.rot) mesh.rotation.set(opts.rot[0], opts.rot[1], opts.rot[2]);
    mesh.castShadow = !!opts.shadow;
    mesh.receiveShadow = false;
    mesh.userData.polishedDetail = true;
    parent.add(mesh);
    return mesh;
  };
  const box = (p, xyz, dims, color, opts) => part('box', p, xyz, dims, color, opts);
  const orb = (p, xyz, dims, color, opts) => part('orb', p, xyz, dims, color, opts);
  const cone = (p, xyz, dims, color, opts) => part('cone', p, xyz, dims, color, opts);
  return { root, head:joints.head || root, tail:joints.tail || root,
    leftWing:joints.leftWing || root, rightWing:joints.rightWing || root,
    ears:joints.ears || root, box, orb, cone };
}

const POLISHED_DETAIL_BUILDERS = Object.freeze({
  frog(k) {
    for (const x of [-.52, 0, .52]) k.orb(k.root,[x,1.02,.48],[.29,.15,.32],0x14532d);
    for (const x of [-.72,-.52,.52,.72]) k.orb(k.root,[x,.11,-1.03],[.17,.11,.29],0x6ee7b7);
    for (const x of [-.42,.42]) k.orb(k.head,[x,1.57,-1.01],[.11,.10,.06],0xffffff,{preserve:true});
    k.box(k.head,[0,.96,-1.18],[.55,.055,.035],0x14532d,{preserve:true});
  },
  bunny(k) {
    for (const x of [-.30,.30]) {
      k.orb(k.head,[x,.05,-.49],[.23,.17,.09],0xfda4af,{preserve:true});
      k.box(k.root,[x,.08,-.78],[.18,.07,.16],0xfda4af,{preserve:true});
    }
    for (const side of [-1,1]) for (let i = 0; i < 2; i++)
      k.box(k.head,[side*.51,-.10+i*.12,-.52],[.33,.018,.018],0xd1d5db,{preserve:true,rot:[0,0,side*.12]});
    k.orb(k.tail,[0,0,.24],[.48,.50,.48],0xffffff,{preserve:true});
  },
  bear(k) {
    for (const x of [-.55,.55]) for (const z of [-1.03,-.70,.60])
      k.box(k.root,[x,.09,z],[.18,.08,.18],0x292524,{preserve:true});
    k.box(k.head,[0,-.30,-.95],[.38,.07,.035],0x292524,{preserve:true});
    for (const x of [-.39,.39]) k.box(k.head,[x,.29,-.60],[.30,.10,.08],0x451a03);
  },
  zebra(k) {
    for (const x of [-.45,.45]) for (const z of [-.65,.65])
      k.box(k.root,[x,.34,z],[.36,.14,.36],0x111827,{preserve:true});
    for (const x of [-.23,.23]) k.orb(k.head,[x,-.14,-.89],[.09,.10,.07],0x111827,{preserve:true});
    for (let i = 0; i < 4; i++) k.cone(k.root,[0,2.50,-.52+i*.17],[.20,.36,.24],0x111827,{preserve:true});
  },
  giraffe(k) {
    for (const side of [-1,1]) for (const z of [-.65,.14,.82])
      k.box(k.root,[side*.78,2.46,z],[.065,.35,.38],0x92400e,{preserve:true});
    for (const side of [-1,1]) for (const y of [3.7,4.4,5.1])
      k.box(k.root,[side*.39,y,-.89],[.055,.31,.36],0x92400e,{preserve:true});
    for (const x of [-.24,.24]) k.orb(k.head,[x,.70,-.15],[.24,.20,.24],0x92400e,{preserve:true});
  },
  lion(k) {
    for (const x of [-1.00,-.55,0,.55,1.00]) {
      k.cone(k.root,[x,2.55,-.92],[.45,.70,.45],0x92400e,{preserve:true,rot:[0,0,x*.22]});
      k.cone(k.root,[x,1.05,-.93],[.43,.56,.44],0x92400e,{preserve:true,rot:[Math.PI,0,0]});
    }
    for (const x of [-.24,.24]) k.orb(k.head,[x,-.26,-.76],[.22,.19,.09],0xfef3c7,{preserve:true});
  },
  camel(k) {
    for (const z of [-.45,.36]) {
      k.orb(k.root,[0,2.32,z],[.75,.42,.60],0xd97706);
      k.box(k.root,[0,2.65,z],[.38,.08,.42],0x92400e,{preserve:true});
    }
    for (const x of [-.50,.50]) for (const z of [-.75,.65])
      k.box(k.root,[x,.17,z],[.48,.16,.48],0x78350f,{preserve:true});
  },
  scorpion(k) {
    for (const side of [-1,1]) for (let i=0; i<3; i++)
      k.box(k.root,[side*(.85+i*.24),.23,-.08+i*.36],[.40,.10,.13],0x92400e,{preserve:true,rot:[0,side*.23,side*.15]});
    for (let i=0; i<4; i++) k.orb(k.tail,[0,.15+i*.27,-i*.37],[.45-i*.06,.34,.42-i*.05],0xf59e0b);
    k.cone(k.tail,[0,1.40,-1.20],[.35,.72,.35],0x7f1d1d,{preserve:true,rot:[Math.PI,0,0]});
  },
  dimetrodon(k) {
    for (let z=-.95; z<1.00; z+=.43) {
      k.box(k.root,[-.075,2.10,z],[.06,.85,.10],0xffc34d,{preserve:true});
      k.box(k.root,[ .075,2.10,z],[.06,.85,.10],0xffc34d,{preserve:true});
    }
    for (const x of [-.75,.75]) for (const z of [-.63,.12,.74])
      k.orb(k.root,[x,1.03,z],[.22,.16,.31],0x854d0e,{preserve:true});
    for (const x of [-.45,.45]) k.orb(k.head,[x,.22,-.57],[.15,.10,.09],0xfff7ed,{preserve:true});
  },
  toucan(k) {
    k.box(k.head,[0,.20,-1.21],[.57,.12,1.07],0xfde047,{preserve:true});
    k.box(k.head,[0,-.43,-1.24],[.57,.055,1.12],0x1f2937,{preserve:true});
    for (const side of [-1,1]) for (let i=0;i<3;i++)
      k.box(side===-1?k.leftWing:k.rightWing,[side*.03,-.32,.34+i*.23],[.18,.12,.30],0x064e3b,{preserve:true});
    for (const x of [-.38,.38]) k.orb(k.head,[x,.14,-.54],[.11,.11,.07],0xffffff,{preserve:true});
  },
  gorilla(k) {
    for (const x of [-.32,.32])
      k.orb(k.root,[x,1.28,-1.10],[.48,.53,.22],0x4b5563,{preserve:true});
    for (const x of [-.91,.91]) for (const dx of [-.14,0,.14])
      k.box(k.root,[x+dx,.11,-.93],[.13,.10,.30],0x111827,{preserve:true});
    k.box(k.head,[0,-.28,-.62],[.52,.27,.18],0x9ca3af,{preserve:true});
  },
  tiger(k) {
    for (const side of [-1,1]) for (let i=0;i<3;i++)
      k.box(k.root,[side*.78,1.53,-.56+i*.53],[.08,.45,.13],0x111827,{preserve:true,rot:[0,0,-side*.12]});
    for (let i=0;i<3;i++) k.box(k.tail,[0,-.3-i*.22,.17+i*.13],[.18,.13,.16],0x111827,{preserve:true});
    for (const side of [-1,1])
      k.box(k.head,[side*.45,.25,-.56],[.12,.34,.07],0x111827,{preserve:true,rot:[0,0,side*.17]});
  },
  seal(k) {
    for (const side of [-1,1]) {
      k.orb(k.head,[side*.18,-.20,-.49],[.20,.12,.12],0xffffff,{preserve:true});
      for (let i=0;i<2;i++)
        k.box(k.head,[side*.44,-.19+i*.13,-.53],[.34,.018,.017],0xf8fafc,{preserve:true,rot:[0,0,side*.20]});
    }
    for (const x of [-.43,.43]) for (const z of [0,.45,.85])
      k.orb(k.root,[x,1.28,z],[.19,.08,.20],0x64748b,{preserve:true});
    k.orb(k.head,[0,-.15,-.55],[.17,.15,.09],0x111827,{preserve:true});
  },
  shark(k) {
    for (const side of [-1,1]) for(let i=0;i<4;i++)
      k.box(k.root,[side*.73,1.11,-.86+i*.19],[.05,.40,.055],0x1e3a8a,{preserve:true,rot:[0,0,side*.06]});
    k.cone(k.root,[0,2.95,-.12],[.35,.57,.48],0x60a5fa);
    for (const x of [-.40,.40]) k.orb(k.head,[x,.18,-.54],[.09,.09,.05],0xffffff,{preserve:true});
  },
  kraken(k) {
    for (const x of [-.42,0,.42])
      k.orb(k.root,[x,2.86,-.48],[.22,.12,.18],0xf9a8d4,{preserve:true});
    for(let i=0;i<8;i++) {
      const a=i*Math.PI/4, x=Math.sin(a)*.90, z=Math.cos(a)*.90;
      k.orb(k.root,[x*.98,.42,z*.98],[.18,.16,.18],0xfbcfe8,{preserve:true});
    }
    k.orb(k.root,[0,2.30,-.81],[.24,.20,.08],0xfef08a,{preserve:true});
  },
  unicorn(k) {
    for(let i=0;i<5;i++)
      k.orb(k.head,[0,.42+i*.25,.10+i*.04],[.24-i*.024,.11,.23-i*.02],0xfef08a,{preserve:true});
    for(const x of [-.45,.45]) for(const z of [-.65,.65])
      k.box(k.root,[x,.26,z],[.36,.08,.37],0xfde68a,{preserve:true});
    for(let i=0;i<3;i++) k.cone(k.tail,[0,-.3-i*.28,.21],[.25,.55,.30],[0xf472b6,0xa78bfa,0x7dd3fc][i],{preserve:true});
  },
  phoenix(k) {
    for(const side of [-1,1]) {
      const wing=side===-1?k.leftWing:k.rightWing;
      for(let i=0;i<5;i++)
        k.cone(wing,[side*(.28+i*.35),-.18,.12+i*.16],[.25,.76,.28],i%2?0xfacc15:0xfb923c,{preserve:true,rot:[Math.PI*.5,0,side*.12]});
    }
    for(let i=0;i<3;i++) k.cone(k.head,[(-1+i)*.21,.92,.15],[.19,.65,.25],0xfde047,{preserve:true});
    for(const x of [-.4,0,.4]) k.orb(k.tail,[x,.14,1.42],[.24,.12,.30],0xf97316,{preserve:true});
  },
  dragon(k) {
    for(const side of [-1,1]) {
      const wing=side===-1?k.leftWing:k.rightWing;
      for(let i=0;i<3;i++)
        k.box(wing,[side*(.05+i*.37),.13,-.45+i*.44],[.11,.10,1.72],0xddd6fe,{preserve:true,rot:[0,0,side*.08]});
    }
    for(let i=0;i<4;i++) k.cone(k.root,[0,2.55,-.62+i*.48],[.32,.70,.35],0x7c3aed,{preserve:true});
    for(const x of [-.36,.36]) k.orb(k.head,[x,.18,-.63],[.15,.11,.06],0xfef08a,{preserve:true});
    k.cone(k.tail,[0,.30,1.92],[.68,.74,.55],0x7c3aed,{preserve:true,rot:[Math.PI*.5,0,0]});
  }
});

// Called once per animal AFTER the original body and mutation aura are built.
function enhanceAnimalModel(group, animalId, scale, animal, mutation) {
  const id = animalId;
  const mutationId = mutation && mutation.id ? mutation.id : 'normal';
  if (!POLISHED_MODEL_PROFILES[id] || group.userData.polishedModel) return group;

  // Retain eyes, teeth, and glowing effects. Refinish Lambert body materials only.
  const replacedMaterials = new Set();
  group.traverse(obj => {
    if (!obj.isMesh || !obj.material || !obj.material.isMeshLambertMaterial) return;
    const m = obj.material;
    const hex = m.color.getHex();
    const preserve = (hex === 0xffffff || hex === 0xf8fafc || hex === 0x111111);
    replacedMaterials.add(m);
    obj.material = polishedMaterial(hex, mutationId, preserve, m.transparent, m.opacity, m.side);
  });
  replacedMaterials.forEach(material => material.dispose());
  const kit = polishedKit(group, scale, mutationId);
  POLISHED_DETAIL_BUILDERS[id](kit);
  group.userData.polishedModel = {
    version: 1, animalId: id, mutationId, profile: POLISHED_MODEL_PROFILES[id]
  };
  return group;
}

function polishedIdleBob(group, phase) {
  const p = group.userData.polishedModel;
  if (!p) return Math.abs(Math.sin(phase)) * .55;
  const speed = p.profile.speed;
  const w = phase * speed;
  if (p.profile.motion === 'hop') return Math.pow(Math.max(0,Math.sin(w)), 2) * p.profile.bob;
  if (['swim','float','flap'].includes(p.profile.motion)) return .17 + Math.sin(w) * p.profile.bob;
  return Math.abs(Math.sin(w)) * p.profile.bob;
}

// Augment existing head/tail/wing animation without replacing its behavior.
function animatePolishedAnimal(group, phase) {
  const p = group.userData.polishedModel;
  if (!p) return;
  if (group.userData.ears && group.userData.ears.children.length)
    group.userData.ears.rotation.z = Math.sin(phase * .7) * .09;
  if (p.profile.motion === 'swim' && group.userData.tail)
    group.userData.tail.rotation.y = Math.sin(phase * 1.8) * .48;
  if (p.profile.motion === 'scuttle' && group.userData.tail)
    group.userData.tail.rotation.x = Math.sin(phase*.7) * .12;
  if (p.profile.motion === 'flap' && group.userData.leftWing && group.userData.rightWing) {
    const flap = Math.sin(phase*2.3) * .52;
    group.userData.leftWing.rotation.z = flap;
    group.userData.rightWing.rotation.z = -flap;
  }
}

// Dispose instance-specific meshes only. Cached detail geometry/materials are shared.
function disposePolishedAnimal(group) {
  if (!group) return;
  group.traverse(obj => {
    if (!obj.isMesh) return;
    const geo = obj.geometry;
    if (geo && !(geo.userData && geo.userData.polishedShared)) geo.dispose();
    const list = Array.isArray(obj.material) ? obj.material : [obj.material];
    for (const mat of list) if (mat && !(mat.userData && mat.userData.polishedShared)) mat.dispose();
  });
  if (group.parent) group.parent.remove(group);
}
