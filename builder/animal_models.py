# -*- coding: utf-8 -*-

JS_ANIMAL_MODELS = """
    /*************************************************************************
     * DEDICATED 3D VOXEL MODELS FOR ALL 18 ANIMALS ACROSS 6 BIOMES
     *************************************************************************/
    function buildDedicatedAnimalModel(animalId, g, s, animal, size, mutation) {
      const baseMat = new THREE.MeshLambertMaterial({ color: animal.color });
      const eyeMat = new THREE.MeshBasicMaterial({ color: 0x111111 });
      const whiteMat = new THREE.MeshBasicMaterial({ color: 0xffffff });

      // Helper: add box mesh with shadow
      function addBox(w, h, d, mat, x, y, z, rx = 0, ry = 0, rz = 0) {
        const geo = new THREE.BoxGeometry(w * s, h * s, d * s);
        const mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(x * s, y * s, z * s);
        if (rx) mesh.rotation.x = rx;
        if (ry) mesh.rotation.y = ry;
        if (rz) mesh.rotation.z = rz;
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        g.add(mesh);
        return mesh;
      }

      function addEyes(headX, headY, headZ, eyeW, eyeH, eyeD, sepX, fwdZ) {
        const eyeBaseL = addBox(eyeW * 1.2, eyeH * 1.2, 0.05, whiteMat, headX - sepX, headY, headZ + fwdZ);
        const eyeBaseR = addBox(eyeW * 1.2, eyeH * 1.2, 0.05, whiteMat, headX + sepX, headY, headZ + fwdZ);
        const eyePupilL = addBox(eyeW, eyeH, 0.08, eyeMat, headX - sepX, headY, headZ + fwdZ + 0.02);
        const eyePupilR = addBox(eyeW, eyeH, 0.08, eyeMat, headX + sepX, headY, headZ + fwdZ + 0.02);
      }

      switch (animalId) {
        // ==================== FOREST (0 - 100m) ====================
        case 'frog': {
          const bellyMat = new THREE.MeshLambertMaterial({ color: 0xa7f3d0 });
          // Body
          addBox(1.5, 0.8, 1.5, baseMat, 0, 0.55, 0);
          addBox(1.1, 0.5, 0.1, bellyMat, 0, 0.55, -0.76);
          // Wide Head & Lower Jaw
          addBox(1.4, 0.7, 1.1, baseMat, 0, 1.15, -0.6);
          addBox(1.4, 0.25, 0.45, baseMat, 0, 0.85, -1.05);
          // Bulging Eye Sockets on Top
          addBox(0.35, 0.35, 0.35, baseMat, -0.42, 1.58, -0.75);
          addBox(0.35, 0.35, 0.35, baseMat, 0.42, 1.58, -0.75);
          addEyes(0, 1.58, -0.75, 0.16, 0.16, 0.05, 0.42, -0.2);
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
          // Body
          addBox(1.15, 1.05, 1.35, baseMat, 0, 0.65, 0);
          // Cute Head
          addBox(0.95, 0.9, 0.9, baseMat, 0, 1.35, -0.65);
          // Tall Upright Rabbit Ears with Pink Inset
          addBox(0.22, 1.35, 0.18, baseMat, -0.28, 2.35, -0.65, 0, 0, 0.1);
          addBox(0.22, 1.35, 0.18, baseMat, 0.28, 2.35, -0.65, 0, 0, -0.1);
          addBox(0.12, 1.1, 0.05, pinkMat, -0.28, 2.35, -0.75, 0, 0, 0.1);
          addBox(0.12, 1.1, 0.05, pinkMat, 0.28, 2.35, -0.75, 0, 0, -0.1);
          // Pink Nose
          addBox(0.14, 0.12, 0.12, pinkMat, 0, 1.25, -1.15);
          addEyes(0, 1.45, -0.65, 0.14, 0.14, 0.05, 0.32, -0.48);
          // Little Paws
          addBox(0.28, 0.25, 0.4, baseMat, -0.32, 0.12, -0.55);
          addBox(0.28, 0.25, 0.4, baseMat, 0.32, 0.12, -0.55);
          addBox(0.35, 0.35, 0.65, baseMat, -0.52, 0.18, 0.25);
          addBox(0.35, 0.35, 0.65, baseMat, 0.52, 0.18, 0.25);
          // Puffy Tail
          addBox(0.38, 0.38, 0.38, baseMat, 0, 0.75, 0.75);
          break;
        }

        case 'bear': {
          const tanMat = new THREE.MeshLambertMaterial({ color: 0xb45309 });
          const darkNose = new THREE.MeshBasicMaterial({ color: 0x1f2937 });
          // Heavy Body
          addBox(1.65, 1.4, 2.1, baseMat, 0, 0.95, 0);
          // Chunky Bear Head
          addBox(1.25, 1.15, 1.15, baseMat, 0, 1.65, -1.05);
          // Tan Snout & Dark Nose
          addBox(0.75, 0.55, 0.65, tanMat, 0, 1.45, -1.65);
          addBox(0.28, 0.2, 0.15, darkNose, 0, 1.65, -1.98);
          // Round Bear Ears
          addBox(0.35, 0.35, 0.18, baseMat, -0.48, 2.25, -1.0);
          addBox(0.35, 0.35, 0.18, baseMat, 0.48, 2.25, -1.0);
          addBox(0.2, 0.2, 0.05, tanMat, -0.48, 2.25, -1.1);
          addBox(0.2, 0.2, 0.05, tanMat, 0.48, 2.25, -1.1);
          addEyes(0, 1.75, -1.05, 0.15, 0.15, 0.05, 0.38, -0.6);
          // 4 Sturdy Legs
          addBox(0.5, 0.85, 0.5, baseMat, -0.6, 0.42, -0.65);
          addBox(0.5, 0.85, 0.5, baseMat, 0.6, 0.42, -0.65);
          addBox(0.5, 0.85, 0.5, baseMat, -0.6, 0.42, 0.65);
          addBox(0.5, 0.85, 0.5, baseMat, 0.6, 0.42, 0.65);
          // Stubby Tail
          addBox(0.3, 0.3, 0.3, baseMat, 0, 1.25, 1.1);
          break;
        }

        // ==================== SAVANNA (100 - 300m) ====================
        case 'zebra': {
          const blackMat = new THREE.MeshBasicMaterial({ color: 0x111827 });
          // Striped Horse Body
          addBox(1.3, 1.25, 2.1, baseMat, 0, 1.4, 0);
          // Neck
          addBox(0.65, 1.35, 0.7, baseMat, 0, 2.25, -0.85, -0.3, 0, 0);
          // Head & Dark Muzzle
          addBox(0.75, 0.75, 1.05, baseMat, 0, 2.75, -1.35);
          addBox(0.6, 0.5, 0.5, blackMat, 0, 2.6, -1.85);
          // Black Mane Ridge along Neck
          addBox(0.18, 1.45, 0.85, blackMat, 0, 2.35, -0.7, -0.3, 0, 0);
          // Ears
          addBox(0.18, 0.45, 0.12, baseMat, -0.25, 3.2, -1.25);
          addBox(0.18, 0.45, 0.12, baseMat, 0.25, 3.2, -1.25);
          addEyes(0, 2.85, -1.35, 0.14, 0.14, 0.05, 0.38, -0.35);
          // 4 Legs with Black Hooves
          [[-0.45, -0.65], [0.45, -0.65], [-0.45, 0.65], [0.45, 0.65]].forEach(([lx, lz]) => {
            addBox(0.32, 1.2, 0.32, baseMat, lx, 0.6, lz);
            addBox(0.34, 0.22, 0.34, blackMat, lx, 0.11, lz);
          });
          // Tail
          addBox(0.12, 0.9, 0.12, blackMat, 0, 1.35, 1.1, 0.2, 0, 0);
          break;
        }

        case 'giraffe': {
          const brownMat = new THREE.MeshLambertMaterial({ color: 0x78350f });
          // Body
          addBox(1.35, 1.3, 1.9, baseMat, 0, 2.3, 0);
          // Super Tall Vertical Neck
          addBox(0.55, 3.2, 0.55, baseMat, 0, 3.8, -0.75);
          // Head
          addBox(0.7, 0.7, 0.95, baseMat, 0, 5.3, -0.95);
          addBox(0.55, 0.45, 0.45, brownMat, 0, 5.15, -1.4);
          // Ossicones (Giraffe Horns)
          addBox(0.12, 0.55, 0.12, baseMat, -0.22, 5.8, -0.85);
          addBox(0.12, 0.55, 0.12, baseMat, 0.22, 5.8, -0.85);
          addBox(0.2, 0.2, 0.2, brownMat, -0.22, 6.05, -0.85);
          addBox(0.2, 0.2, 0.2, brownMat, 0.22, 6.05, -0.85);
          addEyes(0, 5.45, -0.95, 0.14, 0.14, 0.05, 0.35, -0.35);
          // 4 Very Tall Slender Legs with Hooves
          [[-0.45, -0.6], [0.45, -0.6], [-0.45, 0.6], [0.45, 0.6]].forEach(([lx, lz]) => {
            addBox(0.3, 2.1, 0.3, baseMat, lx, 1.05, lz);
            addBox(0.34, 0.25, 0.34, brownMat, lx, 0.12, lz);
          });
          // Tufted Tail
          addBox(0.1, 1.1, 0.1, baseMat, 0, 2.2, 1.0);
          addBox(0.18, 0.35, 0.18, brownMat, 0, 1.6, 1.0);
          break;
        }

        case 'lion': {
          const maneMat = new THREE.MeshLambertMaterial({ color: 0x78350f });
          const noseMat = new THREE.MeshBasicMaterial({ color: 0x1f2937 });
          // Body
          addBox(1.5, 1.25, 2.1, baseMat, 0, 1.15, 0);
          // Volumetric Majestic Collar Mane
          addBox(2.2, 2.1, 1.1, maneMat, 0, 1.75, -0.9);
          // Head emerging from mane
          addBox(1.1, 1.05, 1.05, baseMat, 0, 1.75, -1.25);
          addBox(0.65, 0.48, 0.55, baseMat, 0, 1.55, -1.75);
          addBox(0.25, 0.18, 0.12, noseMat, 0, 1.75, -2.03);
          // Ears peeking from mane
          addBox(0.25, 0.25, 0.12, baseMat, -0.45, 2.35, -1.05);
          addBox(0.25, 0.25, 0.12, baseMat, 0.45, 2.35, -1.05);
          addEyes(0, 1.85, -1.25, 0.14, 0.14, 0.05, 0.35, -0.55);
          // 4 Paws
          [[-0.5, -0.65], [0.5, -0.65], [-0.5, 0.65], [0.5, 0.65]].forEach(([lx, lz]) => {
            addBox(0.42, 0.95, 0.45, baseMat, lx, 0.47, lz);
          });
          // Tail with Tassel
          addBox(0.12, 1.1, 0.12, baseMat, 0, 1.25, 1.15, 0.2, 0, 0);
          addBox(0.26, 0.35, 0.26, maneMat, 0, 0.75, 1.3);
          break;
        }

        // ==================== DESERT (300 - 800m) ====================
        case 'camel': {
          const darkCamel = new THREE.MeshLambertMaterial({ color: 0x92400e });
          // Body
          addBox(1.45, 1.25, 2.3, baseMat, 0, 1.5, 0);
          // Desert Hump
          addBox(1.0, 1.05, 1.1, darkCamel, 0, 2.55, 0.1);
          // S-Curved Neck & Head
          addBox(0.6, 1.5, 0.65, baseMat, 0, 2.35, -0.95, -0.35, 0, 0);
          addBox(0.75, 0.75, 1.1, baseMat, 0, 2.85, -1.45);
          addBox(0.6, 0.45, 0.55, darkCamel, 0, 2.7, -1.95);
          addEyes(0, 2.95, -1.45, 0.14, 0.14, 0.05, 0.38, -0.35);
          // 4 Legs with Padded Hooves
          [[-0.45, -0.75], [0.45, -0.75], [-0.45, 0.75], [0.45, 0.75]].forEach(([lx, lz]) => {
            addBox(0.35, 1.45, 0.35, baseMat, lx, 0.72, lz);
            addBox(0.42, 0.2, 0.42, darkCamel, lx, 0.1, lz);
          });
          addBox(0.12, 0.85, 0.12, baseMat, 0, 1.45, 1.2);
          break;
        }

        case 'scorpion': {
          const stingMat = new THREE.MeshLambertMaterial({ color: 0xd97706 });
          const clawMat = new THREE.MeshLambertMaterial({ color: 0xb45309 });
          // Segmented Low Chitin Body
          addBox(1.3, 0.45, 1.7, baseMat, 0, 0.35, 0);
          // Front Pedipalp Arms & Pincers
          addBox(0.25, 0.2, 0.6, baseMat, -0.55, 0.35, -1.1);
          addBox(0.25, 0.2, 0.6, baseMat, 0.55, 0.35, -1.1);
          addBox(0.35, 0.25, 0.55, clawMat, -0.72, 0.35, -1.5, 0, 0.3, 0);
          addBox(0.35, 0.25, 0.55, clawMat, 0.72, 0.35, -1.5, 0, -0.3, 0);
          addEyes(0, 0.55, -0.85, 0.1, 0.1, 0.05, 0.22, 0);
          // 6 Crawling Side Legs
          for (let i = -1; i <= 1; i++) {
            addBox(0.65, 0.1, 0.12, stingMat, -0.85, 0.2, i * 0.45, 0, 0, -0.3);
            addBox(0.65, 0.1, 0.12, stingMat, 0.85, 0.2, i * 0.45, 0, 0, 0.3);
          }
          // Arched Curved Tail Arching Forward with Stinger
          addBox(0.4, 0.4, 0.5, baseMat, 0, 0.55, 0.95);
          addBox(0.35, 0.5, 0.35, stingMat, 0, 0.95, 1.1, -0.3, 0, 0);
          addBox(0.32, 0.65, 0.32, stingMat, 0, 1.5, 0.9, -0.8, 0, 0);
          addBox(0.28, 0.65, 0.28, stingMat, 0, 1.95, 0.45, -1.4, 0, 0);
          // Poison Barb Stinger Pointing Forward
          addBox(0.18, 0.45, 0.18, clawMat, 0, 1.85, -0.1, -2.1, 0, 0);
          break;
        }

        case 'sphinx': {
          const goldTrim = new THREE.MeshLambertMaterial({ color: 0xfacc15 });
          const whiteTuft = new THREE.MeshLambertMaterial({ color: 0xffffff });
          // Fox Body
          addBox(1.2, 1.05, 1.7, baseMat, 0, 0.85, 0);
          // Head & Muzzle
          addBox(0.85, 0.85, 0.85, baseMat, 0, 1.45, -0.85);
          addBox(0.45, 0.38, 0.6, whiteTuft, 0, 1.3, -1.35);
          addBox(0.18, 0.14, 0.14, eyeMat, 0, 1.45, -1.65);
          // Giant Fennec Fox Ears with White Insets
          addBox(0.4, 1.25, 0.14, baseMat, -0.38, 2.35, -0.8, 0, 0, 0.25);
          addBox(0.4, 1.25, 0.14, baseMat, 0.38, 2.35, -0.8, 0, 0, -0.25);
          addBox(0.24, 1.0, 0.05, whiteTuft, -0.38, 2.35, -0.88, 0, 0, 0.25);
          addBox(0.24, 1.0, 0.05, whiteTuft, 0.38, 2.35, -0.88, 0, 0, -0.25);
          addEyes(0, 1.55, -0.85, 0.14, 0.14, 0.05, 0.28, -0.45);
          // Pharaoh Headdress / Collar
          addBox(1.05, 0.15, 0.95, goldTrim, 0, 1.15, -0.75);
          // 4 Legs
          [[-0.38, -0.55], [0.38, -0.55], [-0.38, 0.55], [0.38, 0.55]].forEach(([lx, lz]) => {
            addBox(0.28, 0.8, 0.28, baseMat, lx, 0.4, lz);
          });
          // Bushy Luxurious Fox Tail with White Tip
          addBox(0.55, 0.55, 1.3, baseMat, 0, 1.15, 1.15, 0.35, 0, 0);
          addBox(0.45, 0.45, 0.55, whiteTuft, 0, 1.45, 1.75, 0.35, 0, 0);
          break;
        }

        // ==================== JUNGLE (800 - 2,000m) ====================
        case 'toucan': {
          const yellowBib = new THREE.MeshLambertMaterial({ color: 0xfacc15 });
          const orangeBeak = new THREE.MeshLambertMaterial({ color: 0xf97316 });
          const redTip = new THREE.MeshLambertMaterial({ color: 0xef4444 });
          const wingMat = new THREE.MeshLambertMaterial({ color: 0x064e3b });
          // Tropical Bird Body
          addBox(1.0, 1.15, 1.35, baseMat, 0, 1.1, 0);
          addBox(0.75, 0.85, 0.1, yellowBib, 0, 1.05, -0.68);
          // Head
          addBox(0.8, 0.8, 0.8, baseMat, 0, 1.85, -0.45);
          // Giant Iconic Toucan Beak
          addBox(0.55, 0.65, 1.15, orangeBeak, 0, 1.75, -1.35);
          addBox(0.48, 0.55, 0.55, redTip, 0, 1.68, -1.95);
          addEyes(0, 1.95, -0.45, 0.14, 0.14, 0.05, 0.35, -0.42);
          // Folded Wings
          addBox(0.18, 0.85, 1.25, wingMat, -0.55, 1.15, 0);
          addBox(0.18, 0.85, 1.25, wingMat, 0.55, 1.15, 0);
          // Tail Feathers
          addBox(0.55, 0.12, 1.05, baseMat, 0, 1.1, 0.95, -0.4, 0, 0);
          // Feet
          addBox(0.2, 0.55, 0.2, yellowBib, -0.3, 0.28, -0.1);
          addBox(0.2, 0.55, 0.2, yellowBib, 0.3, 0.28, -0.1);
          break;
        }

        case 'gorilla': {
          const silverFur = new THREE.MeshLambertMaterial({ color: 0x94a3b8 });
          const chestMat = new THREE.MeshLambertMaterial({ color: 0x1f2937 });
          // Broad Muscular Body
          addBox(1.75, 1.55, 1.8, baseMat, 0, 1.15, 0);
          // Silverback Stripe on Rear
          addBox(1.45, 0.1, 1.3, silverFur, 0, 1.95, 0.2);
          addBox(1.35, 0.9, 0.2, chestMat, 0, 1.15, -0.92);
          // Gorilla Head & Heavy Brow Ridge
          addBox(1.15, 1.0, 1.05, baseMat, 0, 1.85, -0.85);
          addBox(1.05, 0.35, 0.45, chestMat, 0, 2.05, -1.25);
          addEyes(0, 1.85, -0.85, 0.14, 0.14, 0.05, 0.35, -0.55);
          // Powerful Knuckle-Walking Front Arms
          addBox(0.55, 1.65, 0.55, baseMat, -0.85, 0.82, -0.75, 0.15, 0, 0);
          addBox(0.55, 1.65, 0.55, baseMat, 0.85, 0.82, -0.75, 0.15, 0, 0);
          // Shorter Hind Legs
          addBox(0.55, 0.95, 0.55, baseMat, -0.65, 0.47, 0.55);
          addBox(0.55, 0.95, 0.55, baseMat, 0.65, 0.47, 0.55);
          break;
        }

        case 'tiger': {
          const whiteMat = new THREE.MeshLambertMaterial({ color: 0xffffff });
          const stripeMat = new THREE.MeshBasicMaterial({ color: 0x111827 });
          // Tiger Body
          addBox(1.45, 1.25, 2.15, baseMat, 0, 1.15, 0);
          addBox(0.9, 0.6, 1.5, whiteMat, 0, 0.85, 0);
          // Stripes along flank
          for (let i = -1; i <= 1; i++) {
            addBox(1.48, 0.15, 0.15, stripeMat, 0, 1.45, i * 0.45);
          }
          // Tiger Head with Jowls
          addBox(1.1, 1.0, 1.05, baseMat, 0, 1.7, -1.05);
          addBox(1.35, 0.4, 0.65, whiteMat, 0, 1.5, -1.25);
          addBox(0.5, 0.38, 0.45, whiteMat, 0, 1.55, -1.55);
          addBox(0.2, 0.15, 0.1, stripeMat, 0, 1.68, -1.78);
          // Feline Ears
          addBox(0.24, 0.28, 0.12, baseMat, -0.42, 2.25, -1.05);
          addBox(0.24, 0.28, 0.12, baseMat, 0.42, 2.25, -1.05);
          addEyes(0, 1.8, -1.05, 0.14, 0.14, 0.05, 0.35, -0.55);
          // 4 Sturdy Paws
          [[-0.48, -0.65], [0.48, -0.65], [-0.48, 0.65], [0.48, 0.65]].forEach(([lx, lz]) => {
            addBox(0.42, 0.95, 0.42, baseMat, lx, 0.47, lz);
          });
          // Tiger Tail
          addBox(0.14, 1.2, 0.14, baseMat, 0, 1.25, 1.15, 0.3, 0, 0);
          addBox(0.16, 0.3, 0.16, stripeMat, 0, 1.65, 1.45);
          break;
        }

        // ==================== DEEP OCEAN (2,000 - 5,000m) ====================
        case 'seal': {
          const flipperMat = new THREE.MeshLambertMaterial({ color: 0x60a5fa });
          // Hydrodynamic Tapered Seal Body
          addBox(1.35, 1.05, 2.2, baseMat, 0, 0.75, 0);
          addBox(1.0, 0.75, 1.1, baseMat, 0, 0.65, 1.1);
          // Head
          addBox(0.9, 0.85, 0.9, baseMat, 0, 1.1, -0.95);
          addBox(0.45, 0.35, 0.35, flipperMat, 0, 0.95, -1.4);
          addBox(0.16, 0.12, 0.08, eyeMat, 0, 1.08, -1.58);
          addEyes(0, 1.2, -0.95, 0.14, 0.14, 0.05, 0.32, -0.48);
          // Side Flippers
          addBox(0.85, 0.12, 0.55, flipperMat, -0.85, 0.35, -0.25, 0, 0, -0.2);
          addBox(0.85, 0.12, 0.55, flipperMat, 0.85, 0.35, -0.25, 0, 0, 0.2);
          // Split Tail Flippers
          addBox(0.45, 0.1, 0.65, flipperMat, -0.25, 0.55, 1.85, 0, 0.25, 0);
          addBox(0.45, 0.1, 0.65, flipperMat, 0.25, 0.55, 1.85, 0, -0.25, 0);
          break;
        }

        case 'shark': {
          const bellyMat = new THREE.MeshLambertMaterial({ color: 0xf1f5f9 });
          const finMat = new THREE.MeshLambertMaterial({ color: 0x1d4ed8 });
          // Shark Body
          addBox(1.4, 1.25, 2.8, baseMat, 0, 1.0, 0);
          addBox(1.1, 0.2, 2.2, bellyMat, 0, 0.35, 0);
          // Pointed Snout & Teeth
          addBox(1.0, 0.75, 1.15, baseMat, 0, 0.95, -1.65);
          addBox(0.8, 0.15, 0.8, whiteMat, 0, 0.65, -1.75); // Jaw
          addEyes(0, 1.15, -1.35, 0.14, 0.14, 0.05, 0.45, -0.35);
          // Iconic Triangular Dorsal Fin
          addBox(0.22, 1.35, 0.85, finMat, 0, 2.1, -0.2, -0.3, 0, 0);
          // Pectoral Side Fins
          addBox(0.95, 0.14, 0.65, finMat, -0.95, 0.65, -0.45, 0, 0, -0.25);
          addBox(0.95, 0.14, 0.65, finMat, 0.95, 0.65, -0.45, 0, 0, 0.25);
          // Vertical Tail Fin
          addBox(0.18, 1.65, 0.75, finMat, 0, 1.15, 1.65, 0.15, 0, 0);
          break;
        }

        case 'kraken': {
          const glowYellow = new THREE.MeshBasicMaterial({ color: 0xfacc15 });
          const tentacleMat = new THREE.MeshLambertMaterial({ color: 0xbe185d });
          // Bulbous Mantle Head
          addBox(1.5, 1.7, 1.5, baseMat, 0, 1.7, 0);
          addBox(1.1, 0.7, 1.1, baseMat, 0, 2.65, 0);
          // Bioluminescent Eyes
          addBox(0.25, 0.25, 0.1, glowYellow, -0.42, 1.25, -0.76);
          addBox(0.25, 0.25, 0.1, glowYellow, 0.42, 1.25, -0.76);
          // Ring of 8 Splaying Tentacles
          for (let i = 0; i < 8; i++) {
            const angle = (i / 8) * Math.PI * 2;
            const tx = Math.sin(angle) * 0.75;
            const tz = Math.cos(angle) * 0.75;
            addBox(0.32, 1.2, 0.32, tentacleMat, tx, 0.6, tz, Math.cos(angle) * 0.35, 0, Math.sin(angle) * 0.35);
          }
          break;
        }

        // ==================== MYTHICAL PARADISE (5,000m+) ====================
        case 'unicorn': {
          const hornMat = new THREE.MeshBasicMaterial({ color: 0xfacc15 });
          const maneMat = new THREE.MeshLambertMaterial({ color: 0xf472b6 });
          const hoofMat = new THREE.MeshBasicMaterial({ color: 0xfacc15 });
          // Equine Body
          addBox(1.35, 1.25, 2.1, baseMat, 0, 1.4, 0);
          // Arched Neck
          addBox(0.65, 1.35, 0.65, baseMat, 0, 2.25, -0.85, -0.3, 0, 0);
          addBox(0.75, 0.75, 1.05, baseMat, 0, 2.75, -1.35);
          // Flowing Mane along Neck
          addBox(0.25, 1.45, 0.85, maneMat, 0, 2.35, -0.7, -0.3, 0, 0);
          // Glowing Golden Unicorn Horn
          addBox(0.16, 1.35, 0.16, hornMat, 0, 3.75, -1.35, 0.25, 0, 0);
          addEyes(0, 2.85, -1.35, 0.14, 0.14, 0.05, 0.38, -0.35);
          // 4 Equine Legs with Golden Hooves
          [[-0.45, -0.65], [0.45, -0.65], [-0.45, 0.65], [0.45, 0.65]].forEach(([lx, lz]) => {
            addBox(0.32, 1.2, 0.32, baseMat, lx, 0.6, lz);
            addBox(0.34, 0.22, 0.34, hoofMat, lx, 0.11, lz);
          });
          // Flowing Celestial Tail
          addBox(0.2, 1.2, 0.25, maneMat, 0, 1.4, 1.15, 0.3, 0, 0);
          break;
        }

        case 'phoenix': {
          const flameGold = new THREE.MeshBasicMaterial({ color: 0xfacc15 });
          const featherOrange = new THREE.MeshLambertMaterial({ color: 0xf97316 });
          // Fiery Body
          addBox(1.25, 1.25, 1.6, baseMat, 0, 1.4, 0);
          // Eagle Head & Beak
          addBox(0.8, 0.8, 0.85, baseMat, 0, 2.15, -0.75);
          addBox(0.4, 0.4, 0.65, flameGold, 0, 2.05, -1.35, 0.1, 0, 0);
          // Crown Feather Crest
          addBox(0.18, 0.75, 0.55, flameGold, 0, 2.75, -0.65, -0.3, 0, 0);
          addEyes(0, 2.25, -0.75, 0.14, 0.14, 0.05, 0.38, -0.35);
          // Giant Spread Fiery Wings
          addBox(2.2, 0.18, 1.3, featherOrange, -1.45, 1.65, 0, 0, 0, -0.15);
          addBox(2.2, 0.18, 1.3, featherOrange, 1.45, 1.65, 0, 0, 0, 0.15);
          // 3 Flowing Solar Tail Plumes
          addBox(0.25, 0.1, 2.4, flameGold, -0.35, 1.25, 1.85, -0.2, -0.15, 0);
          addBox(0.3, 0.1, 2.7, flameGold, 0, 1.25, 2.0, -0.2, 0, 0);
          addBox(0.25, 0.1, 2.4, flameGold, 0.35, 1.25, 1.85, -0.2, 0.15, 0);
          break;
        }

        case 'dragon': {
          const cosmicGlow = new THREE.MeshBasicMaterial({ color: 0xc084fc });
          const hornMat = new THREE.MeshLambertMaterial({ color: 0x581c87 });
          const fangMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
          // Draconic Serpentine Body
          addBox(1.55, 1.45, 2.6, baseMat, 0, 1.4, 0);
          // Powerful Dragon Head & Snout
          addBox(1.15, 1.05, 1.15, baseMat, 0, 2.15, -1.25);
          addBox(0.85, 0.65, 0.95, baseMat, 0, 1.95, -2.05);
          // Fangs
          addBox(0.12, 0.25, 0.12, fangMat, -0.32, 1.55, -2.25);
          addBox(0.12, 0.25, 0.12, fangMat, 0.32, 1.55, -2.25);
          // Swept-Back Horns
          addBox(0.22, 1.15, 0.22, hornMat, -0.42, 2.95, -1.15, -0.45, 0, -0.25);
          addBox(0.22, 1.15, 0.22, hornMat, 0.42, 2.95, -1.15, -0.45, 0, 0.25);
          addEyes(0, 2.35, -1.25, 0.16, 0.16, 0.05, 0.42, -0.55);
          // Spiny Dorsal Ridge Down Spine
          for (let i = -2; i <= 2; i++) {
            addBox(0.15, 0.45, 0.35, cosmicGlow, 0, 2.25, i * 0.45);
          }
          // Giant Expansive Membrane Wings
          addBox(2.6, 0.15, 1.6, cosmicGlow, -1.75, 1.85, -0.2, 0, 0, -0.2);
          addBox(2.6, 0.15, 1.6, cosmicGlow, 1.75, 1.85, -0.2, 0, 0, 0.2);
          // Serpentine Tail with Spade Barb
          addBox(0.45, 0.45, 1.5, baseMat, 0, 1.35, 1.95, 0.15, 0, 0);
          addBox(0.75, 0.1, 0.75, hornMat, 0, 1.6, 2.85, 0, 0.78, 0);
          break;
        }

        default: {
          // Fallback generic blocky
          addBox(1.4, 1.1, 1.7, baseMat, 0, 0.75, 0);
          addBox(1.1, 1.0, 1.0, baseMat, 0, 1.35, -0.8);
          addEyes(0, 1.45, -0.8, 0.16, 0.16, 0.05, 0.3, -0.52);
          break;
        }
      }

      // Add Mutation Halo / Aura if Golden, Rainbow, or Cosmic
      if (mutation && mutation.mult >= 5) {
        const auraGeo = new THREE.TorusGeometry(1.3 * s, 0.12 * s, 12, 24);
        const auraMat = new THREE.MeshBasicMaterial({ color: mutation.hex });
        const aura = new THREE.Mesh(auraGeo, auraMat);
        aura.rotation.x = Math.PI / 2;
        aura.position.y = 0.25 * s;
        g.add(aura);
      }

      return g;
    }
"""
