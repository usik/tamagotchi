#!/usr/bin/env node
/**
 * postinstall — runs after `npm install` / `npx tamagotchi`
 * Checks that the Python package is installed and prints a hint if not.
 */
const { spawnSync } = require("child_process");

const result = spawnSync("tama", ["--version"], { encoding: "utf8" });

if (result.status !== 0 || result.error) {
  console.log("");
  console.log("👾 tamagotchi npm wrapper installed!");
  console.log("");
  console.log("You still need the Python package:");
  console.log("  pip install tamagotchi");
  console.log("  # or");
  console.log("  pipx install tamagotchi");
  console.log("");
  console.log("Then run:  tama  (or:  npx tamagotchi)");
  console.log("");
} else {
  console.log(`👾 tamagotchi ready — ${result.stdout.trim()}`);
  console.log("Run: tama");
}
