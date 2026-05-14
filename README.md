# RainbowLines

Sublime Text plugin that assigns a distinct background color to each line, cycling through a palette. Makes dense log files scannable at a glance.

![Sublime Text 4](https://img.shields.io/badge/Sublime%20Text-4-orange)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)

## What it does

Each line gets a background color based on its line number mod the palette size. Colors cycle, so adjacent lines are always different. Works on any file type — no syntax required.

Useful for reading long Kubernetes / application logs where every line is wall-to-wall text and it's easy to lose your place.

## Installation

Clone the repo, then symlink it into Sublime's Packages folder for your platform.

**macOS**
```bash
git clone https://github.com/yourname/sublime-color-circlr.git

ln -s "$(pwd)/sublime-color-circlr" \
  ~/Library/Application\ Support/Sublime\ Text/Packages/RainbowLines
```

**Linux**
```bash
git clone https://github.com/yourname/sublime-color-circlr.git

ln -s "$(pwd)/sublime-color-circlr" \
  ~/.config/sublime-text/Packages/RainbowLines
```

**Windows (PowerShell, run as Administrator)**
```powershell
git clone https://github.com/yourname/sublime-color-circlr.git

New-Item -ItemType SymbolicLink `
  -Path "$env:APPDATA\Sublime Text\Packages\RainbowLines" `
  -Target "$PWD\sublime-color-circlr"
```

Sublime hot-reloads packages — no restart needed.

## Usage

| Action | How |
|---|---|
| Toggle on/off (current file) | `⌘ + Option + R` |
| Toggle on/off (current file) | Command Palette → `Rainbow Lines: Toggle (this file)` |
| Toggle on/off (all files) | Command Palette → `Rainbow Lines: Toggle Global (all files)` |
| Pick a palette | Command Palette → `Rainbow Lines: Select Palette` |
| Step to next palette | Command Palette → `Rainbow Lines: Cycle Palette` |

## Palettes

| Name | Colors |
|---|---|
| `rainbow` | cyan, orange, purple, yellow, blue, green (default) |
| `warm` | red, orange, yellow, pink |
| `cool` | cyan, blue, green, purple |
| `two-tone` | cyan, orange |

Switch palette via Command Palette → **Rainbow Lines: Select Palette**. The choice persists across restarts.

## Custom palettes

Add entries to `rainbow_lines.sublime-settings` (Preferences → Package Settings → Rainbow Lines → Settings):

```json
{
    "palette": "my-palette",
    "palettes": {
        "my-palette": ["region.redish", "region.bluish"]
    }
}
```

Available scope names: `region.redish`, `region.orangish`, `region.yellowish`, `region.greenish`, `region.cyanish`, `region.bluish`, `region.purplish`, `region.pinkish`

These are Sublime Text built-ins and work with any active color scheme.

## Settings

| Key | Default | Description |
|---|---|---|
| `enabled` | `true` | Master on/off switch |
| `palette` | `"rainbow"` | Active palette name |
| `palettes` | (see above) | Palette definitions |
| `poll_interval_ms` | `80` | How often to check scroll position (ms) |

## Performance

Only the visible viewport ± 200 lines is colored at any time. On scroll, the colored window follows within ~80ms. Tested on log files with 50k+ lines.

## Uninstall

Remove the symlink for your platform:

**macOS**
```bash
rm ~/Library/Application\ Support/Sublime\ Text/Packages/RainbowLines
```

**Linux**
```bash
rm ~/.config/sublime-text/Packages/RainbowLines
```

**Windows (PowerShell)**
```powershell
Remove-Item "$env:APPDATA\Sublime Text\Packages\RainbowLines"
```
