# EwokVPN icon generator

The EwokVPN icon is drawn in code, so every asset can be rebuilt from these files.

- `gen3.py` draws the icon as SVG: the full day and night icons, the character alone and the single-colour glyph used for the logo, tray and notification icons.
- `build.py` renders the SVGs with Playwright and writes every platform asset into the repository.
- `dmg_background.svg` is the macOS DMG window background, rendered by `render_dmg.js`.

Requirements: Python 3 with Pillow, Node.js with Playwright and Chromium. Set `PLAYWRIGHT_MODULE` to the Playwright package path and `CHROMIUM_PATH` to a Chromium binary when they are not found automatically.

```bash
python3 tools/icon/build.py .
node tools/icon/render_dmg.js tools/icon/dmg_background.svg /tmp/dmg.png
# then scale /tmp/dmg.png to 600x328 and save it as macos/packaging/dmg/background.png
```
