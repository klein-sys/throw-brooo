# -*- coding: utf-8 -*-

JS_THREE = """
    /*************************************************************************
     * 5. 3D THREE.JS WEBGL VOXEL WORLD, EXPANDED CANYON & LAUNCH ARC
     *************************************************************************/
    const container = document.getElementById('webglContainer');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x50bcec);
    scene.fog = new THREE.FogExp2(0x9adcf0, 0.0020);
    const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');

    // The camera-centered sky is independent of the canyon's depth fog.
    const sky = new THREE.Mesh(new THREE.SphereGeometry(980, 24, 12), new THREE.ShaderMaterial({
      side: THREE.BackSide, depthWrite: false,
      uniforms: {
        horizon: { value: new THREE.Color(0x9adcf0) },
        zenith: { value: new THREE.Color(0x168fdf) }
      },
      vertexShader: `
        varying vec3 skyDirection;
        void main() {
          skyDirection = position;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        uniform vec3 horizon;
        uniform vec3 zenith;
        varying vec3 skyDirection;
        void main() {
          float height = smoothstep(-0.06, 0.58, normalize(skyDirection).y);
          gl_FragColor = vec4(mix(horizon, zenith, height), 1.0);
        }
      `
    }));
    sky.renderOrder = -100;
    scene.add(sky);

    const camera = new THREE.PerspectiveCamera(54, window.innerWidth / window.innerHeight, 0.2, 1200);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.13;
    container.appendChild(renderer.domElement);

    function applyGraphicsQuality() {
      const quality = state.settings.graphics || 'auto';
      const low = quality === 'low' || (quality === 'auto' && matchMedia('(pointer: coarse)').matches);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, low ? 1 : 2));
      const shadowsChanged = renderer.shadowMap.enabled === low;
      renderer.shadowMap.enabled = !low;
      if (shadowsChanged) scene.traverse(obj => {
        if (obj.material) (Array.isArray(obj.material) ? obj.material : [obj.material]).forEach(mat => { mat.needsUpdate = true; });
      });
      document.getElementById('graphicsSelect').value = quality;
    }

    function setGraphicsQuality(quality) {
      if (!['auto', 'low', 'high'].includes(quality)) return;
      state.settings.graphics = quality;
      applyGraphicsQuality();
      saveGame();
    }

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
      applyGraphicsQuality();
      resizeOscilloscope();
    });

    // Lighting
    const skyFill = new THREE.HemisphereLight(0xe4f7ff, 0xc3c388, 0.77);
    scene.add(skyFill);

    const sunLight = new THREE.DirectionalLight(0xfff4d2, 1.12);
    sunLight.position.set(-34, 72, 35);
    sunLight.shadow.normalBias = 0.16;
    sunLight.shadow.bias = -0.0003;
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 1024;
    sunLight.shadow.mapSize.height = 1024;
    sunLight.shadow.camera.near = 0.5;
    sunLight.shadow.camera.far = 200;
    sunLight.shadow.camera.left = -90;
    sunLight.shadow.camera.right = 90;
    sunLight.shadow.camera.top = 90;
    sunLight.shadow.camera.bottom = -90;
    scene.add(sunLight, sunLight.target);

    function updateWorldLighting(x, z) {
      // Step the shadow focus with the action without shifting its sun angle.
      const targetX = Math.round(x / 8) * 8;
      const targetZ = Math.round(z / 8) * 8;
      if (sunLight.target.position.x === targetX && sunLight.target.position.z === targetZ) return;
      sunLight.target.position.set(targetX, 0, targetZ);
      sunLight.position.set(targetX - 34, 72, targetZ + 35);
    }

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

      for (const y of [8, 40, 72, 104]) {
        for (const x of [8, 40, 72, 104]) {
          g.fillStyle = 'rgba(24, 30, 11, 0.24)';
          g.fillRect(x + 1, y + 2, 16, 16);
          g.fillStyle = 'rgba(255, 255, 225, 0.16)';
          g.fillRect(x, y, 16, 16);
          g.fillStyle = 'rgba(62, 70, 28, 0.11)';
          g.fillRect(x + 2, y + 2, 12, 12);
          g.fillStyle = 'rgba(0, 0, 0, 0.12)';
          g.fillRect(x + 13, y + 2, 1, 12);
          g.fillRect(x + 2, y + 13, 12, 1);
        }
      }

      const tex = new THREE.CanvasTexture(cnv);
      tex.magFilter = THREE.NearestFilter;
      tex.minFilter = THREE.LinearMipMapLinearFilter;
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(repeatsX, repeatsY);
      return tex;
    }

    // 1) EXPANDED Base Lawn Hub Ground (110 units wide x 90 units deep)
    const hubTex = createStuddedTexture('#46d90a', '#37c70a', 17, 14);
    const hubGround = new THREE.Mesh(
      new THREE.PlaneGeometry(110, 90),
      new THREE.MeshLambertMaterial({ map: hubTex })
    );
    hubGround.rotation.x = -Math.PI / 2;
    hubGround.position.set(0, 0, 20);
    hubGround.receiveShadow = true;
    scene.add(hubGround);

    // 2) EXPANDED Orange & Yellow Checkered Launch Line Strip (z = -14)
    const launchTex = createStuddedTexture('#ff7e13', '#ffba20', 21, 1.5);
    const launchStrip = new THREE.Mesh(
      new THREE.BoxGeometry(68, 0.25, 5.0),
      new THREE.MeshLambertMaterial({ map: launchTex })
    );
    launchStrip.position.set(0, 0.12, -14);
    launchStrip.receiveShadow = true;
    scene.add(launchStrip);

    const launchBase = new THREE.Mesh(
      new THREE.BoxGeometry(68.4, 0.15, 5.25),
      new THREE.MeshLambertMaterial({ color: 0xb65010 })
    );
    launchBase.position.set(0, 0.075, -14);
    scene.add(launchBase);

    // Bright boundary rails make the launch strip readable at a distance.
    [-16.6, -11.4].forEach(stripZ => {
      const neonBorder = new THREE.Mesh(
        new THREE.BoxGeometry(68.2, 0.14, 0.32),
        new THREE.MeshBasicMaterial({ color: 0xfff4b3, toneMapped: false })
      );
      neonBorder.position.set(0, 0.16, stripZ);
      scene.add(neonBorder);
    });

    // Yellow Floating Down-Arrow Marker at Launch Line
    const launchArrowMesh = new THREE.Mesh(
      new THREE.ConeGeometry(0.95, 1.8, 4),
      new THREE.MeshBasicMaterial({ color: 0xfacc15 })
    );
    launchArrowMesh.rotation.x = Math.PI;
    launchArrowMesh.position.set(0, 4.2, -14);
    scene.add(launchArrowMesh);

    // 3) 3D Sinusoidal Launch Ramp & Tangent Arrow at Launch Line
    const rampGroup = new THREE.Group();
    rampGroup.position.set(0, 0.2, -14.5);
    scene.add(rampGroup);

    const rampArrow = new THREE.ArrowHelper(
      new THREE.Vector3(0, 0.707, -0.707).normalize(),
      new THREE.Vector3(0, 1.4, 0),
      5.8,
      0xfde047,
      1.4,
      0.9
    );
    rampGroup.add(rampArrow);

    function update3DRampVisuals() {
      const ramp = evaluateRampCalculus(state.rampX0);
      const dir = new THREE.Vector3(0, Math.sin(ramp.angleRad), -Math.cos(ramp.angleRad)).normalize();
      rampArrow.setDirection(dir);
    }
    update3DRampVisuals();

    // 4) 3D LIVE TANGENT TRAJECTORY ARC IN THE WORLD
    const ARC_POINTS_COUNT = 80;
    const trajectoryPositions = new Float32Array(ARC_POINTS_COUNT * 3);
    const trajectoryGeo = new THREE.BufferGeometry();
    trajectoryGeo.setAttribute('position', new THREE.BufferAttribute(trajectoryPositions, 3));
    const trajectoryMat = new THREE.LineBasicMaterial({
      color: 0x38bdf8,
      linewidth: 3,
      transparent: true,
      opacity: 0.9
    });
    const trajectoryLineMesh = new THREE.Line(trajectoryGeo, trajectoryMat);
    scene.add(trajectoryLineMesh);

    function update3DTrajectoryArc() {
      if (state.activeZone !== 'throw' || state.activeThrow) {
        trajectoryLineMesh.visible = false;
        return;
      }
      trajectoryLineMesh.visible = true;
      const food = getEquippedFood();
      const calc = evaluateFoodCalculus(food, state.t);
      const ramp = evaluateRampCalculus(state.rampX0);
      const previewDist = Math.max(20, Math.pow(getTotalStrength(), 0.72) * food.distMult * (1 + Math.abs(calc.deriv) * 0.18) * ramp.angleEfficiency);
      const normDist = Math.min(1, Math.pow(previewDist / 5500, 0.48));
      const targetZ = -14 - normDist * 880;

      const posAttr = trajectoryGeo.attributes.position;
      const startX = playerGroup ? playerGroup.position.x : 0;
      const startY = 2.2;
      const startZ = -14;

      for (let i = 0; i < ARC_POINTS_COUNT; i++) {
        const p = i / (ARC_POINTS_COUNT - 1);
        const z = startZ + p * (targetZ - startZ);
        const waveArcY = startY + Math.sin(p * Math.PI) * (14 + ramp.slope * 5.2) + Math.sin(p * Math.PI * 4 + state.t * 3) * 0.7;
        posAttr.setXYZ(i, startX, waveArcY, z);
      }
      posAttr.needsUpdate = true;
      trajectoryMat.color.setHex(food.color);
    }

    // 5) EXPANDED Fenced Player Lawn Plot ("My Plot" - 42 units wide x 34 units deep, holds up to 20 pets!)
    const fenceMat = new THREE.MeshLambertMaterial({ color: 0xd97706 });
    function buildPlotFences() {
      const fenceGroup = new THREE.Group();
      const postGeo = new THREE.BoxGeometry(0.65, 2.4, 0.65);
      // Front and Back fence posts
      for (let x = -21; x <= 21; x += 3.5) {
        for (const z of [-2, 32]) {
          if (z === -2 && Math.abs(x) < 4.2) continue; // Entrance gap
          const post = new THREE.Mesh(postGeo, fenceMat);
          post.position.set(x, 1.2, z);
          fenceGroup.add(post);
        }
      }
      // Left and Right fence posts
      for (let z = -2; z <= 32; z += 3.4) {
        for (const x of [-21, 21]) {
          const post = new THREE.Mesh(postGeo, fenceMat);
          post.position.set(x, 1.2, z);
          fenceGroup.add(post);
        }
      }
      // Horizontal Rails
      const railFB = new THREE.Mesh(new THREE.BoxGeometry(42, 0.32, 0.25), fenceMat);
      railFB.position.set(0, 1.5, 32);
      fenceGroup.add(railFB);

      const railFrontL = new THREE.Mesh(new THREE.BoxGeometry(16.5, 0.32, 0.25), fenceMat);
      railFrontL.position.set(-12.5, 1.5, -2);
      const railFrontR = railFrontL.clone();
      railFrontR.position.x = 12.5;
      fenceGroup.add(railFrontL, railFrontR);

      const railL = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.32, 34), fenceMat);
      railL.position.set(-21, 1.5, 15);
      const railR = railL.clone();
      railR.position.x = 21;
      fenceGroup.add(railL, railR);

      // Entrance Gate Archway with Lanterns
      const archMat = new THREE.MeshLambertMaterial({ color: 0x92400e });
      const archL = new THREE.Mesh(new THREE.BoxGeometry(0.55, 4.2, 0.55), archMat);
      archL.position.set(-4.5, 2.1, -2);
      const archR = archL.clone();
      archR.position.x = 4.5;
      const archTop = new THREE.Mesh(new THREE.BoxGeometry(9.8, 0.5, 0.5), archMat);
      archTop.position.set(0, 4.2, -2);
      fenceGroup.add(archL, archR, archTop);

      scene.add(fenceGroup);
    }
    buildPlotFences();

    // 6) Build 3D Physical Stations: Pull-Up Bar, Blue Food Shop Stall, Red Sell Stall
    function createGlowingRing(x, z, colorHex) {
      const ringGeo = new THREE.RingGeometry(3.2, 3.8, 32);
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
        new THREE.BoxGeometry(5.8, 2.3, 3.4),
        new THREE.MeshLambertMaterial({ color: 0x92400e })
      );
      counter.position.y = 1.15;
      counter.castShadow = true;
      g.add(counter);

      const postGeo = new THREE.BoxGeometry(0.38, 5.2, 0.38);
      const postMat = new THREE.MeshLambertMaterial({ color: 0x78350f });
      [[-2.5, -1.4], [2.5, -1.4], [-2.5, 1.4], [2.5, 1.4]].forEach(([px, pz]) => {
        const p = new THREE.Mesh(postGeo, postMat);
        p.position.set(px, 2.6, pz);
        g.add(p);
      });

      for (let i = 0; i < 5; i++) {
        const stripe = new THREE.Mesh(
          new THREE.BoxGeometry(1.25, 0.65, 4.2),
          new THREE.MeshLambertMaterial({ color: i % 2 === 0 ? roofColor1 : roofColor2 })
        );
        stripe.position.set(-2.5 + i * 1.25, 5.2, 0);
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
    const barPostGeo = new THREE.BoxGeometry(0.55, 5.5, 0.55);
    const barPostMat = new THREE.MeshLambertMaterial({ color: 0x92400e });
    const leftPost = new THREE.Mesh(barPostGeo, barPostMat);
    leftPost.position.set(-2.2, 2.75, 0);
    const rightPost = new THREE.Mesh(barPostGeo, barPostMat);
    rightPost.position.set(2.2, 2.75, 0);
    const crossBar = new THREE.Mesh(
      new THREE.CylinderGeometry(0.16, 0.16, 4.8, 16),
      new THREE.MeshLambertMaterial({ color: 0xfde68a })
    );
    crossBar.rotation.z = Math.PI / 2;
    crossBar.position.set(0, 5.1, 0);
    pullUpGroup.add(leftPost, rightPost, crossBar);
    scene.add(pullUpGroup);
    createGlowingRing(STATIONS.pullup.x, STATIONS.pullup.z, 0x38bdf8);

    // 7) 6 EXPANSIVE 3D BIOME RUNWAY ZONES (76 UNITS WIDE, DOWN TO Z = -980)
    const RUNWAY_WIDTH = 76;
    const terrainColors = {
      forest: ['#45df0d', '#36c70a'], savanna: ['#e7be45', '#d4a63d'],
      desert: ['#ecac69', '#d79453'], jungle: ['#3bab56', '#31984b'],
      ocean: ['#3baabf', '#309bae'], mythical: ['#a977dc', '#9765cc']
    };
    const scenicBox = new THREE.BoxGeometry(1, 1, 1);
    const bark = new THREE.MeshLambertMaterial({ color: 0x98502d });
    const leaves = [0x2bac18, 0x4fca1d, 0x72d924].map(color => new THREE.MeshLambertMaterial({ color }));
    const moss = new THREE.MeshLambertMaterial({ color: 0x8ada28 });
    const stone = new THREE.MeshLambertMaterial({ color: 0x94acac });
    const cloudMaterial = new THREE.MeshLambertMaterial({ color: 0xf3fcff, fog: false });

    function scenicBlock(parent, material, x, y, z, w, h, d, castsShadow = false) {
      const mesh = new THREE.Mesh(scenicBox, material);
      mesh.position.set(x, y, z);
      mesh.scale.set(w, h, d);
      mesh.castShadow = castsShadow;
      mesh.receiveShadow = castsShadow;
      parent.add(mesh);
      return mesh;
    }

    function buildForestTree(x, y, z, variant, scale = 1) {
      const tree = new THREE.Group();
      tree.position.set(x, y, z);
      tree.rotation.y = variant * 0.83;
      tree.scale.setScalar(scale);
      scenicBlock(tree, bark, 0, 2.7, 0, 1.45, 5.4, 1.6, true);
      scenicBlock(tree, bark, 0.83, 4.1, -0.04, 0.7, 2.6, 0.7).rotation.z = -0.57;
      scenicBlock(tree, leaves[0], 0, 5.65, 0.1, 5.0, 1.9, 4.4, true);
      scenicBlock(tree, leaves[1], -0.7, 6.9, -0.4, 3.5, 2.0, 3.8, true);
      scenicBlock(tree, leaves[2], 0.87, 7.8, 0.3, 2.65, 1.65, 2.7, true);
      scene.add(tree);
    }

    // Broad cloud silhouettes above the cliffs keep a clear horizon for throwing.
    for (let i = 0; i < 10; i++) {
      const x = (i % 2 === 0 ? -1 : 1) * (37 + (i % 3) * 17);
      const y = 47 + (i % 4) * 7;
      const z = 15 - i * 97;
      scenicBlock(scene, cloudMaterial, x, y, z, 18, 2.1, 7.5);
      scenicBlock(scene, cloudMaterial, x + 2.5, y + 1.6, z - 0.8, 10, 2.2, 6.2);
    }

    BIOMES.forEach((b, idx) => {
      const length = Math.abs(b.zEnd - b.zStart);
      const zCenter = (b.zStart + b.zEnd) / 2;
      const [lightTile, darkTile] = terrainColors[b.id];
      const bTex = createStuddedTexture(lightTile, darkTile, 12, Math.max(1, Math.round(length / 6.4)));
      const plane = new THREE.Mesh(
        new THREE.PlaneGeometry(RUNWAY_WIDTH, length),
        new THREE.MeshLambertMaterial({ map: bTex })
      );
      plane.rotation.x = -Math.PI / 2;
      plane.position.set(0, 0.02, zCenter);
      plane.receiveShadow = true;
      scene.add(plane);

      // Transverse White Runway Lines every 25m & Center Dashed Line (from video)
      for (let z = b.zStart; z > b.zEnd; z -= 25) {
        const line = new THREE.Mesh(
          new THREE.BoxGeometry(RUNWAY_WIDTH * 0.9, 0.06, 0.45),
          new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.85 })
        );
        line.position.set(0, 0.05, z);
        scene.add(line);
      }

      // Monumental Gateway Arch spanning across the canyon at biome start
      if (idx > 0) {
        const archG = new THREE.Group();
        archG.position.set(0, 0, b.zStart);
        const colGeo = new THREE.BoxGeometry(3.5, 26, 3.5);
        const colMat = new THREE.MeshLambertMaterial({ color: 0x78350f });
        const leftCol = new THREE.Mesh(colGeo, colMat);
        leftCol.position.set(-RUNWAY_WIDTH / 2 + 3, 13, 0);
        const rightCol = new THREE.Mesh(colGeo, colMat);
        rightCol.position.set(RUNWAY_WIDTH / 2 - 3, 13, 0);
        const beamGeo = new THREE.BoxGeometry(RUNWAY_WIDTH - 2, 4.0, 4.5);
        const beamMat = new THREE.MeshLambertMaterial({ color: b.colorHex });
        const beam = new THREE.Mesh(beamGeo, beamMat);
        beam.position.set(0, 26, 0);
        archG.add(leftCol, rightCol, beam);
        scene.add(archG);
      }

      if (b.id === 'forest') {
        for (let i = 0, z = b.zStart - 7; z > b.zEnd + 4; i++, z -= 14) {
          for (const side of [-1, 1]) {
            const x = side * (29 + (i % 3) * 2);
            const stagger = side === 1 ? 4 : 0;
            buildForestTree(x, 0, z + stagger, i + side, 0.84 + (i % 3) * 0.16);
            const rockX = side * (23 + (i % 3) * 1.6);
            scenicBlock(scene, stone, rockX, 0.42, z + 5 + stagger, 1.8, 0.84, 1.4).rotation.y = i * 0.7;
            scenicBlock(scene, moss, rockX + 0.1, 0.89, z + 5 + stagger, 1.45, 0.16, 1.1);
            scenicBlock(scene, leaves[1], x - side * 2, 0.68, z - 3 + stagger, 0.46, 1.3, 0.48).rotation.z = side * 0.19;
          }
        }
      }

      // Savanna: Umbrella Acacia Trees & Termite Mounds
      if (b.id === 'savanna') {
        for (let z = b.zStart - 10; z > b.zEnd + 10; z -= 24) {
          [-30, 30].forEach(xSide => {
            const trunk = new THREE.Mesh(new THREE.BoxGeometry(1.6, 6.5, 1.6), new THREE.MeshLambertMaterial({ color: 0x78350f }));
            trunk.position.set(xSide, 3.25, z);
            const canopy = new THREE.Mesh(new THREE.BoxGeometry(8.5, 1.8, 8.5), new THREE.MeshLambertMaterial({ color: 0xca8a04 }));
            canopy.position.set(xSide, 7.2, z);
            scene.add(trunk, canopy);
          });
          const mound = new THREE.Mesh(new THREE.ConeGeometry(1.8, 4.5, 6), new THREE.MeshLambertMaterial({ color: 0xb45309 }));
          mound.position.set((z % 2 === 0 ? -20 : 20), 2.25, z + 8);
          scene.add(mound);
        }
      }

      // Desert: GIANT DINOSAUR RIBCAGE SKELETONS, Skull Fossils, Cacti & Oasis Pools (from video!)
      if (b.id === 'desert') {
        // Giant Ribcage Skeleton arching across runway (exact match to video screenshot!)
        const ribG = new THREE.Group();
        ribG.position.set(-20, 0, (b.zStart + b.zEnd) / 2);
        const boneMat = new THREE.MeshLambertMaterial({ color: 0xf1f5f9 });
        for (let i = -3; i <= 3; i++) {
          const ribL = new THREE.Mesh(new THREE.BoxGeometry(0.9, 9.5, 0.9), boneMat);
          ribL.position.set(-3.5, 4.8, i * 2.2);
          ribL.rotation.z = -0.35;
          const ribR = new THREE.Mesh(new THREE.BoxGeometry(0.9, 9.5, 0.9), boneMat);
          ribR.position.set(3.5, 4.8, i * 2.2);
          ribR.rotation.z = 0.35;
          const spine = new THREE.Mesh(new THREE.BoxGeometry(1.4, 1.4, 2.4), boneMat);
          spine.position.set(0, 9.2, i * 2.2);
          ribG.add(ribL, ribR, spine);
        }
        scene.add(ribG);

        // Oasis Pool with Stone Rim & Palm Trees
        const oasisG = new THREE.Group();
        oasisG.position.set(22, 0, (b.zStart + b.zEnd) / 2 + 15);
        const water = new THREE.Mesh(new THREE.BoxGeometry(11, 0.2, 11), new THREE.MeshLambertMaterial({ color: 0x0284c7 }));
        water.position.y = 0.1;
        const rim = new THREE.Mesh(new THREE.BoxGeometry(12.5, 0.4, 12.5), new THREE.MeshLambertMaterial({ color: 0x78716c }));
        rim.position.y = 0.15;
        oasisG.add(rim, water);
        scene.add(oasisG);
      }

      // Jungle: Segmented Bamboo Groves & Mossy Aztec Pillars
      if (b.id === 'jungle') {
        for (let z = b.zStart - 12; z > b.zEnd + 12; z -= 26) {
          [-28, 28].forEach(xSide => {
            // Bamboo cluster
            for (let bIdx = -2; bIdx <= 2; bIdx++) {
              const bamboo = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 12, 8), new THREE.MeshLambertMaterial({ color: 0x16a34a }));
              bamboo.position.set(xSide + bIdx * 1.1, 6, z + (bIdx % 2) * 1.1);
              scene.add(bamboo);
            }
          });
        }
      }

      // Ocean: Multi-Color Coral Reef Formations & Glowing Crystals
      if (b.id === 'ocean') {
        for (let z = b.zStart - 14; z > b.zEnd + 14; z -= 28) {
          [-28, 28].forEach((xSide, i) => {
            const coral = new THREE.Mesh(new THREE.BoxGeometry(4.5, 7.5, 4.5), new THREE.MeshLambertMaterial({ color: i % 2 === 0 ? 0xec4899 : 0x06b6d4 }));
            coral.position.set(xSide, 3.75, z);
            scene.add(coral);
          });
        }
      }

      // Mythical: Glowing Crystalline Monoliths Pulsating with Calculus Runes
      if (b.id === 'mythical') {
        for (let z = b.zStart - 16; z > b.zEnd + 16; z -= 32) {
          [-28, 28].forEach(xSide => {
            const mono = new THREE.Mesh(new THREE.OctahedronGeometry(4.2, 0), new THREE.MeshLambertMaterial({ color: 0xc084fc, emissive: 0x4a044e }));
            mono.position.set(xSide, 8, z);
            scene.add(mono);
          });
        }
      }
    });

    // Each cliff face has its own world-scale UVs so the studs stay square.
    const dirtTex = createStuddedTexture('#94623f', '#795031', 1, 1);
    const cliffGrass = createStuddedTexture('#50da11', '#3bc50e', 1, 1);
    const wallMat = new THREE.MeshLambertMaterial({ map: dirtTex });
    const grassMat = new THREE.MeshLambertMaterial({ map: cliffGrass });
    function cliffBlock(x, y, z, w, h, d, material, receiveShadow = false) {
      const geo = new THREE.BoxGeometry(w, h, d);
      const uv = geo.attributes.uv;
      [[d,h], [d,h], [w,d], [w,d], [w,h], [w,h]].forEach(([width, height], face) => {
        for (let i = face * 4; i < face * 4 + 4; i++) {
          uv.setXY(i, uv.getX(i) * width / 5.6, uv.getY(i) * height / 5.6);
        }
      });
      const mesh = new THREE.Mesh(geo, material);
      mesh.position.set(x, y, z);
      mesh.receiveShadow = receiveShadow;
      scene.add(mesh);
    }

    for (const side of [-1, 1]) {
      cliffBlock(side * 47, 8.5, -523, 18, 17, 946, wallMat, true);
      cliffBlock(side * 47, 17.8, -523, 19, 1.65, 946, grassMat);
      cliffBlock(side * 67, 15, -480, 22, 30, 1050, wallMat);
      cliffBlock(side * 67, 30.9, -480, 23, 1.8, 1050, grassMat);

      for (let i = 0, z = -55; z > -978; i++, z -= 11) {
        const drop = [1.8, 3.1, 1.15, 2.25, 0.75][(i + (side === 1 ? 2 : 0)) % 5];
        cliffBlock(side * 38, 17.35 - drop / 2, z, 2.15, drop, 2.7 + (i % 3) * 1.3, grassMat);
      }
      for (let i = 0; i < 10; i++) {
        const z = -43 - i * 18;
        buildForestTree(side * (47 + i % 3), 18.625, z, i + side, 0.67 + i % 3 * 0.1);
      }
    }

    // 9) MOUNTED CANYON WALL 3D "LUCKIEST CATCHES - YOUR BEST RECORDS" BILLBOARD
    const luckiestBoardCanvas = document.createElement('canvas');
    luckiestBoardCanvas.width = 768;
    luckiestBoardCanvas.height = 640;
    const luckiestBoardTex = new THREE.CanvasTexture(luckiestBoardCanvas);

    const luckiestBoardGroup = new THREE.Group();
    luckiestBoardGroup.position.set(-37.5, 10.5, -14);
    luckiestBoardGroup.rotation.y = Math.PI / 2;

    const boardFrame = new THREE.Mesh(
      new THREE.BoxGeometry(12.5, 10.5, 0.45),
      new THREE.MeshLambertMaterial({ color: 0x111827 })
    );
    const boardBorder = new THREE.Mesh(
      new THREE.BoxGeometry(12.9, 10.9, 0.4),
      new THREE.MeshLambertMaterial({ color: 0xfacc15 })
    );
    boardBorder.position.z = -0.05;
    luckiestBoardGroup.add(boardFrame, boardBorder);

    const boardFace = new THREE.Mesh(
      new THREE.PlaneGeometry(12.2, 10.0),
      new THREE.MeshBasicMaterial({ map: luckiestBoardTex })
    );
    boardFace.position.z = 0.25;
    luckiestBoardGroup.add(boardFace);
    scene.add(luckiestBoardGroup);

    function update3DLuckiestBoardTexture() {
      const ctx = luckiestBoardCanvas.getContext('2d');
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(0, 0, 768, 640);

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

    // 10) 3D MOVING CALCULUS SKILL SHOT TARGETS IN THE CANYON
    const critRingGroup = new THREE.Group();
    critRingGroup.position.set(0, 7.5, -110);
    const critRingMesh = new THREE.Mesh(
      new THREE.TorusGeometry(4.5, 0.55, 16, 32),
      new THREE.MeshBasicMaterial({ color: 0xfacc15 })
    );
    critRingGroup.add(critRingMesh);
    scene.add(critRingGroup);

    const surgeGateGroup = new THREE.Group();
    surgeGateGroup.position.set(0, 0, -240);
    const gatePostGeo = new THREE.BoxGeometry(1.0, 16, 1.0);
    const gateMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });
    const gateL = new THREE.Mesh(gatePostGeo, gateMat);
    gateL.position.set(-8, 8, 0);
    const gateR = new THREE.Mesh(gatePostGeo, gateMat);
    gateR.position.set(8, 8, 0);
    const gateTop = new THREE.Mesh(new THREE.BoxGeometry(17.6, 1.0, 1.0), gateMat);
    gateTop.position.set(0, 16, 0);
    surgeGateGroup.add(gateL, gateR, gateTop);
    scene.add(surgeGateGroup);

    const targetLabels = [
      { pos: new THREE.Vector3(0, 12.8, -110), text: "🎯 CRITICAL POINT RING: P'(t) ≈ 0 (5x-25x Mutation!)", color: '#facc15' },
      { pos: new THREE.Vector3(0, 17.5, -240), text: "⚡ MAX VELOCITY GATE: |P'(t)| = MAX (+30% Range!)", color: '#38bdf8' }
    ];
    targetLabels.forEach(tl => {
      const el = document.createElement('div');
      el.className = 'absolute -translate-x-1/2 -translate-y-full text-center pointer-events-none font-black text-[11px] rblx-stroke-sm';
      el.style.color = tl.color;
      el.textContent = tl.text;
      document.getElementById('labelsContainer').appendChild(el);
      tl.el = el;
    });

    // Shoulder and hip pivots let the block avatar actually swing its limbs.
    const playerGroup = new THREE.Group();
    const playerRig = new THREE.Group();
    const skin = new THREE.MeshLambertMaterial({ color: 0xffcd95 });
    const jacket = new THREE.MeshLambertMaterial({ color: 0x178fff });
    const jacketLight = new THREE.MeshLambertMaterial({ color: 0x65c4ff });
    const trousers = new THREE.MeshLambertMaterial({ color: 0x283d71 });
    const soles = new THREE.MeshLambertMaterial({ color: 0x17233a });
    const hat = new THREE.MeshLambertMaterial({ color: 0xe92f3d });
    const faceInk = new THREE.MeshBasicMaterial({ color: 0x24263a });

    const torsoMesh = new THREE.Group();
    torsoMesh.position.y = 1.9;
    scenicBlock(torsoMesh, jacket, 0, 0, 0, 1.5, 1.52, 0.86, true);
    scenicBlock(torsoMesh, jacketLight, 0, -0.04, 0.445, 0.12, 1.2, 0.04);
    scenicBlock(torsoMesh, jacketLight, 0, 0.59, 0.17, 1.02, 0.22, 0.62);

    const head = new THREE.Group();
    head.position.y = 1.29;
    scenicBlock(head, skin, 0, 0, 0, 1.06, 0.99, 1.0, true);
    scenicBlock(head, hat, 0, 0.47, 0, 1.18, 0.24, 1.08, true);
    scenicBlock(head, hat, 0, 0.34, 0.44, 1.21, 0.12, 0.7);
    for (const x of [-0.2, 0.2]) {
      scenicBlock(head, faceInk, x, 0.02, 0.514, 0.10, 0.14, 0.035);
    }
    scenicBlock(head, faceInk, 0, -0.2, 0.515, 0.23, 0.055, 0.035);
    torsoMesh.add(head);

    function buildArm(side) {
      const arm = new THREE.Group();
      arm.position.set(side * 1.01, 0.51, 0);
      scenicBlock(arm, jacket, 0, -0.38, 0, 0.51, 0.96, 0.58, true);
      scenicBlock(arm, jacketLight, 0, -0.81, 0, 0.51, 0.12, 0.58);
      scenicBlock(arm, skin, 0, -1.02, 0, 0.45, 0.32, 0.48, true);
      torsoMesh.add(arm);
      return arm;
    }

    function buildLeg(side) {
      const leg = new THREE.Group();
      leg.position.set(side * 0.39, 1.19, 0);
      scenicBlock(leg, trousers, 0, -0.43, 0, 0.66, 0.94, 0.65, true);
      scenicBlock(leg, soles, 0, -1.04, 0.13, 0.69, 0.29, 0.94, true);
      playerRig.add(leg);
      return leg;
    }

    const leftArm = buildArm(-1);
    const rightArm = buildArm(1);
    const leftLeg = buildLeg(-1);
    const rightLeg = buildLeg(1);
    const heldFoodMesh = new THREE.Group();
    heldFoodMesh.position.set(0, -1.01, 0.52);
    heldFoodMesh.scale.setScalar(0.58);
    rightArm.add(heldFoodMesh);
    playerRig.add(torsoMesh);
    playerGroup.add(playerRig);
    playerGroup.position.set(state.playerPos.x, 0, state.playerPos.z);
    playerGroup.rotation.y = Math.PI;
    scene.add(playerGroup);

    // Bait pieces share geometry and are cloned for the hand, flight and reveal.
    const foodModels = new Map();
    function getFoodModel(food) {
      if (foodModels.has(food.id)) return foodModels.get(food.id);
      const foodModel = new THREE.Group();
      const body = new THREE.MeshLambertMaterial({ color: food.color });
      const leaf = new THREE.MeshLambertMaterial({ color: 0x318b30 });
      const stem = new THREE.MeshLambertMaterial({ color: 0x7b4a28 });
      const accent = new THREE.MeshLambertMaterial({ color: new THREE.Color(food.color).multiplyScalar(0.77) });
      const block = (material, x, y, z, w, h, d) => scenicBlock(foodModel, material, x, y, z, w, h, d, true);

      switch (food.id) {
        case 'carrot':
          block(body, 0, 0.23, 0.12, 0.48, 0.46, 0.88);
          block(body, 0, 0.19, -0.43, 0.33, 0.35, 0.45);
          block(accent, 0, 0.14, -0.71, 0.2, 0.25, 0.21);
          block(leaf, 0, 0.26, 0.75, 0.19, 0.17, 0.37);
          block(leaf, -0.13, 0.31, 0.92, 0.17, 0.16, 0.35).rotation.y = 0.53;
          block(leaf, 0.13, 0.31, 0.92, 0.17, 0.16, 0.35).rotation.y = -0.53;
          break;
        case 'apple':
        case 'orange':
        case 'pear': {
          const pear = food.id === 'pear';
          block(body, 0, 0.45, 0, 0.9, 0.63, 0.82);
          block(accent, 0, 0.15, 0, 0.68, 0.27, 0.66);
          block(body, 0, 0.78, 0, pear ? 0.57 : 0.72, pear ? 0.47 : 0.24, 0.67);
          const stemY = pear ? 1.07 : 0.9;
          block(stem, 0.03, stemY, 0.01, 0.12, 0.31, 0.12).rotation.z = -0.2;
          block(leaf, 0.22, stemY + 0.1, 0, 0.36, 0.12, 0.25).rotation.z = 0.43;
          break;
        }
        case 'banana':
          for (let i = -2; i <= 2; i++) {
            block(i % 2 ? body : accent, 0, 0.17 + i * i * 0.067, i * 0.25, 0.32, 0.39, 0.4).rotation.x = i * 0.28;
          }
          block(stem, 0, 0.46, 0.7, 0.16, 0.18, 0.2);
          break;
        case 'toast': {
          const crumb = new THREE.MeshLambertMaterial({ color: 0xfdd896 });
          block(accent, 0, 0.13, 0, 0.85, 0.26, 1.06);
          block(crumb, 0, 0.265, 0, 0.7, 0.06, 0.86);
          block(body, 0, 0.17, -0.48, 0.97, 0.32, 0.32);
          break;
        }
        case 'lobster':
          block(body, 0, 0.3, 0, 0.48, 0.51, 0.93);
          block(accent, 0, 0.2, 0.66, 0.65, 0.28, 0.4);
          for (const side of [-1, 1]) {
            block(accent, side * 0.37, 0.24, -0.23, 0.4, 0.22, 0.22);
            block(body, side * 0.52, 0.3, -0.52, 0.38, 0.34, 0.51).rotation.y = side * 0.22;
          }
          break;
      }

      foodModels.set(food.id, foodModel);
      return foodModel;
    }

    function setFoodModel(holder, food) {
      if (holder.userData.foodId === food.id) return;
      holder.clear();
      holder.add(getFoodModel(food).clone());
      holder.userData.foodId = food.id;
    }

    // 12) 3D VOXEL ANIMAL GENERATOR & LAWN PLOT PET SYNC
    const plotPetsGroup = new THREE.Group();
    scene.add(plotPetsGroup);
    let activePlotPetEntities = [];

    function createBlockyAnimalMesh(animal, size, mutation) {
      if (!animal) return new THREE.Group();
      const g = new THREE.Group();
      const sizeMult = size ? size.scale : 1.0;
      const mutBoost = (mutation && mutation.mult >= 5) ? 1.15 : 1.0;
      const s = (animal.scale || 1.0) * sizeMult * mutBoost;

      return buildDedicatedAnimalModel(animal.id, g, s, animal, size, mutation);
    }

    function sync3DPlotPets() {
      while (plotPetsGroup.children.length > 0) {
        disposePolishedAnimal(plotPetsGroup.children[0]);
      }
      activePlotPetEntities.forEach(ent => ent.labelEl && ent.labelEl.remove());
      activePlotPetEntities = [];

      if (!state.settings.viewYourPets) return;

      const equippedPets = state.inventory.filter(i => i.equipped);
      const labelsRoot = document.getElementById('labelsContainer');

      // Distribute up to 20 pets across the spacious 42x34 lawn plot!
      const cols = 5;
      equippedPets.forEach((pet, idx) => {
        const animal = ANIMALS.find(a => a.id === pet.animalId);
        if (!animal) return;
        const mesh = createBlockyAnimalMesh(animal, pet.size, pet.mutation);
        const px = -15 + (idx % cols) * 7.5 + (Math.random() - 0.5) * 1.5;
        const pz = 2.5 + Math.floor(idx / cols) * 6.5 + (Math.random() - 0.5) * 1.5;
        mesh.position.set(px, 0, pz);
        plotPetsGroup.add(mesh);

        const labelEl = document.createElement('div');
        labelEl.className = 'absolute -translate-x-1/2 -translate-y-full text-center pointer-events-none leading-tight';
        const sizeTag = pet.size && pet.size.id !== 'regular' ? `[${pet.size.name.toUpperCase()}] ` : '';
        labelEl.innerHTML = `
          <div class="text-[11px] font-extrabold text-white rblx-stroke-sm">${animal.emoji} ${sizeTag}${animal.name}</div>
          <div class="text-[10px] font-extrabold rblx-stroke-sm" style="color:${pet.mutation.color}">
            ${pet.mutation.name.split('•').pop().trim()} +$${formatNum(pet.income)}/s
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

        const pos = ent.mesh.position.clone().add(new THREE.Vector3(0, 3.4, 0));
        project3DToScreen(pos, cashPopup);

        setTimeout(() => cashPopup.remove(), 1250);
      });
    }

    // 13) THROW PROJECTILE & CUTSCENE SHOWCASE WITH BEACON AND CONFETTI
    const projectileGroup = new THREE.Group();
    projectileGroup.visible = false;
    scene.add(projectileGroup);

    const cutsceneGroup = new THREE.Group();
    cutsceneGroup.visible = false;
    scene.add(cutsceneGroup);

    // Glowing Particle Aura Beacon Cylinder for Cutscene
    const beaconGeo = new THREE.CylinderGeometry(2.5, 2.5, 24, 16, 1, true);
    const beaconMat = new THREE.MeshBasicMaterial({
      color: 0xfacc15,
      transparent: true,
      opacity: 0.16,
      depthWrite: false,
      side: THREE.DoubleSide
    });
    const cutsceneBeacon = new THREE.Mesh(beaconGeo, beaconMat);
    cutsceneBeacon.position.y = 12;
    cutsceneGroup.add(cutsceneBeacon);

    // Confetti particles for cutscene explosion
    const CONFETTI_COUNT = 32;
    const confettiGeometry = new THREE.PlaneGeometry(0.23, 0.23);
    const confettiGroup = new THREE.Group();
    const confettiMeshes = [];
    const confettiColors = [0xef4444, 0x3b82f6, 0x10b981, 0xfacc15, 0xec4899, 0xa855f7];
    for (let i = 0; i < CONFETTI_COUNT; i++) {
      const cMesh = new THREE.Mesh(
        confettiGeometry,
        new THREE.MeshBasicMaterial({ color: confettiColors[i % confettiColors.length], side: THREE.DoubleSide })
      );
      cMesh.userData = {
        vy: -2 - Math.random() * 4,
        vx: (Math.random() - 0.5) * 5,
        vz: (Math.random() - 0.5) * 5,
        rotSpeed: Math.random() * 10
      };
      confettiMeshes.push(cMesh);
      confettiGroup.add(cMesh);
    }
    cutsceneGroup.add(confettiGroup);

    // Station Floating 3D Labels
    const stationLabels = [];
    function initStationLabels() {
      const labelsRoot = document.getElementById('labelsContainer');
      const list = [
        { key: 'throw',  pos: new THREE.Vector3(0, 5.2, -14),   text: '🎯 LAUNCH LINE (STEP HERE TO THROW)', color: '#fde047' },
        { key: 'pullup', pos: new THREE.Vector3(-24, 6.2, 6),   text: '🏋️ PULL-UP WORKOUT (CHAIN RULE)', color: '#38bdf8' },
        { key: 'shop',   pos: new THREE.Vector3(-24, 6.2, -8),  text: '🛒 FOOD SHOP STALL', color: '#60a5fa' },
        { key: 'sell',   pos: new THREE.Vector3(24, 6.2, -6),   text: '💰 SELL STALL', color: '#f87171' },
        { key: 'plot',   pos: new THREE.Vector3(0, 5.0, -2),    text: '🏡 MY LAWN PLOT (MAX 20 PETS)', color: '#4ade80' }
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
