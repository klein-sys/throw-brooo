# Polished animal model framework (Three.js r128)

This project retains all **18 original procedural voxel animals** and adds a
reusable visual-detail layer for each species. Existing animal IDs, movement,
catch cutscenes, sizes, mutations, odds, inventory, saves, calculus, and income
logic are preserved.

## Architecture

- `builder/model_framework.js` is the readable standalone JavaScript source.
- `builder/js_model_framework.py` embeds that JavaScript as `JS_MODEL_FRAMEWORK`.
- `builder/animal_models.py` builds the original animal and calls
  `enhanceAnimalModel(g, animalId, s, animal, mutation)`.
- `builder/js_three.py` uses `disposePolishedAnimal()` when replacing lawn pets.
- `builder/js_gameplay.py` applies species-specific lawn animations and
  safely removes previous cutscene animals.
- `builder/assemble_game.py` injects the model framework before the original
  animal-model factory.

## Rebuilding the game

In the repository root, run:

```bash
python builder/assemble_game.py
```

This regenerates `index.html` and
`throw_food_for_animals_3d_calculus_edition.html`. Both files are committed
already, so GitHub Pages / static deployments can serve the updated game
without a Python runtime.

## Extend an animal

Edit the appropriate method in `POLISHED_DETAIL_BUILDERS` inside
`builder/model_framework.js`. Use helpers such as:

```js
k.box(k.root, [x, y, z], [width, height, depth], 0xffaa33);
k.orb(k.head, [x, y, z], [width, height, depth], 0xffffff, {preserve: true});
```

Forward is negative Z; feet are at roughly Y=0. The toolkit applies the
current species / size / mutation scale. Attach details to
`k.head`, `k.tail`, `k.leftWing`, or `k.rightWing` to inherit animations.
The `POLISHED_MODEL_PROFILES` registry configures motion for each animal.

**Important:** the builder currently embeds the JS string in a Python module.
After changing `builder/model_framework.js`, synchronize the embedded
`JS_MODEL_FRAMEWORK` source before rebuilding HTML (e.g. regenerate the
Python wrapper as a raw triple-quoted string). Do not change the original
animal IDs, save key, odds or movement/catch interfaces.

## Mutation finishes

Normal, Silver, Gold, Rainbow and Cosmic preserve recognizable species
silhouettes. Eyes, teeth, and key markings retain their color. Shared
detail geometry and material caches reduce repeated allocations. Old per-animal
Lambert materials and instance-specific geometry are disposed.

## Verification

Recommended:
1. Open the game, enable Teacher Demo mode, and inspect your pet lawn.
2. Confirm all 18 animal IDs appear with no console errors.
3. Test one of each mutation and each size.
4. Throw food and verify the eating/jaw cutscene and collection award.
5. Confirm cash, upgrades, index rewards, save/load and 3D camera behavior.
6. Check desktop and mobile rendering performance.

Automated mock-Three.js tests of the standalone framework covered
18 species x 5 mutations (90 constructions) prior to integration.
Full interactive browser QA remains recommended.
