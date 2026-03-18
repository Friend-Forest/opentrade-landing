#!/usr/bin/env python3
"""
img2pixel — Convert images to ASCII art optimized for Bitcount Grid Single font.

Each character in a dot-matrix font has a different visual "density" (how many dots
light up). We map pixel brightness to characters that produce the right dot density,
so the output looks like a proper icon when rendered in Bitcount Grid Single.

Usage:
  python tools/img2pixel.py <image_path> [--width 12] [--invert] [--html]

Examples:
  python tools/img2pixel.py icon.png --width 10
  python tools/img2pixel.py icon.png --width 14 --invert --html > icon.html
"""

import sys
import argparse
from PIL import Image

# Characters ordered by visual density in a dot-matrix/grid font.
# More strokes = more dots lit up = visually "heavier"
# Spaces and dots are lightest, @/M/W are heaviest.
DENSITY_CHARS = " .·:;+*oO#@"
DENSITY_CHARS_INVERTED = "@#Oo*+;:·. "

# Alternative: block-style for chunkier look
BLOCK_CHARS = " ░▒▓█"
BLOCK_CHARS_INVERTED = "█▓▒░ "

# Letters/symbols that look great in Bitcount Grid Single
BITCOUNT_CHARS = " .'\":;!|1iIlL7Jt+r*xvczYXZCUOQ0#MW@"
BITCOUNT_CHARS_INVERTED = BITCOUNT_CHARS[::-1]


def image_to_pixel_art(
    image_path: str,
    width: int = 12,
    invert: bool = False,
    charset: str = "default",
    threshold: float = 0.0,
) -> list[str]:
    """Convert an image to lines of ASCII pixel art."""

    img = Image.open(image_path).convert("RGBA")

    # Composite onto white or black background depending on invert
    bg_color = (0, 0, 0, 255) if not invert else (255, 255, 255, 255)
    background = Image.new("RGBA", img.size, bg_color)
    background.paste(img, mask=img.split()[3])  # paste using alpha channel
    img = background.convert("L")  # grayscale

    # Resize — height is roughly half width because characters are taller than wide
    aspect = img.height / img.width
    height = int(width * aspect * 0.55)
    img = img.resize((width, height), Image.Resampling.LANCZOS)

    # Pick character set
    if charset == "block":
        chars = BLOCK_CHARS_INVERTED if invert else BLOCK_CHARS
    elif charset == "bitcount":
        chars = BITCOUNT_CHARS_INVERTED if invert else BITCOUNT_CHARS
    else:
        chars = DENSITY_CHARS_INVERTED if invert else DENSITY_CHARS

    num_chars = len(chars)
    lines = []

    for y in range(img.height):
        line = ""
        for x in range(img.width):
            brightness = img.getpixel((x, y)) / 255.0

            # Apply threshold — anything below becomes empty
            if not invert and brightness < threshold:
                line += " "
                continue
            if invert and brightness > (1.0 - threshold):
                line += " "
                continue

            idx = int(brightness * (num_chars - 1))
            idx = min(idx, num_chars - 1)
            line += chars[idx]
        lines.append(line)

    return lines


def to_html(lines: list[str], font_size: str = "1.2rem") -> str:
    """Wrap pixel art lines in HTML using Bitcount Grid Single."""
    import html as htmlmod

    escaped = "\n".join(htmlmod.escape(line) for line in lines)
    return f"""<pre class="pixel-icon" style="font-family:'Bitcount Grid Single',monospace;font-weight:300;font-size:{font_size};line-height:1;letter-spacing:0.1em;margin:0;white-space:pre">{escaped}</pre>"""


def to_astro_component(lines: list[str], name: str = "Icon") -> str:
    """Generate an Astro-friendly snippet."""
    import html as htmlmod

    escaped = "\n".join(htmlmod.escape(line) for line in lines)
    return f"""<pre class="pixel-icon-art" style="font-family:var(--font-pixel);font-weight:300;font-size:inherit;line-height:1;letter-spacing:0.1em;margin:0;white-space:pre;display:inline-block">{escaped}</pre>"""


def main():
    parser = argparse.ArgumentParser(description="Convert image to Bitcount Grid pixel art")
    parser.add_argument("image", help="Path to input image (PNG, SVG, JPG, etc.)")
    parser.add_argument("--width", "-w", type=int, default=12, help="Character width (default: 12)")
    parser.add_argument("--invert", "-i", action="store_true", help="Invert (light icon on dark bg)")
    parser.add_argument("--html", action="store_true", help="Output as HTML <pre> block")
    parser.add_argument("--astro", action="store_true", help="Output as Astro component snippet")
    parser.add_argument("--charset", "-c", choices=["default", "block", "bitcount"], default="default",
                        help="Character set to use")
    parser.add_argument("--font-size", "-s", default="1.2rem", help="Font size for HTML output")
    parser.add_argument("--threshold", "-t", type=float, default=0.0,
                        help="Brightness threshold (0-1) below which pixels become empty")
    args = parser.parse_args()

    lines = image_to_pixel_art(
        args.image,
        width=args.width,
        invert=args.invert,
        charset=args.charset,
        threshold=args.threshold,
    )

    if args.html:
        print(to_html(lines, args.font_size))
    elif args.astro:
        print(to_astro_component(lines))
    else:
        for line in lines:
            print(line)


if __name__ == "__main__":
    main()
