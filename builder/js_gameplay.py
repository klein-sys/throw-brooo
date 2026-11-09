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
        if (state.activeZone === 'throw') {
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

        state.playerPos.x = Math.max(-23, Math.min(23, state.playerPos.x));
        state.playerPos.z = Math.max(-20, Math.min(26, state.playerPos.z));

        playerGroup.position.set(state.playerPos.x, 0, state.playerPos.z);
        state.playerRot = Math.atan2(vx, vz);
        playerGroup.rotation.y = state.playerRot;

        walkCycle += dt * 14;
        leftLeg.rotation.x = Math.sin(walkCycle) * 0.7;
        rightLeg.rotation.x = -Math.sin(walkCycle) * 0.7;
        leftArm.rotation.x = -Math.sin(walkCycle) * 0.7;
        rightArm.rotation.x = Math.sin(walkCycle) * 0.7;
        playerGroup.position.y = Math.abs(Math.sin(walkCycle)) * 0.25;
      } else {
        leftLeg.rotation.x = 0;
        rightLeg.rotation.x = 0;
        leftArm.rotation.x = 0;
        rightArm.rotation.x = 0;
        playerGroup.position.y = 0;
      }

      checkZoneTrigger();
    }

    function checkZoneTrigger() {
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
      state.playerPos.z += 4.5;
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
    function executeCalculusThrow() {
      if (state.activeThrow || state.activeZone !== 'throw') {
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
      // Distance strictly controlled by strength power 0.85 and food.distMult!
      // At 48 strength with Carrot, distance ~89m (solidly within Forest: 0 - 100m).
      const rawDist = (Math.pow(getTotalStrength(), 0.85) * food.distMult) * (1 + absDeriv * 0.22) * ramp.angleEfficiency * surgeBonus;
      const distance = Math.max(18, rawDist);

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
      const totalOdds = chosenAnimal.baseOdds * chosenSize.chanceNum * chosenMutation.chanceNum;
      const pctStr = (100 / totalOdds).toFixed(totalOdds >= 100 ? 3 : 1) + '%';
      const oddsDisplayStr = totalOdds >= 1000 ? `1 IN ${formatNum(totalOdds)}` : `1 IN ${totalOdds.toFixed(1)}`;

      const finalIncome = Math.round(chosenAnimal.baseIncome * chosenSize.mult * chosenMutation.mult);
      const isNewDiscovery = !state.unlockedIndex.has(chosenAnimal.id);

      // Distance mapping to 3D Z coordinate
      const normDist = Math.min(1, Math.pow(distance / 5000, 0.52));
      const targetZ = -14 - normDist * 290;

      state.throwCount++;
      projectileMesh.material.color.setHex(food.color);
      projectileGroup.position.set(0, 2.2, -14);
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
        pctStr,
        oddsDisplayStr,
        finalIncome,
        isNewDiscovery,
        isCriticalPoint,
        isMaxDerivSurge,
        t0,
        calc,
        ramp,
        food,
        revealTimer: 0
      };

      saveWorkedExampleTelemetry(state.activeThrow);

      // Record to Player's Personal Best Catches (Hall of Fame)
      recordPersonalBestCatch(state.activeThrow);

      // Auto-Skip repeat catches option
      if (!isNewDiscovery && state.autoSkipRepeats) {
        finalizeAnimalAward(state.activeThrow);
        projectileGroup.visible = false;
        state.activeThrow = null;
        showToast(`⚡ Auto-Skipped: Caught ${chosenSize.name} ${chosenMutation.name} ${chosenAnimal.name} ($${formatNum(finalIncome)}/s) [${oddsDisplayStr}] at ${distance.toFixed(1)}m!`, 'bg-lime-400 text-black');
        return;
      }

      document.getElementById('flightOverlay').classList.remove('hidden');
      document.getElementById('flightOverlay').classList.add('flex');
      document.getElementById('skipFlightBtn').style.display = isNewDiscovery ? 'none' : 'flex';
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
      // Sort by rarest (highest odds number)
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

      while (cutsceneGroup.children.length > 0) {
        cutsceneGroup.remove(cutsceneGroup.children[0]);
      }
      const animalMesh = createBlockyAnimalMesh(th.chosenAnimal, th.chosenSize, th.chosenMutation);
      animalMesh.position.set(0, 0, th.targetZ);

      const bait = projectileMesh.clone();
      bait.position.set(1.1, 0.4, th.targetZ - 0.5);
      bait.scale.set(0.65, 0.65, 0.65);
      cutsceneGroup.add(animalMesh, bait);
      cutsceneGroup.visible = true;

      // Populate Cutscene Modal UI with Exact Rarity Odds & Size Chances
      document.getElementById('catchNewBadge').style.display = th.isNewDiscovery ? 'block' : 'none';
      document.getElementById('catchOddsBadge').textContent = `🎲 CHANCE: ${th.oddsDisplayStr} (${th.pctStr})`;
      document.getElementById('catchAnimalName').textContent = th.chosenAnimal.name.toUpperCase();
      document.getElementById('catchSizeTag').textContent = `${th.chosenSize.name.toUpperCase()} (${th.chosenSize.mult}x Size)`;
      document.getElementById('catchSizeTag').style.color = th.chosenSize.color;
      document.getElementById('catchMutationTag').textContent = `${th.chosenMutation.name} (${th.chosenMutation.mult}x)`;
      document.getElementById('catchMutationTag').style.color = th.chosenMutation.color;
      document.getElementById('catchIncomeRate').textContent = `+$${formatNum(th.finalIncome)}/s`;

      document.getElementById('catchRevealModal').classList.remove('hidden');
      document.getElementById('catchRevealModal').classList.add('flex');

      audio.playCatchSound(th.isNewDiscovery, th.chosenAnimal.rarity);
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

    function closeCatchReveal(e) {
      if (e) e.stopPropagation();
      skipThrowAnimation();
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
        if (d.unlockedIndex) state.unlockedIndex = new Set(d.unlockedIndex);
        if (d.claimedBiomeRewards) state.claimedBiomeRewards = new Set(d.claimedBiomeRewards);
        if (d.playerBestCatches) state.playerBestCatches = d.playerBestCatches;
        if (d.autoSkipRepeats !== undefined) state.autoSkipRepeats = d.autoSkipRepeats;
        if (d.settings) state.settings = { ...state.settings, ...d.settings };

        document.getElementById('musicSlider').value = state.settings.musicVol;
        document.getElementById('musicVolLabel').textContent = `${state.settings.musicVol}%`;
        document.getElementById('sfxSlider').value = state.settings.sfxVol;
        document.getElementById('sfxVolLabel').textContent = `${state.settings.sfxVol}%`;
        document.getElementById('autoSkipCheckbox').checked = state.autoSkipRepeats;
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
      document.getElementById('strengthDisplay').textContent = `${totalStr}`;
      const bonusStr = totalStr - state.baseStrength;
      document.getElementById('indexBonusDisplay').textContent = `+${bonusStr} Index Bonus`;

      const food = getEquippedFood();
      document.getElementById('hudFoodIcon').textContent = food.icon;
      document.getElementById('hudFoodName').textContent = food.name;
      document.getElementById('hudFoodFunc').textContent = food.formulaStr;

      const equippedCount = state.inventory.filter(i => i.equipped).length;
      document.getElementById('plotCountBadge').textContent = `${equippedCount}/${state.plotCapacity}`;
      document.getElementById('indexBadge').textContent = `${state.unlockedIndex.size}/18`;

      const rewardDot = document.getElementById('indexRewardDot');
      if (hasUnclaimedIndexReward()) {
        rewardDot.classList.remove('hidden');
      } else {
        rewardDot.classList.add('hidden');
      }
    }

    function showToast(msg, cls = 'bg-lime-400 text-black') {
      const existing = document.getElementById('toastNotice');
      if (existing) existing.remove();

      const t = document.createElement('div');
      t.id = 'toastNotice';
      t.className = `fixed top-24 left-1/2 -translate-x-1/2 z-50 px-4 py-2 rounded-2xl border-2 border-black font-extrabold text-xs sm:text-sm shadow-2xl transition-all duration-300 ${cls}`;
      t.textContent = msg;
      document.body.appendChild(t);
      setTimeout(() => {
        t.style.opacity = '0';
        setTimeout(() => t.remove(), 300);
      }, 2600);
    }

    /*************************************************************************
     * 13. LIVE CALCULUS OSCILLOSCOPE HTML5 CANVAS RENDERER
     *************************************************************************/
    const oscCanvas = document.getElementById('oscCanvas');
    const oscCtx = oscCanvas.getContext('2d');

    function resizeOscilloscope() {
      const rect = oscCanvas.getBoundingClientRect();
      oscCanvas.width = rect.width * (window.devicePixelRatio || 1);
      oscCanvas.height = rect.height * (window.devicePixelRatio || 1);
    }

    function updateCalculusUIAndOscilloscope() {
      const food = getEquippedFood();
      const t = state.t;
      const calc = evaluateFoodCalculus(food, t);
      const ramp = evaluateRampCalculus(state.rampX0);

      const absDeriv = Math.abs(calc.deriv);
      const derivRatio = absDeriv / (calc.maxDeriv || 1);

      const isCriticalPoint = food.type !== 'tan' && derivRatio <= 0.18;
      const isMaxDerivSurge = derivRatio >= 0.82;

      document.getElementById('livePosEq').textContent = `${food.formulaStr} = ${calc.pos >= 0 ? '+' : ''}${calc.pos.toFixed(2)}`;
      document.getElementById('liveDerivEq').textContent = `${food.derivStr} = ${calc.deriv >= 0 ? '+' : ''}${calc.deriv.toFixed(2)}`;
      document.getElementById('minDerivReadout').textContent = `P'(t) = ${calc.deriv >= 0 ? '+' : ''}${calc.deriv.toFixed(2)}`;
      document.getElementById('minSlopeReadout').textContent = `m = ${ramp.slope.toFixed(2)} (${ramp.angleDeg.toFixed(0)}°)`;

      const regBadge = document.getElementById('calcRegimeBadge');
      const critInd = document.getElementById('critPointIndicator');
      if (isCriticalPoint) {
        regBadge.textContent = 'CRITICAL POINT (MUTATION)';
        regBadge.className = 'text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-yellow-400 text-black shadow animate-pulse';
        critInd.classList.remove('hidden');
      } else if (isMaxDerivSurge) {
        regBadge.textContent = 'MAX DERIVATIVE SURGE';
        regBadge.className = 'text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-cyan-400 text-black shadow';
        critInd.classList.add('hidden');
      } else {
        regBadge.textContent = 'HARMONIC TRANSIT';
        regBadge.className = 'text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-gray-600 text-white';
        critInd.classList.add('hidden');
      }

      const marker = document.getElementById('meterMarker');
      const readout = document.getElementById('meterReadout');
      if (marker && readout) {
        const normPos = Math.max(0, Math.min(1, (calc.pos + (food.type === 'tan' ? 5 : 6)) / 12));
        marker.style.top = `${(1 - normPos) * 88}%`;
        const powerNumber = Math.round(absDeriv * 5);
        readout.textContent = `+${powerNumber}`;
      }

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
      critRingGroup.position.y = 6.5 + Math.sin(state.t * 2.5) * 1.5;
      targetLabels.forEach(tl => project3DToScreen(tl.pos, tl.el));

      // Animate Plot Pets Hopping Inside Fenced Lawn Plot
      if (state.settings.viewYourPets) {
        activePlotPetEntities.forEach(ent => {
          ent.hopPhase += dt * 7.5;
          ent.mesh.position.x += ent.vx * dt;
          ent.mesh.position.z += ent.vz * dt;
          if (ent.mesh.position.x < -9.5 || ent.mesh.position.x > 9.5) ent.vx *= -1;
          if (ent.mesh.position.z < -2.5 || ent.mesh.position.z > 16.5) ent.vz *= -1;
          ent.mesh.position.y = Math.abs(Math.sin(ent.hopPhase)) * 0.65;
          ent.mesh.rotation.y = Math.atan2(ent.vx, -ent.vz);

          const tagPos = ent.mesh.position.clone().add(new THREE.Vector3(0, 2.6, 0));
          project3DToScreen(tagPos, ent.labelEl);
        });
      }

      // Project Station World Labels
      stationLabels.forEach(st => project3DToScreen(st.pos, st.el));

      // Active Projectile Flight or 3D Cutscene Camera
      if (state.activeThrow) {
        const th = state.activeThrow;
        if (th.phase === 'flying') {
          th.progress += dt * 0.65;
          const p = Math.min(1, th.progress);
          const curZ = -14 + p * (th.targetZ - (-14));
          const waveArcY = 2.2 + Math.sin(p * Math.PI) * (12 + th.ramp.slope * 4.8) + Math.sin(p * Math.PI * 6) * 1.2;
          projectileGroup.position.set(0, waveArcY, curZ);
          projectileGroup.rotation.x += dt * 8;
          projectileGroup.rotation.y += dt * 6;

          camera.position.set(8.5, waveArcY + 6.5, curZ + 15);
          camera.lookAt(0, waveArcY, curZ - 6);

          const curDist = th.distance * p;
          document.getElementById('flightDistReadout').textContent = `${curDist.toFixed(1)}m`;
          document.getElementById('flightBiomeReadout').textContent = `Flying down canyon to ${th.landingBiome.icon} ${th.landingBiome.name}!`;

          if (th.progress >= 1.0) {
            transitionTo3DCatchCutscene(th);
          }
        } else if (th.phase === 'reveal') {
          th.revealTimer += dt;
          const animalMesh = cutsceneGroup.children[0];
          if (animalMesh) {
            animalMesh.rotation.y = Math.sin(th.revealTimer * 3.5) * 0.7;
            animalMesh.position.y = Math.abs(Math.sin(th.revealTimer * 8)) * 0.95;
          }
          camera.position.set(Math.sin(th.revealTimer * 0.8) * 5.2, 4.2, th.targetZ + 8.5);
          camera.lookAt(0, 1.8, th.targetZ);
        }
      } else {
        const camDist = 16;
        const cx = playerGroup.position.x + Math.sin(camYaw) * Math.cos(camPitch) * camDist;
        const cy = playerGroup.position.y + Math.sin(camPitch) * camDist + 2.4;
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
