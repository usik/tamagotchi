#!/usr/bin/env node
/**
 * tama — npx entry point
 * Delegates to the Python `tama` CLI installed via pip.
 * If `tama` is not found, offers to install it.
 */
const { execFileSync, spawnSync } = require("child_process");
const { existsSync } = require("fs");
const path = require("path");

function findTama() {
  // Check PATH first
  try {
    const result = spawnSync("which", ["tama"], { encoding: "utf8" });
    if (result.status === 0 && result.stdout.trim()) {
      return result.stdout.trim();
    }
  } catch (_) {}

  // Common pip install locations
  const candidates = [
    path.join(process.env.HOME || "", ".local", "bin", "tama"),
    "/usr/local/bin/tama",
    "/opt/homebrew/bin/tama",
  ];
  for (const c of candidates) {
    if (existsSync(c)) return c;
  }
  return null;
}

const tama = findTama();

if (!tama) {
  console.error("⚠️  tamagotchi Python package not found.");
  console.error("");
  console.error("Install it with:");
  console.error("  pip install tamagotchi");
  console.error("  # or");
  console.error("  pipx install tamagotchi");
  console.error("");
  console.error("Then run: tama");

  // Offer auto-install if pip is available
  const pip = spawnSync("which", ["pip3"], { encoding: "utf8" });
  if (pip.status === 0) {
    const readline = require("readline").createInterface({
      input: process.stdin,
      output: process.stdout,
    });
    readline.question("Install now with pip? [Y/n] ", (answer) => {
      readline.close();
      if (!answer || answer.toLowerCase() === "y") {
        console.log("Running: pip install tamagotchi");
        spawnSync("pip3", ["install", "tamagotchi"], { stdio: "inherit" });
        // Re-find and launch
        const tama2 = findTama();
        if (tama2) {
          spawnSync(tama2, process.argv.slice(2), { stdio: "inherit" });
        } else {
          console.error("Installed but tama not found on PATH. Try: source ~/.zshrc");
        }
      }
    });
  }
  process.exit(1);
}

// Pass all args through to the Python CLI
const result = spawnSync(tama, process.argv.slice(2), { stdio: "inherit" });
process.exit(result.status ?? 0);
