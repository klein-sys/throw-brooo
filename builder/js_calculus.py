# -*- coding: utf-8 -*-

JS_CALCULUS = """
    /*************************************************************************
     * 4. DIFFERENTIAL CALCULUS ENGINE (TRIG DERIVATIVES, TANGENTS & CHAIN RULE)
     *************************************************************************/
    function getTotalStrength() {
      let bonus = 0;
      state.claimedBiomeRewards.forEach(biomeId => {
        const b = BIOMES.find(item => item.id === biomeId);
        if (b) bonus += b.rewardPower;
      });
      return state.baseStrength + bonus;
    }

    function getEquippedFood() {
      return FOODS.find(f => f.id === state.equippedFoodId) || FOODS[0];
    }

    function evaluateFoodCalculus(food, t) {
      if (food.type === 'tan') {
        const arg = food.B * t;
        const cosVal = Math.cos(arg);
        const safeCos = Math.abs(cosVal) < 0.22 ? (cosVal >= 0 ? 0.22 : -0.22) : cosVal;
        const pos = food.A * (Math.sin(arg) / safeCos);
        const secSq = 1 / (safeCos * safeCos);
        const deriv = food.A * food.B * secSq;
        const maxDeriv = food.A * food.B * (1 / (0.22 * 0.22));
        return { pos, deriv, maxDeriv };
      } else {
        const pos = food.A * Math.sin(food.B * t) + food.C * Math.cos(food.D * t);
        const deriv = food.A * food.B * Math.cos(food.B * t) - food.C * food.D * Math.sin(food.D * t);
        const maxDeriv = Math.abs(food.A * food.B) + Math.abs(food.C * food.D);
        return { pos, deriv, maxDeriv };
      }
    }

    function evaluateRampCalculus(x0) {
      const y0 = 2 * Math.sin(x0);
      const slope = 2 * Math.cos(x0);
      const angleRad = Math.atan(slope);
      const angleDeg = (angleRad * 180) / Math.PI;
      const angleEfficiency = Math.max(0.4, Math.sin(2 * angleRad));
      return { y0, slope, angleRad, angleDeg, angleEfficiency };
    }

    function evaluatePullUpCalculus(t) {
      const omega = 3.6;
      const h = Math.sin(omega * t);
      const v = omega * Math.cos(omega * t);
      const isNearPeak = Math.abs(v) >= 0.8 * omega;
      return { h, v, omega, isNearPeak };
    }

    function updateRampSlider(val) {
      state.rampX0 = parseFloat(val);
      const ramp = evaluateRampCalculus(state.rampX0);
      document.getElementById('rampXVal').textContent = state.rampX0.toFixed(2);
      document.getElementById('rampSlopeVal').textContent = `${ramp.slope.toFixed(2)} (${ramp.angleDeg.toFixed(0)}°)`;
      if (typeof update3DRampVisuals === 'function') {
        update3DRampVisuals();
      }
    }

    function togglePauseWave() {
      state.wavePaused = !state.wavePaused;
      const btn = document.getElementById('pauseWaveBtn');
      btn.textContent = state.wavePaused ? '▶ Resume t' : '⏸ Pause t';
      btn.className = state.wavePaused
        ? 'bg-amber-400 text-black text-[10px] font-extrabold px-2 py-0.5 rounded border border-black'
        : 'bg-gray-800 hover:bg-gray-700 text-white text-[10px] font-bold px-2 py-0.5 rounded border border-gray-600';
    }

    function toggleMinimizeCalcHUD(minimize) {
      const minBar = document.getElementById('calcMinimizedBar');
      const expPan = document.getElementById('calcExpandedPanel');
      if (minimize) {
        expPan.classList.add('hidden');
        minBar.classList.remove('hidden');
        minBar.classList.add('flex');
      } else {
        minBar.classList.add('hidden');
        minBar.classList.remove('flex');
        expPan.classList.remove('hidden');
        resizeOscilloscope();
      }
    }

    function saveWorkedExampleTelemetry(th) {
      state.lastWorkedExample = {
        foodName: th.food.name,
        formulaStr: th.food.formulaStr,
        derivStr: th.food.derivStr,
        t0: th.t0,
        posVal: th.calc.pos,
        derivVal: th.calc.deriv,
        maxDeriv: th.calc.maxDeriv,
        derivRatio: Math.abs(th.calc.deriv) / (th.calc.maxDeriv || 1),
        rampX0: state.rampX0,
        rampSlope: th.ramp.slope,
        angleDeg: th.ramp.angleDeg,
        isCritical: th.isCriticalPoint,
        isSurge: th.isMaxDerivSurge,
        distance: th.distance,
        animal: th.chosenAnimal,
        size: th.chosenSize,
        mutation: th.chosenMutation,
        odds: th.totalOdds,
        income: th.finalIncome
      };
      renderWorkedExampleModal();
    }

    function renderWorkedExampleModal() {
      const c = document.getElementById('workedExampleDetails');
      if (!c) return;
      const w = state.lastWorkedExample;
      if (!w) {
        c.innerHTML = '<div class="text-gray-400">Step onto the Launch Line and tap throw to capture real-time differential calculus telemetry!</div>';
        return;
      }
      c.innerHTML = `
        <div class="text-yellow-400 font-extrabold border-b border-gray-700 pb-1">
          📊 TELEMETRY: Throw #${state.throwCount} (${w.foodName})
        </div>
        <div><strong>Time of Launch:</strong> t₀ = ${w.t0.toFixed(3)} s</div>
        <div><strong>Position Function:</strong> ${w.formulaStr} = <span class="text-cyan-400">${w.posVal.toFixed(3)}</span></div>
        <div><strong>Instantaneous Derivative:</strong> ${w.derivStr} = <span class="text-amber-400 font-bold">${w.derivVal.toFixed(3)}</span></div>
        <div><strong>Ramp Tangent Line:</strong> y(x) = 2sin(x) ⟹ m = y'(${w.rampX0.toFixed(2)}) = 2cos(${w.rampX0.toFixed(2)}) = <span class="text-emerald-400 font-bold">${w.rampSlope.toFixed(3)}</span> (Launch θ = ${w.angleDeg.toFixed(1)}°)</div>
        <div class="my-1 border-t border-gray-800 pt-1">
          <strong>Calculus Strategy Evaluation:</strong><br>
          • Derivative Ratio: |P'(t₀)| / Max = ${(w.derivRatio * 100).toFixed(1)}%<br>
          • Critical Point Test (P' ≈ 0): ${w.isCritical ? '<span class="text-yellow-400 font-bold">CRITICAL EXTREMUM DETECTED (Guaranteed 5x-25x Mutation!)</span>' : 'None'}<br>
          • Max Surge Test (|P'| ≥ 82%): ${w.isSurge ? '<span class="text-cyan-400 font-bold">DERIVATIVE VELOCITY SURGE (+30% Distance!)</span>' : 'Standard'}
        </div>
        <div class="border-t border-gray-800 pt-1 text-lime-400">
          <strong>Outcome:</strong> Final Ballistic Distance = <strong>${w.distance.toFixed(1)}m</strong> ⟹ Caught <strong>${w.size ? w.size.name.toUpperCase() : ''} ${w.mutation.name} ${w.animal.name}</strong> (Rarity: 1 in ${formatNum(w.odds || 10)}) earning <strong>$${formatNum(w.income)}/s</strong>!
        </div>
      `;
    }
"""
