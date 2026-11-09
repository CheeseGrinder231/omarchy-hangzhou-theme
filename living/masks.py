#!/usr/bin/env python3
"""Build the living-wallpaper masks for the Hangzhou backgrounds.

Usage: python3 -I masks.py   (writes <name>.mask.png next to this file)

Mask channels, authored in 1920x1080 space and sampled with linear filtering:
  R  water that ripples and shimmers (objects standing in it are cut out)
  G  lights that flicker (only warm pixels inside are affected)
  B  where mist drifts (value = strength)
Needs rsvg-convert and ImageMagick.
"""
import subprocess
import tempfile
from pathlib import Path

W, H = 1920, 1080
HERE = Path(__file__).resolve().parent


def poly(points, v):
    pts = " ".join(f"{x},{y}" for x, y in points)
    return f'<polygon points="{pts}" fill="{grey(v)}"/>'


def rect(x0, y0, x1, y1, v):
    return f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="{grey(v)}"/>'


def ell(cx, cy, rx, ry, v):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{grey(v)}"/>'


def grey(v):
    c = round(max(0.0, min(1.0, v)) * 255)
    return f"rgb({c},{c},{c})"


def water(horizon_px, feather=16):
    return (
        f'<linearGradient id="w" x1="0" y1="{horizon_px - 2}" x2="0" y2="{horizon_px + feather}" gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="black"/><stop offset="1" stop-color="white"/></linearGradient>'
        f'<rect x="0" y="{horizon_px - 2}" width="{W}" height="{H - horizon_px + 2}" fill="url(#w)"/>'
    )


def channel(shapes, blur):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">'
        f'<defs><filter id="f" filterUnits="userSpaceOnUse" x="-100" y="-100" width="{W+200}" height="{H+200}">'
        f'<feGaussianBlur stdDeviation="{blur}"/></filter></defs>'
        f'<rect width="{W}" height="{H}" fill="black"/><g filter="url(#f)">{"".join(shapes)}</g></svg>'
    )


def lantern(cx, top, gourd_r, roof, sphere, base, v=0.0):
    """Union of a Three Pools stone lantern's parts (all in 1920x1080 px)."""
    (rx0, ry0, rx1, ry1) = roof
    (sx, sy, srx, sry) = sphere
    (bx0, by0, bx1, by1) = base
    return [
        ell(cx, top + gourd_r * 0.6, gourd_r * 0.35, gourd_r * 0.6, v),
        ell(cx, top + gourd_r * 1.6, gourd_r * 0.68, gourd_r * 0.68, v),
        ell(cx, top + gourd_r * 3.0, gourd_r, gourd_r, v),
        poly([(rx0, ry1 - 6), (cx - (rx1 - rx0) * 0.2, ry0), (cx + (rx1 - rx0) * 0.2, ry0), (rx1, ry1 - 6), (rx1 - 10, ry1), (rx0 + 10, ry1)], v),
        ell(sx, sy, srx, sry, v),
        rect(bx0, by0, bx1, by1, v),
    ]


SCENES = {
    "1-leifeng-sunset": {
        "R": (
            [water(660)]
            + [
                # rowing boat (canopy, hull) and its oar
                poly([(505, 719), (618, 719), (618, 750), (646, 755), (633, 779), (499, 779), (492, 758), (505, 750)], 0),
                poly([(453, 776), (457, 782), (523, 753), (519, 747)], 0),
                # lotus leaves, bud and floating pads, lower left
                poly([(0, 768), (120, 788), (200, 815), (262, 808), (312, 828), (334, 878), (400, 898), (472, 903), (540, 933),
                      (582, 952), (722, 952), (728, 986), (842, 1000), (848, 1048), (702, 1052), (652, 1080), (0, 1080)], 0),
            ],
            5,
        ),
        "G": ([rect(1595, 280, 1695, 446, 1), rect(1606, 690, 1658, 905, 0.8)], 6),  # pagoda window column, its reflection
        "B": (
            [
                rect(0, 0, W, 380, 0.35),
                rect(0, 380, W, 655, 1.0),
                rect(0, 655, W, 760, 0.4),
                rect(1528, 200, 1712, 452, 0.25),
            ],
            30,
        ),
    },
    "2-three-pools-moon": {
        "R": (
            [water(553)]
            + lantern(705, 578, 24, (620, 660, 790, 697), (705, 745, 64, 47), (626, 784, 787, 817))
            + lantern(1164, 569, 15, (1113, 613, 1215, 636), (1164, 662, 37, 29), (1116, 687, 1214, 708))
            + [
                poly([(1414, 556), (1424, 556), (1429, 584), (1447, 591), (1441, 598), (1439, 611), (1445, 625), (1445, 637),
                      (1393, 637), (1393, 625), (1399, 611), (1397, 598), (1391, 591), (1409, 584)], 0),
                # lotus leaves and pads, lower right
                poly([(1183, 1000), (1250, 968), (1400, 933), (1520, 923), (1570, 878), (1640, 858), (1810, 823), (1920, 813),
                      (1920, 1080), (1183, 1080)], 0),
            ],
            4,
        ),
        "G": (
            [
                ell(705, 745, 58, 32, 1), ell(1164, 662, 34, 17, 1), ell(1419, 610, 20, 10, 1),
                rect(645, 835, 765, 1005, 0.85), rect(1128, 712, 1202, 825, 0.85), rect(1403, 636, 1437, 702, 0.85),
            ],
            5,
        ),
        "B": (
            [
                rect(0, 0, W, 360, 0.3),
                ell(365, 205, 270, 95, 0.6),
                rect(0, 360, W, 553, 1.0),
                rect(0, 553, W, 640, 0.45),
            ],
            30,
        ),
    },
}


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for name, chans in SCENES.items():
            pngs = []
            for ch in "RGB":
                shapes, blur = chans[ch]
                svg = tmp / f"{name}-{ch}.svg"
                svg.write_text(channel(shapes, blur), encoding="utf-8")
                png = tmp / f"{name}-{ch}.png"
                subprocess.run(["rsvg-convert", str(svg), "-o", str(png)], check=True)
                pngs.append(str(png))
            out = HERE / f"{name}.mask.png"
            # take each layer's red channel as-is (no luminance conversion), then combine as RGB
            args = ["magick"]
            for png in pngs:
                args += ["(", png, "-channel", "R", "-separate", "+channel", ")"]
            subprocess.run(args + ["-set", "colorspace", "sRGB", "-combine", "-strip", str(out)], check=True)
            print(out)


if __name__ == "__main__":
    main()
