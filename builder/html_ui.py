# -*- coding: utf-8 -*-

HTML_UI = """
  <!-- 3D THREE.JS WEBGL VIEWPORT -->
  <div id="webglContainer" class="absolute inset-0 w-full h-full z-0"></div>

  <!-- 3D FLOATING LABELS CONTAINER (PLOT PETS, INCOME POPUPS & STATIONS) -->
  <div id="labelsContainer" class="absolute inset-0 pointer-events-none z-10 overflow-hidden"></div>

  <!-- TOP NAVIGATION BAR: TITLE, QUICK-WALK TELEPORTS & SHORTCUTS -->
  <div class="fixed top-2 left-1/2 -translate-x-1/2 z-20 flex flex-wrap items-center justify-center gap-1.5 sm:gap-2 w-[98%] max-w-5xl pointer-events-none">
    
    <!-- Title & Math Pill -->
    <div class="bg-gray-900/95 border-2 border-black rounded-2xl px-3 py-1 flex items-center gap-2 shadow-xl pointer-events-auto">
      <span class="text-yellow-400 font-extrabold text-xs sm:text-base rblx-stroke-sm">🥕 THROW FOOD 3D</span>
      <span class="hidden sm:inline-block bg-cyan-400 text-black text-[10px] font-extrabold px-2 py-0.5 rounded-full border border-black shadow">
        MATH 101 CALCULUS
      </span>
    </div>

    <!-- Quick-Walk Station Teleport Bar -->
    <div class="bg-gray-900/95 border-2 border-black rounded-2xl p-1 flex items-center gap-1 shadow-xl pointer-events-auto">
      <button onclick="walkToStation('throw')" class="rblx-btn bg-amber-500 hover:bg-amber-400 text-black font-extrabold text-[10px] sm:text-xs px-2.5 py-1 rounded-xl">
        🎯 Throw Line
      </button>
      <button onclick="walkToStation('pullup')" class="rblx-btn bg-sky-400 hover:bg-sky-300 text-black font-extrabold text-[10px] sm:text-xs px-2.5 py-1 rounded-xl">
        🏋️ Pull-Up Bar
      </button>
      <button onclick="walkToStation('shop')" class="rblx-btn bg-blue-500 hover:bg-blue-400 text-white font-extrabold text-[10px] sm:text-xs px-2.5 py-1 rounded-xl rblx-stroke-sm">
        🛒 Food Shop
      </button>
      <button onclick="walkToStation('sell')" class="rblx-btn bg-rose-500 hover:bg-rose-400 text-white font-extrabold text-[10px] sm:text-xs px-2.5 py-1 rounded-xl rblx-stroke-sm">
        💰 Sell Stall
      </button>
      <button onclick="walkToStation('plot')" class="rblx-btn bg-emerald-500 hover:bg-emerald-400 text-black font-extrabold text-[10px] sm:text-xs px-2.5 py-1 rounded-xl">
        🏡 My Plot
      </button>
    </div>

    <!-- Teacher God-Mode Demo Pill (For live presentations) -->
    <button onclick="activateTeacherGodMode()" title="Instant End-Game Preview for Professors Aquino & Gatdula" class="rblx-btn bg-gradient-to-r from-amber-400 to-yellow-300 hover:from-amber-300 hover:to-yellow-200 text-black font-black text-[10px] sm:text-xs px-2.5 py-1 rounded-xl pointer-events-auto flex items-center gap-1">
      <span>👨‍🏫 DEMO MODE</span>
    </button>

    <!-- Equipped Bait Pill -->
    <div onclick="openModal('shopModal')" title="Click to change bait in Food Shop" class="cursor-pointer bg-purple-700/95 hover:bg-purple-600 border-2 border-black rounded-2xl px-2.5 py-1 flex items-center gap-1.5 shadow-xl pointer-events-auto">
      <span id="hudFoodIcon" class="text-base sm:text-lg">🥕</span>
      <div class="leading-tight">
        <div id="hudFoodName" class="text-white font-extrabold text-[11px] sm:text-xs rblx-stroke-sm">Carrot</div>
        <div id="hudFoodFunc" class="text-[9px] sm:text-[10px] text-yellow-300 mono-math font-bold">P(t)=2sin(1.2t)</div>
      </div>
    </div>
  </div>

  <!-- CURRENT ZONE BANNER NOTIFIER -->
  <div id="zoneBanner" class="fixed top-14 sm:top-16 left-1/2 -translate-x-1/2 z-20 pointer-events-none transition-all duration-200">
    <div class="bg-black/75 backdrop-blur-md border-2 border-white/30 text-white px-4 py-1 rounded-full text-xs sm:text-sm font-bold flex items-center gap-2 shadow-2xl">
      <span id="zoneBannerIcon">🏃</span>
      <span id="zoneBannerText">Walk to the Orange Checkered Launch Line to Throw Food!</span>
    </div>
  </div>

  <!-- LEFT HUD: SIDEBAR ICONS (INDEX, SHOP, ANIMALS, CALC LAB) & STATS -->
  <div class="fixed left-2 sm:left-3 top-1/2 -translate-y-1/2 z-20 flex flex-col gap-2.5">
    
    <!-- Index Button (Matching Screenshot 75) -->
    <button onclick="openModal('indexModal')" class="rblx-btn bg-gradient-to-b from-blue-500 to-blue-700 w-14 h-14 sm:w-16 sm:h-16 rounded-2xl flex flex-col items-center justify-center relative group">
      <span class="text-xl sm:text-2xl group-hover:scale-110 transition-transform">📘</span>
      <span class="text-white font-extrabold text-[10px] sm:text-xs rblx-stroke-sm">Index</span>
      <span id="indexBadge" class="absolute -top-1.5 -right-1.5 bg-yellow-400 text-black font-extrabold text-[9px] px-1.5 py-0.2 rounded-full border-2 border-black shadow">0/18</span>
      <span id="indexRewardDot" class="hidden absolute -bottom-1.5 -right-1.5 bg-lime-400 text-black font-extrabold text-[9px] px-1.5 rounded-full border-2 border-black animate-bounce shadow">🎁!</span>
    </button>

    <!-- Shop Button (Matching Screenshot 75) -->
    <button onclick="openModal('shopModal')" class="rblx-btn bg-gradient-to-b from-red-500 to-red-700 w-14 h-14 sm:w-16 sm:h-16 rounded-2xl flex flex-col items-center justify-center relative group">
      <span class="text-xl sm:text-2xl group-hover:scale-110 transition-transform">🧺</span>
      <span class="text-white font-extrabold text-[10px] sm:text-xs rblx-stroke-sm">Shop</span>
    </button>

    <!-- Animals / Plot Button (Matching Screenshot 75 & 80) -->
    <button onclick="openModal('animalsModal')" class="rblx-btn bg-gradient-to-b from-orange-400 to-amber-700 w-14 h-14 sm:w-16 sm:h-16 rounded-2xl flex flex-col items-center justify-center relative group">
      <span class="text-xl sm:text-2xl group-hover:scale-110 transition-transform">🐾</span>
      <span class="text-white font-extrabold text-[10px] sm:text-xs rblx-stroke-sm">Animals</span>
      <span id="plotCountBadge" class="absolute -top-1.5 -right-1.5 bg-lime-400 text-black font-extrabold text-[9px] px-1.5 rounded-full border-2 border-black shadow">0/5</span>
    </button>

    <!-- Calculus Lab & Worked Example Button (For Engr. Aquino & Gatdula) -->
    <button onclick="openModal('calcLabModal')" class="rblx-btn bg-gradient-to-b from-indigo-500 to-purple-800 w-14 h-14 sm:w-16 sm:h-16 rounded-2xl flex flex-col items-center justify-center relative group">
      <span class="text-xl sm:text-2xl group-hover:scale-110 transition-transform">📐</span>
      <span class="text-white font-extrabold text-[10px] sm:text-xs rblx-stroke-sm">MATH 101</span>
    </button>

    <!-- Canyon Wall Best Catches Quick Button -->
    <button onclick="openModal('leaderboardModal')" class="rblx-btn bg-gradient-to-b from-yellow-500 to-amber-700 w-14 h-14 sm:w-16 sm:h-16 rounded-2xl flex flex-col items-center justify-center relative group">
      <span class="text-xl sm:text-2xl group-hover:scale-110 transition-transform">🏆</span>
      <span class="text-white font-extrabold text-[10px] sm:text-xs rblx-stroke-sm">Best</span>
    </button>
  </div>

  <!-- BOTTOM-LEFT STATS: MUSCLE STRENGTH & CASH DISPLAY -->
  <div class="fixed bottom-3 left-3 z-20 flex flex-col gap-1.5 pointer-events-auto">
    <!-- Strength Pill with Muscle Icon, Number, Bonus & Settings Gear ⚙️ -->
    <div class="flex items-center gap-2 bg-black/75 backdrop-blur-sm border-2 border-black rounded-2xl px-3 py-1 shadow-2xl">
      <span class="text-2xl sm:text-3xl filter drop-shadow">💪</span>
      <div class="leading-none">
        <div class="flex items-center gap-1.5">
          <span id="strengthDisplay" class="text-sky-400 font-extrabold text-lg sm:text-2xl rblx-stroke-sm">18</span>
          <button onclick="openModal('settingsModal')" title="Open Settings" class="text-slate-400 hover:text-white transition-colors p-0.5">
            <span class="text-sm sm:text-base">⚙️</span>
          </button>
        </div>
        <div id="indexBonusDisplay" class="text-[9px] text-amber-300 font-bold">+0 Index Bonus</div>
      </div>
    </div>

    <!-- Cash Pill with Money Icon, Cash Amount & $/s Passive Rate -->
    <div class="flex items-center gap-2 bg-black/75 backdrop-blur-sm border-2 border-black rounded-2xl px-3 py-1 shadow-2xl">
      <span class="text-2xl sm:text-3xl filter drop-shadow">💵</span>
      <div class="leading-none">
        <div id="cashDisplay" class="text-lime-400 font-extrabold text-lg sm:text-2xl rblx-stroke-sm">$0</div>
        <div id="incomeRateDisplay" class="text-[10px] text-lime-200 font-bold">+$0/s (Plot)</div>
      </div>
    </div>
  </div>

  <!-- VIRTUAL ON-SCREEN JOYSTICK FOR MOBILE / TABLET NAVIGATION -->
  <div id="joystickZone" class="fixed bottom-4 left-36 sm:left-44 z-20 w-28 h-28 sm:w-32 sm:h-32 rounded-full bg-black/40 border-3 border-white/30 backdrop-blur-sm flex items-center justify-center touch-none">
    <div id="joystickKnob" class="w-12 h-12 rounded-full bg-white/85 border-3 border-black shadow-xl pointer-events-none transition-transform duration-75"></div>
  </div>

  <!-- MINIMIZABLE LIVE TRIGONOMETRIC DERIVATIVE HUD (BOTTOM CENTER) -->
  <!-- 1) Minimized Pill Bar -->
  <div id="calcMinimizedBar" class="fixed bottom-3 left-1/2 -translate-x-1/2 z-20 hidden pointer-events-auto">
    <button onclick="toggleMinimizeCalcHUD(false)" class="rblx-btn bg-gray-900/95 border-2 border-black text-white px-4 py-1.5 rounded-full flex items-center gap-2 shadow-2xl">
      <span class="text-cyan-400 font-extrabold text-xs">📈 Expand Calculus HUD</span>
      <span class="text-gray-400 text-xs">|</span>
      <span id="minDerivReadout" class="mono-math text-amber-300 font-bold text-xs">P'(t) = +2.40</span>
      <span class="text-gray-400 text-xs">|</span>
      <span id="minSlopeReadout" class="mono-math text-emerald-300 font-bold text-xs">m = 1.00 (45°)</span>
    </button>
  </div>

  <!-- 2) Expanded Calculus Oscilloscope Panel -->
  <div id="calcExpandedPanel" class="fixed bottom-3 left-1/2 -translate-x-1/2 z-20 w-[94%] max-w-xl bg-gray-900/95 border-3 border-black rounded-2xl p-2.5 sm:p-3 shadow-2xl pointer-events-auto transition-all">
    <!-- Panel Header: Title, Minimizer, Pause & Status Badges -->
    <div class="flex items-center justify-between gap-1 pb-1.5 border-b border-gray-700">
      <div class="flex items-center gap-2">
        <span class="text-cyan-400 font-extrabold text-xs sm:text-sm rblx-stroke-sm">📈 Live Derivative Oscilloscope</span>
        <span id="calcRegimeBadge" class="text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-lime-400 text-black shadow">MAX SURGE</span>
      </div>
      <div class="flex items-center gap-1.5">
        <button onclick="togglePauseWave()" id="pauseWaveBtn" class="bg-gray-800 hover:bg-gray-700 text-white text-[10px] font-bold px-2 py-0.5 rounded border border-gray-600 transition-colors">
          ⏸ Pause t
        </button>
        <button onclick="toggleMinimizeCalcHUD(true)" class="bg-rose-600 hover:bg-rose-500 text-white text-[10px] font-extrabold px-2 py-0.5 rounded border border-black transition-colors" title="Minimize Oscilloscope">
          — Minimize
        </button>
      </div>
    </div>

    <!-- Live Oscilloscope HTML5 Canvas -->
    <div class="relative w-full h-20 sm:h-24 bg-black/80 rounded-xl my-1.5 overflow-hidden border border-gray-700">
      <canvas id="oscCanvas" class="w-full h-full block"></canvas>
      <div class="absolute top-1 left-2 pointer-events-none flex items-center gap-2 text-[9px] mono-math font-bold">
        <span class="text-cyan-400">● P(t) Position Wave</span>
        <span class="text-amber-400">● P'(t) Derivative Velocity</span>
        <span class="text-pink-400">● Tangent Slope</span>
      </div>
      <div id="critPointIndicator" class="hidden absolute top-1 right-2 pointer-events-none text-[9px] font-extrabold text-yellow-300 bg-yellow-950/80 px-2 py-0.5 rounded border border-yellow-500">
        🎯 CRITICAL POINT (P' ≈ 0)
      </div>
    </div>

    <!-- Dynamic Calculus Mathematical Formulas & Tangent Angle Controls -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-1.5 text-[10px] sm:text-xs">
      <div class="bg-gray-800/80 p-1.5 rounded-xl border border-gray-700">
        <div id="livePosEq" class="text-cyan-300 font-bold truncate">P(t) = 2sin(1.2t) = +0.00</div>
        <div id="liveDerivEq" class="text-amber-300 font-bold truncate">P'(t) = 2.4cos(1.2t) = +2.40</div>
      </div>
      <div class="bg-gray-800/80 p-1.5 rounded-xl border border-gray-700 flex flex-col justify-center">
        <div class="flex items-center justify-between text-[10px] leading-tight">
          <span>Ramp <span class="mono-math text-pink-300">x₀=<span id="rampXVal">1.05</span> rad</span></span>
          <span class="mono-math text-emerald-300">m = 2cos(x₀) = <span id="rampSlopeVal">1.00</span> (45°)</span>
        </div>
        <input id="rampSlider" type="range" min="0.1" max="1.45" step="0.01" value="1.05"
          oninput="updateRampSlider(this.value)"
          class="w-full h-1.5 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-emerald-400 mt-1" />
      </div>
    </div>
  </div>

  <!-- THROW HUD (ACTIVE ONLY ON LAUNCH LINE) -->
  <div id="throwZoneHUD" class="fixed right-3 bottom-3 z-20 hidden items-end gap-2.5 pointer-events-auto">
    <!-- Vertical Harmonic Derivative Throw Meter -->
    <div class="flex flex-col items-center">
      <div class="relative w-10 sm:w-12 h-56 sm:h-64 rounded-full border-4 border-black p-1 shadow-2xl flex flex-col justify-between overflow-hidden"
           style="background: linear-gradient(to top, #ef4444 0%, #f97316 25%, #eab308 50%, #84cc16 75%, #22c55e 100%);">
        <div class="w-full h-[3px] bg-black/60 my-auto"></div>
        <div class="w-full h-[3px] bg-black/60 my-auto"></div>
        <div class="w-full h-[3px] bg-black/60 my-auto"></div>
        <div class="w-full h-[3px] bg-black/60 my-auto"></div>
        
        <div id="meterMarker" class="absolute left-0 right-0 h-4 bg-white rounded-full border-2 border-black shadow-lg" style="top: 50%;"></div>
      </div>
      <div id="meterReadout" class="mt-1 text-white font-extrabold text-sm sm:text-base rblx-stroke">+12</div>
    </div>

    <!-- Big Action Buttons & Auto-Skip Toggle -->
    <div class="flex flex-col gap-2">
      <!-- Strategy Badges -->
      <div class="flex flex-col gap-1">
        <div id="badgeCritStatus" class="bg-black/80 border-2 border-yellow-400 rounded-xl px-2.5 py-0.5 text-[10px] text-yellow-300 font-extrabold shadow flex items-center justify-between">
          <span>🎯 CRITICAL POINT (P'≈0):</span>
          <span class="text-yellow-400 font-bold">MUTATION SURGE</span>
        </div>
        <div id="badgeSurgeStatus" class="bg-black/80 border-2 border-cyan-400 rounded-xl px-2.5 py-0.5 text-[10px] text-cyan-300 font-extrabold shadow flex items-center justify-between">
          <span>⚡ MAX SURGE (|P'|=Max):</span>
          <span class="text-cyan-400 font-bold">+35% DISTANCE</span>
        </div>
      </div>

      <!-- Main "TAP TO THROW!" Button -->
      <button onclick="executeCalculusThrow()" id="throwActionBtn" class="rblx-btn bg-gradient-to-b from-yellow-300 via-amber-400 to-amber-500 hover:from-yellow-200 hover:to-amber-400 text-black font-extrabold text-lg sm:text-2xl px-6 sm:px-8 py-3 sm:py-4 rounded-3xl rblx-stroke-sm shadow-2xl flex flex-col items-center leading-none">
        <span>TAP TO THROW!</span>
        <span class="text-[10px] sm:text-xs font-bold text-gray-900 mt-1">or press SPACE</span>
      </button>

      <!-- Auto-Skip Repeat Catches Grind Toggle -->
      <label class="flex items-center gap-2 bg-black/75 border-2 border-black rounded-xl px-2.5 py-1 cursor-pointer shadow">
        <input id="autoSkipCheckbox" type="checkbox" onchange="toggleAutoSkipRepeats(this.checked)" class="w-4 h-4 accent-amber-400 rounded">
        <span class="text-[10px] sm:text-xs text-white font-bold select-none">Auto-Skip Repeat Cutscenes</span>
      </label>
    </div>
  </div>

  <!-- PULL-UP BAR HUD (MATCHING SCREENSHOT 78) -->
  <div id="pullUpZoneHUD" class="fixed inset-x-0 bottom-4 z-20 hidden flex-col items-center gap-2 pointer-events-auto">
    <button onclick="exitPullUpStation()" class="rblx-btn bg-red-600 hover:bg-red-500 text-white font-extrabold text-base sm:text-xl px-8 py-2 rounded-2xl rblx-stroke-sm shadow-2xl">
      STOP
    </button>

    <div class="w-[92%] max-w-md bg-black/85 border-3 border-black rounded-2xl p-2.5 shadow-2xl flex flex-col gap-1.5">
      <div class="flex items-center justify-between text-xs sm:text-sm font-extrabold text-white rblx-stroke-sm">
        <span id="pullUpLevelTitle">Level 1</span>
        <span id="pullUpXpFraction">4/5</span>
      </div>
      <div class="w-full h-4 bg-gray-950 rounded-full border-2 border-black overflow-hidden relative">
        <div id="pullUpProgressBar" class="h-full bg-gradient-to-r from-blue-600 to-sky-400 transition-all duration-100" style="width: 80%;"></div>
      </div>
      <button onclick="doCalculusPullUpRep()" class="rblx-btn bg-gradient-to-r from-sky-400 to-blue-500 hover:from-sky-300 hover:to-blue-400 text-black font-black text-xs sm:text-sm py-1.5 rounded-xl mt-1">
        🏋️ PULL UP! (Tap Near Peak Velocity h'(t) for 2x XP)
      </button>
    </div>
  </div>

  <!-- 3D FLIGHT TRACKING OVERLAY & SKIP BUTTON (MATCHING RECORDING 003051) -->
  <div id="flightOverlay" class="fixed inset-0 pointer-events-none z-30 hidden flex-col justify-between p-4 sm:p-6">
    <!-- Top Center Dark Translucent Pill Banner (from video) -->
    <div class="self-center flex flex-col items-center gap-1">
      <div class="bg-black/85 border-3 border-black rounded-3xl px-8 py-2.5 shadow-2xl flex flex-col items-center min-w-[240px]">
        <!-- Luck Multiplier with bold stroke (from video: e.g. 19.09X LUCK) -->
        <div id="flightLuckMult" class="text-rose-500 font-black text-3xl sm:text-4xl rblx-stroke-lg tracking-wide leading-none">
          19.09X
        </div>
        <div class="text-white font-black text-xs sm:text-sm tracking-widest mt-0.5">LUCK</div>
      </div>
      <!-- Biome Name Translucent Banner (from video: e.g. Forest 🌲, Savanna 🌾, Desert 🏜️) -->
      <div class="bg-black/60 border border-white/20 rounded-full px-5 py-1 backdrop-blur-sm flex items-center gap-2 shadow-lg">
        <span id="flightBiomeIcon" class="text-lg">🌲</span>
        <span id="flightBiomeName" class="text-white font-black text-xs sm:text-sm rblx-stroke-sm">Forest</span>
        <span class="text-gray-400 text-xs">|</span>
        <span id="flightDistReadout" class="text-yellow-400 font-extrabold text-xs sm:text-sm mono-math">0.0m</span>
      </div>
    </div>

    <!-- Skippable Flight Button -->
    <div class="self-center pointer-events-auto mb-4">
      <button id="skipFlightBtn" onclick="skipThrowAnimation()" class="rblx-btn bg-amber-400 hover:bg-amber-300 text-black font-extrabold text-sm sm:text-base px-8 py-2.5 rounded-2xl shadow-2xl flex items-center gap-1.5">
        <span>⏭ SKIP ANIMATION</span>
      </button>
    </div>
  </div>

  <!-- 3D CATCH REVEAL CUTSCENE MODAL (EXACT REPLICATION OF RECORDING 003051) -->
  <div id="catchRevealModal" onclick="handleCatchRevealTap()" class="fixed inset-0 comic-vignette z-40 hidden flex-col items-center justify-between py-6 px-4 cursor-pointer select-none">
    
    <!-- Top Center Header with Starburst Rays & Rolling Odds Slot (Matching Video) -->
    <div class="relative w-full flex flex-col items-center justify-center pt-2">
      <!-- Spinning Starburst Rays Background -->
      <div id="cutsceneStarburst" class="starburst-rays"></div>

      <!-- Celebratory Rarity Banner (e.g. SUPER LUCKY!, LUCKY!, NICE CATCH!) -->
      <div id="catchRarityHeader" class="text-rose-500 font-black text-3xl sm:text-5xl rblx-stroke-lg tracking-wide transform -rotate-1 relative z-10 animate-bounce">
        SUPER LUCKY!
      </div>

      <!-- Rolling Exact Odds Slot (from video: e.g. 1 in 1 -> rolls to 1 in 51) -->
      <div id="catchOddsNumber" class="text-white font-black text-4xl sm:text-6xl rblx-stroke-lg tracking-tight mt-1 relative z-10">
        1 in 51
      </div>
    </div>

    <!-- Center is transparent for Three.js 3D camera zooming into the animal eating food! -->
    <div class="flex-1 w-full flex items-center justify-center"></div>

    <!-- Bottom Center Mystery Hangman Name Reveal & Badges (Matching Video) -->
    <div class="flex flex-col items-center gap-1 text-center pointer-events-auto" onclick="event.stopPropagation()">
      
      <!-- Mutation Tag (Above Animal Name, e.g. GOLD, RAINBOW, COSMIC) -->
      <div id="catchMutationTag" class="text-yellow-400 font-black text-sm sm:text-lg rblx-stroke-sm tracking-wider uppercase">
        GOLD
      </div>

      <!-- Huge Cartoon Animal Name with Mystery Letter-by-Letter Slot Reveal -->
      <div id="catchAnimalName" class="text-white font-black text-3xl sm:text-6xl rblx-stroke-lg tracking-wider">
        DIMETRODON
      </div>

      <!-- Size Tag (Below Animal Name, e.g. REGULAR, BIG, TITANIC, COLOSSAL) -->
      <div id="catchSizeTag" class="text-sky-300 font-black text-base sm:text-2xl rblx-stroke-sm tracking-wide uppercase">
        BIG
      </div>

      <!-- Income Rate Popup (e.g. $56T/s or +$300/s) -->
      <div id="catchIncomeRate" class="text-lime-400 font-black text-2xl sm:text-4xl rblx-stroke-sm tracking-wide mt-0.5">
        +$300/s
      </div>

      <!-- Prompt: tap to continue -->
      <div id="catchTapPrompt" class="text-white/80 font-bold text-xs sm:text-sm tracking-wide mt-1 animate-pulse">
        tap to continue
      </div>
    </div>
  </div>

  <!-- "NEW FOOD UNLOCKED!" POPUP MODAL (SCREENSHOT 81) -->
  <div id="newFoodModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden items-center justify-center p-4">
    <div class="bg-gray-950 border-4 border-black rounded-3xl w-full max-w-sm overflow-hidden shadow-2xl flex flex-col">
      <div class="rblx-modal-header px-4 py-2 flex items-center justify-between">
        <span class="text-white font-extrabold text-sm sm:text-base rblx-stroke-sm">NEW FOOD UNLOCKED!</span>
        <button onclick="closeModal('newFoodModal')" class="rblx-btn bg-red-600 hover:bg-red-500 text-white font-black text-xs px-2 py-0.5 rounded-lg">✕</button>
      </div>
      <div class="p-6 flex items-center gap-4 bg-gray-900">
        <div id="newFoodIconBox" class="w-20 h-20 bg-gray-800 rounded-2xl border-3 border-black flex items-center justify-center text-4xl shadow-inner">
          🍌
        </div>
        <div class="flex-1">
          <div class="text-gray-400 text-xs font-bold">YOU CAN NOW BUY</div>
          <div id="newFoodTitle" class="text-white font-extrabold text-xl sm:text-2xl rblx-stroke-sm">BANANA</div>
          <div id="newFoodCost" class="text-lime-400 font-extrabold text-sm sm:text-base">$150</div>
        </div>
      </div>
      <div class="p-4 bg-gray-950 flex justify-end border-t border-gray-800">
        <button onclick="closeModal('newFoodModal'); openModal('shopModal')" class="rblx-btn bg-lime-400 hover:bg-lime-300 text-black font-extrabold text-base px-6 py-2 rounded-2xl">
          SHOP
        </button>
      </div>
    </div>
  </div>

  <!-- SETTINGS MODAL (SCREENSHOT 82) -->
  <div id="settingsModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden items-center justify-center p-4">
    <div class="bg-gray-900 border-4 border-black rounded-3xl w-full max-w-md overflow-hidden shadow-2xl flex flex-col">
      <div class="bg-gradient-to-r from-gray-700 to-gray-800 px-4 py-2.5 border-b-3 border-black flex items-center justify-between">
        <span class="text-white font-extrabold text-base sm:text-lg rblx-stroke-sm">Settings</span>
        <button onclick="closeModal('settingsModal')" class="rblx-btn bg-red-600 hover:bg-red-500 text-white font-black text-xs px-2.5 py-0.5 rounded-xl">✕</button>
      </div>
      <div class="p-5 flex flex-col gap-4 text-white text-sm sm:text-base font-bold">
        <div class="flex items-center justify-between gap-3">
          <span class="w-20">Music</span>
          <input id="musicSlider" type="range" min="0" max="100" value="70" oninput="setMusicVolume(this.value)" class="flex-1 h-3 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-sky-400">
          <span id="musicVolLabel" class="w-12 text-right mono-math">70%</span>
        </div>
        <div class="flex items-center justify-between gap-3">
          <span class="w-20">SFX</span>
          <input id="sfxSlider" type="range" min="0" max="100" value="85" oninput="setSfxVolume(this.value)" class="flex-1 h-3 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-sky-400">
          <span id="sfxVolLabel" class="w-12 text-right mono-math">85%</span>
        </div>
        <div class="flex items-center justify-between">
          <span>View Others Pets</span>
          <div class="flex items-center gap-2">
            <span id="viewOthersLabel" class="text-xs text-lime-400">ON</span>
            <input type="checkbox" id="viewOthersToggle" checked onchange="toggleViewOthersPets(this.checked)" class="w-6 h-6 accent-lime-400 cursor-pointer">
          </div>
        </div>
        <div class="flex items-center justify-between">
          <span>View Your Pets</span>
          <div class="flex items-center gap-2">
            <span id="viewYoursLabel" class="text-xs text-lime-400">ON</span>
            <input type="checkbox" id="viewYoursToggle" checked onchange="toggleViewYourPets(this.checked)" class="w-6 h-6 accent-lime-400 cursor-pointer">
          </div>
        </div>
        <hr class="border-gray-700 my-1">
        <div class="flex items-center justify-between gap-2">
          <button onclick="activateTeacherGodMode(); closeModal('settingsModal')" class="rblx-btn bg-amber-400 hover:bg-amber-300 text-black font-extrabold text-xs px-3 py-2 rounded-xl flex-1">
            👨‍🏫 God-Mode Demo
          </button>
          <button onclick="resetPlayerProgress()" class="rblx-btn bg-gray-700 hover:bg-gray-600 text-rose-300 font-extrabold text-xs px-3 py-2 rounded-xl">
            Reset Data
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- FOOD SHOP MODAL -->
  <div id="shopModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden items-center justify-center p-3 sm:p-4">
    <div class="bg-gray-900 border-4 border-black rounded-3xl w-full max-w-2xl max-h-[90vh] flex flex-col overflow-hidden shadow-2xl">
      <div class="rblx-modal-header px-4 py-2.5 flex items-center justify-between">
        <span class="text-white font-extrabold text-base sm:text-lg rblx-stroke-sm">Food Shop</span>
        <button onclick="closeModal('shopModal')" class="rblx-btn bg-red-600 hover:bg-red-500 text-white font-black text-xs px-2.5 py-0.5 rounded-xl">✕</button>
      </div>
      <div class="p-3 sm:p-4 overflow-y-auto flex-1 flex flex-col gap-3">
        <div id="foodShopGrid" class="grid grid-cols-2 sm:grid-cols-3 gap-2.5 sm:gap-3"></div>
        <!-- Plot Expansion Upgrade Card (Starts 5, Max 20 Pets) -->
        <div class="bg-gray-800 border-2 border-black rounded-2xl p-3 flex flex-wrap items-center justify-between gap-2 shadow-lg">
          <div class="flex items-center gap-2">
            <span class="text-2xl">🏡</span>
            <div>
              <div class="text-white font-extrabold text-xs sm:text-sm">Expand Lawn Plot Capacity</div>
              <div class="text-gray-400 text-[10px]">Hold up to 20 pets on your fenced yard!</div>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <span id="shopPlotCapText" class="text-yellow-400 font-extrabold text-xs sm:text-sm">5/20</span>
            <button id="upgradePlotBtn" onclick="upgradePlotCapacity()" class="rblx-btn bg-lime-400 hover:bg-lime-300 text-black font-extrabold text-xs px-3 py-1.5 rounded-xl">
              UPGRADE ($100)
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- SELL STALL MODAL -->
  <div id="sellModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden items-center justify-center p-3 sm:p-4">
    <div class="bg-gray-900 border-4 border-black rounded-3xl w-full max-w-xl max-h-[85vh] flex flex-col overflow-hidden shadow-2xl">
      <div class="bg-gradient-to-r from-red-600 to-rose-700 px-4 py-2.5 border-b-3 border-black flex items-center justify-between">
        <span class="text-white font-extrabold text-base sm:text-lg rblx-stroke-sm">Sell Stall</span>
        <button onclick="closeModal('sellModal')" class="rblx-btn bg-red-600 hover:bg-red-500 text-white font-black text-xs px-2.5 py-0.5 rounded-xl">✕</button>
      </div>
      <div class="p-3 sm:p-4 flex-1 overflow-y-auto flex flex-col gap-2.5">
        <div class="flex items-center justify-between bg-gray-800/80 p-2.5 rounded-2xl border border-gray-700">
          <span class="text-xs text-gray-300">Sell duplicate or unequipped pets for instant cash!</span>
          <button onclick="sellAllUnequipped()" class="rblx-btn bg-rose-500 hover:bg-rose-400 text-white font-extrabold text-xs px-3 py-1 rounded-xl">
            SELL ALL UNEQUIPPED
          </button>
        </div>
        <div id="sellListGrid" class="grid grid-cols-1 sm:grid-cols-2 gap-2"></div>
      </div>
    </div>
  </div>

  <!-- "MY ANIMALS" MODAL (MATCHING SCREENSHOT 80) -->
  <div id="animalsModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden items-center justify-center p-3 sm:p-4">
    <div class="bg-gray-900 border-4 border-black rounded-3xl w-full max-w-md max-h-[90vh] flex flex-col overflow-hidden shadow-2xl">
      <div class="rblx-modal-header px-4 py-2.5 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="text-white font-extrabold text-base sm:text-lg rblx-stroke-sm">My Animals</span>
          <span id="animalsPlotBadge" class="bg-lime-400 text-black font-extrabold text-xs px-2 py-0.5 rounded-full border border-black">0/5</span>
        </div>
        <button onclick="closeModal('animalsModal')" class="rblx-btn bg-red-600 hover:bg-red-500 text-white font-black text-xs px-2.5 py-0.5 rounded-xl">✕</button>
      </div>
      <div class="p-3 overflow-y-auto flex-1 flex flex-col gap-2" id="myAnimalsList"></div>
      <div class="p-3 bg-gray-950 border-t border-gray-800 flex justify-center">
        <button onclick="equipBestAnimals()" class="rblx-btn bg-gradient-to-r from-yellow-400 to-amber-500 hover:from-yellow-300 hover:to-amber-400 text-black font-black text-lg px-8 py-3 rounded-2xl w-full shadow-2xl">
          EQUIP BEST
        </button>
      </div>
    </div>
  </div>

  <!-- ANIMAL INDEX MODAL (MATCHING SCREENSHOT 73) -->
  <div id="indexModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden items-center justify-center p-3 sm:p-4">
    <div class="bg-gray-900 border-4 border-black rounded-3xl w-full max-w-2xl max-h-[90vh] flex flex-col overflow-hidden shadow-2xl">
      <div class="rblx-modal-header px-4 py-2.5 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="text-white font-extrabold text-base sm:text-lg rblx-stroke-sm">Animal Index</span>
          <span id="indexModalCount" class="text-yellow-300 text-xs font-bold">Unlocked: 0/18</span>
        </div>
        <button onclick="closeModal('indexModal')" class="rblx-btn bg-red-600 hover:bg-red-500 text-white font-black text-xs px-2.5 py-0.5 rounded-xl">✕</button>
      </div>
      <div id="indexBiomeContainer" class="p-3 sm:p-4 overflow-y-auto flex-1 flex flex-col gap-3"></div>
    </div>
  </div>

  <!-- PLAYER'S LUCKIEST CATCHES (PERSONAL RECORDS MODAL) -->
  <div id="leaderboardModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden items-center justify-center p-3 sm:p-4">
    <div class="bg-gray-900 border-4 border-black rounded-3xl w-full max-w-lg max-h-[85vh] flex flex-col overflow-hidden shadow-2xl">
      <div class="bg-gradient-to-r from-amber-500 to-yellow-600 px-4 py-2.5 border-b-3 border-black flex items-center justify-between">
        <div>
          <span class="text-black font-extrabold text-base sm:text-lg rblx-stroke-sm">🏆 Your Luckiest Catches</span>
          <div class="text-[10px] text-gray-900 font-bold">Personal Hall of Fame & Best Records</div>
        </div>
        <button onclick="closeModal('leaderboardModal')" class="rblx-btn bg-red-600 hover:bg-red-500 text-white font-black text-xs px-2.5 py-0.5 rounded-xl">✕</button>
      </div>
      <div class="p-4 overflow-y-auto flex-1 flex flex-col gap-2.5">
        <div class="text-xs text-gray-300 bg-gray-800 p-2.5 rounded-xl border border-gray-700">
          Ranked by overall rarity probability! Throws with critical points and high strength unlock giant sizes & mutations.
        </div>
        <div id="leaderboardList" class="flex flex-col gap-2"></div>
      </div>
    </div>
  </div>

  <!-- MATH 101 DIFFERENTIAL CALCULUS PRESENTATION & WORKED EXAMPLE MODAL -->
  <div id="calcLabModal" class="fixed inset-0 bg-black/85 backdrop-blur-md z-50 hidden items-center justify-center p-3 sm:p-5">
    <div class="bg-gray-950 border-4 border-indigo-600 rounded-3xl w-full max-w-3xl max-h-[92vh] flex flex-col overflow-hidden shadow-2xl text-white">
      <div class="bg-gradient-to-r from-indigo-700 via-purple-700 to-pink-700 px-5 py-3 border-b-3 border-black flex items-center justify-between">
        <div>
          <div class="font-extrabold text-base sm:text-lg rblx-stroke-sm">MATH 101 • Differential Calculus Project</div>
          <div class="text-[11px] text-pink-200">Prepared for: Engr. Hilarion S. Aquino III & Engr. James Marvin C. Gatdula</div>
        </div>
        <button onclick="closeModal('calcLabModal')" class="rblx-btn bg-red-600 hover:bg-red-500 text-white font-black text-xs px-2.5 py-0.5 rounded-xl">✕</button>
      </div>
      
      <div class="p-4 sm:p-5 overflow-y-auto flex-1 flex flex-col gap-4 text-xs sm:text-sm">
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center text-[10px] font-bold">
          <div class="bg-blue-900/60 border border-blue-400 p-2 rounded-xl">
            <div class="text-blue-300">Calculus Rubric</div>
            <div class="text-lg text-white font-black">30%</div>
            <div class="text-gray-300 text-[9px]">Rigorous Trig Derivatives</div>
          </div>
          <div class="bg-emerald-900/60 border border-emerald-400 p-2 rounded-xl">
            <div class="text-emerald-300">Programming</div>
            <div class="text-lg text-white font-black">20%</div>
            <div class="text-gray-300 text-[9px]">WebGL 3D Simulator</div>
          </div>
          <div class="bg-amber-900/60 border border-amber-400 p-2 rounded-xl">
            <div class="text-amber-300">Creativity & Rules</div>
            <div class="text-lg text-white font-black">30%</div>
            <div class="text-gray-300 text-[9px]">Roblox Simulator Loop</div>
          </div>
          <div class="bg-purple-900/60 border border-purple-400 p-2 rounded-xl">
            <div class="text-purple-300">Presentation</div>
            <div class="text-lg text-white font-black">20%</div>
            <div class="text-gray-300 text-[9px]">Live Worked Telemetry</div>
          </div>
        </div>

        <div class="bg-gray-900 border border-gray-800 p-3 rounded-2xl">
          <div class="text-yellow-400 font-extrabold text-sm mb-1.5">1. Core Trigonometric Derivatives Applied</div>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 mono-math text-[11px]">
            <div class="bg-black/60 p-2 rounded-lg border border-gray-700">
              <span class="text-cyan-400 font-bold">Sine Derivative:</span><br>
              d/dt [sin(t)] = cos(t)<br>
              Chain: d/dt [A sin(Bt)] = AB cos(Bt)
            </div>
            <div class="bg-black/60 p-2 rounded-lg border border-gray-700">
              <span class="text-amber-400 font-bold">Cosine Derivative:</span><br>
              d/dt [cos(t)] = -sin(t)<br>
              Chain: d/dt [C cos(Dt)] = -CD sin(Dt)
            </div>
            <div class="bg-black/60 p-2 rounded-lg border border-gray-700">
              <span class="text-purple-400 font-bold">Tangent Derivative:</span><br>
              d/dt [tan(t)] = sec²(t)<br>
              Chain: d/dt [A tan(Bt)] = AB sec²(Bt)
            </div>
          </div>
        </div>

        <div class="bg-gray-900 border border-gray-800 p-3 rounded-2xl">
          <div class="text-emerald-400 font-extrabold text-sm mb-1.5">2. Tangent Line Launch Ramp & Chain Rule Training</div>
          <p class="text-gray-300 leading-relaxed mb-2">
            The launch ramp is modeled by the sinusoidal profile <span class="mono-math text-emerald-300">y(x) = 2 sin(x)</span>.
            The instantaneous tangent slope is obtained directly by differentiation:
            <span class="mono-math text-yellow-300 font-bold">m = y'(x₀) = 2 cos(x₀)</span>.
            The physical launch angle is <span class="mono-math text-pink-300">θ = arctan(m)</span>, directly controlling 3D projectile ballistic trajectory!
          </p>
          <p class="text-gray-300 leading-relaxed">
            In the Pull-Up Workout station, vertical body displacement is <span class="mono-math text-sky-300">h(t) = sin(ωt)</span>.
            By the Chain Rule, vertical velocity is <span class="mono-math text-yellow-300 font-bold">h'(t) = ω cos(ωt)</span>.
            Timing rep clicks near peak velocity grants a <strong>2x XP bonus</strong>!
          </p>
        </div>

        <div class="bg-gray-900 border border-gray-800 p-3 rounded-2xl">
          <div class="text-pink-400 font-extrabold text-sm mb-1.5">3. Live Worked Example Telemetry (Last Throw)</div>
          <div id="workedExampleDetails" class="mono-math text-[11px] bg-black/70 p-3 rounded-xl border border-gray-700 space-y-1">
            <div class="text-gray-400">Perform a throw at the Launch Line to generate step-by-step calculus telemetry!</div>
          </div>
        </div>
      </div>
    </div>
  </div>
"""
