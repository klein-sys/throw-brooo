# -*- coding: utf-8 -*-

JS_GAMEPLAY = """
    /*************************************************************************
     * 6. CONTROLS, CAMERA ORBIT & VIRTUAL JOYSTICK
     *************************************************************************/
    const keys = {};
    let camYaw = 0;
    let camPitch = 0.32;
    let isDraggingCam = false;
    let lastMouseX = 0;
    let lastMouseY = 0;

    window.addEventListener('keydown', e => {
      keys[e.key.toLowerCase()] = true;
      if (e.code === 'Space') {
        if (state.activeThrow && state.activeThrow.phase === 'reveal') {
          e.preventDefault();
          skipThrowAnimation();
        } else if (state.activeZone === 'throw') {
          e.preventDefault();
          executeCalculusThrow();
        } else if (state.activeZone === 'pullup') {
          e.preventDefault();
          doCalculusPullUpRep();
        }
      }
    });
    window.addEventListener('keyup', e => {
      keys[e.key.toLowerCase()] = false;
    });

    // Mouse Drag Camera Orbit
    window.addEventListener('mousedown', e => {
      if (e.target.closest('button, input, select, #joystickZone, .pointer-events-auto')) return;
      isDraggingCam = true;
      lastMouseX = e.clientX;
      lastMouseY = e.clientY;
    });
    window.addEventListener('mousemove', e => {
      if (!isDraggingCam) return;
      const dx = e.clientX - lastMouseX;
      const dy = e.clientY - lastMouseY;
      lastMouseX = e.clientX;
      lastMouseY = e.clientY;
      camYaw -= dx * 0.005;
      camPitch = Math.max(0.08, Math.min(1.2, camPitch + dy * 0.005));
    });
    window.addEventListener('mouseup', () => { isDraggingCam = false; });

    // Touch Drag Camera Orbit
    let touchStartCamX = 0;
    let touchStartCamY = 0;
    window.addEventListener('touchstart', e => {
      if (e.target.closest('button, input, #joystickZone, .pointer-events-auto')) return;
      if (e.touches.length === 1) {
        touchStartCamX = e.touches[0].clientX;
        touchStartCamY = e.touches[0].clientY;
      }
    }, { passive: true });
    window.addEventListener('touchmove', e => {
      if (e.target.closest('button, input, #joystickZone, .pointer-events-auto')) return;
      if (e.touches.length === 1) {
        const dx = e.touches[0].clientX - touchStartCamX;
        const dy = e.touches[0].clientY - touchStartCamY;
        touchStartCamX = e.touches[0].clientX;
        touchStartCamY = e.touches[0].clientY;
        camYaw -= dx * 0.006;
        camPitch = Math.max(0.08, Math.min(1.2, camPitch + dy * 0.006));
      }
    }, { passive: true });

    // Virtual Touch Joystick
    let joystickActive = false;
    let joystickDir = { x: 0, y: 0 };
    const joyZone = document.getElementById('joystickZone');
    const joyKnob = document.getElementById('joystickKnob');

    function handleJoystickMove(clientX, clientY) {
      const rect = joyZone.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const dx = clientX - cx;
      const dy = clientY - cy;
      const dist = Math.hypot(dx, dy);
      const maxR = rect.width / 2;
      const clampedDist = Math.min(dist, maxR);
      const angle = Math.atan2(dy, dx);
      const nx = Math.cos(angle) * (clampedDist / maxR);
      const ny = Math.sin(angle) * (clampedDist / maxR);
      joystickDir = { x: nx, y: ny };
      joyKnob.style.transform = `translate(${nx * maxR}px, ${ny * maxR}px)`;
    }

    function resetJoystick() {
      joystickActive = false;
      joystickDir = { x: 0, y: 0 };
      joyKnob.style.transform = `translate(0px, 0px)`;
    }

    joyZone.addEventListener('touchstart', e => {
      joystickActive = true;
      handleJoystickMove(e.touches[0].clientX, e.touches[0].clientY);
    }, { passive: true });
    joyZone.addEventListener('touchmove', e => {
      if (!joystickActive) return;
      handleJoystickMove(e.touches[0].clientX, e.touches[0].clientY);
    }, { passive: true });
    joyZone.addEventListener('touchend', resetJoystick, { passive: true });
    joyZone.addEventListener('touchcancel', resetJoystick, { passive: true });

    function walkToStation(stationKey) {
      audio.playClickSound();
      const st = STATIONS[stationKey];
      if (!st) return;
      state.playerPos.x = st.x;
      state.playerPos.z = st.z;
      playerGroup.position.set(st.x, 0, st.z);
      checkZoneTrigger();
    }

    /*************************************************************************
     * 7. PLAYER MOVEMENT & ZONE INTERACTION ENGINE
     *************************************************************************/
    let walkCycle = 0;
    function updatePlayerMovement(dt) {
      if (state.activeThrow || state.isPullingUp) return;

      let mx = 0;
      let mz = 0;

      if (keys['w'] || keys['arrowup']) mz -= 1;
      if (keys['s'] || keys['arrowdown']) mz += 1;
      if (keys['a'] || keys['arrowleft']) mx -= 1;
      if (keys['d'] || keys['arrowright']) mx += 1;

      if (joystickActive) {
        mx = joystickDir.x;
        mz = joystickDir.y;
      }

      const len = Math.hypot(mx, mz);
      if (len > 0.05) {
        const moveSpeed = 16.5;
        const sinY = Math.sin(camYaw);
        const cosY = Math.cos(camYaw);
        const forwardX = -sinY;
        const forwardZ = -cosY;
        const rightX = cosY;
        const rightZ = -sinY;

        const vx = (rightX * mx + forwardX * (-mz)) / (len > 1 ? len : 1);
        const vz = (rightZ * mx + forwardZ * (-mz)) / (len > 1 ? len : 1);

        state.playerPos.x += vx * moveSpeed * dt;
        state.playerPos.z += vz * moveSpeed * dt;

        // Boundaries of the expanded hub ground
        state.playerPos.x = Math.max(-50, Math.min(50, state.playerPos.x));
        state.playerPos.z = Math.max(-20, Math.min(60, state.playerPos.z));

        playerGroup.position.set(state.playerPos.x, 0, state.playerPos.z);
        playerGroup.rotation.y = Math.atan2(vx, vz);

        walkCycle += dt * 14;
        leftLeg.rotation.x = Math.sin(walkCycle) * 0.7;
        rightLeg.rotation.x = -Math.sin(walkCycle) * 0.7;
        leftArm.rotation.x = -Math.sin(walkCycle) * 0.55;
        rightArm.rotation.x = Math.sin(walkCycle) * 0.55;
      } else {
        leftLeg.rotation.x = 0;
        rightLeg.rotation.x = 0;
        leftArm.rotation.x = 0;
        rightArm.rotation.x = 0;
      }

      checkZoneTrigger();
    }

    function checkZoneTrigger() {
      if (state.activeThrow || state.isPullingUp) return;

      let detectedZone = null;
      for (const [key, st] of Object.entries(STATIONS)) {
        const dist = Math.hypot(state.playerPos.x - st.x, state.playerPos.z - st.z);
        if (dist <= st.radius) {
          detectedZone = key;
          break;
        }
      }

      if (detectedZone !== state.activeZone) {
        state.activeZone = detectedZone;
        onZoneChanged(detectedZone);
      }
    }

    function onZoneChanged(zone) {
      const banner = document.getElementById('zoneBanner');
      const icon = document.getElementById('zoneBannerIcon');
      const text = document.getElementById('zoneBannerText');
      const throwHUD = document.getElementById('throwZoneHUD');

      throwHUD.classList.add('hidden');
      throwHUD.classList.remove('flex');

      if (zone === 'throw') {
        icon.textContent = '🎯';
        text.textContent = 'Orange Checkered Launch Line! (Press SPACE or Click TAP TO THROW)';
        banner.className = 'fixed top-14 sm:top-16 left-1/2 -translate-x-1/2 z-20 transition-all duration-200 pointer-events-none pulse-glow';
        throwHUD.classList.remove('hidden');
        throwHUD.classList.add('flex');
        update3DTrajectoryArc();
      } else if (zone === 'pullup') {
        icon.textContent = '🏋️';
        text.textContent = 'Pull-Up Bar Station! Chain Rule Training Mode Active.';
        banner.className = 'fixed top-14 sm:top-16 left-1/2 -translate-x-1/2 z-20 transition-all duration-200 pointer-events-none';
        enterPullUpStation();
      } else if (zone === 'shop') {
        icon.textContent = '🛒';
        text.textContent = 'Food Shop Stall! Buy bait & expand lawn capacity.';
        banner.className = 'fixed top-14 sm:top-16 left-1/2 -translate-x-1/2 z-20 transition-all duration-200 pointer-events-none';
        openModal('shopModal');
      } else if (zone === 'sell') {
        icon.textContent = '💰';
        text.textContent = 'Sell Stall! Liquidate duplicate or unequipped pets.';
        banner.className = 'fixed top-14 sm:top-16 left-1/2 -translate-x-1/2 z-20 transition-all duration-200 pointer-events-none';
        openModal('sellModal');
      } else if (zone === 'plot') {
        icon.textContent = '🏡';
        text.textContent = `My Plot! ${state.inventory.filter(i => i.equipped).length}/${state.plotCapacity} pets roaming.`;
        banner.className = 'fixed top-14 sm:top-16 left-1/2 -translate-x-1/2 z-20 transition-all duration-200 pointer-events-none';
      } else {
        icon.textContent = '🏃';
        text.textContent = 'Walk to the Orange Checkered Launch Line to Throw Food!';
        banner.className = 'fixed top-14 sm:top-16 left-1/2 -translate-x-1/2 z-20 transition-all duration-200 pointer-events-none opacity-85';
      }
    }

    /*************************************************************************
     * 8. PULL-UP BAR CHAIN RULE WORKOUT (MATCHING SCREENSHOT 78)
     *************************************************************************/
    let pullUpRepTime = 0;
    function enterPullUpStation() {
      state.isPullingUp = true;
      state.playerPos.x = STATIONS.pullup.x;
      state.playerPos.z = STATIONS.pullup.z;
      playerGroup.position.set(STATIONS.pullup.x, 2.0, STATIONS.pullup.z);
      playerGroup.rotation.y = 0;

      leftArm.rotation.x = Math.PI;
      rightArm.rotation.x = Math.PI;

      document.getElementById('pullUpZoneHUD').classList.remove('hidden');
      document.getElementById('pullUpZoneHUD').classList.add('flex');
      renderPullUpHUD();
    }

    function exitPullUpStation() {
      state.isPullingUp = false;
      leftArm.rotation.x = 0;
      rightArm.rotation.x = 0;
      playerGroup.position.y = 0;
      document.getElementById('pullUpZoneHUD').classList.add('hidden');
      document.getElementById('pullUpZoneHUD').classList.remove('flex');
      state.playerPos.z += 5.5;
      playerGroup.position.set(state.playerPos.x, 0, state.playerPos.z);
      checkZoneTrigger();
    }

    function doCalculusPullUpRep() {
      if (!state.isPullingUp) return;
      const calc = evaluatePullUpCalculus(pullUpRepTime);
      const isPerfect = calc.isNearPeak;
      const xpGain = isPerfect ? 2 : 1;

      state.pullUpXp += xpGain;
      audio.playPullUpSound(isPerfect);

      showFloatingPopup(playerGroup.position, isPerfect ? '+2 XP (PERFECT VELOCITY!)' : '+1 XP', isPerfect ? '#facc15' : '#38bdf8');

      if (state.pullUpXp >= state.pullUpMaxXp) {
        state.pullUpXp = 0;
        state.pullUpLevel++;
        state.pullUpMaxXp = Math.round(state.pullUpMaxXp * 1.5);
        state.baseStrength += 5;
        audio.playLevelUpSound();
        showToast(`🎉 Pull-Up Level ${state.pullUpLevel}! Base Strength +5 💪`, 'bg-sky-400 text-black');
        checkNewFoodUnlock();
      }

      renderPullUpHUD();
      updateHUD();
      saveGame();
    }

    function renderPullUpHUD() {
      document.getElementById('pullUpLevelTitle').textContent = `Level ${state.pullUpLevel}`;
      document.getElementById('pullUpXpFraction').textContent = `${state.pullUpXp}/${state.pullUpMaxXp}`;
      const pct = (state.pullUpXp / state.pullUpMaxXp) * 100;
      document.getElementById('pullUpProgressBar').style.width = `${pct}%`;
    }

    /*************************************************************************
     * 9. HARMONIC THROW EXECUTION, REBALANCED DISTANCE & ODDS ENGINE
     *************************************************************************/
    let isThrowWindup = false;

    function executeCalculusThrow() {
      if (state.activeThrow || state.activeZone !== 'throw' || isThrowWindup) {
        if (state.activeZone !== 'throw') {
          showToast('🎯 Walk onto the Orange Checkered Launch Line to Throw!', 'bg-amber-400 text-black');
          walkToStation('throw');
        }
        return;
      }

      const food = getEquippedFood();
      const t0 = state.t;
      const calc = evaluateFoodCalculus(food, t0);
      const ramp = evaluateRampCalculus(state.rampX0);

      const absDeriv = Math.abs(calc.deriv);
      const derivRatio = absDeriv / (calc.maxDeriv || 1);

      const isCriticalPoint = food.type !== 'tan' && derivRatio <= 0.18;
      const isMaxDerivSurge = derivRatio >= 0.82;
      const surgeBonus = isMaxDerivSurge ? 1.30 : 1.0;

      // REBALANCED PROGRESSION FORMULA:
      // Distance strictly controlled by strength power 0.72 and food.distMult!
      // At 48 strength with Carrot, distance is ~29m (solidly within Forest: 0 - 120m).
      // Even with Apple, distance is ~55m (still in Forest).
      const rawDist = (Math.pow(getTotalStrength(), 0.72) * food.distMult) * (1 + absDeriv * 0.18) * ramp.angleEfficiency * surgeBonus;
      const distance = Math.max(16, rawDist);

      // Determine landing biome
      let landingBiome = BIOMES[0];
      for (const b of BIOMES) {
        if (distance >= b.minDist) landingBiome = b;
      }

      // Roll Animal from Landing Biome
      const biomeAnimals = ANIMALS.filter(a => a.biome === landingBiome.id);
      const weightedPool = biomeAnimals.map((a, idx) => {
        const boost = idx === 0 ? 1 : idx === 1 ? Math.pow(food.luck, 0.35) : Math.pow(food.luck, 0.65);
        return { animal: a, weight: a.weight * boost };
      });
      const totalW = weightedPool.reduce((s, i) => s + i.weight, 0);
      let r = Math.random() * totalW;
      let chosenAnimal = weightedPool[0].animal;
      for (const item of weightedPool) {
        if (r < item.weight) { chosenAnimal = item.animal; break; }
        r -= item.weight;
      }

      // Roll Animal Size based on probability chances
      let chosenSize = SIZES[0];
      const totalSizeWeight = SIZES.reduce((s, sz) => s + sz.weight, 0);
      let rSize = Math.random() * totalSizeWeight;
      for (const sz of SIZES) {
        if (rSize < sz.weight) { chosenSize = sz; break; }
        rSize -= sz.weight;
      }

      // Roll Mutation based on Critical Point Calculus condition
      let chosenMutation = MUTATIONS[0];
      if (isCriticalPoint) {
        const cr = Math.random();
        if (cr < 0.15) chosenMutation = MUTATIONS[4]; // Cosmic 25x
        else if (cr < 0.45) chosenMutation = MUTATIONS[3]; // Rainbow 10x
        else chosenMutation = MUTATIONS[2]; // Golden 5x
      } else {
        const sr = Math.random();
        if (sr < 0.05) chosenMutation = MUTATIONS[2]; // Golden 5x
        else if (sr < 0.25) chosenMutation = MUTATIONS[1]; // Silver 2x
      }

      // Calculate Combined Exact Catch Probability (1 in X)
      const totalOdds = Math.round(chosenAnimal.baseOdds * chosenSize.chanceNum * chosenMutation.chanceNum);
      const oddsDisplayStr = `1 in ${formatNum(totalOdds)}`;

      const finalIncome = Math.round(chosenAnimal.baseIncome * chosenSize.mult * chosenMutation.mult);
      const isNewDiscovery = !state.unlockedIndex.has(chosenAnimal.id);

      // Distance mapping to expanded 3D Z coordinate (-14 to -900)
      const normDist = Math.min(1, Math.pow(distance / 5500, 0.48));
      const targetZ = -14 - normDist * 880;

      // START DYNAMIC CHARACTER THROW ANIMATION (Anticipation -> Release)
      isThrowWindup = true;
      rightArm.rotation.x = -Math.PI * 0.7;
      rightArm.rotation.z = 0.35;
      torsoMesh.rotation.x = -0.22;

      // Floating readout on throw
      const readoutText = isMaxDerivSurge ? '⚡ MAX SURGE! +19 POWER' : isCriticalPoint ? '🎯 CRITICAL POINT!' : 'PERFECT!';
      const readoutColor = isMaxDerivSurge ? '#38bdf8' : isCriticalPoint ? '#facc15' : '#4ade80';
      showFloatingPopup(playerGroup.position, readoutText, readoutColor);

      setTimeout(() => {
        // Violently whip right arm forward & release food
        rightArm.rotation.x = Math.PI * 0.85;
        rightArm.rotation.z = -0.2;
        torsoMesh.rotation.x = 0.25;
        heldFoodMesh.visible = false;

        state.throwCount++;
        projectileMesh.material.color.setHex(food.color);
        projectileGroup.position.set(playerGroup.position.x, 2.4, -14);
        projectileGroup.visible = true;

        audio.playThrowSound(isMaxDerivSurge, isCriticalPoint);
        if (isMaxDerivSurge) triggerScreenShake();

        state.activeThrow = {
          phase: 'flying',
          progress: 0,
          distance,
          targetZ,
          landingBiome,
          chosenAnimal,
          chosenSize,
          chosenMutation,
          totalOdds,
          oddsDisplayStr,
          finalIncome,
          isNewDiscovery,
          isCriticalPoint,
          isMaxDerivSurge,
          t0,
          calc,
          ramp,
          food,
          revealTimer: 0,
          oddsRollTimer: 0,
          nameRevealStep: 0,
          chosenAnimalMesh: null
        };

        saveWorkedExampleTelemetry(state.activeThrow);
        recordPersonalBestCatch(state.activeThrow);

        // Auto-Skip repeat catches option
        if (!isNewDiscovery && state.autoSkipRepeats) {
          finalizeAnimalAward(state.activeThrow);
          projectileGroup.visible = false;
          state.activeThrow = null;
          isThrowWindup = false;
          rightArm.rotation.set(0, 0, 0);
          torsoMesh.rotation.set(0, 0, 0);
          heldFoodMesh.visible = true;
          showToast(`⚡ Auto-Skipped: Caught ${chosenSize.name} ${chosenMutation.name} ${chosenAnimal.name} ($${formatNum(finalIncome)}/s) [${oddsDisplayStr}] at ${distance.toFixed(1)}m!`, 'bg-lime-400 text-black');
          return;
        }

        document.getElementById('flightOverlay').classList.remove('hidden');
        document.getElementById('flightOverlay').classList.add('flex');
        document.getElementById('skipFlightBtn').style.display = isNewDiscovery ? 'none' : 'flex';

        setTimeout(() => {
          isThrowWindup = false;
          rightArm.rotation.set(0, 0, 0);
          torsoMesh.rotation.set(0, 0, 0);
          heldFoodMesh.visible = true;
        }, 250);

      }, 160);
    }

    function recordPersonalBestCatch(th) {
      if (!state.playerBestCatches) state.playerBestCatches = [];
      const entry = {
        id: th.chosenAnimal.id,
        name: th.chosenAnimal.name,
        emoji: th.chosenAnimal.emoji,
        size: th.chosenSize,
        mutation: th.chosenMutation,
        odds: th.totalOdds,
        distance: th.distance,
        income: th.finalIncome
      };

      state.playerBestCatches.push(entry);
      state.playerBestCatches.sort((a, b) => b.odds - a.odds);
      if (state.playerBestCatches.length > 5) {
        state.playerBestCatches = state.playerBestCatches.slice(0, 5);
      }
      update3DLuckiestBoardTexture();
    }

    function skipThrowAnimation() {
      if (!state.activeThrow) return;
      const th = state.activeThrow;
      finalizeAnimalAward(th);
      projectileGroup.visible = false;
      cutsceneGroup.visible = false;
      document.getElementById('flightOverlay').classList.add('hidden');
      document.getElementById('flightOverlay').classList.remove('flex');
      document.getElementById('catchRevealModal').classList.add('hidden');
      document.getElementById('catchRevealModal').classList.remove('flex');
      state.activeThrow = null;
      showToast(`🐾 Caught ${th.chosenSize.name} ${th.chosenMutation.name} ${th.chosenAnimal.name} (+$${formatNum(th.finalIncome)}/s)!`, 'bg-lime-400 text-black');
    }

    function transitionTo3DCatchCutscene(th) {
      th.phase = 'reveal';
      projectileGroup.visible = false;
      document.getElementById('flightOverlay').classList.add('hidden');
      document.getElementById('flightOverlay').classList.remove('flex');

      // Clear previous cutscene showcase models
      while (cutsceneGroup.children.length > 2) {
        cutsceneGroup.remove(cutsceneGroup.children[2]);
      }

      // Spawn Animal Mesh in front of thrown food
      const animalMesh = createBlockyAnimalMesh(th.chosenAnimal, th.chosenSize, th.chosenMutation);
      animalMesh.position.set(0, 0, th.targetZ);
      th.chosenAnimalMesh = animalMesh;

      // Spawn Thrown Food Bait on the ground right in front of the animal
      const bait = projectileMesh.clone();
      bait.position.set(0, 0.45, th.targetZ - 1.8);
      bait.scale.set(0.7, 0.7, 0.7);

      // Aura Beacon Cylinder positioned at target
      cutsceneBeacon.position.set(0, 12, th.targetZ);
      cutsceneBeacon.material.color.setHex(th.chosenMutation.hex || 0xfacc15);

      // Reset Confetti flakes around animal
      confettiMeshes.forEach(cm => {
        cm.position.set(
          (Math.random() - 0.5) * 14,
          8 + Math.random() * 12,
          th.targetZ + (Math.random() - 0.5) * 14
        );
      });

      cutsceneGroup.add(animalMesh, bait);
      cutsceneGroup.visible = true;

      // Setup Starburst Rays Color (Red for normal, Gold for golden, Purple for cosmic)
      const starburst = document.getElementById('cutsceneStarburst');
      starburst.className = 'starburst-rays ' + (th.chosenMutation.id === 'golden' ? 'gold' : th.chosenMutation.id === 'cosmic' ? 'cosmic' : '');

      // Setup Rarity Celebratory Header Banner
      const rarityHeader = document.getElementById('catchRarityHeader');
      if (th.chosenAnimal.rarity === 'Common') {
        rarityHeader.textContent = 'NICE CATCH!';
        rarityHeader.className = 'text-lime-400 font-black text-3xl sm:text-5xl rblx-stroke-lg tracking-wide transform -rotate-1 relative z-10 animate-bounce';
      } else if (th.chosenAnimal.rarity === 'Uncommon' || th.chosenAnimal.rarity === 'Rare') {
        rarityHeader.textContent = 'LUCKY!';
        rarityHeader.className = 'text-amber-400 font-black text-3xl sm:text-5xl rblx-stroke-lg tracking-wide transform -rotate-1 relative z-10 animate-bounce';
      } else if (th.chosenAnimal.rarity === 'Epic' || th.chosenAnimal.rarity === 'Legendary') {
        rarityHeader.textContent = 'SUPER LUCKY!';
        rarityHeader.className = 'text-rose-500 font-black text-3xl sm:text-5xl rblx-stroke-lg tracking-wide transform -rotate-1 relative z-10 animate-bounce';
      } else {
        rarityHeader.textContent = 'INSANE LUCK!';
        rarityHeader.className = 'text-purple-400 font-black text-3xl sm:text-5xl rblx-stroke-lg tracking-wide transform -rotate-1 relative z-10 animate-bounce';
      }

      // Initialize Suspense Rolling Odds Slot: Starts at "1 in 1" (Exact replication of video!)
      document.getElementById('catchOddsNumber').textContent = '1 in 1';

      // Initialize Mystery Hangman Name Reveal with underscores (Exact replication of video!)
      const animalNameUpper = th.chosenAnimal.name.toUpperCase();
      let blankStr = animalNameUpper.replace(/[A-Z]/g, '_ ');
      document.getElementById('catchAnimalName').textContent = blankStr;

      // Mutation & Size Tags
      const mutEl = document.getElementById('catchMutationTag');
      if (th.chosenMutation && th.chosenMutation.id !== 'normal') {
        mutEl.textContent = th.chosenMutation.name;
        mutEl.style.color = th.chosenMutation.color;
        mutEl.style.display = 'block';
      } else {
        mutEl.style.display = 'none';
      }

      const sizeEl = document.getElementById('catchSizeTag');
      sizeEl.textContent = th.chosenSize.name.toUpperCase();
      sizeEl.style.color = th.chosenSize.color;

      document.getElementById('catchIncomeRate').textContent = `+$${formatNum(th.finalIncome)}/s`;

      document.getElementById('catchRevealModal').classList.remove('hidden');
      document.getElementById('catchRevealModal').classList.add('flex');

      audio.playExplosionSound();
    }

    function finalizeAnimalAward(th) {
      state.unlockedIndex.add(th.chosenAnimal.id);
      const newPet = {
        uid: 'pet_' + Date.now() + '_' + Math.floor(Math.random() * 1000),
        animalId: th.chosenAnimal.id,
        size: th.chosenSize,
        mutation: th.chosenMutation,
        income: th.finalIncome,
        equipped: false
      };

      const currentEquipped = state.inventory.filter(i => i.equipped).length;
      if (currentEquipped < state.plotCapacity) {
        newPet.equipped = true;
      }
      state.inventory.push(newPet);

      sync3DPlotPets();
      updateHUD();
      checkNewFoodUnlock();
      saveGame();
    }

    function handleCatchRevealTap() {
      if (state.activeThrow && state.activeThrow.phase === 'reveal') {
        skipThrowAnimation();
      }
    }

    function toggleAutoSkipRepeats(checked) {
      state.autoSkipRepeats = checked;
      saveGame();
    }

    function triggerScreenShake() {
      document.body.classList.remove('shake-active');
      void document.body.offsetWidth;
      document.body.classList.add('shake-active');
      setTimeout(() => document.body.classList.remove('shake-active'), 450);
    }

    function showFloatingPopup(pos3D, text, color) {
      const el = document.createElement('div');
      el.className = 'absolute font-black text-sm rblx-stroke floating-cash-anim';
      el.style.color = color;
      el.textContent = text;
      document.getElementById('labelsContainer').appendChild(el);
      project3DToScreen(pos3D.clone().add(new THREE.Vector3(0, 3.5, 0)), el);
      setTimeout(() => el.remove(), 1250);
    }

    /*************************************************************************
     * 10. MODAL MANAGERS: FOOD SHOP, SELL, ANIMALS, INDEX & RECORDS
     *************************************************************************/
    function openModal(id) {
      audio.playClickSound();
      document.getElementById(id).classList.remove('hidden');
      document.getElementById(id).classList.add('flex');
      if (id === 'shopModal') renderFoodShop();
      if (id === 'sellModal') renderSellStall();
      if (id === 'animalsModal') renderMyAnimals();
      if (id === 'indexModal') renderAnimalIndex();
      if (id === 'leaderboardModal') renderLeaderboardModal();
      if (id === 'calcLabModal') renderWorkedExampleModal();
    }

    function closeModal(id) {
      audio.playClickSound();
      document.getElementById(id).classList.add('hidden');
      document.getElementById(id).classList.remove('flex');
    }

    function renderFoodShop() {
      const grid = document.getElementById('foodShopGrid');
      grid.innerHTML = '';

      FOODS.forEach(food => {
        const isOwned = state.unlockedFoods.includes(food.id);
        const isEquipped = state.equippedFoodId === food.id;

        const card = document.createElement('div');
        card.className = `bg-gray-800 rounded-2xl p-2.5 sm:p-3 border-3 flex flex-col items-center justify-between shadow-lg ${
          isEquipped ? 'border-lime-400 ring-2 ring-lime-400' : isOwned ? 'border-gray-600' : 'border-gray-700 opacity-90'
        }`;

        card.innerHTML = `
          <div class="text-center">
            <div class="text-white font-extrabold text-xs sm:text-sm">${food.name}</div>
            <div class="text-[9px] text-gray-400 font-bold">${food.tier}</div>
          </div>
          <div class="text-3xl sm:text-4xl my-2">${food.icon}</div>
          <div class="mono-math text-[9px] text-yellow-300 font-bold text-center truncate w-full mb-1">
            ${food.formulaStr}
          </div>
          <div class="text-[9px] text-gray-400 mb-2">Distance: ${food.distMult}x • Luck: ${food.luck}x</div>
          ${
            isEquipped
              ? `<button class="rblx-btn bg-gray-600 text-gray-300 font-black text-xs px-3 py-1 rounded-xl w-full cursor-default">EQUIPPED</button>`
              : isOwned
              ? `<button onclick="selectFood('${food.id}')" class="rblx-btn bg-sky-400 hover:bg-sky-300 text-black font-black text-xs px-3 py-1 rounded-xl w-full">EQUIP</button>`
              : `<button onclick="buyFood('${food.id}')" class="rblx-btn bg-red-600 hover:bg-red-500 text-white font-black text-xs px-3 py-1 rounded-xl w-full">$${formatNum(food.cost)}</button>`
          }
        `;
        grid.appendChild(card);
      });

      document.getElementById('shopPlotCapText').textContent = `${state.plotCapacity}/20 Max`;
      const upBtn = document.getElementById('upgradePlotBtn');
      if (state.plotCapacity >= 20) {
        upBtn.textContent = 'MAX REACHED';
        upBtn.className = 'rblx-btn bg-gray-600 text-gray-400 font-extrabold text-xs px-3 py-1.5 rounded-xl cursor-default';
      } else {
        const cost = Math.round(150 * Math.pow(1.85, state.plotCapacity - 5));
        upBtn.textContent = `UPGRADE ($${formatNum(cost)})`;
      }
    }

    function buyFood(foodId) {
      const food = FOODS.find(f => f.id === foodId);
      if (!food) return;
      if (state.cash < food.cost) {
        audio.playClickSound();
        showToast('❌ Not enough cash to buy ' + food.name + '!', 'bg-rose-500 text-white');
        return;
      }
      state.cash -= food.cost;
      state.unlockedFoods.push(food.id);
      state.equippedFoodId = food.id;
      audio.playUnlockSound();
      showToast(`🎉 Bought and equipped ${food.name}!`, 'bg-lime-400 text-black');
      renderFoodShop();
      updateHUD();
      saveGame();
    }

    function selectFood(foodId) {
      audio.playClickSound();
      state.equippedFoodId = foodId;
      renderFoodShop();
      updateHUD();
      saveGame();
    }

    function upgradePlotCapacity() {
      if (state.plotCapacity >= 20) return;
      const cost = Math.round(150 * Math.pow(1.85, state.plotCapacity - 5));
      if (state.cash < cost) {
        audio.playClickSound();
        showToast('❌ Not enough cash for plot upgrade!', 'bg-rose-500 text-white');
        return;
      }
      state.cash -= cost;
      state.plotCapacity++;
      audio.playUnlockSound();
      showToast(`🏡 Lawn Plot expanded to ${state.plotCapacity}/20 pets!`, 'bg-lime-400 text-black');
      renderFoodShop();
      updateHUD();
      saveGame();
    }

    function renderSellStall() {
      const grid = document.getElementById('sellListGrid');
      grid.innerHTML = '';
      const unequipped = state.inventory.filter(i => !i.equipped);

      if (unequipped.length === 0) {
        grid.innerHTML = '<div class="col-span-2 text-center text-gray-400 py-6">No unequipped pets in inventory to sell!</div>';
        return;
      }

      unequipped.forEach(pet => {
        const animal = ANIMALS.find(a => a.id === pet.animalId);
        if (!animal) return;
        const sellValue = Math.max(10, pet.income * 25);
        const card = document.createElement('div');
        card.className = 'bg-gray-800 rounded-xl p-2.5 flex items-center justify-between border border-gray-700 shadow';
        const sizeTag = pet.size && pet.size.id !== 'regular' ? `[${pet.size.name}] ` : '';
        card.innerHTML = `
          <div class="flex items-center gap-2">
            <span class="text-2xl">${animal.emoji}</span>
            <div>
              <div class="text-white font-extrabold text-xs">${sizeTag}${animal.name}</div>
              <div class="text-[10px]" style="color:${pet.mutation.color}">${pet.mutation.name}</div>
            </div>
          </div>
          <button onclick="sellSingleAnimal('${pet.uid}')" class="rblx-btn bg-rose-500 hover:bg-rose-400 text-white font-extrabold text-xs px-3 py-1 rounded-xl">
            SELL (+$${formatNum(sellValue)})
          </button>
        `;
        grid.appendChild(card);
      });
    }

    function sellSingleAnimal(uid) {
      const idx = state.inventory.findIndex(i => i.uid === uid);
      if (idx === -1) return;
      const pet = state.inventory[idx];
      const sellValue = Math.max(10, pet.income * 25);
      state.cash += sellValue;
      state.inventory.splice(idx, 1);
      audio.playCoinSound();
      renderSellStall();
      updateHUD();
      saveGame();
    }

    function sellAllUnequipped() {
      const unequipped = state.inventory.filter(i => !i.equipped);
      if (unequipped.length === 0) return;
      let total = 0;
      unequipped.forEach(pet => { total += Math.max(10, pet.income * 25); });
      state.cash += total;
      state.inventory = state.inventory.filter(i => i.equipped);
      audio.playCoinSound();
      showToast(`💰 Sold ${unequipped.length} unequipped pets for +$${formatNum(total)}!`, 'bg-lime-400 text-black');
      renderSellStall();
      updateHUD();
      saveGame();
    }

    function renderMyAnimals() {
      const list = document.getElementById('myAnimalsList');
      list.innerHTML = '';
      const equippedCount = state.inventory.filter(i => i.equipped).length;
      document.getElementById('animalsPlotBadge').textContent = `${equippedCount}/${state.plotCapacity}`;

      if (state.inventory.length === 0) {
        list.innerHTML = '<div class="text-center text-gray-400 py-8">No animals caught yet! Walk to the Launch Line to throw food.</div>';
        return;
      }

      state.inventory.forEach(pet => {
        const animal = ANIMALS.find(a => a.id === pet.animalId);
        if (!animal) return;
        const card = document.createElement('div');
        card.className = 'bg-gray-800 rounded-2xl p-2.5 flex items-center justify-between border-2 border-black shadow';
        const sizeTag = pet.size && pet.size.id !== 'regular' ? `[${pet.size.name.toUpperCase()}] ` : '';
        card.innerHTML = `
          <div class="flex items-center gap-2.5">
            <div class="w-12 h-12 bg-gray-900 rounded-xl border border-gray-700 flex items-center justify-center text-2xl">
              ${animal.emoji}
            </div>
            <div>
              <div class="text-white font-extrabold text-xs sm:text-sm">${sizeTag}${animal.name}</div>
              <div class="text-[10px] font-bold" style="color:${pet.mutation.color}">${pet.mutation.name}</div>
              <div class="text-[10px] text-lime-400 font-bold">+$${formatNum(pet.income)}/s</div>
            </div>
          </div>
          <div class="flex items-center gap-1.5">
            <button onclick="toggleEquipAnimal('${pet.uid}')" class="rblx-btn ${
              pet.equipped ? 'bg-sky-500 text-white' : 'bg-lime-400 text-black'
            } font-extrabold text-xs px-3 py-1.5 rounded-xl">
              ${pet.equipped ? 'PICK UP' : 'EQUIP'}
            </button>
            <button onclick="sellSingleAnimal('${pet.uid}'); renderMyAnimals()" class="rblx-btn bg-red-600 hover:bg-red-500 text-white font-extrabold text-xs px-2.5 py-1.5 rounded-xl">
              SELL
            </button>
          </div>
        `;
        list.appendChild(card);
      });
    }

    function toggleEquipAnimal(uid) {
      const pet = state.inventory.find(i => i.uid === uid);
      if (!pet) return;
      audio.playClickSound();

      if (pet.equipped) {
        pet.equipped = false;
      } else {
        const equippedCount = state.inventory.filter(i => i.equipped).length;
        if (equippedCount >= state.plotCapacity) {
          showToast(`❌ Lawn Plot full (${state.plotCapacity}/${state.plotCapacity})! Expand plot in Shop or pick up a pet.`, 'bg-rose-500 text-white');
          return;
        }
        pet.equipped = true;
      }

      sync3DPlotPets();
      renderMyAnimals();
      updateHUD();
      saveGame();
    }

    function equipBestAnimals() {
      audio.playClickSound();
      state.inventory.sort((a, b) => b.income - a.income);
      state.inventory.forEach((pet, idx) => {
        pet.equipped = idx < state.plotCapacity;
      });
      sync3DPlotPets();
      renderMyAnimals();
      updateHUD();
      audio.playLevelUpSound();
      showToast('⭐ Equipped your highest income animals on the lawn!', 'bg-amber-400 text-black');
      saveGame();
    }

    function renderAnimalIndex() {
      const cont = document.getElementById('indexBiomeContainer');
      cont.innerHTML = '';
      document.getElementById('indexModalCount').textContent = `Unlocked: ${state.unlockedIndex.size}/18`;

      BIOMES.forEach(biome => {
        const biomeAnimals = ANIMALS.filter(a => a.biome === biome.id);
        const unlockedInBiome = biomeAnimals.filter(a => state.unlockedIndex.has(a.id)).length;
        const isComplete = unlockedInBiome === biomeAnimals.length;
        const isClaimed = state.claimedBiomeRewards.has(biome.id);

        const sec = document.createElement('div');
        sec.className = 'bg-gray-800 rounded-2xl p-3 border-2 border-black flex flex-col gap-2 shadow-lg';

        let rewardBtnHtml = '';
        if (isClaimed) {
          rewardBtnHtml = `<span class="bg-gray-700 text-lime-400 font-bold text-[10px] px-2.5 py-1 rounded-xl">✓ REWARD CLAIMED (+${biome.rewardPower} 💪)</span>`;
        } else if (isComplete) {
          rewardBtnHtml = `<button onclick="claimBiomeIndexReward('${biome.id}')" class="rblx-btn bg-gradient-to-r from-amber-400 to-yellow-300 text-black font-black text-xs px-3 py-1 rounded-xl animate-bounce">🎁 CLAIM (+${biome.rewardPower} 💪)</button>`;
        } else {
          rewardBtnHtml = `<span class="text-gray-400 text-[10px]">Reward: +${biome.rewardPower} 💪 (${unlockedInBiome}/3)</span>`;
        }

        sec.innerHTML = `
          <div class="flex items-center justify-between border-b border-gray-700 pb-1.5">
            <div class="flex items-center gap-1.5">
              <span class="text-lg">${biome.icon}</span>
              <span class="text-white font-extrabold text-xs sm:text-sm">${biome.name} (${biome.minDist} - ${biome.maxDist}m)</span>
            </div>
            <div>${rewardBtnHtml}</div>
          </div>
          <div class="grid grid-cols-3 gap-2">
            ${biomeAnimals.map(a => {
              const discovered = state.unlockedIndex.has(a.id);
              return `
                <div class="bg-gray-900 rounded-xl p-2 border ${discovered ? 'border-gray-600' : 'border-gray-800 opacity-60'} flex flex-col items-center text-center">
                  <div class="text-2xl sm:text-3xl my-1 filter ${discovered ? '' : 'brightness-0'}">
                    ${discovered ? a.emoji : '❓'}
                  </div>
                  <div class="text-white font-extrabold text-[10px] sm:text-xs truncate w-full">
                    ${discovered ? a.name : '???'}
                  </div>
                  <div class="text-[9px] text-gray-400">${discovered ? a.rarity : 'Undiscovered'}</div>
                  <div class="text-[9px] text-amber-300 font-bold">${a.oddsStr}</div>
                  <div class="text-[9px] text-lime-400 font-bold">${discovered ? '$' + formatNum(a.baseIncome) + '/s' : ''}</div>
                </div>
              `;
            }).join('')}
          </div>
        `;
        cont.appendChild(sec);
      });
    }

    function claimBiomeIndexReward(biomeId) {
      const b = BIOMES.find(item => item.id === biomeId);
      if (!b || state.claimedBiomeRewards.has(biomeId)) return;
      state.claimedBiomeRewards.add(biomeId);
      audio.playUnlockSound();
      showToast(`🎁 Claimed ${b.name} Mastery Reward! Permanent +${b.rewardPower} Throw Strength!`, 'bg-amber-400 text-black');
      renderAnimalIndex();
      updateHUD();
      saveGame();
    }

    // Personal Luckiest Catches (Hall of Fame Modal)
    function renderLeaderboardModal() {
      const list = document.getElementById('leaderboardList');
      list.innerHTML = '';
      const catches = state.playerBestCatches || [];

      if (catches.length === 0) {
        list.innerHTML = '<div class="text-center text-gray-400 py-8">No catches recorded yet! Head to the Launch Line to start your record collection.</div>';
        return;
      }

      catches.forEach((c, idx) => {
        const item = document.createElement('div');
        item.className = 'bg-gray-800 p-3 rounded-2xl flex items-center justify-between border-2 border-black shadow';
        item.innerHTML = `
          <div class="flex items-center gap-3">
            <span class="text-yellow-400 font-black text-sm sm:text-base w-7">#${idx + 1}</span>
            <span class="text-2xl">${c.emoji}</span>
            <div>
              <div class="text-white font-extrabold text-xs sm:text-sm">
                ${c.size.name.toUpperCase()} ${c.name}
              </div>
              <div class="text-[10px] font-bold" style="color:${c.mutation.color}">
                ${c.mutation.name} • +$${formatNum(c.income)}/s
              </div>
            </div>
          </div>
          <div class="text-right">
            <div class="text-amber-300 font-black text-xs sm:text-sm">1 IN ${formatNum(c.odds)}</div>
            <div class="text-[9px] text-gray-400 font-bold">${c.distance.toFixed(1)}m away</div>
          </div>
        `;
        list.appendChild(item);
      });
    }

    let lastNotifiedFoodIndex = 0;
    function checkNewFoodUnlock() {
      FOODS.forEach((food, idx) => {
        if (idx === 0) return;
        if (!state.unlockedFoods.includes(food.id) && idx > lastNotifiedFoodIndex) {
          if (state.cash >= food.cost || getTotalStrength() >= idx * 25) {
            lastNotifiedFoodIndex = idx;
            document.getElementById('newFoodIconBox').textContent = food.icon;
            document.getElementById('newFoodTitle').textContent = food.name.toUpperCase();
            document.getElementById('newFoodCost').textContent = `$${formatNum(food.cost)}`;
            openModal('newFoodModal');
            audio.playUnlockSound();
          }
        }
      });
    }

    /*************************************************************************
     * 11. SETTINGS & AUDIO CONTROLS
     *************************************************************************/
    function setMusicVolume(val) {
      state.settings.musicVol = parseInt(val);
      document.getElementById('musicVolLabel').textContent = `${val}%`;
      audio.setMusicVol(state.settings.musicVol);
      saveGame();
    }

    function setSfxVolume(val) {
      state.settings.sfxVol = parseInt(val);
      document.getElementById('sfxVolLabel').textContent = `${val}%`;
      audio.setSfxVol(state.settings.sfxVol);
      saveGame();
    }

    function toggleViewOthersPets(checked) {
      state.settings.viewOthersPets = checked;
      document.getElementById('viewOthersLabel').textContent = checked ? 'ON' : 'OFF';
      document.getElementById('viewOthersLabel').className = checked ? 'text-xs text-lime-400' : 'text-xs text-gray-500';
      saveGame();
    }

    function toggleViewYourPets(checked) {
      state.settings.viewYourPets = checked;
      document.getElementById('viewYoursLabel').textContent = checked ? 'ON' : 'OFF';
      document.getElementById('viewYoursLabel').className = checked ? 'text-xs text-lime-400' : 'text-xs text-gray-500';
      sync3DPlotPets();
      saveGame();
    }

    /*************************************************************************
     * 12. TEACHER GOD-MODE DEMO BUTTON & AUTO-SAVE ENGINE
     *************************************************************************/
    function activateTeacherGodMode() {
      audio.playLevelUpSound();
      state.cash = 10000000;
      state.baseStrength = 5000;
      state.plotCapacity = 20;
      state.unlockedFoods = FOODS.map(f => f.id);
      state.equippedFoodId = 'lobster';
      ANIMALS.forEach(a => state.unlockedIndex.add(a.id));
      BIOMES.forEach(b => state.claimedBiomeRewards.add(b.id));

      state.inventory = [];
      state.playerBestCatches = [];

      for (let i = 0; i < 20; i++) {
        const anim = ANIMALS[ANIMALS.length - 1 - (i % 6)];
        const sz = SIZES[Math.min(SIZES.length - 1, 3 + (i % 3))]; // Giant, Titanic, Colossal
        const mut = MUTATIONS[2 + (i % 3)]; // Golden, Rainbow, Cosmic
        const income = Math.round(anim.baseIncome * sz.mult * mut.mult);
        const odds = anim.baseOdds * sz.chanceNum * mut.chanceNum;

        state.inventory.push({
          uid: 'god_pet_' + i,
          animalId: anim.id,
          size: sz,
          mutation: mut,
          income: income,
          equipped: true
        });

        if (i < 5) {
          state.playerBestCatches.push({
            id: anim.id,
            name: anim.name,
            emoji: anim.emoji,
            size: sz,
            mutation: mut,
            odds: odds,
            distance: 5500 + i * 400,
            income: income
          });
        }
      }

      state.playerBestCatches.sort((a, b) => b.odds - a.odds);
      update3DLuckiestBoardTexture();
      sync3DPlotPets();
      updateHUD();
      showToast('👨‍🏫 TEACHER DEMO ACTIVATED! $10M Cash, 20 Mutated Pets & All Trig Tiers Unlocked!', 'bg-yellow-400 text-black');
      saveGame();
    }

    function resetPlayerProgress() {
      if (confirm('Reset all game data back to student start?')) {
        localStorage.removeItem(SAVE_KEY);
        location.reload();
      }
    }

    function saveGame() {
      try {
        const data = {
          cash: state.cash,
          baseStrength: state.baseStrength,
          pullUpLevel: state.pullUpLevel,
          pullUpXp: state.pullUpXp,
          pullUpMaxXp: state.pullUpMaxXp,
          plotCapacity: state.plotCapacity,
          inventory: state.inventory,
          unlockedFoods: state.unlockedFoods,
          equippedFoodId: state.equippedFoodId,
          unlockedIndex: Array.from(state.unlockedIndex),
          claimedBiomeRewards: Array.from(state.claimedBiomeRewards),
          playerBestCatches: state.playerBestCatches,
          autoSkipRepeats: state.autoSkipRepeats,
          settings: state.settings
        };
        localStorage.setItem(SAVE_KEY, JSON.stringify(data));
      } catch (e) {
        console.warn('LocalStorage save failed:', e);
      }
    }

    function loadGame() {
      try {
        const raw = localStorage.getItem(SAVE_KEY);
        if (!raw) return;
        const d = JSON.parse(raw);
        if (d.cash !== undefined) state.cash = d.cash;
        if (d.baseStrength !== undefined) state.baseStrength = d.baseStrength;
        if (d.pullUpLevel !== undefined) state.pullUpLevel = d.pullUpLevel;
        if (d.pullUpXp !== undefined) state.pullUpXp = d.pullUpXp;
        if (d.pullUpMaxXp !== undefined) state.pullUpMaxXp = d.pullUpMaxXp;
        if (d.plotCapacity !== undefined) state.plotCapacity = d.plotCapacity;
        if (d.inventory) state.inventory = d.inventory;
        if (d.unlockedFoods) state.unlockedFoods = d.unlockedFoods;
        if (d.equippedFoodId) state.equippedFoodId = d.equippedFoodId;
        if (d.unlockedIndex && Array.isArray(d.unlockedIndex)) state.unlockedIndex = new Set(d.unlockedIndex);
        if (d.claimedBiomeRewards && Array.isArray(d.claimedBiomeRewards)) state.claimedBiomeRewards = new Set(d.claimedBiomeRewards);
        if (d.playerBestCatches && Array.isArray(d.playerBestCatches)) state.playerBestCatches = d.playerBestCatches;
        if (d.autoSkipRepeats !== undefined) state.autoSkipRepeats = d.autoSkipRepeats;
        if (d.settings) state.settings = { ...state.settings, ...d.settings };

        const musicSlider = document.getElementById('musicSlider');
        if (musicSlider) musicSlider.value = state.settings.musicVol;
        const musicLabel = document.getElementById('musicVolLabel');
        if (musicLabel) musicLabel.textContent = `${state.settings.musicVol}%`;
        const sfxSlider = document.getElementById('sfxSlider');
        if (sfxSlider) sfxSlider.value = state.settings.sfxVol;
        const sfxLabel = document.getElementById('sfxVolLabel');
        if (sfxLabel) sfxLabel.textContent = `${state.settings.sfxVol}%`;
        const autoSkipBox = document.getElementById('autoSkipCheckbox');
        if (autoSkipBox) autoSkipBox.checked = state.autoSkipRepeats;
      } catch (e) {
        console.warn('LocalStorage load failed:', e);
      }
    }

    function formatNum(n) {
      if (n >= 1e12) return (n / 1e12).toFixed(2) + 'T';
      if (n >= 1e9) return (n / 1e9).toFixed(2) + 'B';
      if (n >= 1e6) return (n / 1e6).toFixed(2) + 'M';
      if (n >= 1e3) return (n / 1e3).toFixed(1) + 'K';
      return Math.round(n).toString();
    }

    function getPassiveIncome() {
      return state.inventory.filter(i => i.equipped).reduce((sum, pet) => sum + pet.income, 0);
    }

    function hasUnclaimedIndexReward() {
      for (const b of BIOMES) {
        const biomeAnimals = ANIMALS.filter(a => a.biome === b.id);
        const unlockedInBiome = biomeAnimals.filter(a => state.unlockedIndex.has(a.id)).length;
        if (unlockedInBiome === biomeAnimals.length && !state.claimedBiomeRewards.has(b.id)) {
          return true;
        }
      }
      return false;
    }

    function updateHUD() {
      document.getElementById('cashDisplay').textContent = `$${formatNum(state.cash)}`;
      const rate = getPassiveIncome();
      document.getElementById('incomeRateDisplay').textContent = `+$${formatNum(rate)}/s (Plot)`;

      const totalStr = getTotalStrength();
      const bonus = getIndexMasteryBonus();
      document.getElementById('strengthDisplay').textContent = totalStr;
      document.getElementById('indexBonusDisplay').textContent = `+${bonus} Index Bonus`;

      document.getElementById('indexBadge').textContent = `${state.unlockedIndex.size}/18`;
      const dot = document.getElementById('indexRewardDot');
      if (hasUnclaimedIndexReward()) dot.classList.remove('hidden');
      else dot.classList.add('hidden');

      const equippedCount = state.inventory.filter(i => i.equipped).length;
      document.getElementById('plotCountBadge').textContent = `${equippedCount}/${state.plotCapacity}`;

      const food = getEquippedFood();
      document.getElementById('hudFoodIcon').textContent = food.icon;
      document.getElementById('hudFoodName').textContent = food.name;
      document.getElementById('hudFoodFunc').textContent = food.formulaStr;

      heldFoodMesh.material.color.setHex(food.color);
    }

    function showToast(msg, colorClass) {
      const container = document.body;
      const t = document.createElement('div');
      t.className = `fixed top-20 left-1/2 -translate-x-1/2 z-50 px-5 py-2 rounded-2xl border-2 border-black font-extrabold text-xs sm:text-sm shadow-2xl rblx-stroke-sm transition-all duration-300 pointer-events-none ${colorClass}`;
      t.textContent = msg;
      container.appendChild(t);
      setTimeout(() => {
        t.style.opacity = '0';
        t.style.transform = 'translate(-50%, -15px)';
        setTimeout(() => t.remove(), 350);
      }, 2400);
    }

    function togglePauseWave() {
      state.wavePaused = !state.wavePaused;
      document.getElementById('pauseWaveBtn').textContent = state.wavePaused ? '▶ Resume t' : '⏸ Pause t';
    }

    function toggleMinimizeCalcHUD(minimize) {
      const minBar = document.getElementById('calcMinimizedBar');
      const expPanel = document.getElementById('calcExpandedPanel');
      if (minimize) {
        expPanel.classList.add('hidden');
        minBar.classList.remove('hidden');
      } else {
        minBar.classList.add('hidden');
        expPanel.classList.remove('hidden');
      }
    }

    function updateRampSlider(val) {
      state.rampX0 = parseFloat(val);
      const ramp = evaluateRampCalculus(state.rampX0);
      document.getElementById('rampXVal').textContent = state.rampX0.toFixed(2);
      document.getElementById('rampSlopeVal').textContent = `${ramp.slope.toFixed(2)} (${ramp.angleDeg.toFixed(0)}°)`;
      document.getElementById('minSlopeReadout').textContent = `m = ${ramp.slope.toFixed(2)} (${ramp.angleDeg.toFixed(0)}°)`;
      update3DRampVisuals();
      update3DTrajectoryArc();
    }

    /*************************************************************************
     * 13. LIVE CALCULUS DERIVATIVE OSCILLOSCOPE HTML5 CANVAS RENDERER
     *************************************************************************/
    const oscCanvas = document.getElementById('oscCanvas');
    const oscCtx = oscCanvas.getContext('2d');

    function resizeOscilloscope() {
      const rect = oscCanvas.parentElement.getBoundingClientRect();
      oscCanvas.width = rect.width * (window.devicePixelRatio || 1);
      oscCanvas.height = rect.height * (window.devicePixelRatio || 1);
    }

    function updateCalculusUIAndOscilloscope() {
      const food = getEquippedFood();
      const t = state.t;
      const calc = evaluateFoodCalculus(food, t);
      const absDeriv = Math.abs(calc.deriv);
      const derivRatio = absDeriv / (calc.maxDeriv || 1);

      const isCriticalPoint = food.type !== 'tan' && derivRatio <= 0.18;
      const isMaxDerivSurge = derivRatio >= 0.82;

      const meterPct = Math.max(0, Math.min(100, ((calc.pos + (calc.maxPos || 4)) / ((calc.maxPos || 4) * 2)) * 100));
      document.getElementById('meterMarker').style.top = `${100 - meterPct}%`;
      document.getElementById('meterReadout').textContent = (calc.deriv >= 0 ? '+' : '') + Math.round(calc.deriv * 6);

      document.getElementById('livePosEq').textContent = `${food.formulaStr} = ${(calc.pos >= 0 ? '+' : '') + calc.pos.toFixed(2)}`;
      document.getElementById('liveDerivEq').textContent = `${food.derivStr} = ${(calc.deriv >= 0 ? '+' : '') + calc.deriv.toFixed(2)}`;
      document.getElementById('minDerivReadout').textContent = `P'(t) = ${(calc.deriv >= 0 ? '+' : '') + calc.deriv.toFixed(2)}`;

      const badgeCrit = document.getElementById('badgeCritStatus');
      const badgeSurge = document.getElementById('badgeSurgeStatus');
      const indCrit = document.getElementById('critPointIndicator');
      const regimeBadge = document.getElementById('calcRegimeBadge');

      if (isCriticalPoint) {
        badgeCrit.className = 'bg-yellow-400 border-2 border-black rounded-xl px-2.5 py-0.5 text-[10px] text-black font-black shadow pulse-glow';
        indCrit.classList.remove('hidden');
      } else {
        badgeCrit.className = 'bg-black/80 border-2 border-yellow-400 rounded-xl px-2.5 py-0.5 text-[10px] text-yellow-300 font-extrabold shadow';
        indCrit.classList.add('hidden');
      }

      if (isMaxDerivSurge) {
        badgeSurge.className = 'bg-cyan-400 border-2 border-black rounded-xl px-2.5 py-0.5 text-[10px] text-black font-black shadow pulse-glow';
        regimeBadge.textContent = 'MAX SURGE';
        regimeBadge.className = 'text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-cyan-400 text-black shadow';
      } else if (isCriticalPoint) {
        regimeBadge.textContent = 'CRITICAL POINT';
        regimeBadge.className = 'text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-yellow-400 text-black shadow';
      } else {
        badgeSurge.className = 'bg-black/80 border-2 border-cyan-400 rounded-xl px-2.5 py-0.5 text-[10px] text-cyan-300 font-extrabold shadow';
        regimeBadge.textContent = 'STEADY';
        regimeBadge.className = 'text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-gray-600 text-white shadow';
      }

      // Draw Oscilloscope Canvas
      const W = oscCanvas.width;
      const H = oscCanvas.height;
      if (W === 0 || H === 0) return;

      oscCtx.clearRect(0, 0, W, H);
      const midY = H / 2;

      oscCtx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
      oscCtx.lineWidth = 1;
      oscCtx.beginPath();
      oscCtx.moveTo(0, midY);
      oscCtx.lineTo(W, midY);
      oscCtx.stroke();

      const timeWindow = 4.0;
      const scaleY = H * 0.35 / (food.type === 'tan' ? 6 : Math.max(4, food.A + food.C + 1));

      // P(t) Wave
      oscCtx.strokeStyle = '#38bdf8';
      oscCtx.lineWidth = 2.5;
      oscCtx.beginPath();
      for (let x = 0; x < W; x += 3) {
        const tau = t - timeWindow + (x / W) * timeWindow;
        const pt = evaluateFoodCalculus(food, tau);
        const y = midY - pt.pos * scaleY;
        if (x === 0) oscCtx.moveTo(x, y);
        else oscCtx.lineTo(x, y);
      }
      oscCtx.stroke();

      // P'(t) Curve
      const derivScale = H * 0.35 / (calc.maxDeriv || 8);
      oscCtx.strokeStyle = '#facc15';
      oscCtx.lineWidth = 2.0;
      oscCtx.beginPath();
      for (let x = 0; x < W; x += 3) {
        const tau = t - timeWindow + (x / W) * timeWindow;
        const pt = evaluateFoodCalculus(food, tau);
        const y = midY - pt.deriv * derivScale;
        if (x === 0) oscCtx.moveTo(x, y);
        else oscCtx.lineTo(x, y);
      }
      oscCtx.stroke();

      // Tangent Line
      const curY = midY - calc.pos * scaleY;
      const tangentSlopePixel = -calc.deriv * scaleY * (timeWindow / W);
      oscCtx.strokeStyle = '#f472b6';
      oscCtx.lineWidth = 2.5;
      oscCtx.beginPath();
      oscCtx.moveTo(W - 40, curY - tangentSlopePixel * (-40));
      oscCtx.lineTo(W, curY);
      oscCtx.stroke();

      oscCtx.fillStyle = '#f472b6';
      oscCtx.beginPath();
      oscCtx.arc(W - 2, curY, 5, 0, Math.PI * 2);
      oscCtx.fill();
    }

    /*************************************************************************
     * 14. 3D TO 2D SCREEN PROJECTION & MAIN ANIMATION LOOP
     *************************************************************************/
    function project3DToScreen(vec3, el) {
      const v = vec3.clone().project(camera);
      if (v.z > 1) {
        el.style.display = 'none';
        return;
      }
      const x = (v.x * 0.5 + 0.5) * window.innerWidth;
      const y = (-(v.y * 0.5) + 0.5) * window.innerHeight;
      el.style.display = 'block';
      el.style.left = `${x}px`;
      el.style.top = `${y}px`;
    }

    let lastFrameTime = performance.now();
    function animateLoop(now) {
      const dt = Math.min(0.05, (now - lastFrameTime) / 1000);
      lastFrameTime = now;

      if (!state.wavePaused) {
        state.t += dt;
        pullUpRepTime += dt;
      }

      updatePlayerMovement(dt);
      updateCalculusUIAndOscilloscope();
      update3DTrajectoryArc();

      // Animate Target Skill-Shot Rings
      critRingMesh.rotation.z += dt * 1.5;
      critRingMesh.rotation.x += dt * 0.8;
      critRingGroup.position.y = 7.5 + Math.sin(state.t * 2.5) * 1.6;
      targetLabels.forEach(tl => project3DToScreen(tl.pos, tl.el));

      // Living Animations for Plot Pets Inside Fenced Lawn Plot
      if (state.settings.viewYourPets) {
        activePlotPetEntities.forEach(ent => {
          ent.hopPhase += dt * 6.5;
          ent.mesh.position.x += ent.vx * dt;
          ent.mesh.position.z += ent.vz * dt;
          if (ent.mesh.position.x < -19 || ent.mesh.position.x > 19) ent.vx *= -1;
          if (ent.mesh.position.z < 0 || ent.mesh.position.z > 30) ent.vz *= -1;
          ent.mesh.position.y = Math.abs(Math.sin(ent.hopPhase)) * 0.55;
          ent.mesh.rotation.y = Math.atan2(ent.vx, -ent.vz);

          // Living Micro-Animations: tail, wings, head
          if (ent.mesh.userData) {
            if (ent.mesh.userData.tail) {
              ent.mesh.userData.tail.rotation.y = Math.sin(ent.hopPhase * 1.4) * 0.35;
            }
            if (ent.mesh.userData.leftWing && ent.mesh.userData.rightWing) {
              const flap = Math.sin(ent.hopPhase * 2.2) * 0.35;
              ent.mesh.userData.leftWing.rotation.z = flap;
              ent.mesh.userData.rightWing.rotation.z = -flap;
            }
            if (ent.mesh.userData.head) {
              ent.mesh.userData.head.rotation.x = Math.sin(ent.hopPhase * 0.7) * 0.1;
            }
          }

          const tagPos = ent.mesh.position.clone().add(new THREE.Vector3(0, 3.2, 0));
          project3DToScreen(tagPos, ent.labelEl);
        });
      }

      // Project Station World Labels
      stationLabels.forEach(st => project3DToScreen(st.pos, st.el));

      // Active Projectile Flight or 3D Cutscene Camera
      if (state.activeThrow) {
        const th = state.activeThrow;
        if (th.phase === 'flying') {
          th.progress += dt * 0.52;
          const p = Math.min(1, th.progress);
          const curZ = -14 + p * (th.targetZ - (-14));
          const waveArcY = 2.4 + Math.sin(p * Math.PI) * (14 + th.ramp.slope * 5.2) + Math.sin(p * Math.PI * 6) * 1.2;
          projectileGroup.position.set(playerGroup.position.x, waveArcY, curZ);
          projectileGroup.rotation.x += dt * 8;
          projectileGroup.rotation.y += dt * 6;

          // Camera follows behind and slightly above the spinning projectile (matching video)
          camera.position.set(playerGroup.position.x + 8.5, waveArcY + 6.0, curZ + 16);
          camera.lookAt(playerGroup.position.x, waveArcY, curZ - 12);

          const curDist = th.distance * p;
          document.getElementById('flightDistReadout').textContent = `${curDist.toFixed(1)}m`;

          // Check current biome during flight
          let curB = BIOMES[0];
          for (const b of BIOMES) {
            if (curDist >= b.minDist) curB = b;
          }
          document.getElementById('flightBiomeName').textContent = curB.name;
          document.getElementById('flightBiomeIcon').textContent = curB.icon;

          // Multiplier banner (e.g. 19.09X LUCK from video)
          const liveLuck = (Math.abs(th.calc.deriv) * th.food.luck * 4.2 + 1).toFixed(2);
          document.getElementById('flightLuckMult').textContent = `${liveLuck}X`;

          if (th.progress >= 1.0) {
            transitionTo3DCatchCutscene(th);
          }
        } else if (th.phase === 'reveal') {
          th.revealTimer += dt;

          // Animate Eating: Animal bends down, jaws open and close repeatedly eating food!
          const animalMesh = th.chosenAnimalMesh;
          if (animalMesh) {
            // Eating bobs
            animalMesh.position.y = Math.abs(Math.sin(th.revealTimer * 7)) * 0.25;
            if (animalMesh.userData && animalMesh.userData.jaw) {
              animalMesh.userData.jaw.rotation.x = Math.max(0, Math.sin(th.revealTimer * 12) * 0.45);
            }
            if (animalMesh.userData && animalMesh.userData.head) {
              animalMesh.userData.head.rotation.x = 0.25 + Math.sin(th.revealTimer * 7) * 0.15;
            }
            if (animalMesh.userData && animalMesh.userData.tail) {
              animalMesh.userData.tail.rotation.y = Math.sin(th.revealTimer * 8) * 0.4;
            }
          }

          // Animate Confetti falling down around animal
          confettiMeshes.forEach(cm => {
            cm.position.y += cm.userData.vy * dt;
            cm.position.x += cm.userData.vx * dt;
            cm.position.z += cm.userData.vz * dt;
            cm.rotation.x += cm.userData.rotSpeed * dt;
            cm.rotation.y += cm.userData.rotSpeed * dt;
            if (cm.position.y < 0.2) {
              cm.position.y = 14 + Math.random() * 4;
            }
          });

          // Aura Beacon gentle spin & pulsation
          cutsceneBeacon.rotation.y += dt * 1.5;

          // Camera swoops down low in front of the food pellet framing the eating animal
          camera.position.set(0, 3.4, th.targetZ - 6.5);
          camera.lookAt(0, 1.8, th.targetZ);

          // 1) Suspense Odds Slot Machine Roll (Exact match to Recording 003051)
          if (th.revealTimer < 1.1) {
            th.oddsRollTimer += dt;
            if (th.oddsRollTimer > 0.045) {
              th.oddsRollTimer = 0;
              const progressFraction = Math.min(1, th.revealTimer / 1.0);
              const interimOdds = Math.max(1, Math.round(1 + Math.pow(progressFraction, 2.5) * (th.totalOdds - 1)));
              document.getElementById('catchOddsNumber').textContent = `1 in ${formatNum(interimOdds)}`;
              audio.playTickSound();
            }
          } else {
            document.getElementById('catchOddsNumber').textContent = `1 in ${formatNum(th.totalOdds)}`;
          }

          // 2) Mystery Hangman Letter-by-Letter Name Reveal (Exact match to Recording 003051)
          const targetName = th.chosenAnimal.name.toUpperCase();
          const cleanChars = targetName.split('');
          const revealProgress = Math.max(0, Math.min(1, (th.revealTimer - 0.25) / 0.85));
          const numLettersToReveal = Math.floor(revealProgress * cleanChars.length);

          if (numLettersToReveal > th.nameRevealStep) {
            th.nameRevealStep = numLettersToReveal;
            audio.playRevealLetterSound();
          }

          let displayStr = '';
          for (let i = 0; i < cleanChars.length; i++) {
            if (cleanChars[i] === ' ') {
              displayStr += '  ';
            } else if (i < numLettersToReveal || revealProgress >= 1.0) {
              displayStr += cleanChars[i] + ' ';
            } else {
              displayStr += '_ ';
            }
          }
          document.getElementById('catchAnimalName').textContent = displayStr.trim();
        }
      } else {
        const camDist = 18;
        const cx = playerGroup.position.x + Math.sin(camYaw) * Math.cos(camPitch) * camDist;
        const cy = playerGroup.position.y + Math.sin(camPitch) * camDist + 2.5;
        const cz = playerGroup.position.z + Math.cos(camYaw) * Math.cos(camPitch) * camDist;
        camera.position.set(cx, cy, cz);
        camera.lookAt(playerGroup.position.x, playerGroup.position.y + 2.2, playerGroup.position.z - 2);
      }

      renderer.render(scene, camera);
      requestAnimationFrame(animateLoop);
    }

    /*************************************************************************
     * 15. INITIALIZATION & RECURRING LOOPS
     *************************************************************************/
    window.onload = function () {
      loadGame();
      initStationLabels();
      sync3DPlotPets();
      update3DLuckiestBoardTexture();
      updateRampSlider(state.rampX0);
      updateHUD();
      resizeOscilloscope();
      renderWorkedExampleModal();

      checkZoneTrigger();

      setInterval(() => {
        const rate = getPassiveIncome();
        if (rate > 0) {
          state.cash += rate;
          updateHUD();
          spawnFloatingCashPopups();
          audio.playCoinSound();
        }
      }, 1000);

      setInterval(saveGame, 5000);

      requestAnimationFrame(animateLoop);
    };
  </script>
</body>
</html>
"""
