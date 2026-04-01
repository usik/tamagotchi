# Homebrew Tap

This formula lives here until the package has enough PyPI downloads to be
accepted into homebrew-core (typically requires 75+ forks or 75+ watchers).

## Setup

Create a separate GitHub repo named `homebrew-tamagotchi` under your account,
copy `tamagotchi.rb` into it, then users can install with:

```bash
brew tap usik/tamagotchi
brew install tamagotchi
```

## Steps to publish

1. Create repo: `gh repo create homebrew-tamagotchi --public`
2. Copy formula: `cp homebrew/tamagotchi.rb <path-to-homebrew-tamagotchi>/Formula/tamagotchi.rb`
3. After PyPI publish, update the `url` and `sha256` in the formula:
   ```bash
   curl -sL https://pypi.org/pypi/tamagotchi/json | python3 -c "
   import sys, json
   d = json.load(sys.stdin)
   v = d['info']['version']
   for f in d['releases'][v]:
       if f['filename'].endswith('.tar.gz'):
           print(f['url'])
           print(f['digests']['sha256'])
   "
   ```
4. Commit and push — `brew audit --new Formula/tamagotchi.rb` should pass
