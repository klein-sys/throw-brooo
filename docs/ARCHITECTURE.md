# Architecture and activity improvements

Reviewed from `main` at `d054fd2`. This is a static, single-player Three.js r128 game, not a server-backed multiplayer game. “Modes” are station activities in a shared world, plus the calculus lab and teacher demo.

## How the game is built

```text
Python source fragments + mobile.css
              │
     builder/assemble_game.py
              │
      ┌───────┴────────┐
  index.html    named standalone HTML (identical)
              │
    Browser: shared JavaScript scope
              │
  data → audio → calculus → models → world → gameplay
```

| Source | Responsibility |
| --- | --- |
| `builder/html_head.py`, `html_ui.py`, `mobile.css` | Document, HUDs, dialogs, responsive layouts and accessibility |
| `builder/js_data.py` | Seven foods, six biomes, 18 species, sizes, mutations, stations and initial state |
| `builder/js_audio.py` | Procedural Web Audio music and effects |
| `builder/js_calculus.py` | Food derivatives, ramp slope/angle, training rhythm, mastery strength and worked examples |
| `builder/animal_models.py` | Species geometry and articulated joints |
| `builder/model_framework.js`, `js_model_framework.py` | Additional model detail, shared resources, mutation finishes and animation profiles; currently duplicated source |
| `builder/js_three.py` | Renderer, lighting, world, avatar, plot pets, trajectory, labels and cutscene objects |
| `builder/js_gameplay.py` | Inputs, station transitions, throwing/rewards, inventory/economy, dialogs, saves and animation loop |

The generated files include third-party CDN references for Three.js, Tailwind and fonts. Python is needed only when rebuilding. Node/Playwright is used only for development tests. There is no runtime backend or bundler.

## State and activity lifecycle

`state` owns progression, inventory, preferences, current zone and active throw. `requestAnimationFrame` updates controls, calculus, pets, projectile flight, camera and rendering. Separate intervals award income each second and save every five seconds.

Throwing transitions through wind-up → flight → reveal → collection. Collection creates an inventory entry, equips it if the plot has space, and updates the index and income. Each equipped pet has a generated Three.js model and DOM label. The same browser save key (`TF4A_CALC_SAVE_V5`) is retained.

The controls now use a pointer ID for each camera/joystick gesture, with pointer capture and cleanup on cancellation, focus loss and hidden tabs. A single modal owner gates movement and actions. `syncActivityUI()` derives HUD visibility and station selection from existing activity state. This is a small coordination layer; it is not yet a full state-machine refactor.

Demo progress is a temporary in-memory session cloned from normal progress. Save writes are suppressed until exiting demo, which restores the original state. Reloading also returns to the normal save. Demo now displays all 18 species across 20 pets.

## Changes by activity

| Activity | Improvements |
| --- | --- |
| Throwing and catch reveal | Separated touch action/joystick/graph, legible throw button and timing badges, no station teleport during wind-up/flight, collectible catch button with keyboard support, long names wrap on phones |
| Pull-up training | Live velocity meter and gold timing cue, visible vertical movement, Space repeat protection, brief input cooldown, XP carry-over on level-up, reliable station exit and Escape |
| Shop and selling | Scrollable dialogs within safe viewport bounds, 44px action/close targets, background movement blocked, predictable focus, reopen same station via its shortcut |
| Pet plot and collection | Reachable plot/animals controls on small screens, safe dialog scrolling, restored visibility settings, lower-cost rendering option |
| Index, records and calculus lab | Shared accessible dialog behavior, focus containment, mobile graph starts collapsed and resizes correctly on expansion; unused graph drawing skipped |
| Teacher demo | Clear Exit Demo control, all-species showcase and isolation from normal saves |
| Shared experience | Independent two-finger movement/look, blur cleanup, selected-station indicator, portrait/landscape layouts, safe-area padding, system reduced-motion support for CSS effects, saved mute respected |

Graphics defaults to Auto: coarse-pointer devices use pixel ratio ≤1 with shadows off; other devices use pixel ratio ≤2 with shadows. Settings offers Battery saver and High detail overrides. These reduce rendering work; they are not a measured promise of a particular frame rate.

## Validation

`npm test` runs real Chromium/WebGL integration tests at 1440×900, 390×844, 360×640, 844×390 and 768×1024. It covers keyboard and simultaneous touch input, station changes, modal focus, catch collection, demo save isolation, pet equipment/selling, saved settings, and visible/reachable controls. Screenshots are written to ignored `test-results/`.

The test suite supports `CHROMIUM_PATH` for an existing browser. In managed environments, `TEST_CURL_PROXY=1` retrieves the same CDN resources using curl with inherited proxy/CA configuration; TLS verification stays enabled. On ordinary machines no bridge is needed.

## Recommended next architecture work

1. Extract activity transitions and reward/economy calculations from `js_gameplay.py` into independent modules; make reward application idempotent and test it without rendering.
2. Make `model_framework.js` the single model-framework source during assembly instead of maintaining its Python string copy manually.
3. Add save-schema validation/migrations and a recoverable import/export path before adding new progression systems.
4. Profile real phones with a full 20-pet plot, then consider instanced geometry, model detail levels and fewer DOM label updates. Emulation cannot establish device thermals or Safari behavior.
5. Review the mathematics separately: for equal-frequency sine/cosine combinations, the current derivative maximum uses an upper bound rather than the exact amplitude; the tangent clipping and displayed ramp efficiency also deserve an educational accuracy pass.

Existing food costs, catch distributions, world geometry and animal model design are retained. New challenge or competitive modes would be a separate product decision.
