# -*- coding: utf-8 -*-

JS_DATA = """
    /*************************************************************************
     * 1. BALANCED PROGRESSION DATA: 7 FOODS, 6 3D BIOMES, SIZES & MUTATIONS
     *************************************************************************/
    const SIZES = [
      { id: 'regular',  name: 'Regular',  mult: 1.0,  scale: 1.0,  weight: 6400, chanceNum: 1.56,  chanceStr: '1 in 1.6 (64%)',   color: '#9ca3af' },
      { id: 'big',      name: 'Big',      mult: 1.8,  scale: 1.22, weight: 2200, chanceNum: 4.55,  chanceStr: '1 in 4.5 (22%)',   color: '#38bdf8' },
      { id: 'huge',     name: 'Huge',     mult: 3.5,  scale: 1.48, weight: 950,  chanceNum: 10.5,  chanceStr: '1 in 10.5 (9.5%)', color: '#4ade80' },
      { id: 'giant',    name: 'Giant',    mult: 7.0,  scale: 1.78, weight: 350,  chanceNum: 28.5,  chanceStr: '1 in 28.5 (3.5%)', color: '#f59e0b' },
      { id: 'titanic',  name: 'Titanic',  mult: 15.0, scale: 2.15, weight: 90,   chanceNum: 111,   chanceStr: '1 in 111 (0.9%)',  color: '#ec4899' },
      { id: 'colossal', name: 'Colossal', mult: 40.0, scale: 2.65, weight: 10,   chanceNum: 1000,  chanceStr: '1 in 1,000 (0.1%)', color: '#a855f7' }
    ];

    const MUTATIONS = [
      { id: 'normal',  name: 'NORMAL',                   mult: 1.0,  chanceNum: 1.25, chanceStr: '1 in 1.3',   color: '#9ca3af', hex: 0x9ca3af },
      { id: 'silver',  name: 'SILVER',                   mult: 2.0,  chanceNum: 8.0,  chanceStr: '1 in 8',     color: '#e2e8f0', hex: 0xe2e8f0 },
      { id: 'golden',  name: 'CRITICAL POINT • GOLDEN',  mult: 5.0,  chanceNum: 35,   chanceStr: '1 in 35',    color: '#facc15', hex: 0xfacc15 },
      { id: 'rainbow', name: 'CRITICAL POINT • RAINBOW', mult: 10.0, chanceNum: 150,  chanceStr: '1 in 150',   color: '#f472b6', hex: 0xf472b6 },
      { id: 'cosmic',  name: 'CRITICAL POINT • COSMIC',  mult: 25.0, chanceNum: 1000, chanceStr: '1 in 1,000', color: '#c084fc', hex: 0xc084fc }
    ];

    const FOODS = [
      {
        id: 'carrot', name: 'Carrot', icon: '🥕', tier: 'Tier 1 • Common', cost: 0,
        type: 'sincos', A: 2, B: 1.2, C: 0, D: 1.2,
        formulaStr: 'P(t) = 2sin(1.2t)', derivStr: "P'(t) = 2.4cos(1.2t)",
        distMult: 2.2, foodMult: 1.0, luck: 1.0, color: 0xf97316
      },
      {
        id: 'apple', name: 'Apple', icon: '🍎', tier: 'Tier 1 • Common', cost: 80,
        type: 'sincos', A: 0, B: 1.4, C: 3, D: 1.4,
        formulaStr: 'P(t) = 3cos(1.4t)', derivStr: "P'(t) = -4.2sin(1.4t)",
        distMult: 4.8, foodMult: 1.8, luck: 1.4, color: 0xef4444
      },
      {
        id: 'banana', name: 'Banana', icon: '🍌', tier: 'Tier 2 • Uncommon', cost: 450,
        type: 'sincos', A: 3, B: 1.5, C: 2, D: 1.5,
        formulaStr: 'P(t) = 3sin(1.5t) + 2cos(1.5t)', derivStr: "P'(t) = 4.5cos(1.5t) - 3sin(1.5t)",
        distMult: 9.5, foodMult: 3.2, luck: 2.2, color: 0xfacc15
      },
      {
        id: 'toast', name: 'Toast', icon: '🍞', tier: 'Tier 2 • Rare', cost: 3500,
        type: 'sincos', A: 4, B: 2.0, C: -2, D: 2.0,
        formulaStr: 'P(t) = 4sin(2t) - 2cos(2t)', derivStr: "P'(t) = 8cos(2t) + 4sin(2t)",
        distMult: 20.0, foodMult: 6.5, luck: 4.0, color: 0xd97706
      },
      {
        id: 'orange', name: 'Orange', icon: '🍊', tier: 'Tier 3 • Epic', cost: 30000,
        type: 'sincos', A: 5, B: 2.4, C: 3, D: 1.2,
        formulaStr: 'P(t) = 5sin(2.4t) + 3cos(1.2t)', derivStr: "P'(t) = 12cos(2.4t) - 3.6sin(1.2t)",
        distMult: 42.0, foodMult: 15.0, luck: 8.5, color: 0xfb923c
      },
      {
        id: 'pear', name: 'Golden Pear', icon: '🍐', tier: 'Tier 4 • Legendary', cost: 250000,
        type: 'sincos', A: 4, B: 1.4, C: 6, D: 2.8,
        formulaStr: 'P(t) = 4sin(1.4t) + 6cos(2.8t)', derivStr: "P'(t) = 5.6cos(1.4t) - 16.8sin(2.8t)",
        distMult: 75.0, foodMult: 35.0, luck: 20.0, color: 0xa3e635
      },
      {
        id: 'lobster', name: 'Cosmic Lobster', icon: '🦞', tier: 'Tier 5 • Cosmic', cost: 1800000,
        type: 'tan', A: 2.5, B: 0.9, C: 0, D: 0.9,
        formulaStr: 'P(t) = 2.5tan(0.9t)', derivStr: "P'(t) = 2.25sec²(0.9t)",
        distMult: 140.0, foodMult: 90.0, luck: 60.0, color: 0xc084fc
      }
    ];

    const BIOMES = [
      { id: 'forest',   name: 'Forest',            minDist: 0,    maxDist: 100,  rewardPower: 25,   colorHex: 0x22c55e, cssColor: '#22c55e', icon: '🌲', zStart: -22,  zEnd: -70 },
      { id: 'savanna',  name: 'Savanna',           minDist: 100,  maxDist: 300,  rewardPower: 75,   colorHex: 0xeab308, cssColor: '#eab308', icon: '🌾', zStart: -70,  zEnd: -120 },
      { id: 'desert',   name: 'Desert',            minDist: 300,  maxDist: 800,  rewardPower: 200,  colorHex: 0xf97316, cssColor: '#f97316', icon: '🌵', zStart: -120, zEnd: -170 },
      { id: 'jungle',   name: 'Jungle',            minDist: 800,  maxDist: 2000, rewardPower: 600,  colorHex: 0x059669, cssColor: '#059669', icon: '🌴', zStart: -170, zEnd: -220 },
      { id: 'ocean',    name: 'Deep Ocean',        minDist: 2000, maxDist: 5000, rewardPower: 1800, colorHex: 0x0284c7, cssColor: '#0284c7', icon: '🌊', zStart: -220, zEnd: -270 },
      { id: 'mythical', name: 'Mythical Paradise', minDist: 5000, maxDist: 99999,rewardPower: 6000, colorHex: 0x9333ea, cssColor: '#9333ea', icon: '✨', zStart: -270, zEnd: -340 }
    ];

    const ANIMALS = [
      // Forest (0 - 100m)
      { id: 'frog',     name: 'Frog',              biome: 'forest',   emoji: '🐸', rarity: 'Common',    baseIncome: 2,        baseOdds: 1.67,  oddsStr: '1 in 1.7 (60%)',  color: 0x22c55e, scale: 0.9,  weight: 60 },
      { id: 'bunny',    name: 'Bunny',             biome: 'forest',   emoji: '🐰', rarity: 'Uncommon',  baseIncome: 6,        baseOdds: 3.57,  oddsStr: '1 in 3.6 (28%)',  color: 0xf3f4f6, scale: 0.95, weight: 28 },
      { id: 'bear',     name: 'Grizzly Bear',      biome: 'forest',   emoji: '🐻', rarity: 'Rare',      baseIncome: 18,       baseOdds: 8.33,  oddsStr: '1 in 8.3 (12%)',  color: 0x78350f, scale: 1.25, weight: 12 },
      // Savanna (100 - 300m)
      { id: 'zebra',    name: 'Zebra',             biome: 'savanna',  emoji: '🦓', rarity: 'Common',    baseIncome: 45,       baseOdds: 1.72,  oddsStr: '1 in 1.7 (58%)',  color: 0xe2e8f0, scale: 1.05, weight: 58 },
      { id: 'giraffe',  name: 'Giraffe',           biome: 'savanna',  emoji: '🦒', rarity: 'Rare',      baseIncome: 120,      baseOdds: 3.33,  oddsStr: '1 in 3.3 (30%)',  color: 0xfacc15, scale: 1.35, weight: 30 },
      { id: 'lion',     name: 'King Lion',         biome: 'savanna',  emoji: '🦁', rarity: 'Epic',      baseIncome: 350,      baseOdds: 8.33,  oddsStr: '1 in 8.3 (12%)',  color: 0xd97706, scale: 1.25, weight: 12 },
      // Desert (300 - 800m)
      { id: 'camel',    name: 'Dune Camel',        biome: 'desert',   emoji: '🐪', rarity: 'Uncommon',  baseIncome: 800,      baseOdds: 1.72,  oddsStr: '1 in 1.7 (58%)',  color: 0xb45309, scale: 1.2,  weight: 58 },
      { id: 'scorpion', name: 'Gold Scorpion',     biome: 'desert',   emoji: '🦂', rarity: 'Rare',      baseIncome: 2000,     baseOdds: 3.33,  oddsStr: '1 in 3.3 (30%)',  color: 0xeab308, scale: 1.0,  weight: 30 },
      { id: 'sphinx',   name: 'Pharaoh Fox',       biome: 'desert',   emoji: '🦊', rarity: 'Legendary', baseIncome: 5500,     baseOdds: 8.33,  oddsStr: '1 in 8.3 (12%)',  color: 0xf97316, scale: 1.15, weight: 12 },
      // Jungle (800 - 2,000m)
      { id: 'toucan',   name: 'Emerald Toucan',    biome: 'jungle',   emoji: '🦜', rarity: 'Rare',      baseIncome: 14000,    baseOdds: 1.72,  oddsStr: '1 in 1.7 (58%)',  color: 0x10b981, scale: 1.0,  weight: 58 },
      { id: 'gorilla',  name: 'Silverback',        biome: 'jungle',   emoji: '🦍', rarity: 'Epic',      baseIncome: 35000,    baseOdds: 3.33,  oddsStr: '1 in 3.3 (30%)',  color: 0x374151, scale: 1.35, weight: 30 },
      { id: 'tiger',    name: 'Bengal Tiger',      biome: 'jungle',   emoji: '🐅', rarity: 'Legendary', baseIncome: 90000,    baseOdds: 8.33,  oddsStr: '1 in 8.3 (12%)',  color: 0xfb923c, scale: 1.25, weight: 12 },
      // Deep Ocean (2,000 - 5,000m)
      { id: 'seal',     name: 'Arctic Seal',       biome: 'ocean',    emoji: '🦭', rarity: 'Rare',      baseIncome: 220000,   baseOdds: 1.72,  oddsStr: '1 in 1.7 (58%)',  color: 0x93c5fd, scale: 1.05, weight: 58 },
      { id: 'shark',    name: 'Megalodon',         biome: 'ocean',    emoji: '🦈', rarity: 'Epic',      baseIncome: 550000,   baseOdds: 3.33,  oddsStr: '1 in 3.3 (30%)',  color: 0x2563eb, scale: 1.4,  weight: 30 },
      { id: 'kraken',   name: 'Abyssal Kraken',    biome: 'ocean',    emoji: '🦑', rarity: 'Mythic',    baseIncome: 1500000,  baseOdds: 8.33,  oddsStr: '1 in 8.3 (12%)',  color: 0xdb2777, scale: 1.5,  weight: 12 },
      // Mythical Paradise (5,000m+)
      { id: 'unicorn',  name: 'Starlight Unicorn', biome: 'mythical', emoji: '🦄', rarity: 'Epic',      baseIncome: 4000000,  baseOdds: 1.72,  oddsStr: '1 in 1.7 (58%)',  color: 0xf472b6, scale: 1.25, weight: 58 },
      { id: 'phoenix',  name: 'Solar Phoenix',     biome: 'mythical', emoji: '🦅', rarity: 'Mythic',    baseIncome: 12000000, baseOdds: 3.33,  oddsStr: '1 in 3.3 (30%)',  color: 0xfacc15, scale: 1.4,  weight: 30 },
      { id: 'dragon',   name: 'Celestial Dragon',  biome: 'mythical', emoji: '🐉', rarity: 'Cosmic',    baseIncome: 40000000, baseOdds: 8.33,  oddsStr: '1 in 8.3 (12%)',  color: 0xa855f7, scale: 1.65, weight: 12 }
    ];

    const STATIONS = {
      throw:  { x: 0,   z: -14, radius: 5.5, name: 'Orange Checkered Launch Line' },
      pullup: { x: -16, z: 4,   radius: 4.2, name: 'Pull-Up Bar Station' },
      shop:   { x: -16, z: -8,  radius: 4.5, name: 'Food Shop Stall' },
      sell:   { x: 16,  z: -6,  radius: 4.5, name: 'Red & White Sell Stall' },
      plot:   { x: 0,   z: 7,   radius: 11.0, name: 'Fenced Lawn Plot' }
    };

    /*************************************************************************
     * 2. GAME STATE & PERSISTENCE ENGINE
     *************************************************************************/
    const SAVE_KEY = 'TF4A_CALC_SAVE_V4';

    let state = {
      cash: 50,
      baseStrength: 18,
      pullUpLevel: 1,
      pullUpXp: 0,
      pullUpMaxXp: 5,
      plotCapacity: 5, // Starts at 5, upgradable up to 20!
      inventory: [],
      unlockedFoods: ['carrot'],
      equippedFoodId: 'carrot',
      unlockedIndex: new Set(['frog']),
      claimedBiomeRewards: new Set(),
      playerBestCatches: [], // Personal Hall of Fame (Top 5 Luckiest Catches)
      t: 0,
      wavePaused: false,
      rampX0: 1.05,
      activeZone: null,
      autoSkipRepeats: false,
      activeThrow: null,
      throwCount: 0,
      lastWorkedExample: null,
      playerPos: { x: 0, z: -14 },
      playerRot: 0,
      isPullingUp: false,
      settings: {
        musicVol: 70,
        sfxVol: 85,
        viewOthersPets: true,
        viewYourPets: true
      }
    };
"""
