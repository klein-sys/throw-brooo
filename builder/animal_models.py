# -*- coding: utf-8 -*-

JS_ANIMAL_MODELS = """
    /*************************************************************************
     * DEDICATED 3D VOXEL MODELS FOR ALL 18 ANIMALS ACROSS 6 BIOMES
     * Each model crafted with rich anatomy, distinct textures, and living joints
     *************************************************************************/
    function buildDedicatedAnimalModel(animalId, g, s, animal, size, mutation) {
      // Determine base materials based on mutation
      const isGold = mutation && mutation.id === 'golden';
      const isRainbow = mutation && mutation.id === 'rainbow';
      const isCosmic = mutation && mutation.id === 'cosmic';

      let bodyColor = animal.color;
      let emissiveColor = 0x000000;
      if (isGold) {
        bodyColor = 0xfacc15;
        emissiveColor = 0x443300;
      } else if (isRainbow) {
        bodyColor = 0xf472b6;
        emissiveColor = 0x331133;
      } else if (isCosmic) {
        bodyColor = 0xc084fc;
        emissiveColor = 0x330055;
      }

      const baseMat = new THREE.MeshLambertMaterial({ color: bodyColor, emissive: emissiveColor });
      const eyeMat = new THREE.MeshBasicMaterial({ color: 0x111111 });
      const whiteMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
      const toothMat = new THREE.MeshBasicMaterial({ color: 0xf8fafc });

      // Helper: add box mesh with shadow
      function addBox(w, h, d, mat, x, y, z, rx = 0, ry = 0, rz = 0, parent = g) {
        const geo = new THREE.BoxGeometry(w * s, h * s, d * s);
        const mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(x * s, y * s, z * s);
        if (rx) mesh.rotation.x = rx;
        if (ry) mesh.rotation.y = ry;
        if (rz) mesh.rotation.z = rz;
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        parent.add(mesh);
        return mesh;
      }

      function addEyes(headX, headY, headZ, eyeW, eyeH, eyeD, sepX, fwdZ, parent = g) {
        addBox(eyeW * 1.25, eyeH * 1.25, 0.05, whiteMat, headX - sepX, headY, headZ + fwdZ, 0, 0, 0, parent);
        addBox(eyeW * 1.25, eyeH * 1.25, 0.05, whiteMat, headX + sepX, headY, headZ + fwdZ, 0, 0, 0, parent);
        addBox(eyeW, eyeH, 0.08, eyeMat, headX - sepX, headY, headZ + fwdZ + 0.02, 0, 0, 0, parent);
        addBox(eyeW, eyeH, 0.08, eyeMat, headX + sepX, headY, headZ + fwdZ + 0.02, 0, 0, 0, parent);
      }

      // Initialize animatable sub-groups
      const headGroup = new THREE.Group();
      const jawGroup = new THREE.Group();
      const tailGroup = new THREE.Group();
      const leftWingGroup = new THREE.Group();
      const rightWingGroup = new THREE.Group();
      const earGroup = new THREE.Group();

      g.add(headGroup, tailGroup, leftWingGroup, rightWingGroup, earGroup);
      g.userData = { head: headGroup, jaw: jawGroup, tail: tailGroup, leftWing: leftWingGroup, rightWing: rightWingGroup, ears: earGroup };

      switch (animalId) {
        // ==================== FOREST (0 - 120m) ====================
        case 'frog': {
          const bellyMat = new THREE.MeshLambertMaterial({ color: isGold ? 0xfef08a : 0xa7f3d0 });
          // Body & Light Belly
          addBox(1.5, 0.8, 1.5, baseMat, 0, 0.55, 0);
          addBox(1.1, 0.5, 0.1, bellyMat, 0, 0.55, -0.76);
          // Wide Frog Head
          addBox(1.4, 0.65, 1.1, baseMat, 0, 1.15, -0.6, 0, 0, 0, headGroup);
          // Bulging Eye Sockets on Top
          addBox(0.35, 0.35, 0.35, baseMat, -0.42, 1.55, -0.75, 0, 0, 0, headGroup);
          addBox(0.35, 0.35, 0.35, baseMat, 0.42, 1.55, -0.75, 0, 0, 0, headGroup);
          addEyes(0, 1.55, -0.75, 0.16, 0.16, 0.05, 0.42, -0.2, headGroup);
          // Lower Articulated Jaw for Eating
          jawGroup.position.set(0, 0.85 * s, -0.6 * s);
          g.add(jawGroup);
          addBox(1.35, 0.22, 0.8, bellyMat, 0, 0, -0.4, 0, 0, 0, jawGroup);
          // Front Legs
          addBox(0.24, 0.65, 0.24, baseMat, -0.55, 0.32, -0.65);
          addBox(0.24, 0.65, 0.24, baseMat, 0.55, 0.32, -0.65);
          addBox(0.4, 0.1, 0.45, baseMat, -0.55, 0.05, -0.85);
          addBox(0.4, 0.1, 0.45, baseMat, 0.55, 0.05, -0.85);
          // Folded Hind Thighs & Feet
          addBox(0.48, 0.75, 0.85, baseMat, -0.82, 0.45, 0.25);
          addBox(0.48, 0.75, 0.85, baseMat, 0.82, 0.45, 0.25);
          addBox(0.42, 0.1, 0.7, baseMat, -0.82, 0.05, -0.15);
          addBox(0.42, 0.1, 0.7, baseMat, 0.82, 0.05, -0.15);
          break;
        }

        case 'bunny': {
          const pinkMat = new THREE.MeshLambertMaterial({ color: 0xf472b6 });
          // Fluffy Body
          addBox(1.15, 1.05, 1.35, baseMat, 0, 0.65, 0);
          // Head
          headGroup.position.set(0, 1.35 * s, -0.65 * s);
          addBox(0.95, 0.9, 0.9, baseMat, 0, 0, 0, 0, 0, 0, headGroup);
          // Tall Upright Rabbit Ears with Pink Inset
          addBox(0.22, 1.35, 0.18, baseMat, -0.28, 1.0, 0, 0, 0, 0.1, headGroup);
          addBox(0.22, 1.35, 0.18, baseMat, 0.28, 1.0, 0, 0, 0, -0.1, headGroup);
          addBox(0.12, 1.1, 0.05, pinkMat, -0.28, 1.0, -0.1, 0, 0, 0.1, headGroup);
          addBox(0.12, 1.1, 0.05, pinkMat, 0.28, 1.0, -0.1, 0, 0, -0.1, headGroup);
          // Pink Nose
          addBox(0.14, 0.12, 0.12, pinkMat, 0, -0.1, -0.5, 0, 0, 0, headGroup);
          addEyes(0, 0.1, 0, 0.14, 0.14, 0.05, 0.32, -0.48, headGroup);
          // Paws
          addBox(0.28, 0.25, 0.4, baseMat, -0.32, 0.12, -0.55);
          addBox(0.28, 0.25, 0.4, baseMat, 0.32, 0.12, -0.55);
          addBox(0.35, 0.35, 0.65, baseMat, -0.52, 0.18, 0.25);
          addBox(0.35, 0.35, 0.65, baseMat, 0.52, 0.18, 0.25);
          // Puffy Tail
          tailGroup.position.set(0, 0.75 * s, 0.75 * s);
          addBox(0.42, 0.42, 0.42, baseMat, 0, 0, 0, 0, 0, 0, tailGroup);
          break;
        }

        case 'bear': {
          const tanMat = new THREE.MeshLambertMaterial({ color: isGold ? 0xfef08a : 0xb45309 });
          const darkNose = new THREE.MeshBasicMaterial({ color: 0x1f2937 });
          // Heavy Muscular Body & Shoulder Hump
          addBox(1.7, 1.4, 2.2, baseMat, 0, 0.95, 0);
          addBox(1.3, 0.45, 1.0, baseMat, 0, 1.75, -0.2);
          // Head
          headGroup.position.set(0, 1.65 * s, -1.05 * s);
          addBox(1.25, 1.15, 1.15, baseMat, 0, 0, 0, 0, 0, 0, headGroup);
          // Snout & Nose
          addBox(0.75, 0.55, 0.65, tanMat, 0, -0.2, -0.6, 0, 0, 0, headGroup);
          addBox(0.28, 0.2, 0.15, darkNose, 0, 0, -0.93, 0, 0, 0, headGroup);
          // Round Ears
          addBox(0.35, 0.35, 0.18, baseMat, -0.48, 0.6, 0.05, 0, 0, 0, headGroup);
          addBox(0.35, 0.35, 0.18, baseMat, 0.48, 0.6, 0.05, 0, 0, 0, headGroup);
          addBox(0.2, 0.2, 0.05, tanMat, -0.48, 0.6, -0.05, 0, 0, 0, headGroup);
          addBox(0.2, 0.2, 0.05, tanMat, 0.48, 0.6, -0.05, 0, 0, 0, headGroup);
          addEyes(0, 0.1, 0, 0.15, 0.15, 0.05, 0.38, -0.6, headGroup);
          // 4 Sturdy Claws Legs
          [[-0.55, -0.7], [0.55, -0.7], [-0.55, 0.7], [0.55, 0.7]].forEach(([lx, lz]) => {
            addBox(0.48, 0.85, 0.52, baseMat, lx, 0.42, lz);
          });
          // Stubby Tail
          tailGroup.position.set(0, 1.1 * s, 1.15 * s);
          addBox(0.32, 0.32, 0.32, baseMat, 0, 0, 0, 0, 0, 0, tailGroup);
          break;
        }

        // ==================== SAVANNA (120 - 320m) ====================
        case 'zebra': {
          const blackMat = new THREE.MeshBasicMaterial({ color: 0x111827 });
          // Striped Body
          addBox(1.35, 1.25, 2.2, baseMat, 0, 1.35, 0);
          for (let i = -2; i <= 2; i++) {
            addBox(1.38, 1.26, 0.18, blackMat, 0, 1.35, i * 0.38);
          }
          // Neck & Mohawk Mane
          addBox(0.65, 1.35, 0.75, baseMat, 0, 2.15, -0.85, -0.3, 0, 0);
          addBox(0.18, 1.45, 0.85, blackMat, 0, 2.25, -0.7, -0.3, 0, 0);
          // Head & Muzzle
          headGroup.position.set(0, 2.65 * s, -1.35 * s);
          addBox(0.75, 0.75, 1.1, baseMat, 0, 0, 0, 0, 0, 0, headGroup);
          addBox(0.65, 0.55, 0.55, blackMat, 0, -0.1, -0.6, 0, 0, 0, headGroup);
          addBox(0.18, 0.35, 0.12, baseMat, -0.28, 0.45, 0.25, 0, 0, 0, headGroup);
          addBox(0.18, 0.35, 0.12, baseMat, 0.28, 0.45, 0.25, 0, 0, 0, headGroup);
          addEyes(0, 0.1, 0, 0.14, 0.14, 0.05, 0.38, -0.35, headGroup);
          // 4 Hooved Legs
          [[-0.45, -0.65], [0.45, -0.65], [-0.45, 0.65], [0.45, 0.65]].forEach(([lx, lz]) => {
            addBox(0.32, 1.15, 0.32, baseMat, lx, 0.58, lz);
            addBox(0.34, 0.2, 0.34, blackMat, lx, 0.1, lz);
          });
          // Tail
          tailGroup.position.set(0, 1.35 * s, 1.15 * s);
          addBox(0.1, 1.0, 0.1, baseMat, 0, -0.4, 0, 0.2, 0, 0, tailGroup);
          addBox(0.22, 0.35, 0.22, blackMat, 0, -0.85, 0.1, 0.2, 0, 0, tailGroup);
          break;
        }

        case 'giraffe': {
          const brownMat = new THREE.MeshLambertMaterial({ color: isGold ? 0xca8a04 : 0x78350f });
          // Tall Body with Spotted Patches
          addBox(1.5, 1.45, 2.3, baseMat, 0, 2.5, 0);
          for (let i = -1; i <= 1; i++) {
            addBox(1.52, 0.45, 0.55, brownMat, 0, 2.5, i * 0.7);
          }
          // Giraffe Neck
          addBox(0.75, 3.8, 0.75, baseMat, 0, 4.4, -0.9, -0.15, 0, 0);
          // Head & Ossicones (Horns)
          headGroup.position.set(0, 6.2 * s, -1.25 * s);
          addBox(0.75, 0.75, 1.05, baseMat, 0, 0, 0, 0, 0, 0, headGroup);
          addBox(0.65, 0.5, 0.55, brownMat, 0, -0.1, -0.55, 0, 0, 0, headGroup);
          addBox(0.14, 0.45, 0.14, brownMat, -0.22, 0.48, -0.15, 0, 0, 0, headGroup);
          addBox(0.14, 0.45, 0.14, brownMat, 0.22, 0.48, -0.15, 0, 0, 0, headGroup);
          addEyes(0, 0.1, 0, 0.14, 0.14, 0.05, 0.35, -0.35, headGroup);
          // 4 Long Legs with Hooves
          [[-0.45, -0.6], [0.45, -0.6], [-0.45, 0.6], [0.45, 0.6]].forEach(([lx, lz]) => {
            addBox(0.3, 2.1, 0.3, baseMat, lx, 1.05, lz);
            addBox(0.34, 0.25, 0.34, brownMat, lx, 0.12, lz);
          });
          // Tail
          tailGroup.position.set(0, 2.4 * s, 1.15 * s);
          addBox(0.1, 1.2, 0.1, baseMat, 0, -0.5, 0, 0, 0, 0, tailGroup);
          addBox(0.22, 0.4, 0.22, brownMat, 0, -1.1, 0, 0, 0, 0, tailGroup);
          break;
        }

        case 'lion': {
          const maneMat = new THREE.MeshLambertMaterial({ color: isGold ? 0xca8a04 : 0x78350f });
          const noseMat = new THREE.MeshBasicMaterial({ color: 0x1f2937 });
          // Muscular Feline Body
          addBox(1.55, 1.3, 2.2, baseMat, 0, 1.15, 0);
          // Volumetric Majestic Collar Mane
          addBox(2.3, 2.2, 1.2, maneMat, 0, 1.75, -0.9);
          // Head emerging from mane
          headGroup.position.set(0, 1.75 * s, -1.25 * s);
          addBox(1.15, 1.1, 1.1, baseMat, 0, 0, 0, 0, 0, 0, headGroup);
          addBox(0.65, 0.5, 0.55, baseMat, 0, -0.15, -0.5, 0, 0, 0, headGroup);
          addBox(0.25, 0.18, 0.12, noseMat, 0, 0.05, -0.78, 0, 0, 0, headGroup);
          // Ears
          addBox(0.25, 0.25, 0.12, baseMat, -0.45, 0.6, 0.2, 0, 0, 0, headGroup);
          addBox(0.25, 0.25, 0.12, baseMat, 0.45, 0.6, 0.2, 0, 0, 0, headGroup);
          addEyes(0, 0.1, 0, 0.14, 0.14, 0.05, 0.35, -0.55, headGroup);
          // Articulated Jaw with Fangs
          jawGroup.position.set(0, 1.45 * s, -1.35 * s);
          g.add(jawGroup);
          addBox(0.65, 0.25, 0.55, baseMat, 0, 0, -0.3, 0, 0, 0, jawGroup);
          addBox(0.08, 0.15, 0.08, toothMat, -0.22, 0.12, -0.5, 0, 0, 0, jawGroup);
          addBox(0.08, 0.15, 0.08, toothMat, 0.22, 0.12, -0.5, 0, 0, 0, jawGroup);
          // 4 Paws
          [[-0.5, -0.65], [0.5, -0.65], [-0.5, 0.65], [0.5, 0.65]].forEach(([lx, lz]) => {
            addBox(0.42, 0.95, 0.45, baseMat, lx, 0.47, lz);
          });
          // Tail
          tailGroup.position.set(0, 1.25 * s, 1.15 * s);
          addBox(0.12, 1.1, 0.12, baseMat, 0, -0.4, 0.2, 0.2, 0, 0, tailGroup);
          addBox(0.26, 0.35, 0.26, maneMat, 0, -0.9, 0.4, 0.2, 0, 0, tailGroup);
          break;
        }

        // ==================== DESERT (320 - 850m) ====================
        case 'camel': {
          const darkCamel = new THREE.MeshLambertMaterial({ color: isGold ? 0xca8a04 : 0x92400e });
          // Body
          addBox(1.5, 1.3, 2.4, baseMat, 0, 1.5, 0);
          // Two Desert Humps
          addBox(1.0, 1.0, 0.85, darkCamel, 0, 2.5, -0.35);
          addBox(1.0, 1.0, 0.85, darkCamel, 0, 2.5, 0.55);
          // S-Curved Neck & Head
          addBox(0.6, 1.6, 0.65, baseMat, 0, 2.4, -0.95, -0.35, 0, 0);
          headGroup.position.set(0, 3.0 * s, -1.45 * s);
          addBox(0.75, 0.75, 1.1, baseMat, 0, 0, 0, 0, 0, 0, headGroup);
          addBox(0.6, 0.45, 0.55, darkCamel, 0, -0.15, -0.5, 0, 0, 0, headGroup);
          addEyes(0, 0.1, 0, 0.14, 0.14, 0.05, 0.38, -0.35, headGroup);
          // 4 Legs
          [[-0.45, -0.75], [0.45, -0.75], [-0.45, 0.75], [0.45, 0.75]].forEach(([lx, lz]) => {
            addBox(0.35, 1.45, 0.35, baseMat, lx, 0.72, lz);
            addBox(0.42, 0.2, 0.42, darkCamel, lx, 0.1, lz);
          });
          // Tail
          tailGroup.position.set(0, 1.6 * s, 1.25 * s);
          addBox(0.12, 0.9, 0.12, baseMat, 0, -0.4, 0, 0, 0, 0, tailGroup);
          break;
        }

        case 'scorpion': {
          const stingMat = new THREE.MeshLambertMaterial({ color: isGold ? 0xfacc15 : 0xd97706 });
          const clawMat = new THREE.MeshLambertMaterial({ color: isGold ? 0xca8a04 : 0xb45309 });
          // Chitin Carapace Body
          addBox(1.35, 0.45, 1.75, baseMat, 0, 0.35, 0);
          // Pincer Arms
          addBox(0.25, 0.2, 0.6, baseMat, -0.55, 0.35, -1.1);
          addBox(0.25, 0.2, 0.6, baseMat, 0.55, 0.35, -1.1);
          addBox(0.38, 0.25, 0.55, clawMat, -0.72, 0.35, -1.5, 0, 0.3, 0);
          addBox(0.38, 0.25, 0.55, clawMat, 0.72, 0.35, -1.5, 0, -0.3, 0);
          addEyes(0, 0.55, -0.85, 0.1, 0.1, 0.05, 0.22, 0);
          // 6 Side Legs
          for (let i = -1; i <= 1; i++) {
            addBox(0.7, 0.1, 0.12, stingMat, -0.88, 0.2, i * 0.45, 0, 0, -0.3);
            addBox(0.7, 0.1, 0.12, stingMat, 0.88, 0.2, i * 0.45, 0, 0, 0.3);
          }
          // Arched Tail with Stinger
          tailGroup.position.set(0, 0.55 * s, 0.95 * s);
          addBox(0.4, 0.4, 0.5, baseMat, 0, 0, 0, 0, 0, 0, tailGroup);
          addBox(0.35, 0.5, 0.35, stingMat, 0, 0.4, 0.15, -0.3, 0, 0, tailGroup);
          addBox(0.32, 0.65, 0.32, stingMat, 0, 0.95, -0.05, -0.8, 0, 0, tailGroup);
          addBox(0.28, 0.65, 0.28, stingMat, 0, 1.4, -0.5, -1.4, 0, 0, tailGroup);
          addBox(0.18, 0.45, 0.18, clawMat, 0, 1.3, -1.05, -2.1, 0, 0, tailGroup);
          break;
        }

        // DIMETRODON - The iconic prehistoric Desert apex reptile from user's video!
        case 'dimetrodon': {
          const sailSpineMat = new THREE.MeshLambertMaterial({ color: isGold ? 0xfde047 : 0xf59e0b });
          const sailMembraneMat = new THREE.MeshLambertMaterial({
            color: isGold ? 0xfacc15 : 0xef4444,
            transparent: true,
            opacity: 0.95
          });
          const clawMat = new THREE.MeshBasicMaterial({ color: 0x111827 });

          // Low-slung Muscular Reptile Body
          addBox(1.65, 0.95, 2.6, baseMat, 0, 0.75, 0);

          // Giant Majestic Dorsal Sail with Spines
          const sailHeight = 2.8;
          addBox(0.12, sailHeight, 2.3, sailMembraneMat, 0, 2.45, -0.1);
          // Vertical Sail Rib Spines
          for (let i = -4; i <= 4; i++) {
            const h = sailHeight * (1 - Math.pow(i / 5, 2) * 0.45);
            addBox(0.18, h, 0.14, sailSpineMat, 0, 1.05 + h / 2, i * 0.26);
          }

          // Large Crocodile-like Reptile Head
          headGroup.position.set(0, 0.95 * s, -1.45 * s);
          addBox(1.2, 0.85, 1.35, baseMat, 0, 0, 0, 0, 0, 0, headGroup);
          addBox(0.85, 0.65, 0.95, baseMat, 0, -0.05, -0.85, 0, 0, 0, headGroup);
          addEyes(0, 0.2, -0.2, 0.14, 0.14, 0.05, 0.45, -0.4, headGroup);

          // Upper Jaw Teeth
          for (let i = -2; i <= 2; i++) {
            addBox(0.06, 0.16, 0.06, toothMat, -0.38, -0.4, -0.6 + i * 0.18, 0, 0, 0, headGroup);
            addBox(0.06, 0.16, 0.06, toothMat, 0.38, -0.4, -0.6 + i * 0.18, 0, 0, 0, headGroup);
          }

          // Articulated Lower Jaw for Eating Cutscene
          jawGroup.position.set(0, 0.65 * s, -1.45 * s);
          g.add(jawGroup);
          addBox(0.82, 0.22, 1.15, baseMat, 0, 0, -0.6, 0, 0, 0, jawGroup);
          // Lower Teeth
          for (let i = -2; i <= 2; i++) {
            addBox(0.06, 0.14, 0.06, toothMat, -0.36, 0.15, -0.6 + i * 0.18, 0, 0, 0, jawGroup);
            addBox(0.06, 0.14, 0.06, toothMat, 0.36, 0.15, -0.6 + i * 0.18, 0, 0, 0, jawGroup);
          }

          // 4 Splayed Reptilian Crawling Legs with Sharp Claws
          [[-0.95, -0.75, 0.45], [0.95, -0.75, -0.45], [-0.95, 0.75, 0.45], [0.95, 0.75, -0.45]].forEach(([lx, lz, rotZ]) => {
            addBox(0.42, 0.6, 0.42, baseMat, lx, 0.55, lz, 0, 0, rotZ);
            addBox(0.55, 0.14, 0.65, baseMat, lx * 1.1, 0.08, lz);
            // Black Claws
            addBox(0.1, 0.08, 0.2, clawMat, lx * 1.1 - 0.16, 0.08, lz - 0.38);
            addBox(0.1, 0.08, 0.2, clawMat, lx * 1.1, 0.08, lz - 0.4);
            addBox(0.1, 0.08, 0.2, clawMat, lx * 1.1 + 0.16, 0.08, lz - 0.38);
          });

          // Long Tapered Lizard Tail
          tailGroup.position.set(0, 0.65 * s, 1.35 * s);
          addBox(0.55, 0.55, 1.4, baseMat, 0, 0, 0.65, 0, 0, 0, tailGroup);
          addBox(0.35, 0.35, 1.4, baseMat, 0, -0.05, 1.95, 0, 0, 0, tailGroup);
          addBox(0.18, 0.18, 1.0, baseMat, 0, -0.08, 3.05, 0, 0, 0, tailGroup);
          break;
        }

        // ==================== JUNGLE (850 - 2,200m) ====================
        case 'toucan': {
          const yellowBib = new THREE.MeshLambertMaterial({ color: isGold ? 0xfef08a : 0xfacc15 });
          const orangeBeak = new THREE.MeshLambertMaterial({ color: 0xf97316 });
          const redTip = new THREE.MeshLambertMaterial({ color: 0xef4444 });
          const wingMat = new THREE.MeshLambertMaterial({ color: isGold ? 0xca8a04 : 0x064e3b });
          // Tropical Body
          addBox(1.05, 1.2, 1.4, baseMat, 0, 1.15, 0);
          addBox(0.75, 0.85, 0.1, yellowBib, 0, 1.1, -0.71);
          // Head
          headGroup.position.set(0, 1.9 * s, -0.45 * s);
          addBox(0.85, 0.85, 0.85, baseMat, 0, 0, 0, 0, 0, 0, headGroup);
          // Giant Iconic Toucan Beak
          addBox(0.55, 0.65, 1.25, orangeBeak, 0, -0.1, -0.95, 0, 0, 0, headGroup);
          addBox(0.48, 0.55, 0.55, redTip, 0, -0.15, -1.65, 0, 0, 0, headGroup);
          addEyes(0, 0.1, 0, 0.14, 0.14, 0.05, 0.38, -0.42, headGroup);
          // Wings
          leftWingGroup.position.set(-0.55 * s, 1.15 * s, 0);
          rightWingGroup.position.set(0.55 * s, 1.15 * s, 0);
          addBox(0.18, 0.85, 1.35, wingMat, 0, 0, 0, 0, 0, 0, leftWingGroup);
          addBox(0.18, 0.85, 1.35, wingMat, 0, 0, 0, 0, 0, 0, rightWingGroup);
          // Tail Feathers
          tailGroup.position.set(0, 1.15 * s, 0.95 * s);
          addBox(0.55, 0.12, 1.15, baseMat, 0, 0, 0.45, -0.3, 0, 0, tailGroup);
          // Feet
          addBox(0.2, 0.55, 0.2, yellowBib, -0.3, 0.28, -0.1);
          addBox(0.2, 0.55, 0.2, yellowBib, 0.3, 0.28, -0.1);
          break;
        }

        case 'gorilla': {
          const silverFur = new THREE.MeshLambertMaterial({ color: isGold ? 0xfef08a : 0x94a3b8 });
          const chestMat = new THREE.MeshLambertMaterial({ color: isGold ? 0xca8a04 : 0x1f2937 });
          // Broad Muscular Torso & Silver Fur Stripe
          addBox(1.85, 1.6, 1.9, baseMat, 0, 1.15, 0);
          addBox(1.5, 0.1, 1.4, silverFur, 0, 1.98, 0.2);
          addBox(1.4, 0.9, 0.2, chestMat, 0, 1.15, -0.96);
          // Heavy Gorilla Brow Ridge & Head
          headGroup.position.set(0, 1.9 * s, -0.85 * s);
          addBox(1.2, 1.05, 1.1, baseMat, 0, 0, 0, 0, 0, 0, headGroup);
          addBox(1.1, 0.35, 0.45, chestMat, 0, 0.2, -0.4, 0, 0, 0, headGroup);
          addEyes(0, 0, 0, 0.14, 0.14, 0.05, 0.35, -0.55, headGroup);
          // Powerful Front Knuckle-Walking Arms
          addBox(0.55, 1.7, 0.55, baseMat, -0.9, 0.85, -0.75, 0.15, 0, 0);
          addBox(0.55, 1.7, 0.55, baseMat, 0.9, 0.85, -0.75, 0.15, 0, 0);
          // Shorter Hind Legs
          addBox(0.55, 0.95, 0.55, baseMat, -0.65, 0.47, 0.55);
          addBox(0.55, 0.95, 0.55, baseMat, 0.65, 0.47, 0.55);
          break;
        }

        case 'tiger': {
          const whiteMat = new THREE.MeshLambertMaterial({ color: 0xffffff });
          const stripeMat = new THREE.MeshBasicMaterial({ color: 0x111827 });
          // Tiger Body & Belly
          addBox(1.5, 1.3, 2.25, baseMat, 0, 1.15, 0);
          addBox(0.95, 0.6, 1.6, whiteMat, 0, 0.85, 0);
          for (let i = -2; i <= 2; i++) {
            addBox(1.53, 0.16, 0.16, stripeMat, 0, 1.45, i * 0.4);
          }
          // Head with Jowls
          headGroup.position.set(0, 1.75 * s, -1.05 * s);
          addBox(1.15, 1.05, 1.1, baseMat, 0, 0, 0, 0, 0, 0, headGroup);
          addBox(1.4, 0.42, 0.65, whiteMat, 0, -0.2, -0.2, 0, 0, 0, headGroup);
          addBox(0.5, 0.38, 0.45, whiteMat, 0, -0.15, -0.5, 0, 0, 0, headGroup);
          addBox(0.2, 0.15, 0.1, stripeMat, 0, 0, -0.73, 0, 0, 0, headGroup);
          addBox(0.24, 0.28, 0.12, baseMat, -0.42, 0.55, 0, 0, 0, 0, headGroup);
          addBox(0.24, 0.28, 0.12, baseMat, 0.42, 0.55, 0, 0, 0, 0, headGroup);
          addEyes(0, 0.1, 0, 0.14, 0.14, 0.05, 0.35, -0.55, headGroup);
          // 4 Paws
          [[-0.48, -0.65], [0.48, -0.65], [-0.48, 0.65], [0.48, 0.65]].forEach(([lx, lz]) => {
            addBox(0.42, 0.95, 0.42, baseMat, lx, 0.47, lz);
          });
          // Tail
          tailGroup.position.set(0, 1.25 * s, 1.15 * s);
          addBox(0.14, 1.25, 0.14, baseMat, 0, -0.45, 0.2, 0.3, 0, 0, tailGroup);
          addBox(0.16, 0.3, 0.16, stripeMat, 0, -0.9, 0.45, 0.3, 0, 0, tailGroup);
          break;
        }

        // ==================== DEEP OCEAN (2,200 - 5,500m) ====================
        case 'seal': {
          const flipperMat = new THREE.MeshLambertMaterial({ color: isGold ? 0xfef08a : 0x60a5fa });
          // Streamlined Seal Body
          addBox(1.35, 1.05, 2.2, baseMat, 0, 0.75, 0);
          addBox(1.0, 0.75, 1.1, baseMat, 0, 0.65, 1.1);
          // Head
          headGroup.position.set(0, 1.15 * s, -0.95 * s);
          addBox(0.9, 0.85, 0.9, baseMat, 0, 0, 0, 0, 0, 0, headGroup);
          addBox(0.45, 0.35, 0.35, flipperMat, 0, -0.15, -0.45, 0, 0, 0, headGroup);
          addEyes(0, 0.1, 0, 0.14, 0.14, 0.05, 0.32, -0.48, headGroup);
          // Side Flippers
          addBox(0.95, 0.12, 0.55, flipperMat, -0.9, 0.35, -0.25, 0, 0, -0.2);
          addBox(0.95, 0.12, 0.55, flipperMat, 0.9, 0.35, -0.25, 0, 0, 0.2);
          // Split Tail Flippers
          tailGroup.position.set(0, 0.55 * s, 1.85 * s);
          addBox(0.45, 0.1, 0.65, flipperMat, -0.25, 0, 0, 0, 0.25, 0, tailGroup);
          addBox(0.45, 0.1, 0.65, flipperMat, 0.25, 0, 0, 0, -0.25, 0, tailGroup);
          break;
        }

        case 'shark': {
          const bellyMat = new THREE.MeshLambertMaterial({ color: 0xf1f5f9 });
          const finMat = new THREE.MeshLambertMaterial({ color: isGold ? 0xca8a04 : 0x1d4ed8 });
          // Hydrodynamic Shark Body & White Belly
          addBox(1.45, 1.3, 2.9, baseMat, 0, 1.05, 0);
          addBox(1.15, 0.22, 2.3, bellyMat, 0, 0.38, 0);
          // Pointed Snout & Head
          headGroup.position.set(0, 1.0 * s, -1.65 * s);
          addBox(1.05, 0.8, 1.25, baseMat, 0, 0, 0, 0, 0, 0, headGroup);
          addEyes(0, 0.2, 0, 0.14, 0.14, 0.05, 0.45, -0.35, headGroup);
          // Articulated Toothy Jaw
          jawGroup.position.set(0, 0.65 * s, -1.75 * s);
          g.add(jawGroup);
          addBox(0.85, 0.18, 0.9, whiteMat, 0, 0, 0, 0, 0, 0, jawGroup);
          for (let i = -2; i <= 2; i++) {
            addBox(0.06, 0.12, 0.06, toothMat, -0.32, 0.12, -0.3 + i * 0.14, 0, 0, 0, jawGroup);
            addBox(0.06, 0.12, 0.06, toothMat, 0.32, 0.12, -0.3 + i * 0.14, 0, 0, 0, jawGroup);
          }
          // Iconic Triangular Dorsal Fin
          addBox(0.24, 1.45, 0.95, finMat, 0, 2.2, -0.2, -0.3, 0, 0);
          // Pectoral Fins
          addBox(1.1, 0.14, 0.7, finMat, -1.05, 0.65, -0.45, 0, 0, -0.25);
          addBox(1.1, 0.14, 0.7, finMat, 1.05, 0.65, -0.45, 0, 0, 0.25);
          // Vertical Tail Fin
          tailGroup.position.set(0, 1.15 * s, 1.75 * s);
          addBox(0.18, 1.75, 0.85, finMat, 0, 0, 0.35, 0.15, 0, 0, tailGroup);
          break;
        }

        case 'kraken': {
          const glowYellow = new THREE.MeshBasicMaterial({ color: isGold ? 0xffffff : 0xfacc15 });
          const tentacleMat = new THREE.MeshLambertMaterial({ color: isGold ? 0xca8a04 : 0xbe185d });
          // Bulbous Mantle Head
          addBox(1.6, 1.8, 1.6, baseMat, 0, 1.75, 0);
          addBox(1.2, 0.75, 1.2, baseMat, 0, 2.75, 0);
          // Glowing Eyes
          addBox(0.28, 0.28, 0.1, glowYellow, -0.45, 1.25, -0.81);
          addBox(0.28, 0.28, 0.1, glowYellow, 0.45, 1.25, -0.81);
          // 8 Splaying Coiled Tentacles
          for (let i = 0; i < 8; i++) {
            const angle = (i / 8) * Math.PI * 2;
            const tx = Math.sin(angle) * 0.85;
            const tz = Math.cos(angle) * 0.85;
            addBox(0.35, 1.35, 0.35, tentacleMat, tx, 0.65, tz, Math.cos(angle) * 0.35, 0, Math.sin(angle) * 0.35);
          }
          break;
        }

        // ==================== MYTHICAL PARADISE (5,500m+) ====================
        case 'unicorn': {
          const hornMat = new THREE.MeshBasicMaterial({ color: 0xfde047 });
          const maneMat = new THREE.MeshLambertMaterial({ color: isGold ? 0xfef08a : 0xf472b6 });
          const hoofMat = new THREE.MeshBasicMaterial({ color: 0xfacc15 });
          // White Equine Body
          addBox(1.4, 1.3, 2.2, baseMat, 0, 1.45, 0);
          addBox(0.65, 1.4, 0.65, baseMat, 0, 2.35, -0.85, -0.3, 0, 0);
          // Head & Golden Spiral Horn
          headGroup.position.set(0, 2.85 * s, -1.35 * s);
          addBox(0.75, 0.75, 1.1, baseMat, 0, 0, 0, 0, 0, 0, headGroup);
          addBox(0.16, 1.45, 0.16, hornMat, 0, 1.0, 0, 0.25, 0, 0, headGroup);
          addBox(0.25, 1.5, 0.85, maneMat, 0, -0.2, 0.65, -0.3, 0, 0, headGroup);
          addEyes(0, 0.1, 0, 0.14, 0.14, 0.05, 0.38, -0.35, headGroup);
          // 4 Legs with Golden Hooves
          [[-0.45, -0.65], [0.45, -0.65], [-0.45, 0.65], [0.45, 0.65]].forEach(([lx, lz]) => {
            addBox(0.32, 1.2, 0.32, baseMat, lx, 0.6, lz);
            addBox(0.34, 0.22, 0.34, hoofMat, lx, 0.11, lz);
          });
          // Flowing Celestial Tail
          tailGroup.position.set(0, 1.45 * s, 1.15 * s);
          addBox(0.2, 1.3, 0.25, maneMat, 0, -0.5, 0.25, 0.3, 0, 0, tailGroup);
          break;
        }

        case 'phoenix': {
          const flameGold = new THREE.MeshBasicMaterial({ color: 0xfacc15 });
          const featherOrange = new THREE.MeshLambertMaterial({ color: isGold ? 0xfef08a : 0xf97316 });
          // Fiery Body
          addBox(1.3, 1.3, 1.7, baseMat, 0, 1.45, 0);
          // Crown Feather Crest & Head
          headGroup.position.set(0, 2.25 * s, -0.75 * s);
          addBox(0.85, 0.85, 0.9, baseMat, 0, 0, 0, 0, 0, 0, headGroup);
          addBox(0.42, 0.42, 0.7, flameGold, 0, -0.1, -0.65, 0.1, 0, 0, headGroup);
          addBox(0.18, 0.85, 0.6, flameGold, 0, 0.65, 0.1, -0.3, 0, 0, headGroup);
          addEyes(0, 0.1, 0, 0.14, 0.14, 0.05, 0.38, -0.35, headGroup);
          // Spread Fiery Wings
          leftWingGroup.position.set(-1.45 * s, 1.75 * s, 0);
          rightWingGroup.position.set(1.45 * s, 1.75 * s, 0);
          addBox(2.3, 0.18, 1.4, featherOrange, 0, 0, 0, 0, 0, -0.15, leftWingGroup);
          addBox(2.3, 0.18, 1.4, featherOrange, 0, 0, 0, 0, 0, 0.15, rightWingGroup);
          // 3 Flowing Solar Tail Plumes
          tailGroup.position.set(0, 1.35 * s, 1.85 * s);
          addBox(0.25, 0.1, 2.5, flameGold, -0.35, 0, 0.5, -0.2, -0.15, 0, tailGroup);
          addBox(0.3, 0.1, 2.8, flameGold, 0, 0, 0.65, -0.2, 0, 0, tailGroup);
          addBox(0.25, 0.1, 2.5, flameGold, 0.35, 0, 0.5, -0.2, 0.15, 0, tailGroup);
          break;
        }

        case 'dragon': {
          const cosmicGlow = new THREE.MeshBasicMaterial({ color: isGold ? 0xfef08a : 0xc084fc });
          const hornMat = new THREE.MeshLambertMaterial({ color: isGold ? 0xca8a04 : 0x581c87 });
          // Serpentine Dragon Torso
          addBox(1.65, 1.5, 2.8, baseMat, 0, 1.45, 0);
          // Head & Swept-Back Horns
          headGroup.position.set(0, 2.25 * s, -1.35 * s);
          addBox(1.2, 1.1, 1.2, baseMat, 0, 0, 0, 0, 0, 0, headGroup);
          addBox(0.9, 0.7, 1.05, baseMat, 0, -0.2, -0.85, 0, 0, 0, headGroup);
          addBox(0.22, 1.2, 0.22, hornMat, -0.42, 0.85, 0.1, -0.45, 0, -0.25, headGroup);
          addBox(0.22, 1.2, 0.22, hornMat, 0.42, 0.85, 0.1, -0.45, 0, 0.25, headGroup);
          addEyes(0, 0.2, 0, 0.16, 0.16, 0.05, 0.42, -0.55, headGroup);
          // Articulated Jaw with Fangs
          jawGroup.position.set(0, 1.85 * s, -1.85 * s);
          g.add(jawGroup);
          addBox(0.85, 0.25, 0.95, baseMat, 0, 0, -0.2, 0, 0, 0, jawGroup);
          addBox(0.12, 0.25, 0.12, toothMat, -0.32, 0.15, -0.5, 0, 0, 0, jawGroup);
          addBox(0.12, 0.25, 0.12, toothMat, 0.32, 0.15, -0.5, 0, 0, 0, jawGroup);
          // Spiny Dorsal Ridge Down Spine
          for (let i = -2; i <= 2; i++) {
            addBox(0.16, 0.5, 0.35, cosmicGlow, 0, 2.35, i * 0.45);
          }
          // Expansive Membrane Wings
          leftWingGroup.position.set(-1.8 * s, 1.95 * s, -0.2 * s);
          rightWingGroup.position.set(1.8 * s, 1.95 * s, -0.2 * s);
          addBox(2.8, 0.15, 1.7, cosmicGlow, 0, 0, 0, 0, 0, -0.2, leftWingGroup);
          addBox(2.8, 0.15, 1.7, cosmicGlow, 0, 0, 0, 0, 0, 0.2, rightWingGroup);
          // Serpentine Tail with Spade Barb
          tailGroup.position.set(0, 1.4 * s, 2.05 * s);
          addBox(0.48, 0.48, 1.6, baseMat, 0, 0, 0.8, 0.15, 0, 0, tailGroup);
          addBox(0.8, 0.1, 0.8, hornMat, 0, 0.25, 1.7, 0, 0.78, 0, tailGroup);
          break;
        }

        default: {
          addBox(1.4, 1.1, 1.7, baseMat, 0, 0.75, 0);
          addBox(1.1, 1.0, 1.0, baseMat, 0, 1.35, -0.8);
          addEyes(0, 1.45, -0.8, 0.16, 0.16, 0.05, 0.3, -0.52);
          break;
        }
      }

      // Add Glowing Halo / Aura Ring if Golden, Rainbow, or Cosmic
      if (mutation && mutation.mult >= 5) {
        const auraGeo = new THREE.TorusGeometry(1.4 * s, 0.14 * s, 16, 32);
        const auraMat = new THREE.MeshBasicMaterial({ color: mutation.hex });
        const aura = new THREE.Mesh(auraGeo, auraMat);
        aura.rotation.x = Math.PI / 2;
        aura.position.y = 0.25 * s;
        g.add(aura);
      }

      return enhanceAnimalModel(g, animalId, s, animal, mutation);
    }
"""
