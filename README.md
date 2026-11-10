# 🥕 Throw Food For Animals 3D: Calculus Edition

> **MATH 101 – Differential Calculus Semestral Project**  
> *Designing Digital Worlds Through Differential Calculus*  
> **Course Facilitators:** Engr. Hilarion S. Aquino III & Engr. James Marvin C. Gatdula

---

## 🎮 Playable WebGL Simulator

A fully 3D responsive WebGL simulator inspired by the Roblox hit *Throw Food For Animals*, engineered with real-time trigonometric differential calculus principles governing food flight, launch tangent ramps, workout chain rule rhythms, and mutational optimization.

### 🌟 Key Upgrades & Features

1. **Massive Expanded 3D Voxel World (Three.js)**
   * **Expansive Map Runway:** Extended from 44 to **76 units wide**, stretching down to **$z = -980$** across 6 sequential biomes: **Forest (0–120m)**, **Savanna (120–320m)**, **Desert (320–850m)**, **Jungle (850–2,200m)**, **Deep Ocean (2,200–5,500m)**, and **Mythical Paradise (5,500m+)**.
   * **Multi-Tiered Stepped Dirt Cliffs:** 4-tier terraced canyon walls rising 36 units high with bright green grass ridge caps.
   * **Rich Thematic 3D Props Along the Canyon:**
     * *Forest:* Layered evergreen pines, golden birch trees, mossy boulders, tree stumps with sprouts.
     * *Savanna:* Flat-topped umbrella acacia trees, tall termite mounds, dry grass.
     * *Desert:* **Giant dinosaur ribcage skeletons** arching across the runway (matching Roblox simulator screenshots), dinosaur skull fossils, saguaro cacti, and stone-rimmed oasis pools.
     * *Jungle:* Segmented bamboo stalks with shoots, mossy Aztec stone pillars, vines.
     * *Ocean:* Multi-colored branching coral reefs (pink, cyan, yellow), sea crystal spires, nautical fossils.
     * *Mythical:* Glowing crystalline monoliths pulsating with KaTeX calculus runes, celestial rings, floating stars.
   * **Monumental Biome Gateway Arches:** Spanning across the canyon runway at every biome threshold with floating 3D signs.

