# -*- coding: utf-8 -*-

HTML_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
  <title>Throw Food For Animals 3D: Calculus Edition (MATH 101)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700;800;900&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">
  <style>
    * {
      user-select: none;
      -webkit-user-select: none;
      box-sizing: border-box;
      touch-action: manipulation;
    }
    body {
      margin: 0;
      padding: 0;
      overflow: hidden;
      font-family: 'Fredoka', sans-serif;
      background: #0f172a;
    }
    .mono-math {
      font-family: 'JetBrains Mono', monospace;
    }
    .rblx-stroke {
      text-shadow:
        -2.5px -2.5px 0 #000,
         2.5px -2.5px 0 #000,
        -2.5px  2.5px 0 #000,
         2.5px  2.5px 0 #000,
         0px    4.5px 0 #000;
    }
    .rblx-stroke-lg {
      text-shadow:
        -3.5px -3.5px 0 #000,
         3.5px -3.5px 0 #000,
        -3.5px  3.5px 0 #000,
         3.5px  3.5px 0 #000,
        -4px    0px   0 #000,
         4px    0px   0 #000,
         0px    5.5px 0 #000;
    }
    .rblx-stroke-sm {
      text-shadow:
        -1.5px -1.5px 0 #000,
         1.5px -1.5px 0 #000,
        -1.5px  1.5px 0 #000,
         1.5px  1.5px 0 #000,
         0px    2.5px 0 #000;
    }
    .rblx-stroke-subtle {
      text-shadow:
        -1px -1px 0 #000,
         1px -1px 0 #000,
        -1px  1px 0 #000,
         1px  1px 0 #000;
    }
    .rblx-btn {
      border: 3px solid #111;
      box-shadow: 0 5px 0 #111, inset 0 3px 0 rgba(255,255,255,0.4);
      transition: transform 0.08s ease, box-shadow 0.08s ease;
      cursor: pointer;
    }
    .rblx-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 7px 0 #111, inset 0 3px 0 rgba(255,255,255,0.5);
    }
    .rblx-btn:active {
      transform: translateY(3px);
      box-shadow: 0 2px 0 #111, inset 0 2px 0 rgba(255,255,255,0.2);
    }
    .rblx-card {
      border: 3px solid #111;
      box-shadow: 0 6px 0 #111;
    }
    .rblx-modal-header {
      background: linear-gradient(135deg, #ec4899 0%, #db2777 50%, #be185d 100%);
      border-bottom: 3px solid #111;
    }
    ::-webkit-scrollbar {
      width: 8px;
    }
    ::-webkit-scrollbar-track {
      background: #1e293b;
      border-radius: 6px;
    }
    ::-webkit-scrollbar-thumb {
      background: #475569;
      border-radius: 6px;
    }
    @keyframes floatSlow {
      0%, 100% { transform: translateY(0px); }
      50% { transform: translateY(-6px); }
    }
    .animate-float {
      animation: floatSlow 2s ease-in-out infinite;
    }
    @keyframes cashFloatUp {
      0% { opacity: 0; transform: translate(-50%, 0) scale(0.7); }
      20% { opacity: 1; transform: translate(-50%, -12px) scale(1.15); }
      80% { opacity: 1; transform: translate(-50%, -40px) scale(1); }
      100% { opacity: 0; transform: translate(-50%, -60px) scale(0.85); }
    }
    .floating-cash-anim {
      animation: cashFloatUp 1.3s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
      pointer-events: none;
    }
    @keyframes pulseGlow {
      0%, 100% { filter: drop-shadow(0 0 5px rgba(250, 204, 21, 0.7)); }
      50% { filter: drop-shadow(0 0 16px rgba(250, 204, 21, 1)); }
    }
    .pulse-glow {
      animation: pulseGlow 1.5s infinite;
    }
    @keyframes screenShake {
      0%, 100% { transform: translate(0, 0); }
      20% { transform: translate(-6px, 4px); }
      40% { transform: translate(6px, -5px); }
      60% { transform: translate(-5px, 3px); }
      80% { transform: translate(4px, -2px); }
    }
    .shake-active {
      animation: screenShake 0.45s ease-out;
    }

    /* Starburst Flare Rays from Roblox Video Cutscene */
    @keyframes starburstSpin {
      0% { transform: translate(-50%, -50%) rotate(0deg); }
      100% { transform: translate(-50%, -50%) rotate(360deg); }
    }
    .starburst-rays {
      position: absolute;
      width: 480px;
      height: 480px;
      left: 50%;
      top: 50%;
      background: repeating-conic-gradient(
        from 0deg,
        rgba(239, 68, 68, 0.45) 0deg 15deg,
        transparent 15deg 30deg
      );
      border-radius: 50%;
      animation: starburstSpin 14s linear infinite;
      pointer-events: none;
      filter: blur(1px);
    }
    .starburst-rays.gold {
      background: repeating-conic-gradient(
        from 0deg,
        rgba(250, 204, 21, 0.5) 0deg 15deg,
        transparent 15deg 30deg
      );
    }
    .starburst-rays.cosmic {
      background: repeating-conic-gradient(
        from 0deg,
        rgba(192, 132, 252, 0.55) 0deg 15deg,
        transparent 15deg 30deg
      );
    }

    /* Radial Comic Vignette Zoom Lines during Cutscene */
    .comic-vignette {
      background: radial-gradient(
        circle,
        rgba(0, 0, 0, 0) 45%,
        rgba(0, 0, 0, 0.35) 75%,
        rgba(0, 0, 0, 0.75) 100%
      );
    }

    /* Hangman mystery letter flip */
    @keyframes letterPop {
      0% { transform: scale(0.4) translateY(10px); opacity: 0; }
      70% { transform: scale(1.25) translateY(-2px); opacity: 1; }
      100% { transform: scale(1.0) translateY(0); opacity: 1; }
    }
    .letter-reveal-pop {
      display: inline-block;
      animation: letterPop 0.18s cubic-bezier(0.18, 0.89, 0.32, 1.28) forwards;
    }

    /* Toggle Switch Custom */
    .toggle-checkbox:checked {
      right: 0;
      border-color: #22c55e;
    }
    .toggle-checkbox:checked + .toggle-label {
      background-color: #22c55e;
    }
  </style>
</head>
<body class="relative w-screen h-screen overflow-hidden select-none bg-slate-900 text-white">
"""
