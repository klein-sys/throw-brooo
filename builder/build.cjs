// Cross-platform assembly script that invokes Python if available,
// falling back safely to pre-built root static assets in environments without Python.
const cp = require('node:child_process');
const path = require('node:path');
const fs = require('node:fs');

const root = path.resolve(__dirname, '..');
const assembleScript = path.join(__dirname, 'assemble_game.py');
const pyCommands = ['python3', 'python', 'py'];

let built = false;
for (const cmd of pyCommands) {
  try {
    cp.execFileSync(cmd, [assembleScript], { cwd: root, stdio: 'inherit' });
    built = true;
    break;
  } catch {}
}

if (!built) {
  const file1 = path.join(root, 'index.html');
  const file2 = path.join(root, 'throw_food_for_animals_3d_calculus_edition.html');
  if (fs.existsSync(file1) && fs.existsSync(file2)) {
    console.log(`Python not detected; serving committed static game files (${fs.statSync(file1).size} bytes).`);
  } else {
    console.error('Build failed: neither Python nor committed HTML entry points were found.');
    process.exitCode = 1;
  }
}
