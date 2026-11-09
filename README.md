# Hangzhou Omarchy theme

West Lake (西湖) at dusk: ink-mist water, rice-paper text, Southern Song
celadon as the signal color. Made for Omarchy Meetup Hangzhou, 2026-11-15.

Install:

    omarchy theme install https://github.com/CheeseGrinder231/omarchy-hangzhou-theme

or Omarchy menu → Install → Style → Theme, and paste the link.

| Role | Color | Source |
|---|---|---|
| background | `#141b1d` | the lake at night |
| foreground | `#e3dccb` | rice paper (宣纸) |
| accent / cyan | `#8cc0ab` / `#7fb7a6` | celadon glaze (粉青, 青瓷) |
| red | `#d0654f` | vermilion seal paste (朱砂) |
| yellow | `#dcb25e` | osmanthus, the city flower (桂花) |
| orange | `#d98a5b` | Leifeng Pagoda at sunset (雷峰夕照) |
| green | `#9ab06a` | Longjing tea (龙井) |
| blue | `#729cb8` | West Lake water |
| magenta | `#cf8aa0` | lotus at Quyuan (曲院风荷) |

Window border: celadon into lake blue. Icons: Yaru-sage. Terminal, Neovim,
VS Code, btop, Hyprland and shell files are generated from `colors.toml`.

Backgrounds (cycle with `omarchy theme bg next`):

1. `1-leifeng-sunset.png`: Leifeng Pagoda at sunset over the Su Causeway
2. `2-three-pools-moon.png`: Three Pools Mirroring the Moon (三潭印月)

Both were drawn by GPT image generation (Codex CLI built-in `image_gen`,
2026-11-05) at 1672x941 and Lanczos-upscaled to 3840x2160. The exact
prompts are in `prompts/`.

## Living wallpaper (optional, not included)

The `living/` folder holds animation data for both backgrounds: water ripples
toward you, the sun and moon reflections glint, mist drifts through the hills,
candles and pagoda windows flicker.

- `living/<wallpaper>.json`: per-wallpaper settings (horizon line, ripple,
  shimmer, flicker, flicker speed, mist strength and color).
- `living/<wallpaper>.mask.png`: R = water that moves (boat, lanterns and
  lotus cut out), G = lights that flicker, B = where mist drifts.
  Rebuild with `python3 -I living/masks.py`.

The shell plugin that draws it is not published yet. Without it the two
backgrounds are ordinary still wallpapers, and the theme works the same.

## Screensaver

`screensaver.txt` shows Leifeng Pagoda (雷峰塔) and Chenghuang Pavilion
(城隍阁) over West Lake, drawn from the Omarchy Meetup Hangzhou pixel art,
with an OMARCHY · HANGZHOU title. Omarchy
themes cannot set the screensaver, so apply it yourself:

    cp ~/.config/omarchy/themes/hangzhou/screensaver.txt ~/.config/omarchy/branding/screensaver.txt
    omarchy-launch-screensaver force

This replaces your current screensaver text. Back up
`~/.config/omarchy/branding/screensaver.txt` first if you customised it, or
go back to the Omarchy logo with `omarchy branding screensaver reset`.
