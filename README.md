# 🥕 Throw Food For Animals 3D: Calculus Edition

> **MATH 101 – Differential Calculus Semestral Project**  
> *Designing Digital Worlds Through Differential Calculus*  
> **Course Facilitators:** Engr. Hilarion S. Aquino III & Engr. James Marvin C. Gatdula

---

## 🎮 Playable WebGL Simulator

A fully 3D responsive WebGL simulator inspired by the Roblox hit *Throw Food For Animals*, engineered with real-time trigonometric differential calculus principles governing food flight, launch tangent ramps, workout chain rule rhythms, and mutational optimization.

### 🌟 Key Features

1. **Full 3D Voxel World (Three.js)**
   * Authentic Roblox-style studded voxel grid textures on lawn hubs and stepped dirt canyon cliffs.
   * 6 sequential canyon biomes: **Forest (0–100m)**, **Savanna (100–300m)**, **Desert (300–800m)**, **Jungle (800–2,000m)**, **Deep Ocean (2,000–5,000m)**, and **Mythical Paradise (5,000m+)**.
   * Responsive controls: Desktop (WASD / Arrow Keys + Mouse Drag Orbit) and Mobile (Virtual Thumbstick + Touch Drag Orbit + Large Action Buttons).

2. **Physical Zone-Triggered Stations**
   * **Orange Checkered Launch Line:** Throwing UI, vertical power meter, and 3D trajectory arc activate ONLY when standing on the launch line.
   * **Pull-Up Bar Station:** 3D hanging workout with Chain Rule timing ($h'(t) = \omega\cos(\omega t)$).
   * **Food Shop Stall (Blue/White):** Purchase 7 tiers of food bait and expand lawn capacity up to 20 pets.
   * **Sell Stall (Red/White):** Liquidate duplicate or unequipped animals for instant cash.
   * **Fenced Lawn Plot (`My Plot`):** Up to 20 pets wandering in 3D with live floating `+$X/s` cash indicators and mutation aura rings.

3. **3D Live Tangent Trajectory Arc**
   * Projects a glowing 3D ballistic trajectory arc directly from the player's held food into the canyon.
   * The launch angle is dictated in real-time by the derivative slope: $m = y'(x_0) = 2\cos(x_0) \implies \theta = \arctan(m)$.

4. **Skippable 3D Catch Cutscene with Exact Rarity Odds & Dedicated 3D Models**
   * Dramatic 3D camera zoom on the caught animal eating bait.
   * **18 Dedicated Handcrafted 3D Voxel Models:** Every single animal features dedicated voxel anatomy:
     * *Frog:* Wide amphibian jaw, raised eye bumps, front webbed feet, folded hind frog thighs.
     * *Bunny:* Tall upright ears with pink insets, pink nose, cotton-ball puffy tail.
     * *Grizzly Bear:* Heavy bear snout, dark nose, rounded ears with tan cups, sturdy paws.
     * *Zebra:* Striped mane along neck, dark muzzle, black hooves, striped tail.
     * *Giraffe:* Long vertical neck, knobby ossicones (horns), brown spots, tall legs.
     * *King Lion:* Volumetric dark collar mane framing face, feline jowls, tufted tail.
     * *Dune Camel:* Iconic desert hump, curved S-neck, flat desert padded hooves.
     * *Gold Scorpion:* Segmented low carapace, front jointed pincer claws, arched curved sting tail with forward barb.
     * *Pharaoh Fox:* Giant fennec ears, golden collar, white-tipped sweeping bushy tail.
     * *Emerald Toucan:* Massive curved beak with emerald/orange/red gradient, yellow chest bib, side wings.
     * *Silverback Gorilla:* Broad chest, silver-grey back plate, powerful knuckle-walking arms.
     * *Bengal Tiger:* Feline jowls, tiger stripes, white throat, curved striped tail.
     * *Arctic Seal:* Sleek hydrodynamic body, front flippers, split swimming rear tail flippers.
     * *Megalodon Shark:* Pointed snout, jagged teeth, sharp pectoral fins, tall triangular dorsal fin, vertical tail.
     * *Abyssal Kraken:* Bulbous mantle head, glowing bioluminescent eyes, 8 curling splaying tentacles.
     * *Starlight Unicorn:* Arched neck, flowing pastel mane, spiraled golden horn on forehead, golden hooves.
     * *Solar Phoenix:* Crown feather crest, eagle beak, wide spread fiery wings, 3 flowing solar tail plumes.
     * *Celestial Dragon:* Horned dragon head, white fangs, membrane wings, spiny dorsal ridge, spade barb tail.
   * Displays the exact probability / rarity odds (e.g., `1 IN 450 (0.22%)`).
   * Displays both **Size** (Regular, Big, Huge, Giant, Titanic, Colossal) and **Mutation** (Normal, Silver, Golden, Rainbow, Cosmic).
   * Instant `⏭ SKIP ANIMATION` button on repeats and an `Auto-Skip Repeat Cutscenes` toggle.

5. **Personal Luckiest Catches (Hall of Fame)**
   * Mounted directly on the left canyon dirt cliff wall: a dedicated 3D billboard showing the player's personal top 5 rarest catches.
   * Updates dynamically in 3D in real time whenever a new record pet is caught!

6. **Procedural Web Audio Synthesizer**
   * Zero external audio files required! 100% procedural Web Audio synthesizer.
   * Features cheerful background music and sound effects (throws, sonic booms, critical sparkles, catch fanfares, pull-up dings, coin collects).
   * Settings modal (matching Roblox UI) with Music %, SFX %, and pet visibility toggles.

7. **Teacher God-Mode / Demo Button**
   * Convenient `👨‍🏫 DEMO MODE` button in the top bar to instantly unlock $10,000,000 cash, 20 mutated pets, and all 7 foods (including the *Cosmic Lobster*) for instant classroom demonstration.

---

## 📐 Differential Calculus Mechanics (MATH 101)

### 1. Basic Trigonometric Derivatives
$$\frac{d}{dt}\sin(t) = \cos(t), \quad \frac{d}{dt}\cos(t) = -\sin(t), \quad \frac{d}{dt}\tan(t) = \sec^2(t)$$

### 2. Harmonic Food Oscillations & Critical Point Optimization
Each food tier oscillates according to a linear combination or tangent function:
$$P(t) = A\sin(Bt) + C\cos(Dt) \implies P'(t) = AB\cos(Bt) - CD\sin(Dt)$$
* **Critical Points ($P'(t_0) \approx 0$):** Tapping when the derivative rate of change vanishes marks a stationary point, optimizing bait focus and guaranteeing a high-tier mutation (**Golden 5x**, **Rainbow 10x**, or **Cosmic 25x**).
* **Max Derivative Surge ($|P'(t_0)| \approx \text{Max}$):** Tapping at peak instantaneous velocity triggers a **+30% Distance Surge** accompanied by a sonic boom.

### 3. Tangent Line Ballistic Launch Ramp
Modeled by the sinusoidal ramp profile $y(x) = 2\sin(x)$:
$$m = y'(x_0) = 2\cos(x_0)$$
$$\theta = \arctan(m)$$
The ballistic efficiency is governed by $\sin(2\theta)$, providing maximum aerodynamic range when $\theta \approx 45^\circ$.

### 4. Pull-Up Bar Chain Rule Training
Vertical displacement:
$$h(t) = \sin(\omega t), \quad \omega = 3.6\text{ rad/s}$$
Instantaneous vertical velocity:
$$h'(t) = \frac{d}{dt}\sin(\omega t) = \omega\cos(\omega t)$$
Timing reps near peak velocity ($|h'| \ge 0.8\omega$) grants **2x XP/rep** with a perfect velocity flash.

---

## 🚀 Running the Project

Open `index.html` or `throw_food_for_animals_3d_calculus_edition.html` in any modern web browser (Google Chrome, Microsoft Edge, Safari, Firefox). No build step, Node server, or external downloads required!

