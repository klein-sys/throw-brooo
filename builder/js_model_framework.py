# -*- coding: utf-8 -*-
# Polished animal model framework for Throw Brooo.
JS_MODEL_FRAMEWORK = r'''
/* Throw Brooo / Polished Model Framework v2.0
 * Three.js r128, classic <script> compatible. Loaded before animal_models.py.
 * Zero external 3D assets; procedural HTML5 canvas textures + fine voxel anatomy.
 */
const POLISHED_MODEL_PROFILES = Object.freeze({
  frog:        { motion:'hop',     bob:.38, speed:1.10 },
  bunny:       { motion:'hop',     bob:.30, speed:1.05 },
  bear:        { motion:'walk',    bob:.08, speed:.65 },
  zebra:       { motion:'trot',    bob:.14, speed:1.10 },
  giraffe:     { motion:'walk',    bob:.10, speed:.60 },
  lion:        { motion:'walk',    bob:.09, speed:.72 },
  camel:       { motion:'walk',    bob:.08, speed:.60 },
  scorpion:    { motion:'scuttle', bob:.05, speed:1.20 },
  dimetrodon:  { motion:'walk',    bob:.06, speed:.50 },
  toucan:      { motion:'flap',    bob:.22, speed:1.30 },
  gorilla:     { motion:'walk',    bob:.10, speed:.65 },
  tiger:       { motion:'walk',    bob:.10, speed:.75 },
  seal:        { motion:'swim',    bob:.20, speed:.85 },
  shark:       { motion:'swim',    bob:.23, speed:.75 },
  kraken:      { motion:'float',   bob:.25, speed:.66 },
  unicorn:     { motion:'trot',    bob:.14, speed:1.05 },
  phoenix:     { motion:'flap',    bob:.30, speed:1.35 },
  dragon:      { motion:'flap',    bob:.24, speed:.80 }
});

// Unit primitives per geometry type. Cached and shared.
const POLISHED_GEO = {
  box: new THREE.BoxGeometry(1, 1, 1),
  orb: new THREE.IcosahedronGeometry(0.5, 1),
  cone: new THREE.ConeGeometry(0.5, 1, 6)
};
Object.values(POLISHED_GEO).forEach(geo => { geo.userData.polishedShared = true; });
const POLISHED_MATERIALS = new Map();
const ANIMAL_TEXTURE_CACHE = new Map();

/**
 * Procedural HTML5 2D Canvas Texture Generator for all 18 Animal Species
 * Creates crisp 128x128 textures with NearestFilter for authentic voxel aesthetic.
 */
function createAnimalTexture(animalId, mutationId, baseHex) {
  const key = `${animalId}:${mutationId}:${baseHex}`;
  if (ANIMAL_TEXTURE_CACHE.has(key)) return ANIMAL_TEXTURE_CACHE.get(key);

  const canvas = document.createElement('canvas');
  canvas.width = 128;
  canvas.height = 128;
  const ctx = canvas.getContext('2d');

  const r0 = (baseHex >> 16) & 255;
  const g0 = (baseHex >> 8) & 255;
  const b0 = baseHex & 255;

  const isSilver = mutationId === 'silver';
  const isGold = mutationId === 'golden';
  const isRainbow = mutationId === 'rainbow';
  const isCosmic = mutationId === 'cosmic';

  let baseFill = `rgb(${r0},${g0},${b0})`;
  if (isSilver) baseFill = '#cbd5e1';
  else if (isGold) baseFill = '#facc15';
  else if (isRainbow) baseFill = '#f472b6';
  else if (isCosmic) baseFill = '#3b0764';

  ctx.fillStyle = baseFill;
  ctx.fillRect(0, 0, 128, 128);

  switch (animalId) {
    case 'frog': {
      // Mottled emerald/dark spots + lime-yellow ventral belly
      ctx.fillStyle = isSilver ? '#94a3b8' : isGold ? '#d97706' : isCosmic ? '#581c87' : '#14532d';
      const frogSpots = [[24, 28, 9], [64, 20, 12], [104, 32, 10], [38, 54, 11], [88, 52, 13], [64, 74, 9]];
      for (const [x, y, r] of frogSpots) {
        ctx.beginPath();
        ctx.arc(x, y, r, 0, Math.PI * 2);
        ctx.fill();
      }
      const bellyGrad = ctx.createLinearGradient(0, 78, 0, 128);
      bellyGrad.addColorStop(0, 'rgba(254, 240, 138, 0)');
      bellyGrad.addColorStop(1, isSilver ? 'rgba(241, 245, 249, 0.85)' : isGold ? 'rgba(254, 240, 138, 0.95)' : isCosmic ? 'rgba(216, 180, 254, 0.7)' : 'rgba(167, 243, 208, 0.9)');
      ctx.fillStyle = bellyGrad;
      ctx.fillRect(0, 78, 128, 50);
      break;
    }

    case 'bunny': {
      // Soft fur grain micro-dither + rosy paw pad beans
      ctx.fillStyle = isSilver ? '#e2e8f0' : isGold ? '#fef08a' : isCosmic ? '#8b5cf6' : '#f8fafc';
      for (let y = 6; y < 120; y += 8) {
        for (let x = (y % 16 === 0 ? 4 : 12); x < 124; x += 16) {
          ctx.fillRect(x, y, 6, 2);
        }
      }
      ctx.fillStyle = isSilver ? '#fbcfe8' : isGold ? '#fef08a' : isCosmic ? '#f472b6' : '#fda4af';
      ctx.beginPath();
      ctx.arc(104, 108, 7, 0, Math.PI * 2);
      ctx.arc(94, 96, 3.5, 0, Math.PI * 2);
      ctx.arc(104, 93, 3.5, 0, Math.PI * 2);
      ctx.arc(114, 96, 3.5, 0, Math.PI * 2);
      ctx.fill();
      break;
    }

    case 'bear': {
      // Grizzly fur striations + tan snout patch
      ctx.fillStyle = isSilver ? '#64748b' : isGold ? '#b45309' : isCosmic ? '#2e1065' : '#292524';
      for (let y = 8; y < 124; y += 12) {
        for (let x = 6; x < 122; x += 14) {
          ctx.fillRect(x + (y % 8), y, 8, 3);
        }
      }
      ctx.fillStyle = isSilver ? '#cbd5e1' : isGold ? '#fef3c7' : isCosmic ? '#c084fc' : '#d97706';
      ctx.beginPath();
      ctx.ellipse(64, 110, 26, 16, 0, 0, Math.PI * 2);
      ctx.fill();
      break;
    }

    case 'zebra': {
      // Bold black & white zebra stripes
      ctx.fillStyle = isSilver ? '#0f172a' : isGold ? '#78350f' : isCosmic ? '#090514' : '#111827';
      const zebraStripes = [
        [0, 10, 128, 20], [0, 36, 128, 48], [0, 64, 128, 76],
        [0, 92, 128, 106], [0, 118, 128, 128]
      ];
      for (const [x1, y1, x2, y2] of zebraStripes) {
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.bezierCurveTo(40, y1 - 6, 80, y2 + 4, x2, y2);
        ctx.lineTo(x2, y2 + 10);
        ctx.bezierCurveTo(80, y2 + 14, 40, y1 + 4, x1, y1 + 10);
        ctx.closePath();
        ctx.fill();
      }
      break;
    }

    case 'giraffe': {
      // Reticulated polygonal patches with cream border channels
      ctx.strokeStyle = isSilver ? '#e2e8f0' : isGold ? '#fef9c3' : isCosmic ? '#e9d5ff' : '#fef3c7';
      ctx.lineWidth = 4;
      ctx.fillStyle = isSilver ? '#475569' : isGold ? '#b45309' : isCosmic ? '#581c87' : '#92400e';
      const patches = [
        [[10, 12], [54, 8], [50, 48], [12, 44]],
        [[66, 10], [118, 14], [114, 52], [62, 46]],
        [[14, 58], [56, 56], [52, 94], [8, 92]],
        [[68, 58], [116, 62], [112, 102], [64, 96]],
        [[12, 104], [58, 106], [50, 124], [14, 124]],
        [[70, 108], [114, 112], [110, 124], [66, 124]]
      ];
      for (const poly of patches) {
        ctx.beginPath();
        ctx.moveTo(poly[0][0], poly[0][1]);
        for (let i = 1; i < poly.length; i++) ctx.lineTo(poly[i][0], poly[i][1]);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
      }
      break;
    }

    case 'lion': {
      // Golden coat with pale underbelly and whisker dots
      const lionGrad = ctx.createLinearGradient(0, 60, 0, 128);
      lionGrad.addColorStop(0, 'rgba(254, 243, 199, 0)');
      lionGrad.addColorStop(1, isSilver ? 'rgba(241, 245, 249, 0.85)' : isGold ? 'rgba(254, 240, 138, 0.95)' : isCosmic ? 'rgba(216, 180, 254, 0.7)' : 'rgba(254, 243, 199, 0.9)');
      ctx.fillStyle = lionGrad;
      ctx.fillRect(0, 60, 128, 68);

      ctx.fillStyle = isSilver ? '#334155' : isGold ? '#78350f' : isCosmic ? '#3b0764' : '#451a03';
      for (const [x, y] of [[28, 94], [38, 92], [48, 95], [28, 104], [38, 102], [48, 105], [80, 95], [90, 92], [100, 94], [80, 105], [90, 102], [100, 104]]) {
        ctx.beginPath();
        ctx.arc(x, y, 2.2, 0, Math.PI * 2);
        ctx.fill();
      }
      break;
    }

    case 'camel': {
      // Fluffy woolly coat + decorative desert saddlecloth
      ctx.fillStyle = isSilver ? '#94a3b8' : isGold ? '#d97706' : isCosmic ? '#6b21a8' : '#92400e';
      for (let y = 4; y < 45; y += 8) {
        for (let x = 4; x < 124; x += 10) {
          ctx.fillRect(x + (y % 4), y, 4, 3);
        }
      }
      ctx.fillStyle = '#dc2626';
      ctx.fillRect(0, 52, 128, 30);
      ctx.fillStyle = '#06b6d4';
      for (let x = 6; x < 128; x += 22) {
        ctx.beginPath();
        ctx.moveTo(x + 11, 56);
        ctx.lineTo(x + 18, 67);
        ctx.lineTo(x + 11, 78);
        ctx.lineTo(x + 4, 67);
        ctx.closePath();
        ctx.fill();
      }
      ctx.fillStyle = '#fde047';
      ctx.fillRect(0, 50, 128, 3);
      ctx.fillRect(0, 81, 128, 3);
      break;
    }

    case 'scorpion': {
      // Segmented chitin plates with amber rim sheen
      ctx.fillStyle = isSilver ? '#475569' : isGold ? '#b45309' : isCosmic ? '#1e0d43' : '#78350f';
      for (let y = 14; y < 124; y += 22) {
        ctx.fillRect(0, y, 128, 14);
        ctx.fillStyle = isSilver ? '#94a3b8' : isGold ? '#fde047' : isCosmic ? '#c084fc' : '#f59e0b';
        ctx.fillRect(0, y - 2, 128, 3);
        ctx.fillStyle = isSilver ? '#475569' : isGold ? '#b45309' : isCosmic ? '#1e0d43' : '#78350f';
      }
      break;
    }

    case 'dimetrodon': {
      // Reptilian hide + sunburst sail gradient
      const sailGrad = ctx.createLinearGradient(0, 0, 0, 70);
      sailGrad.addColorStop(0, '#facc15');
      sailGrad.addColorStop(0.5, '#ea580c');
      sailGrad.addColorStop(1, '#991b1b');
      ctx.fillStyle = sailGrad;
      ctx.fillRect(0, 0, 128, 70);

      ctx.fillStyle = '#1c1917';
      for (let x = 12; x < 128; x += 18) {
        ctx.fillRect(x, 0, 3, 70);
      }
      ctx.fillStyle = isSilver ? '#64748b' : isGold ? '#b45309' : isCosmic ? '#3b0764' : '#854d0e';
      for (let y = 78; y < 126; y += 8) {
        for (let x = (y % 16 === 0 ? 4 : 10); x < 124; x += 12) {
          ctx.beginPath();
          ctx.arc(x, y, 3, 0, Math.PI * 2);
          ctx.fill();
        }
      }
      break;
    }

    case 'toucan': {
      // Jet-black plumage + white throat ruff + rainbow beak gradient
      ctx.fillStyle = isSilver ? '#1e293b' : isCosmic ? '#0a0319' : '#0f172a';
      ctx.fillRect(0, 0, 128, 128);

      ctx.fillStyle = '#f8fafc';
      ctx.beginPath();
      ctx.ellipse(64, 40, 48, 26, 0, 0, Math.PI * 2);
      ctx.fill();

      const beakColors = ['#fde047', '#fb923c', '#ef4444', '#06b6d4'];
      for (let i = 0; i < 4; i++) {
        ctx.fillStyle = beakColors[i];
        ctx.fillRect(i * 32, 88, 32, 40);
      }
      break;
    }

    case 'gorilla': {
      // Dark fur + silverback dorsal striations + chiseled chest
      ctx.fillStyle = isSilver ? '#e2e8f0' : isGold ? '#fef08a' : isCosmic ? '#d8b4fe' : '#9ca3af';
      for (let y = 10; y < 70; y += 6) {
        ctx.fillRect(16, y, 96, 2.5);
      }
      ctx.fillStyle = isSilver ? '#334155' : isCosmic ? '#1e0d43' : '#1f2937';
      ctx.beginPath();
      ctx.rect(22, 78, 38, 36);
      ctx.rect(68, 78, 38, 36);
      ctx.fill();
      break;
    }

    case 'tiger': {
      // Fiery orange coat with distinctive vertical tiger stripes
      ctx.fillStyle = isSilver ? '#0f172a' : isGold ? '#78350f' : isCosmic ? '#090514' : '#111827';
      const tigerStripes = [
        [16, 12, 10, 52], [38, 8, 8, 58], [62, 14, 11, 48],
        [86, 10, 9, 54], [108, 16, 10, 46],
        [24, 76, 9, 44], [48, 72, 11, 48], [76, 78, 9, 42], [100, 74, 10, 46]
      ];
      for (const [sx, sy, sw, sh] of tigerStripes) {
        ctx.beginPath();
        ctx.moveTo(sx, sy);
        ctx.lineTo(sx + sw, sy);
        ctx.lineTo(sx + sw * 0.4, sy + sh);
        ctx.closePath();
        ctx.fill();
      }
      ctx.fillStyle = '#f8fafc';
      ctx.beginPath();
      ctx.ellipse(64, 124, 34, 14, 0, 0, Math.PI * 2);
      ctx.fill();
      break;
    }

    case 'seal': {
      // Glossy blubber texture with spotted leopard-seal markings
      ctx.fillStyle = isSilver ? '#475569' : isGold ? '#b45309' : isCosmic ? '#4c1d95' : '#334155';
      const sealSpots = [[20, 24, 5], [44, 38, 7], [80, 28, 6], [108, 40, 5], [32, 68, 6], [64, 60, 8], [94, 72, 7]];
      for (const [x, y, r] of sealSpots) {
        ctx.beginPath();
        ctx.arc(x, y, r, 0, Math.PI * 2);
        ctx.fill();
      }
      const sealBelly = ctx.createLinearGradient(0, 80, 0, 128);
      sealBelly.addColorStop(0, 'rgba(241, 245, 249, 0)');
      sealBelly.addColorStop(1, 'rgba(241, 245, 249, 0.9)');
      ctx.fillStyle = sealBelly;
      ctx.fillRect(0, 80, 128, 48);
      break;
    }

    case 'shark': {
      // Ocean countershading: top half deep slate blue, bottom half stark white
      ctx.fillStyle = '#f8fafc';
      ctx.fillRect(0, 64, 128, 64);

      ctx.fillStyle = '#0f172a';
      for (let i = 0; i < 5; i++) {
        ctx.fillRect(20 + i * 10, 36, 3, 24);
      }
      break;
    }

    case 'kraken': {
      // Suction cups + bioluminescent glowing mantle spots
      ctx.fillStyle = '#fbcfe8';
      ctx.strokeStyle = '#be185d';
      ctx.lineWidth = 2;
      for (let y = 18; y < 120; y += 28) {
        for (const x of [32, 64, 96]) {
          ctx.beginPath();
          ctx.arc(x, y, 9, 0, Math.PI * 2);
          ctx.fill();
          ctx.stroke();
          ctx.fillStyle = '#be185d';
          ctx.beginPath();
          ctx.arc(x, y, 3, 0, Math.PI * 2);
          ctx.fill();
          ctx.fillStyle = '#fbcfe8';
        }
      }
      ctx.fillStyle = isCosmic ? '#67e8f9' : '#fef08a';
      for (const [x, y] of [[18, 14], [110, 14], [16, 80], [112, 80], [64, 120]]) {
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, Math.PI * 2);
        ctx.fill();
      }
      break;
    }

    case 'unicorn': {
      // Pearlescent ivory coat + pastel rainbow mane highlights
      const maneColors = ['#f472b6', '#c084fc', '#818cf8', '#38bdf8', '#34d399'];
      for (let i = 0; i < 5; i++) {
        ctx.fillStyle = maneColors[i];
        ctx.fillRect(i * 25, 0, 26, 44);
      }
      ctx.fillStyle = '#facc15';
      const sparkles = [[24, 70], [86, 62], [54, 96], [108, 104]];
      for (const [x, y] of sparkles) {
        ctx.fillRect(x - 1, y - 4, 2, 8);
        ctx.fillRect(x - 4, y - 1, 8, 2);
      }
      break;
    }

    case 'phoenix': {
      // Burning flame feather gradient from crimson to golden yellow
      const flameGrad = ctx.createLinearGradient(0, 0, 0, 128);
      flameGrad.addColorStop(0, '#fde047');
      flameGrad.addColorStop(0.4, '#f97316');
      flameGrad.addColorStop(1, '#b91c1c');
      ctx.fillStyle = flameGrad;
      ctx.fillRect(0, 0, 128, 128);

      ctx.fillStyle = 'rgba(254, 240, 138, 0.45)';
      for (let y = 10; y < 120; y += 14) {
        for (let x = 8; x < 120; x += 16) {
          ctx.beginPath();
          ctx.moveTo(x, y);
          ctx.lineTo(x + 8, y + 10);
          ctx.lineTo(x - 4, y + 10);
          ctx.closePath();
          ctx.fill();
        }
      }
      break;
    }

    case 'dragon': {
      // Draconic overlapping diamond scales
      ctx.strokeStyle = isSilver ? '#94a3b8' : isGold ? '#fef08a' : isCosmic ? '#c084fc' : '#a855f7';
      ctx.lineWidth = 1.8;
      ctx.fillStyle = isSilver ? '#334155' : isGold ? '#b45309' : isCosmic ? '#2e1065' : '#581c87';
      const step = 20;
      for (let y = 0; y < 128; y += step) {
        const offset = (y / step) % 2 === 0 ? 0 : step / 2;
        for (let x = -step; x < 128 + step; x += step) {
          ctx.beginPath();
          ctx.moveTo(x + offset, y);
          ctx.lineTo(x + offset + step / 2, y + step / 2);
          ctx.lineTo(x + offset, y + step);
          ctx.lineTo(x + offset - step / 2, y + step / 2);
          ctx.closePath();
          ctx.fill();
          ctx.stroke();
        }
      }
      break;
    }
  }

  // Starry cosmic nebula overlay for Cosmic mutations
  if (isCosmic) {
    ctx.fillStyle = '#ffffff';
    const cosmicStars = [
      [14, 18, 1.5], [42, 34, 1.0], [78, 16, 2.0], [112, 28, 1.5],
      [28, 64, 1.2], [64, 52, 2.2], [96, 70, 1.5], [120, 84, 1.0],
      [18, 108, 1.8], [54, 114, 1.2], [88, 98, 2.0], [110, 118, 1.5]
    ];
    for (const [sx, sy, sr] of cosmicStars) {
      ctx.beginPath();
      ctx.arc(sx, sy, sr, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  const tex = new THREE.CanvasTexture(canvas);
  tex.magFilter = THREE.NearestFilter;
  tex.minFilter = THREE.NearestFilter;
  ANIMAL_TEXTURE_CACHE.set(key, tex);
  return tex;
}

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

function polishedMaterial(hex, mutationId, preserve, transparent, opacity, side, animalId) {
  const key = [hex, mutationId, preserve ? 1:0, transparent ? 1:0, opacity === undefined ? 1 : opacity, side === undefined ? 0 : side, animalId || ''].join(':');
  if (POLISHED_MATERIALS.has(key)) return POLISHED_MATERIALS.get(key);
  const isSilver = !preserve && mutationId === 'silver';
  const isGolden = !preserve && mutationId === 'golden';
  const isCosmic = !preserve && mutationId === 'cosmic';

  let map = null;
  if (!preserve && animalId) {
    map = createAnimalTexture(animalId, mutationId, hex);
  }

  const mat = new THREE.MeshStandardMaterial({
    color: polishedColor(hex, mutationId, preserve),
    roughness: isGolden ? 0.18 : isSilver ? 0.22 : 0.58,
    metalness: isGolden ? 0.72 : isSilver ? 0.65 : 0.08,
    map: map,
    flatShading: true,
    transparent: Boolean(transparent),
    opacity: opacity === undefined ? 1 : opacity,
    side: side === undefined ? THREE.FrontSide : side,
    emissive: isCosmic ? 0x3b0764 : 0x000000,
    emissiveIntensity: isCosmic ? 0.45 : 0
  });
  mat.userData.polishedShared = true;
  POLISHED_MATERIALS.set(key, mat);
  return mat;
}

// Create reusable anatomical parts.
function polishedKit(root, scale, mutationId, animalId) {
  const joints = root.userData || {};
  const part = (shape, parent, xyz, dims, color, opts = {}) => {
    const mesh = new THREE.Mesh(POLISHED_GEO[shape], polishedMaterial(
      color, mutationId, !!opts.preserve, !!opts.transparent, opts.opacity, opts.side, opts.textured ? animalId : undefined
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

/**
 * 1-by-1 Sculpted 3D Anatomical Voxel Detail Builders for All 18 Animals
 */
const POLISHED_DETAIL_BUILDERS = Object.freeze({
  // 1. Forest: Tree Frog
  frog(k) {
    // Mottled skin bumps along spine
    for (const x of [-.52, 0, .52]) k.orb(k.root, [x, 1.02, .48], [.29, .15, .32], 0x14532d);
    // 3D webbed digits with toe suction pads on all 4 limbs
    for (const x of [-.72, -.52, .52, .72]) k.orb(k.root, [x, .11, -1.03], [.17, .11, .29], 0x6ee7b7);
    for (const x of [-.95, -.78, .78, .95]) k.orb(k.root, [x, .11, .38], [.19, .12, .26], 0x6ee7b7);
    // Bulging golden eyes with horizontal black pupil slits
    for (const x of [-.42, .42]) {
      k.orb(k.head, [x, 1.57, -1.01], [.13, .12, .07], 0xfacc15, {preserve:true});
      k.box(k.head, [x, 1.57, -1.05], [.08, .025, .04], 0x111111, {preserve:true});
    }
    // Wide mouth seam line
    k.box(k.head, [0, .96, -1.18], [.55, .055, .035], 0x14532d, {preserve:true});
  },

  // 2. Forest: Bunny
  bunny(k) {
    // Pink inner ears
    for (const x of [-.30, .30]) {
      k.orb(k.head, [x, .05, -.49], [.23, .17, .09], 0xfda4af, {preserve:true});
      k.box(k.root, [x, .08, -.78], [.18, .07, .16], 0xfda4af, {preserve:true});
    }
    // Whiskers and cheek fluffs
    for (const side of [-1, 1]) {
      k.orb(k.head, [side * .42, -.12, -.48], [.18, .16, .14], 0xffffff, {preserve:true});
      for (let i = 0; i < 2; i++)
        k.box(k.head, [side * .51, -.10 + i * .12, -.52], [.33, .018, .018], 0xd1d5db, {preserve:true, rot:[0, 0, side * .12]});
    }
    // Fluffy cottontail puff
    k.orb(k.tail, [0, 0, .24], [.48, .50, .48], 0xffffff, {preserve:true});
  },

  // 3. Forest: Bear
  bear(k) {
    // Dark curved claws on all 4 paws
    for (const x of [-.55, .55]) {
      for (const z of [-1.03, .60]) {
        for (const dx of [-.09, 0, .09])
          k.box(k.root, [x + dx, .08, z - .12], [.06, .06, .14], 0x1c1917, {preserve:true});
      }
    }
    // Snout with nose pad and nostrils
    k.box(k.head, [0, -.30, -.95], [.38, .07, .035], 0x292524, {preserve:true});
    k.orb(k.head, [-.08, -.26, -1.02], [.06, .05, .04], 0x111111, {preserve:true});
    k.orb(k.head, [.08, -.26, -1.02], [.06, .05, .04], 0x111111, {preserve:true});
    // Round ears with deep cup shading
    for (const x of [-.39, .39]) k.box(k.head, [x, .29, -.60], [.30, .10, .08], 0x451a03);
  },

  // 4. Savanna: Zebra
  zebra(k) {
    // Polished dark hooves
    for (const x of [-.45, .45]) for (const z of [-.65, .65])
      k.box(k.root, [x, .34, z], [.36, .14, .36], 0x111827, {preserve:true});
    // Dark muzzle with nostrils
    for (const x of [-.23, .23]) k.orb(k.head, [x, -.14, -.89], [.09, .10, .07], 0x111827, {preserve:true});
    // Stiff bristled two-tone mane along neck crest
    for (let i = 0; i < 5; i++)
      k.cone(k.root, [0, 2.50, -.52 + i * .17], [.20, .36, .24], i % 2 === 0 ? 0x111827 : 0xffffff, {preserve:true});
  },

  // 5. Savanna: Giraffe
  giraffe(k) {
    // Polygonal side patches
    for (const side of [-1, 1]) for (const z of [-.65, .14, .82])
      k.box(k.root, [side * .78, 2.46, z], [.065, .35, .38], 0x92400e, {preserve:true});
    for (const side of [-1, 1]) for (const y of [3.7, 4.4, 5.1])
      k.box(k.root, [side * .39, y, -.89], [.055, .31, .36], 0x92400e, {preserve:true});
    // Sculpted ossicones (tufted horn stalks)
    for (const x of [-.24, .24]) {
      k.box(k.head, [x, .76, -.15], [.08, .32, .08], 0xd97706);
      k.orb(k.head, [x, .92, -.15], [.18, .16, .18], 0x92400e, {preserve:true});
    }
    // Long fringed tail tuft
    k.cone(k.tail, [0, -.42, .32], [.22, .54, .22], 0x92400e, {preserve:true});
  },

  // 6. Savanna: Lion
  lion(k) {
    // Voluminous layered mane with amber tips
    for (const x of [-1.00, -.55, 0, .55, 1.00]) {
      k.cone(k.root, [x, 2.55, -.92], [.45, .70, .45], 0x92400e, {preserve:true, rot:[0, 0, x * .22]});
      k.cone(k.root, [x, 1.05, -.93], [.43, .56, .44], 0x92400e, {preserve:true, rot:[Math.PI, 0, 0]});
    }
    // Whisker pads on muzzle
    for (const x of [-.24, .24]) k.orb(k.head, [x, -.26, -.76], [.22, .19, .09], 0xfef3c7, {preserve:true});
    // Tail tassel tuft
    k.orb(k.tail, [0, -.36, .42], [.28, .28, .36], 0x92400e, {preserve:true});
  },

  // 7. Desert: Camel
  camel(k) {
    // Woolly textured dual humps
    for (const z of [-.45, .36]) {
      k.orb(k.root, [0, 2.32, z], [.75, .42, .60], 0xd97706);
      k.box(k.root, [0, 2.65, z], [.38, .08, .42], 0x92400e, {preserve:true});
    }
    // Split hooves
    for (const x of [-.50, .50]) for (const z of [-.75, .65])
      k.box(k.root, [x, .17, z], [.48, .16, .48], 0x78350f, {preserve:true});
    // Saddlecloth tassels
    for (const side of [-1, 1])
      k.cone(k.root, [side * .62, 1.45, -.05], [.14, .32, .14], 0xfacc15, {preserve:true});
  },

  // 8. Desert: Scorpion
  scorpion(k) {
    // Walking leg segments
    for (const side of [-1, 1]) for (let i = 0; i < 3; i++)
      k.box(k.root, [side * (.85 + i * .24), .23, -.08 + i * .36], [.40, .10, .13], 0x92400e, {preserve:true, rot:[0, side * .23, side * .15]});
    // Segmented arched tail
    for (let i = 0; i < 4; i++)
      k.orb(k.tail, [0, .15 + i * .27, -i * .37], [.45 - i * .06, .34, .42 - i * .05], 0xf59e0b);
    // Sharp curved venomous stinger barb
    k.cone(k.tail, [0, 1.40, -1.20], [.35, .72, .35], 0x7f1d1d, {preserve:true, rot:[Math.PI, 0, 0]});
    k.orb(k.tail, [0, 1.05, -1.25], [.12, .12, .12], 0x22c55e, {preserve:true});
  },

  // 9. Desert: Dimetrodon
  dimetrodon(k) {
    // Spiny dorsal neural spines across sunburst sail
    for (let z = -.95; z < 1.00; z += .43) {
      k.box(k.root, [-.075, 2.10, z], [.06, .85, .10], 0xffc34d, {preserve:true});
      k.box(k.root, [ .075, 2.10, z], [.06, .85, .10], 0xffc34d, {preserve:true});
    }
    // Scaly flank scutes
    for (const x of [-.75, .75]) for (const z of [-.63, .12, .74])
      k.orb(k.root, [x, 1.03, z], [.22, .16, .31], 0x854d0e, {preserve:true});
    // Heterodont fangs
    for (const x of [-.45, .45]) k.orb(k.head, [x, .22, -.57], [.15, .10, .09], 0xfff7ed, {preserve:true});
  },

  // 10. Jungle: Toucan
  toucan(k) {
    // Sculpted rainbow beak gradient (yellow, orange, red, cyan)
    k.box(k.head, [0, .20, -1.21], [.57, .12, 1.07], 0xfde047, {preserve:true});
    k.box(k.head, [0, .08, -1.24], [.54, .08, .98], 0xfb923c, {preserve:true});
    k.box(k.head, [0, -.06, -1.26], [.52, .07, .90], 0xef4444, {preserve:true});
    k.box(k.head, [0, -.43, -1.24], [.57, .055, 1.12], 0x06b6d4, {preserve:true});
    // Wing flight feathers
    for (const side of [-1, 1]) for (let i = 0; i < 3; i++)
      k.box(side === -1 ? k.leftWing : k.rightWing, [side * .03, -.32, .34 + i * .23], [.18, .12, .30], 0x064e3b, {preserve:true});
    // Azure eye mask ring
    for (const x of [-.38, .38]) {
      k.orb(k.head, [x, .14, -.54], [.18, .18, .07], 0x38bdf8, {preserve:true});
      k.orb(k.head, [x, .14, -.56], [.11, .11, .07], 0xffffff, {preserve:true});
    }
  },

  // 11. Gorilla
  gorilla(k) {
    // Chiseled chest muscle plates
    for (const x of [-.32, .32])
      k.orb(k.root, [x, 1.28, -1.10], [.48, .53, .22], 0x4b5563, {preserve:true});
    // Knuckles for knuckle-walking
    for (const x of [-.91, .91]) for (const dx of [-.14, 0, .14])
      k.box(k.root, [x + dx, .11, -.93], [.13, .10, .30], 0x111827, {preserve:true});
    // Brow ridge above eyes
    k.box(k.head, [0, .18, -.70], [.62, .12, .16], 0x1f2937, {preserve:true});
    k.box(k.head, [0, -.28, -.62], [.52, .27, .18], 0x9ca3af, {preserve:true});
  },

  // 12. Tiger
  tiger(k) {
    // Vertical tiger stripes
    for (const side of [-1, 1]) for (let i = 0; i < 3; i++)
      k.box(k.root, [side * .78, 1.53, -.56 + i * .53], [.08, .45, .13], 0x111827, {preserve:true, rot:[0, 0, -side * .12]});
    // Banded tail
    for (let i = 0; i < 3; i++) k.box(k.tail, [0, -.3 - i * .22, .17 + i * .13], [.18, .13, .16], 0x111827, {preserve:true});
    // Side whisker tufts & white muzzle
    for (const side of [-1, 1]) {
      k.box(k.head, [side * .45, .25, -.56], [.12, .34, .07], 0x111827, {preserve:true, rot:[0, 0, side * .17]});
      k.orb(k.head, [side * .48, -.14, -.48], [.16, .14, .12], 0xffffff, {preserve:true});
    }
  },

  // 13. Ocean: Seal
  seal(k) {
    // Whiskers and dark muzzle
    for (const side of [-1, 1]) {
      k.orb(k.head, [side * .18, -.20, -.49], [.20, .12, .12], 0xffffff, {preserve:true});
      for (let i = 0; i < 2; i++)
        k.box(k.head, [side * .44, -.19 + i * .13, -.53], [.34, .018, .017], 0xf8fafc, {preserve:true, rot:[0, 0, side * .20]});
    }
    // Blubber spots
    for (const x of [-.43, .43]) for (const z of [0, .45, .85])
      k.orb(k.root, [x, 1.28, z], [.19, .08, .20], 0x64748b, {preserve:true});
    // Webbed rear flipper blades
    for (const side of [-1, 1])
      k.box(k.tail, [side * .26, -.10, .48], [.38, .06, .45], 0x475569, {preserve:true, rot:[0, side * .25, 0]});
    k.orb(k.head, [0, -.15, -.55], [.17, .15, .09], 0x111827, {preserve:true});
  },

  // 14. Ocean: Shark
  shark(k) {
    // Gill slits
    for (const side of [-1, 1]) for (let i = 0; i < 4; i++)
      k.box(k.root, [side * .73, 1.11, -.86 + i * .19], [.05, .40, .055], 0x1e3a8a, {preserve:true, rot:[0, 0, side * .06]});
    // Dorsal fin with trailing notch
    k.cone(k.root, [0, 2.95, -.12], [.35, .57, .48], 0x60a5fa);
    k.box(k.root, [0, 2.75, .15], [.12, .18, .14], 0x1e293b, {preserve:true});
    // Shark tooth row inside mouth
    for (let i = -3; i <= 3; i++)
      k.cone(k.head, [i * .10, -.28, -.82], [.07, .14, .07], 0xffffff, {preserve:true});
    for (const x of [-.40, .40]) k.orb(k.head, [x, .18, -.54], [.09, .09, .05], 0xffffff, {preserve:true});
  },

  // 15. Ocean: Kraken
  kraken(k) {
    // Mantle ridges
    for (const x of [-.42, 0, .42])
      k.orb(k.root, [x, 2.86, -.48], [.22, .12, .18], 0xf9a8d4, {preserve:true});
    // Rows of suction cup orbs on coiled tentacles
    for (let i = 0; i < 8; i++) {
      const a = i * Math.PI / 4, x = Math.sin(a) * .90, z = Math.cos(a) * .90;
      k.orb(k.root, [x * .98, .42, z * .98], [.18, .16, .18], 0xfbcfe8, {preserve:true});
      k.orb(k.root, [x * .82, .24, z * .82], [.14, .12, .14], 0xf472b6, {preserve:true});
    }
    // Piercing golden cephalopod eye
    k.orb(k.root, [0, 2.30, -.81], [.24, .20, .08], 0xfef08a, {preserve:true});
    k.box(k.root, [0, 2.30, -.85], [.16, .04, .04], 0x111111, {preserve:true});
  },

  // 16. Mythical: Unicorn
  unicorn(k) {
    // Spiral golden alicorn horn with emissive tip
    k.cone(k.head, [0, 1.25, -.58], [.22, .88, .22], 0xfacc15, {preserve:true, rot:[-.28, 0, 0]});
    k.orb(k.head, [0, 1.68, -.70], [.10, .10, .10], 0xfef08a, {preserve:true});
    // Flowing pastel mane strands along neck
    const pastelColors = [0xf472b6, 0xc084fc, 0x818cf8, 0x38bdf8, 0x34d399];
    for (let i = 0; i < 5; i++)
      k.orb(k.head, [0, .42 + i * .25, .10 + i * .04], [.24 - i * .024, .11, .23 - i * .02], pastelColors[i], {preserve:true});
    // Golden hooves
    for (const x of [-.45, .45]) for (const z of [-.65, .65])
      k.box(k.root, [x, .26, z], [.36, .08, .37], 0xfde68a, {preserve:true});
    // Flowing tail strands
    for (let i = 0; i < 3; i++)
      k.cone(k.tail, [0, -.3 - i * .28, .21], [.25, .55, .30], pastelColors[i], {preserve:true});
  },

  // 17. Mythical: Phoenix
  phoenix(k) {
    // Flame wings with gradient flight feathers
    for (const side of [-1, 1]) {
      const wing = side === -1 ? k.leftWing : k.rightWing;
      for (let i = 0; i < 5; i++)
        k.cone(wing, [side * (.28 + i * .35), -.18, .12 + i * .16], [.25, .76, .28], i % 2 ? 0xfacc15 : 0xfb923c, {preserve:true, rot:[Math.PI * .5, 0, side * .12]});
    }
    // Fiery crown crest on head
    for (let i = 0; i < 3; i++)
      k.cone(k.head, [(-1 + i) * .21, .92, .15], [.19, .65, .25], 0xfde047, {preserve:true});
    // Trailing ember plumes
    for (const x of [-.4, 0, .4])
      k.orb(k.tail, [x, .14, 1.42], [.24, .12, .30], 0xf97316, {preserve:true});
    k.cone(k.tail, [0, -.20, 1.85], [.32, .88, .32], 0xef4444, {preserve:true, rot:[Math.PI * .5, 0, 0]});
  },

  // 18. Mythical: Dragon
  dragon(k) {
    // Leathery bat wings with thumb claws
    for (const side of [-1, 1]) {
      const wing = side === -1 ? k.leftWing : k.rightWing;
      for (let i = 0; i < 3; i++)
        k.box(wing, [side * (.05 + i * .37), .13, -.45 + i * .44], [.11, .10, 1.72], 0xddd6fe, {preserve:true, rot:[0, 0, side * .08]});
      k.cone(wing, [side * 1.15, .35, -.45], [.16, .35, .16], 0xfacc15, {preserve:true, rot:[0, 0, side * .65]});
    }
    // Backward horned crown ridges
    for (const side of [-1, 1])
      k.cone(k.head, [side * .34, .75, .25], [.22, .65, .22], 0x1f2937, {preserve:true, rot:[-.45, 0, side * .18]});
    // Spiny dorsal crest along spine
    for (let i = 0; i < 4; i++)
      k.cone(k.root, [0, 2.55, -.62 + i * .48], [.32, .70, .35], 0x7c3aed, {preserve:true});
    // Dragon fangs
    for (const x of [-.36, .36]) {
      k.orb(k.head, [x, .18, -.63], [.15, .11, .06], 0xfef08a, {preserve:true});
      k.cone(k.head, [x * .82, -.32, -.75], [.08, .22, .08], 0xffffff, {preserve:true, rot:[Math.PI, 0, 0]});
    }
    // Tail spade / arrowhead
    k.cone(k.tail, [0, .30, 1.92], [.68, .74, .55], 0x7c3aed, {preserve:true, rot:[Math.PI * .5, 0, 0]});
  }
});

// Called once per animal AFTER the original body and mutation aura are built.
function enhanceAnimalModel(group, animalId, scale, animal, mutation) {
  const id = animalId;
  const mutationId = mutation && mutation.id ? mutation.id : 'normal';
  if (!POLISHED_MODEL_PROFILES[id] || group.userData.polishedModel) return group;

  // Retain eyes, teeth, and glowing effects. Refinish Lambert body materials with textured polished materials.
  const replacedMaterials = new Set();
  group.traverse(obj => {
    if (!obj.isMesh || !obj.material || !obj.material.isMeshLambertMaterial) return;
    const m = obj.material;
    const hex = m.color.getHex();
    const preserve = (hex === 0xffffff || hex === 0xf8fafc || hex === 0x111111);
    replacedMaterials.add(m);
    obj.material = polishedMaterial(hex, mutationId, preserve, m.transparent, m.opacity, m.side, id);
  });
  replacedMaterials.forEach(material => material.dispose());
  const kit = polishedKit(group, scale, mutationId, id);
  POLISHED_DETAIL_BUILDERS[id](kit);
  group.userData.polishedModel = {
    version: 2, animalId: id, mutationId, profile: POLISHED_MODEL_PROFILES[id]
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
  const breath = 1 + Math.sin(phase * 0.45) * 0.03;
  if (!group.userData.origScaleY) group.userData.origScaleY = group.scale.y;
  group.scale.y = group.userData.origScaleY * breath;

  if (group.userData.head) {
    group.userData.head.rotation.x = Math.sin(phase * 0.6) * 0.06;
  }
  if (group.userData.ears && group.userData.ears.children.length) {
    group.userData.ears.rotation.x = Math.sin(phase * 1.4) * 0.12;
    group.userData.ears.rotation.z = Math.sin(phase * 0.7) * 0.09;
  }
  if (group.userData.tail) {
    if (p.profile.motion === 'swim') group.userData.tail.rotation.y = Math.sin(phase * 1.8) * 0.48;
    else if (p.profile.motion === 'scuttle') group.userData.tail.rotation.x = Math.sin(phase * 0.7) * 0.12;
    else group.userData.tail.rotation.y = Math.sin(phase * 1.3) * 0.28;
  }
  if (p.profile.motion === 'flap' && group.userData.leftWing && group.userData.rightWing) {
    const flap = Math.sin(phase * 2.3) * 0.52;
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
'''
