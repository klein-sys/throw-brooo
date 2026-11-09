# -*- coding: utf-8 -*-

JS_THREE = """
    /*************************************************************************
     * 5. 3D THREE.JS WEBGL VOXEL WORLD, CANYON & LAUNCH ARC
     *************************************************************************/
    const container = document.getElementById('webglContainer');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x38bdf8); // Vibrant Roblox sky blue
    scene.fog = new THREE.FogExp2(0x38bdf8, 0.0035);

    const camera = new THREE.PerspectiveCamera(54, window.innerWidth / window.innerHeight, 0.2, 800);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.05;
    container.appendChild(renderer.domElement);

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
      resizeOscilloscope();
    });

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.75);
    scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0xfffbeb, 0.9);
    sunLight.position.set(45, 80, 50);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 1024;
    sunLight.shadow.mapSize.height = 1024;
    sunLight.shadow.camera.near = 0.5;
    sunLight.shadow.camera.far = 400;
    sunLight.shadow.camera.left = -60;
    sunLight.shadow.camera.right = 60;
    sunLight.shadow.camera.top = 60;
    sunLight.shadow.camera.bottom = -60;
    scene.add(sunLight);

    // Helper: Create Authentic Roblox Studded Canvas Texture
    function createStuddedTexture(c1, c2, repeatsX, repeatsY) {
      const cnv = document.createElement('canvas');
      cnv.width = 128;
      cnv.height = 128;
      const g = cnv.getContext('2d');

      g.fillStyle = c1;
      g.fillRect(0, 0, 128, 128);
      g.fillStyle = c2;
      g.fillRect(0, 0, 64, 64);
      g.fillRect(64, 64, 64, 64);

      const centers = [[32, 32], [96, 32], [32, 96], [96, 96]];
      centers.forEach(([cx, cy]) => {
        g.fillStyle = 'rgba(0, 0, 0, 0.18)';
        g.beginPath();
        g.arc(cx, cy + 2, 12, 0, Math.PI * 2);
        g.fill();

        g.fillStyle = 'rgba(255, 255, 255, 0.22)';
        g.beginPath();
        g.arc(cx, cy, 12, 0, Math.PI * 2);
        g.fill();

        g.fillStyle = 'rgba(0, 0, 0, 0.12)';
        g.beginPath();
        g.arc(cx, cy, 9.5, 0, Math.PI * 2);
        g.fill();

        g.fillStyle = 'rgba(255, 255, 255, 0.3)';
        g.beginPath();
        g.arc(cx - 2, cy - 2, 7, 0, Math.PI * 2);
        g.fill();
      });

      const tex = new THREE.CanvasTexture(cnv);
      tex.magFilter = THREE.NearestFilter;
      tex.minFilter = THREE.LinearMipMapLinearFilter;
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(repeatsX, repeatsY);
      return tex;
    }

    // 1) Base Lawn Hub Ground (z = -22 to +28)
    const hubTex = createStuddedTexture('#4ade80', '#22c55e', 24, 24);
    const hubGround = new THREE.Mesh(
      new THREE.PlaneGeometry(56, 52),
      new THREE.MeshLambertMaterial({ map: hubTex })
    );
    hubGround.rotation.x = -Math.PI / 2;
    hubGround.position.set(0, 0, 4);
    hubGround.receiveShadow = true;
    scene.add(hubGround);

    // 2) Orange & Yellow Checkered Launch Line Strip (z = -14)
    const launchTex = createStuddedTexture('#f59e0b', '#fde047', 16, 2);
    const launchStrip = new THREE.Mesh(
      new THREE.BoxGeometry(38, 0.25, 4.5),
      new THREE.MeshLambertMaterial({ map: launchTex })
    );
    launchStrip.position.set(0, 0.12, -14);
    launchStrip.receiveShadow = true;
    scene.add(launchStrip);

    // Glowing Neon Boundary Strips flanking Launch Line
    [-16.25, -11.75].forEach(stripZ => {
      const neonBorder = new THREE.Mesh(
        new THREE.BoxGeometry(38.2, 0.32, 0.35),
        new THREE.MeshBasicMaterial({ color: 0xffffff })
      );
      neonBorder.position.set(0, 0.16, stripZ);
      scene.add(neonBorder);
    });

    // Yellow Floating Down-Arrow Marker at Launch Line
    const launchArrowMesh = new THREE.Mesh(
      new THREE.ConeGeometry(0.85, 1.6, 4),
      new THREE.MeshBasicMaterial({ color: 0xfacc15 })
    );
    launchArrowMesh.rotation.x = Math.PI;
    launchArrowMesh.position.set(0, 3.8, -14);
    scene.add(launchArrowMesh);

    // 3) 3D Sinusoidal Launch Ramp & Tangent Arrow at Launch Line
    const rampGroup = new THREE.Group();
    rampGroup.position.set(0, 0.2, -14.5);
    scene.add(rampGroup);

    const rampArrow = new THREE.ArrowHelper(
      new THREE.Vector3(0, 0.707, -0.707).normalize(),
      new THREE.Vector3(0, 1.4, 0),
      5.2,
      0xfde047,
      1.3,
      0.85
    );
    rampGroup.add(rampArrow);

    function update3DRampVisuals() {
      const ramp = evaluateRampCalculus(state.rampX0);
      const dir = new THREE.Vector3(0, Math.sin(ramp.angleRad), -Math.cos(ramp.angleRad)).normalize();
      rampArrow.setDirection(dir);
    }
    update3DRampVisuals();

    // 4) 3D LIVE TANGENT TRAJECTORY ARC IN THE WORLD
    const ARC_POINTS_COUNT = 64;
    const trajectoryPositions = new Float32Array(ARC_POINTS_COUNT * 3);
    const trajectoryGeo = new THREE.BufferGeometry();
    trajectoryGeo.setAttribute('position', new THREE.BufferAttribute(trajectoryPositions, 3));
    const trajectoryMat = new THREE.LineBasicMaterial({
      color: 0x38bdf8,
      linewidth: 3,
      transparent: true,
      opacity: 0.85
    });
    const trajectoryLineMesh = new THREE.Line(trajectoryGeo, trajectoryMat);
    scene.add(trajectoryLineMesh);

    function update3DTrajectoryArc() {
      if (state.activeZone !== 'throw') {
        trajectoryLineMesh.visible = false;
        return;
      }
      trajectoryLineMesh.visible = true;
      const food = getEquippedFood();
      const calc = evaluateFoodCalculus(food, state.t);
      const ramp = evaluateRampCalculus(state.rampX0);
      const previewDist = Math.max(20, Math.pow(getTotalStrength(), 0.85) * food.distMult * (1 + Math.abs(calc.deriv) * 0.22) * ramp.angleEfficiency);
      const normDist = Math.min(1, Math.pow(previewDist / 5000, 0.52));
      const targetZ = -14 - normDist * 290;

      const posAttr = trajectoryGeo.attributes.position;
      const startX = playerGroup ? playerGroup.position.x : 0;
      const startY = 2.2;
      const startZ = -14;

      for (let i = 0; i < ARC_POINTS_COUNT; i++) {
        const p = i / (ARC_POINTS_COUNT - 1);
        const z = startZ + p * (targetZ - startZ);
        const waveArcY = startY + Math.sin(p * Math.PI) * (10 + ramp.slope * 4.5) + Math.sin(p * Math.PI * 4 + state.t * 3) * 0.6;
        posAttr.setXYZ(i, startX, waveArcY, z);
      }
      posAttr.needsUpdate = true;
      trajectoryMat.color.setHex(food.color);
    }

    // 5) Fenced Player Lawn Plot ("My Plot" in center-back z = -4 to +18, x = -11 to +11)
    const fenceMat = new THREE.MeshLambertMaterial({ color: 0xd97706 });
    function buildPlotFences() {
      const fenceGroup = new THREE.Group();
      const postGeo = new THREE.BoxGeometry(0.55, 2.2, 0.55);
      for (let x = -11; x <= 11; x += 2.75) {
        for (const z of [-4, 18]) {
          if (z === -4 && Math.abs(x) < 3) continue;
          const post = new THREE.Mesh(postGeo, fenceMat);
          post.position.set(x, 1.1, z);
          fenceGroup.add(post);
        }
      }
      for (let z = -4; z <= 18; z += 2.75) {
        for (const x of [-11, 11]) {
          const post = new THREE.Mesh(postGeo, fenceMat);
          post.position.set(x, 1.1, z);
          fenceGroup.add(post);
        }
      }
      const railFB = new THREE.Mesh(new THREE.BoxGeometry(22, 0.28, 0.22), fenceMat);
      railFB.position.set(0, 1.45, 18);
      fenceGroup.add(railFB);
      const railL = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.28, 22), fenceMat);
      railL.position.set(-11, 1.45, 7);
      fenceGroup.add(railL);
      const railR = railL.clone();
      railR.position.x = 11;
      fenceGroup.add(railR);

      const archMat = new THREE.MeshLambertMaterial({ color: 0x92400e });
      const archL = new THREE.Mesh(new THREE.BoxGeometry(0.4, 3.8, 0.4), archMat);
      archL.position.set(-3.2, 1.9, -4);
      const archR = archL.clone();
      archR.position.x = 3.2;
      const archTop = new THREE.Mesh(new THREE.BoxGeometry(6.8, 0.4, 0.4), archMat);
      archTop.position.set(0, 3.8, -4);
      fenceGroup.add(archL, archR, archTop);

      scene.add(fenceGroup);
    }
    buildPlotFences();

    // 6) Build 3D Physical Stations: Pull-Up Bar, Blue Food Shop Stall, Red Sell Stall
    function createGlowingRing(x, z, colorHex) {
      const ringGeo = new THREE.RingGeometry(2.8, 3.3, 32);
      const ringMat = new THREE.MeshBasicMaterial({ color: colorHex, side: THREE.DoubleSide });
      const ring = new THREE.Mesh(ringGeo, ringMat);
      ring.rotation.x = -Math.PI / 2;
      ring.position.set(x, 0.08, z);
      scene.add(ring);
      return ring;
    }

    function buildStall3D(x, z, roofColor1, roofColor2, labelText) {
      const g = new THREE.Group();
      g.position.set(x, 0, z);
      const counter = new THREE.Mesh(
        new THREE.BoxGeometry(5.2, 2.2, 3.2),
        new THREE.MeshLambertMaterial({ color: 0x92400e })
      );
      counter.position.y = 1.1;
      counter.castShadow = true;
      g.add(counter);

      const postGeo = new THREE.BoxGeometry(0.35, 4.8, 0.35);
      const postMat = new THREE.MeshLambertMaterial({ color: 0x78350f });
      [[-2.2, -1.3], [2.2, -1.3], [-2.2, 1.3], [2.2, 1.3]].forEach(([px, pz]) => {
        const p = new THREE.Mesh(postGeo, postMat);
        p.position.set(px, 2.4, pz);
        g.add(p);
      });

      for (let i = 0; i < 5; i++) {
        const stripe = new THREE.Mesh(
          new THREE.BoxGeometry(1.15, 0.6, 3.8),
          new THREE.MeshLambertMaterial({ color: i % 2 === 0 ? roofColor1 : roofColor2 })
        );
        stripe.position.set(-2.3 + i * 1.15, 4.9, 0);
        g.add(stripe);
      }
      scene.add(g);
    }

    buildStall3D(STATIONS.shop.x, STATIONS.shop.z, 0x2563eb, 0xffffff, 'FOOD SHOP');
    createGlowingRing(STATIONS.shop.x, STATIONS.shop.z + 2.5, 0x3b82f6);

    buildStall3D(STATIONS.sell.x, STATIONS.sell.z, 0xef4444, 0xffffff, 'SELL');
    createGlowingRing(STATIONS.sell.x, STATIONS.sell.z + 2.5, 0xef4444);

    const pullUpGroup = new THREE.Group();
    pullUpGroup.position.set(STATIONS.pullup.x, 0, STATIONS.pullup.z);
    const barPostGeo = new THREE.BoxGeometry(0.5, 5.2, 0.5);
    const barPostMat = new THREE.MeshLambertMaterial({ color: 0x92400e });
    const leftPost = new THREE.Mesh(barPostGeo, barPostMat);
    leftPost.position.set(-2.0, 2.6, 0);
    const rightPost = new THREE.Mesh(barPostGeo, barPostMat);
    rightPost.position.set(2.0, 2.6, 0);
    const crossBar = new THREE.Mesh(
      new THREE.CylinderGeometry(0.14, 0.14, 4.4, 16),
      new THREE.MeshLambertMaterial({ color: 0xfde68a })
    );
    crossBar.rotation.z = Math.PI / 2;
    crossBar.position.set(0, 4.8, 0);
    pullUpGroup.add(leftPost, rightPost, crossBar);
    scene.add(pullUpGroup);
    createGlowingRing(STATIONS.pullup.x, STATIONS.pullup.z, 0x38bdf8);

    // 7) 6 SEQUENTIAL 3D BIOME RUNWAY ZONES & BROWN VOXEL CANYON WALLS
    BIOMES.forEach((b, idx) => {
      const length = Math.abs(b.zEnd - b.zStart);
      const zCenter = (b.zStart + b.zEnd) / 2;
      const bTex = createStuddedTexture(b.cssColor, '#1e293b', 16, 16);
      const plane = new THREE.Mesh(
        new THREE.PlaneGeometry(44, length),
        new THREE.MeshLambertMaterial({ map: bTex })
      );
      plane.rotation.x = -Math.PI / 2;
      plane.position.set(0, 0.02, zCenter);
      plane.receiveShadow = true;
      scene.add(plane);

      // Decorative trees along canyon edges
      for (let z = b.zStart - 6; z > b.zEnd + 4; z -= 14) {
        [-17, 17].forEach(xSide => {
          const trunk = new THREE.Mesh(
            new THREE.BoxGeometry(1.2, 4.2, 1.2),
            new THREE.MeshLambertMaterial({ color: 0x78350f })
          );
          trunk.position.set(xSide, 2.1, z);
          const leaves = new THREE.Mesh(
            new THREE.BoxGeometry(4.0, 4.0, 4.0),
            new THREE.MeshLambertMaterial({ color: b.colorHex })
          );
          leaves.position.set(xSide, 5.5, z);
          scene.add(trunk, leaves);
        });
      }
    });

    // Stepped Brown Voxel Dirt Canyon Walls
    const dirtTex = createStuddedTexture('#78350f', '#5a2507', 8, 48);
    const wallMat = new THREE.MeshLambertMaterial({ map: dirtTex });
    const wallTopMat = new THREE.MeshLambertMaterial({ color: 0x22c55e });

    [-29, 29].forEach(xWall => {
      const wall = new THREE.Mesh(new THREE.BoxGeometry(12, 24, 400), wallMat);
      wall.position.set(xWall, 12, -160);
      const topGrass = new THREE.Mesh(new THREE.BoxGeometry(12.8, 2.6, 400), wallTopMat);
      topGrass.position.set(xWall, 24.5, -160);
      scene.add(wall, topGrass);
    });

    // 8) MOUNTED CANYON WALL 3D "LUCKIEST CATCHES - YOUR BEST RECORDS" BILLBOARD
    // Removed TOP MONEY board as requested; dedicated to player's best catches!
    const luckiestBoardCanvas = document.createElement('canvas');
    luckiestBoardCanvas.width = 768;
    luckiestBoardCanvas.height = 640;
    const luckiestBoardTex = new THREE.CanvasTexture(luckiestBoardCanvas);

    const luckiestBoardGroup = new THREE.Group();
    luckiestBoardGroup.position.set(-22.4, 9.5, -14);
    luckiestBoardGroup.rotation.y = Math.PI / 2;

    const boardFrame = new THREE.Mesh(
      new THREE.BoxGeometry(11.5, 9.5, 0.4),
      new THREE.MeshLambertMaterial({ color: 0x111827 })
    );
    const boardBorder = new THREE.Mesh(
      new THREE.BoxGeometry(11.9, 9.9, 0.35),
      new THREE.MeshLambertMaterial({ color: 0xfacc15 })
    );
    boardBorder.position.z = -0.05;
    luckiestBoardGroup.add(boardFrame, boardBorder);

    const boardFace = new THREE.Mesh(
      new THREE.PlaneGeometry(11.2, 9.0),
      new THREE.MeshBasicMaterial({ map: luckiestBoardTex })
    );
    boardFace.position.z = 0.22;
    luckiestBoardGroup.add(boardFace);
    scene.add(luckiestBoardGroup);

    function update3DLuckiestBoardTexture() {
      const ctx = luckiestBoardCanvas.getContext('2d');
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(0, 0, 768, 640);

      // Gold Top Banner
      ctx.fillStyle = '#facc15';
      ctx.fillRect(0, 0, 768, 85);
      ctx.fillStyle = '#000000';
      ctx.font = 'bold 36px Fredoka, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('🏆 LUCKIEST CATCHES (YOUR BEST RECORDS)', 384, 58);

      const catches = state.playerBestCatches || [];
      ctx.textAlign = 'left';
      ctx.font = 'bold 24px Fredoka, sans-serif';

      for (let i = 0; i < 5; i++) {
        const y = 145 + i * 95;
        ctx.fillStyle = i % 2 === 0 ? '#1e293b' : '#334155';
        ctx.fillRect(25, y - 40, 718, 75);

        if (catches[i]) {
          const c = catches[i];
          ctx.fillStyle = '#facc15';
          ctx.fillText(`#${i + 1}`, 45, y + 8);
          ctx.fillStyle = '#ffffff';
          ctx.fillText(`${c.emoji} ${c.name} [${c.size.name}]`, 110, y + 8);

          ctx.fillStyle = c.mutation.color || '#4ade80';
          ctx.fillText(`${c.mutation.name.split('•').pop().trim()}`, 430, y + 8);

          ctx.fillStyle = '#fbbf24';
          ctx.textAlign = 'right';
          ctx.fillText(`1 in ${formatNum(c.odds)}`, 715, y + 8);
          ctx.textAlign = 'left';
        } else {
          ctx.fillStyle = '#64748b';
          ctx.fillText(`#${i + 1} — No Record Yet (Throw Food!)`, 45, y + 8);
        }
      }
      luckiestBoardTex.needsUpdate = true;
    }

    // 9) 3D MOVING CALCULUS SKILL SHOT TARGETS IN THE CANYON
    const critRingGroup = new THREE.Group();
    critRingGroup.position.set(0, 6.5, -95);
    const critRingMesh = new THREE.Mesh(
      new THREE.TorusGeometry(3.6, 0.45, 16, 32),
      new THREE.MeshBasicMaterial({ color: 0xfacc15 })
    );
    critRingGroup.add(critRingMesh);
    scene.add(critRingGroup);

    const surgeGateGroup = new THREE.Group();
    surgeGateGroup.position.set(0, 0, -195);
    const gatePostGeo = new THREE.BoxGeometry(0.8, 14, 0.8);
    const gateMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });
    const gateL = new THREE.Mesh(gatePostGeo, gateMat);
    gateL.position.set(-6, 7, 0);
    const gateR = new THREE.Mesh(gatePostGeo, gateMat);
    gateR.position.set(6, 7, 0);
    const gateTop = new THREE.Mesh(new THREE.BoxGeometry(13.6, 0.8, 0.8), gateMat);
    gateTop.position.set(0, 14, 0);
    surgeGateGroup.add(gateL, gateR, gateTop);
    scene.add(surgeGateGroup);

    const targetLabels = [
      { pos: new THREE.Vector3(0, 11.2, -95), text: "🎯 CRITICAL POINT RING: P'(t) ≈ 0 (5x-25x Mutation!)", color: '#facc15' },
      { pos: new THREE.Vector3(0, 15.5, -195), text: "⚡ MAX VELOCITY GATE: |P'(t)| = MAX (+35% Range!)", color: '#38bdf8' }
    ];
    targetLabels.forEach(tl => {
      const el = document.createElement('div');
      el.className = 'absolute -translate-x-1/2 -translate-y-full text-center pointer-events-none font-black text-[11px] rblx-stroke-sm';
      el.style.color = tl.color;
      el.textContent = tl.text;
      document.getElementById('labelsContainer').appendChild(el);
      tl.el = el;
    });

    // 10) 3D BLOCKY ROBLOX PLAYER CHARACTER
    const playerGroup = new THREE.Group();
    const headMesh = new THREE.Mesh(
      new THREE.BoxGeometry(1.1, 1.1, 1.1),
      new THREE.MeshLambertMaterial({ color: 0xfde047 })
    );
    headMesh.position.y = 3.25;
    headMesh.castShadow = true;

    const torsoMesh = new THREE.Mesh(
      new THREE.BoxGeometry(1.5, 1.6, 0.8),
      new THREE.MeshLambertMaterial({ color: 0xef4444 })
    );
    torsoMesh.position.y = 1.9;
    torsoMesh.castShadow = true;

    const leftArm = new THREE.Mesh(
      new THREE.BoxGeometry(0.5, 1.5, 0.5),
      new THREE.MeshLambertMaterial({ color: 0xfde047 })
    );
    leftArm.position.set(-1.05, 1.9, 0);

    const rightArm = leftArm.clone();
    rightArm.position.set(1.05, 1.9, 0);

    const leftLeg = new THREE.Mesh(
      new THREE.BoxGeometry(0.65, 1.1, 0.65),
      new THREE.MeshLambertMaterial({ color: 0x2563eb })
    );
    leftLeg.position.set(-0.4, 0.55, 0);

    const rightLeg = leftLeg.clone();
    rightLeg.position.set(0.4, 0.55, 0);

    const heldFoodMesh = new THREE.Mesh(
      new THREE.BoxGeometry(0.7, 0.7, 0.7),
      new THREE.MeshLambertMaterial({ color: 0xf97316 })
    );
    heldFoodMesh.position.set(1.15, 2.2, -0.6);

    playerGroup.add(headMesh, torsoMesh, leftArm, rightArm, leftLeg, rightLeg, heldFoodMesh);
    playerGroup.position.set(state.playerPos.x, 0, state.playerPos.z);
    scene.add(playerGroup);

    // 11) 3D VOXEL ANIMAL GENERATOR WITH SIZE & MUTATION SCALING
    const plotPetsGroup = new THREE.Group();
    scene.add(plotPetsGroup);
    let activePlotPetEntities = [];

    function createBlockyAnimalMesh(animal, size, mutation) {
      const g = new THREE.Group();
      const sizeMult = size ? size.scale : 1.0;
      const mutBoost = (mutation && mutation.mult >= 5) ? 1.15 : 1.0;
      const s = animal.scale * sizeMult * mutBoost;

      const bodyMat = new THREE.MeshLambertMaterial({ color: animal.color });
      const body = new THREE.Mesh(new THREE.BoxGeometry(1.4 * s, 1.1 * s, 1.7 * s), bodyMat);
      body.position.y = 0.75 * s;
      body.castShadow = true;
      g.add(body);

      const head = new THREE.Mesh(new THREE.BoxGeometry(1.1 * s, 1.0 * s, 1.0 * s), bodyMat);
      head.position.set(0, 1.35 * s, -0.8 * s);
      head.castShadow = true;
      g.add(head);

      const eyeMat = new THREE.MeshBasicMaterial({ color: 0x111111 });
      const eyeL = new THREE.Mesh(new THREE.BoxGeometry(0.18 * s, 0.18 * s, 0.1 * s), eyeMat);
      eyeL.position.set(-0.3 * s, 1.45 * s, -1.32 * s);
      const eyeR = eyeL.clone();
      eyeR.position.x = 0.3 * s;
      g.add(eyeL, eyeR);

      // Mutation Glowing Particle Aura / Halo Ring
      if (mutation && mutation.mult >= 5) {
        const auraGeo = new THREE.TorusGeometry(1.2 * s, 0.12 * s, 12, 24);
        const auraMat = new THREE.MeshBasicMaterial({ color: mutation.hex });
        const aura = new THREE.Mesh(auraGeo, auraMat);
        aura.rotation.x = Math.PI / 2;
        aura.position.y = 0.25;
        g.add(aura);
      }
      return g;
    }

    function sync3DPlotPets() {
      while (plotPetsGroup.children.length > 0) {
        plotPetsGroup.remove(plotPetsGroup.children[0]);
      }
      activePlotPetEntities.forEach(ent => ent.labelEl && ent.labelEl.remove());
      activePlotPetEntities = [];

      if (!state.settings.viewYourPets) return;

      const equippedPets = state.inventory.filter(i => i.equipped);
      const labelsRoot = document.getElementById('labelsContainer');

      equippedPets.forEach((pet, idx) => {
        const animal = ANIMALS.find(a => a.id === pet.animalId);
        const mesh = createBlockyAnimalMesh(animal, pet.size, pet.mutation);
        const cols = 5;
        const px = -7.5 + (idx % cols) * 3.75 + (Math.random() - 0.5) * 0.8;
        const pz = -1.5 + Math.floor(idx / cols) * 4.2 + (Math.random() - 0.5) * 0.8;
        mesh.position.set(px, 0, pz);
        plotPetsGroup.add(mesh);

        const labelEl = document.createElement('div');
        labelEl.className = 'absolute -translate-x-1/2 -translate-y-full text-center pointer-events-none leading-tight';
        const sizeTag = pet.size && pet.size.id !== 'regular' ? `[${pet.size.name.toUpperCase()}] ` : '';
        labelEl.innerHTML = `
          <div class="text-[11px] font-extrabold text-white rblx-stroke-sm">${animal.emoji} ${sizeTag}${animal.name}</div>
          <div class="text-[10px] font-extrabold rblx-stroke-sm" style="color:${pet.mutation.color}">
            ${pet.mutation.name.split('•').pop().trim()} $${formatNum(pet.income)}/s
          </div>
        `;
        labelsRoot.appendChild(labelEl);

        activePlotPetEntities.push({
          pet,
          mesh,
          labelEl,
          vx: (Math.random() - 0.5) * 2.2,
          vz: (Math.random() - 0.5) * 2.2,
          hopPhase: Math.random() * Math.PI * 2
        });
      });
    }

    function spawnFloatingCashPopups() {
      if (!state.settings.viewYourPets) return;
      const labelsRoot = document.getElementById('labelsContainer');
      activePlotPetEntities.forEach(ent => {
        const cashPopup = document.createElement('div');
        cashPopup.className = 'absolute font-black text-lime-400 text-sm rblx-stroke floating-cash-anim';
        cashPopup.textContent = `+$${formatNum(ent.pet.income)}`;
        labelsRoot.appendChild(cashPopup);

        const pos = ent.mesh.position.clone().add(new THREE.Vector3(0, 3.2, 0));
        project3DToScreen(pos, cashPopup);

        setTimeout(() => cashPopup.remove(), 1250);
      });
    }

    // 12) THROW PROJECTILE MESH & CUTSCENE SHOWCASE
    const projectileGroup = new THREE.Group();
    projectileGroup.visible = false;
    const projectileMesh = new THREE.Mesh(
      new THREE.BoxGeometry(0.85, 0.85, 0.85),
      new THREE.MeshLambertMaterial({ color: 0xf97316 })
    );
    projectileGroup.add(projectileMesh);
    scene.add(projectileGroup);

    const cutsceneGroup = new THREE.Group();
    cutsceneGroup.visible = false;
    scene.add(cutsceneGroup);

    // Station Floating 3D Labels
    const stationLabels = [];
    function initStationLabels() {
      const labelsRoot = document.getElementById('labelsContainer');
      const list = [
        { key: 'throw',  pos: new THREE.Vector3(0, 5.0, -14),  text: '🎯 LAUNCH LINE (STEP HERE TO THROW)', color: '#fde047' },
        { key: 'pullup', pos: new THREE.Vector3(-16, 5.8, 4),  text: '🏋️ PULL-UP WORKOUT (CHAIN RULE)', color: '#38bdf8' },
        { key: 'shop',   pos: new THREE.Vector3(-16, 5.8, -8), text: '🛒 FOOD SHOP STALL', color: '#60a5fa' },
        { key: 'sell',   pos: new THREE.Vector3(16, 5.8, -6),  text: '💰 SELL STALL', color: '#f87171' },
        { key: 'plot',   pos: new THREE.Vector3(0, 4.6, -4),   text: '🏡 MY LAWN PLOT (MAX 20 PETS)', color: '#4ade80' }
      ];
      list.forEach(st => {
        const el = document.createElement('div');
        el.className = 'absolute -translate-x-1/2 -translate-y-full text-center pointer-events-none font-extrabold text-[11px] rblx-stroke-sm';
        el.style.color = st.color;
        el.textContent = st.text;
        labelsRoot.appendChild(el);
        stationLabels.push({ ...st, el });
      });
    }
"""
