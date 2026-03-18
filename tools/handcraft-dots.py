#!/usr/bin/env python3
"""
Hand-craft dot-grid SVGs — Bitcount Grid Single style.
Big round dots, tight spacing, nearly touching.
"""

def grid_to_svg(grid: list[str], dot_r: float = 2.3, gap: float = 5.5, color: str = "currentColor") -> str:
    rows = len(grid)
    cols = max(len(row) for row in grid)
    w = cols * gap
    h = rows * gap

    dots = []
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == '1':
                cx = x * gap + gap / 2
                cy = y * gap + gap / 2
                dots.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{dot_r}" fill="{color}"/>')

    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" xmlns="http://www.w3.org/2000/svg">{"".join(dots)}</svg>'


# ─── ARROW UP ──────────────────────────────
# Gemini style: single dot tip, each row adds 2 dots, wide base, thick shaft
arrow_up = [
    "000000100000000",
    "000001110000000",
    "000011111000000",
    "000111111100000",
    "001111111110000",
    "011111111111000",
    "111111111111100",
    "000001110000000",
    "000001110000000",
    "000001110000000",
    "000001110000000",
    "000001110000000",
    "000001110000000",
    "000001110000000",
    "000001110000000",
]

# ─── LIGHTNING BOLT ────────────────────────
# Sharp angular zigzag - NOT curved. Hard angle in the middle.
bolt = [
    "001111100",
    "001111000",
    "011110000",
    "011100000",
    "111000000",
    "111111110",
    "000011110",
    "000011100",
    "000111000",
    "000110000",
    "001100000",
    "001000000",
]

# ─── REFRESH / CYCLE ──────────────────────
# Open circle with two arrowheads pointing clockwise
refresh = [
    "000111111110000",
    "001100000011100",
    "011000000001110",
    "110000000000110",
    "110000000000010",
    "110000000000000",
    "110000000000000",
    "000000000000011",
    "000000000000011",
    "010000000000011",
    "011000000000110",
    "011100000001100",
    "000111000011000",
    "000011111110000",
]

# ─── GEAR / COG ───────────────────────────
gear = [
    "00000111100000",
    "00000111100000",
    "00111111111100",
    "01111111111110",
    "01110000001110",
    "11110000001111",
    "11100000000111",
    "11100000000111",
    "11110000001111",
    "01110000001110",
    "01111111111110",
    "00111111111100",
    "00000111100000",
    "00000111100000",
]

icons = {
    "arrow-up": arrow_up,
    "bolt": bolt,
    "refresh": refresh,
    "gear": gear,
}

for name, grid in icons.items():
    svg = grid_to_svg(grid)
    print(f"=== {name} ===")
    # Print visual preview
    for row in grid:
        print(''.join('●' if c == '1' else ' ' for c in row))
    print()
    with open(f"tools/test-icons/{name}-perfect.svg", "w") as f:
        f.write(svg)
    print(f"Saved to tools/test-icons/{name}-perfect.svg")
    print()