2. **Physical Zone-Triggered Stations & Expanded 20-Pet Lawn Plot**
   * **Orange Checkered Launch Line:** Throwing UI, vertical power meter, and 3D trajectory arc activate ONLY when standing on the launch line.
   * **Pull-Up Bar Station:** 3D hanging workout with Chain Rule timing ($h'(t) = \omega\cos(\omega t)$).
   * **Food Shop Stall (Blue/White):** Purchase 7 tiers of food bait and expand lawn capacity up to 20 pets.
   * **Sell Stall (Red/White):** Liquidate duplicate or unequipped animals for instant cash.
   * **Fenced Lawn Plot (`My Plot`):** Enormous **42x34 unit fenced plot** holding up to **20 pets** with living micro-animations (tail wags, wing flaps, head tilts), live floating `+$X/s` cash indicators, and mutation aura rings.

3. **Authentic Roblox Animation Replication**
   * **Character Throw Animation:** Dynamic anticipation wind-up (right arm pulls up and back, torso twists back) followed by high-velocity forward release and follow-through.
   * **Flight Tracking Camera & HUD:** Smooth trailing camera tracking the spinning food down the canyon with a top dark translucent pill displaying the current biome (`Forest 🌲`, `Savanna 🌾`, `Desert 🏜️`) and live luck multiplier (`19.09X LUCK`).
   * **Catch Cutscene (Matching Video Recording):**
     * Radial comic zoom vignette speedlines.
     * Rotating starburst flare rays behind the celebratory header (`SUPER LUCKY!`, `LUCKY!`, `NICE CATCH!`, `INSANE LUCK!`).
     * **Suspense Odds Slot Machine Roll:** Numbers rapidly roll up from `1 in 1` to the final rarity odds (e.g. `1 in 51`) with ticking sound effects.
     * **Mystery Hangman Letter-by-Letter Name Reveal:** The animal's name initially appears as underscores (`_ _ _ _ _ _ _ _ _ _`) and reveals letters one by one (`D _ _ _ _ O _ _ _ _` $\to$ `DIMETRODON`) with crisp impact sounds.
     * **3D Animated Eating:** The animal bends down with articulated opening and closing jaws taking bites of the thrown food pellet, surrounded by an aura beacon and celebratory confetti explosion!
     * Prompt: `tap to continue` or press Space to claim pet.

4. **18 Dedicated Handcrafted 3D Voxel Models with Living Joints**
   * **Forest:** Tree Frog (wide jaws, bulging eyes), Meadow Bunny (tall ears, puffy tail), Grizzly Bear (muscular hump, snout).
   * **Savanna:** Striped Zebra (striped mane and body), Savanna Giraffe (tall neck, ossicones), King Lion (volumetric collar mane, toothy jaws).
   * **Desert:** Dune Camel (double humps, padded hooves), Gold Scorpion (pincer claws, sting tail), **Dimetrodon** (the iconic prehistoric apex reptile from the Roblox video with large ridged dorsal sail, toothy jaws with white fangs, claws, and animated eating jaws).
   * **Jungle:** Emerald Toucan (massive curved gradient beak), Silverback Gorilla (silver fur crest, knuckle-walking arms), Bengal Tiger (striped coat, white whisker ruffs).
   * **Ocean:** Harbor Seal (streamlined flippers), Great White Shark (white belly countershading, dorsal fin, pointed teeth), Abyssal Kraken (mantle head, glowing eyes, 8 tentacles).
   * **Mythical:** Starlight Unicorn (golden horn, flowing mane), Solar Phoenix (flaming crest, spread fiery wings, 3 solar plumes), Celestial Dragon (horns, membrane wings, spiky dorsal ridge, spade tail).

5. **Personal Luckiest Catches (Hall of Fame)**
   * Mounted directly on the canyon wall: a dedicated 3D billboard showing the player's personal top 5 rarest catches (animal, size, mutation, exact odds, distance).

6. **Balanced Progression & Index Biome Mastery Rewards**
   * Distance strictly calculated by $\text{Strength}^{0.72} \times \text{Food Mult} \times (1 + 0.18|P'|) \times \sin(2\theta) \times \text{Surge}$.
   * Players at 48 power stay safely inside Forest (~29m); advancing to Savanna, Desert, and beyond requires pull-up training and purchasing higher food tiers.
   * Collecting all 3 animals in a biome unlocks permanent bonus throw strength (`+25 💪` up to `+6,000 💪`).

7. **Procedural Web Audio Synthesizer**
   * 100% procedural Web Audio synthesizer: zero external audio assets required.
   * Includes upbeat BGM, throw whoosh, surge boom, critical chime, pull-up dings, coin collects, slot machine ticks, letter reveal pops, and confetti fanfare.

8. **Teacher God-Mode / Demo Button**
   * Convenient `👨‍🏫 DEMO MODE` button in the top bar to instantly unlock $10,000,000 cash, 20 mutated pets, and all 7 foods (including the *Cosmic Lobster*) for instant classroom demonstration.

---

## 📐 Differential Calculus Mechanics (MATH 101)

### 1. Basic Trigonometric Derivatives
$$\frac{d}{dt}\sin(t) = \cos(t), \quad \frac{d}{dt}\cos(t) = -\sin(t), \quad \frac{d}{dt}\tan(t) = \sec^2(t)$$

### 2. Harmonic Food Oscillations & Critical Point Optimization
Each food tier oscillates according to a linear combination or tangent function:
$$P(t) = A\sin(Bt) + C\cos(Dt) \implies P'(t) = AB\cos(Bt) - CD\sin(Dt)$$
* **Critical Points ($P'(t_0) \approx 0$):** Tapping when the derivative rate of change vanishes marks a stationary point, optimizing bait focus and guaranteeing a high-tier mutation (**Golden 5x**, **Rainbow 10x**, or **Cosmic 25x**).
* **Max Derivative Surge ($|P'(t_0)| \approx \text{Max}$):** Tapping at peak instantaneous velocity triggers a **+30% Distance Surge** accompanied by a screen shake and sonic boom.

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

Open `index.html` or `throw_food_for_animals_3d_calculus_edition.html` directly in any modern web browser. No build step, Node server, or external downloads required!

## 🎨 Polished 3D Animal Models

All 18 species now receive reusable polished details, mutation finishes and biome-appropriate idle motions, while retaining the original Three.js game mechanics. See [Polished Model Framework](docs/POLISHED_MODELS.md) for source structure, customization and rebuilding instructions.
