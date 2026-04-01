#!/usr/bin/env node
/**
 * tama-install — npx entry point for `npx tamagotchi install`
 * Shortcut: npx tamagotchi install --claude-code
 */
const { spawnSync } = require("child_process");

// Delegate to `tama install` with all args
const result = spawnSync("tama", ["install", ...process.argv.slice(2)], {
  stdio: "inherit",
});
process.exit(result.status ?? 0);
