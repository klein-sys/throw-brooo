# Throw Food For Animals 3D: Calculus Edition

This MATH 101 project is a single-player WebGL game built with vanilla JavaScript and Three.js r128. Players train strength, adjust a launch ramp, time food throws, and collect animals across six biomes. The calculus lab explains food derivatives, ramp tangents, and the chain rule behind the pull-up mechanic.

## Where to work

- Edit `builder/js_calculus.py` for the formulas and worked examples, and `builder/js_data.py` for food tiers, biomes, animals, and initial state.
- Edit `builder/js_gameplay.py` for input, stations, throws, rewards, inventory, economy, saves, and demo mode.
- Edit `builder/js_three.py` for the 3D world and rendering, `builder/animal_models.py` for animal geometry, and `builder/js_audio.py` for procedural audio. If you change `builder/model_framework.js`, sync its embedded copy in `builder/js_model_framework.py`.
- Edit `builder/html_head.py`, `builder/html_ui.py`, and `builder/mobile.css` for the HUD, dialogs, and responsive layouts.
- See [Architecture](docs/ARCHITECTURE.md) for the activity lifecycle and [Polished models](docs/POLISHED_MODELS.md) for animal rendering. `reference/` contains visual references.

## Build and test

- Run `python3 builder/assemble_game.py` from the repository root to rebuild both committed entry points, `index.html` and `throw_food_for_animals_3d_calculus_edition.html`. On Windows, use `python` if available under that name. Make game changes in the builder and commit both regenerated files.
- Serve the root with `python3 -m http.server 8000` and open `http://localhost:8000`. Vercel serves the static game from `index.html`. The browser loads Three.js, Tailwind, and fonts from CDNs.
- Run `npm ci`, `npx playwright install chromium`, and `npm test` for browser tests. `CHROMIUM_PATH` can point to an existing Chromium executable. For gameplay changes, check the affected desktop and touch flows.
- Keep stable animal IDs compatible with existing browser saves under `TF4A_CALC_SAVE_V5`. Teacher Demo progress is in-memory and has a separate lifecycle from normal progression.

## Project skills

- [Superpowers](https://github.com/obra/superpowers/tree/22f0b463e7a5e579904dd6211a520321035526f7) is in `.agents/skills/superpowers/` for workflows such as planning, debugging, and verification. Apply the parts relevant to the task within the user's scope.
- [Awesome Gamedev Agent Skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/tree/c6ca6c41c839b68319ffc08430b99ab768debc32) is in `.agents/skills/awesome-gamedev-agent-skills/`. For game development, start with `router/SKILL.md` there and open the matching engine and discipline guides. This project uses a CDN-loaded Three.js r128 global. Check examples against r128 before using them.
