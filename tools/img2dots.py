#!/usr/bin/env python3
"""
img2dots — Convert images to dot-grid SVGs matching the Bitcount Grid Single font style.

Takes an icon image and renders it as a grid of small circles (dots) — only placing
dots where the source image has content. The result looks like the icon was drawn
in the same dot-matrix style as the Bitcount Grid Single font.

Usage:
  python tools/img2dots.py <image_path> [--cols 12] [--dot-radius 1.8] [--gap 5]
  python tools/img2dots.py icon.png --cols 14 --color white > icon.svg

Examples:
  python tools/img2dots.py tools/test-icons/gear-hq.png --cols 16
  python tools/img2dots.py tools/test-icons/bolt.png --cols 12 --color "#22c55e"
"""

import sys
import argparse
from PIL import Image


def image_to_dot_svg(
    image_path: str,
    cols: int = 12,
    dot_radius: float = 1.8,
    gap: float = 5.0,
    color: str = "currentColor",
    threshold: float = 0.3,
    opacity_mode: bool = False,
) -> str:
    """Convert an image to a dot-grid SVG."""

    img = Image.open(image_path).convert("RGBA")

    # Calculate rows based on aspect ratio
    aspect = img.height / img.width
    rows = max(1, round(cols * aspect))

    # Resize to grid dimensions
    img_resized = img.resize((cols, rows), Image.Resampling.LANCZOS)

    # SVG dimensions
    svg_w = cols * gap
    svg_h = rows * gap

    dots = []

    for y in range(rows):
        for x in range(cols):
            r, g, b, a = img_resized.getpixel((x, y))

            # Calculate brightness (0-1) weighted by alpha
            alpha = a / 255.0
            brightness = ((r + g + b) / 3.0 / 255.0) * alpha

            if brightness < threshold:
                continue

            cx = x * gap + gap / 2
            cy = y * gap + gap / 2

            if opacity_mode:
                # Variable opacity based on brightness
                dot_opacity = min(1.0, brightness * 1.2)
                dots.append(
                    f'    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{dot_radius}" fill="{color}" opacity="{dot_opacity:.2f}"/>'
                )
            else:
                # Binary: dot or no dot
                dots.append(
                    f'    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{dot_radius}" fill="{color}"/>'
                )

    dots_str = "\n".join(dots)

    svg = f"""<svg width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}" fill="none" xmlns="http://www.w3.org/2000/svg">
{dots_str}
</svg>"""

    return svg


def main():
    parser = argparse.ArgumentParser(
        description="Convert image to dot-grid SVG (Bitcount Grid Single style)"
    )
    parser.add_argument("image", help="Path to input image (PNG, JPG, etc.)")
    parser.add_argument("--cols", "-c", type=int, default=12, help="Number of dot columns (default: 12)")
    parser.add_argument("--dot-radius", "-r", type=float, default=1.8, help="Dot radius (default: 1.8)")
    parser.add_argument("--gap", "-g", type=float, default=5.0, help="Gap between dot centers (default: 5.0)")
    parser.add_argument("--color", default="currentColor", help="Dot color (default: currentColor)")
    parser.add_argument("--threshold", "-t", type=float, default=0.3, help="Brightness threshold 0-1 (default: 0.3)")
    parser.add_argument("--opacity", "-o", action="store_true", help="Use variable opacity based on brightness")
    parser.add_argument("--save", "-s", help="Save to file instead of stdout")

    args = parser.parse_args()

    svg = image_to_dot_svg(
        args.image,
        cols=args.cols,
        dot_radius=args.dot_radius,
        gap=args.gap,
        color=args.color,
        threshold=args.threshold,
        opacity_mode=args.opacity,
    )

    if args.save:
        with open(args.save, "w") as f:
            f.write(svg)
        print(f"Saved to {args.save}", file=sys.stderr)
    else:
        print(svg)


if __name__ == "__main__":
    main()
