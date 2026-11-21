"""Draw the 21 November 2026 front page: "THE WORLD IN ONE PICTURE".

Flat vector-style newspaper front page, 1024x1024, drawn with PIL.
Run:  python3 draw.py        # writes entry.png next to this file
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024

PAPER = (246, 241, 231)
INK = (24, 24, 24)
RED = (166, 30, 30)
BLUE = (31, 78, 121)
GOLD = (198, 152, 46)
PANEL = (255, 253, 246)
MUTED = (84, 84, 84)
NIGHT = (18, 32, 58)
NIGHT2 = (28, 52, 88)
LINE = (24, 24, 24)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width` px."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, fnt, width, fill=INK, leading=1.28):
    """Draw wrapped paragraph; returns y just below the last line."""
    size = fnt.size
    for line in wrap(d, text, fnt, width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += int(size * leading)
    return y


def headline(d, x, y, text, fnt, width, fill=INK, leading=1.04):
    size = fnt.size
    for line in wrap(d, text, fnt, width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += int(size * leading)
    return y


def kicker(d, x, y, text, color=RED):
    f = font(SANS_B, 15)
    d.text((x, y), text.upper(), font=f, fill=color)
    return y + 22


def panel(d, x, y, w, h, fill=PANEL):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=fill,
                        outline=INK, width=2)


def burst(d, cx, cy, r, color):
    """Explosion starburst."""
    import math
    pts = []
    for i in range(16):
        ang = i * math.pi / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)
    d.ellipse([cx - r * 0.28, cy - r * 0.28, cx + r * 0.28, cy + r * 0.28],
              fill=(255, 214, 90))


def skyline(d, x0, y_base, heights, color, width=14, gap=6):
    x = x0
    for h in heights:
        d.rectangle([x, y_base - h, x + width, y_base], fill=color)
        x += width + gap
    return x


def draw_lead_art(d, x, y, w, h):
    """Night sky over Kyiv: missile streaks, blasts, Polish flag marker."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=NIGHT)
    # stars
    for sx, sy, r in [(30, 22, 2), (90, 48, 2), (150, 18, 3), (210, 55, 2),
                      (260, 26, 2), (330, 44, 2), (380, 20, 2), (120, 78, 2)]:
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                  fill=(255, 255, 220))
    # missile streaks
    for (x1, y1, x2, y2) in [(40, 30, 190, 150), (150, 18, 300, 130),
                             (260, 40, 390, 140)]:
        d.line([x + x1, y + y1, x + x2, y + y2], fill=(255, 170, 60), width=5)
        d.ellipse([x + x2 - 7, y + y2 - 7, x + x2 + 7, y + y2 + 7],
                  fill=(255, 220, 120))
    burst(d, x + 190, y + 150, 26, (255, 120, 40))
    burst(d, x + 330, y + 128, 20, (255, 120, 40))
    # skyline
    skyline(d, x + 12, y + h - 8, [52, 78, 44, 92, 60, 84, 48, 70],
            (8, 16, 34))
    # windows
    for wx in range(24, w - 20, 34):
        for wy in range(h - 66, h - 14, 18):
            d.rectangle([x + wx, y + wy, x + wx + 6, y + wy + 8],
                        fill=(255, 214, 90))
    # Polish flag tag
    fx, fy = x + w - 118, y + 14
    d.rectangle([fx, fy, fx + 104, fy + 16], fill=(255, 255, 255),
                outline=INK, width=2)
    d.rectangle([fx, fy + 16, fx + 104, fy + 32], fill=(220, 20, 60),
                outline=INK, width=2)
    d.text((fx + 4, fy + 38), "POLAND", font=font(SANS_B, 14), fill=(255, 255, 255))


def draw_chart_art(d, x, y, w, h):
    """Falling red market chart."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(255, 240, 238))
    pts = [(x + 12, y + 18), (x + 58, y + 28), (x + 104, y + 26),
           (x + 150, y + 52), (x + 196, y + 64), (x + 242, y + 78),
           (x + 266, y + 88)]
    d.line(pts, fill=RED, width=6, joint="curve")
    for px, py in pts:
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED)
    # down arrow
    d.polygon([(x + w - 34, y + 12), (x + w - 12, y + 12), (x + w - 23, y + 36)],
              fill=RED)
    d.text((x + 14, y + h - 34), "S&P 500  -3.7%", font=font(SANS_B, 14),
           fill=RED)
    d.text((x + 148, y + h - 34), "NASDAQ  -5.3%", font=font(SANS_B, 14),
           fill=RED)


def draw_quake_art(d, x, y, w, h):
    """Cracked ground and seismograph trace."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(238, 232, 214))
    # shaking building
    bx, by = x + 40, y + h - 96
    d.rectangle([bx, by, bx + 74, y + h - 16], fill=(120, 84, 60),
                outline=INK, width=2)
    for wy in range(by + 12, y + h - 24, 22):
        for wx in (bx + 10, bx + 40):
            d.rectangle([wx, wy, wx + 16, wy + 12], fill=(255, 214, 90))
    d.polygon([(bx - 6, by), (bx + 37, by - 26), (bx + 80, by)],
              fill=(166, 30, 30))
    # crack in the ground (kept in the bottom strip)
    d.line([(x + 130, y + h - 14), (x + 165, y + h - 30), (x + 200, y + h - 16),
            (x + 235, y + h - 28), (x + 280, y + h - 14)], fill=INK, width=4)
    # seismograph zigzag across the top
    pts = []
    px = x + 130
    py = y + 28
    for i, dy in enumerate([0, -14, 18, -20, 12, -6, 14, -16, 5, 0]):
        pts.append((px + i * 16, py + dy))
    d.line(pts, fill=RED, width=4, joint="curve")
    d.text((x + 130, y + 60), "MAG 6.8", font=font(SANS_B, 26), fill=RED)


def draw_cop_art(d, x, y, w, h):
    """Globe with rising thermometer at COP31, Antalya."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(222, 238, 248))
    cx, cy, r = x + 95, y + 62, 46
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 140, 190),
              outline=INK, width=2)
    d.ellipse([cx - 28, cy - 20, cx + 4, cy + 6], fill=(90, 180, 110))
    d.ellipse([cx + 2, cy + 14, cx + 28, cy + 38], fill=(90, 180, 110))
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255),
          width=3)
    # thermometer
    tx = x + 210
    d.rounded_rectangle([tx, y + 26, tx + 26, y + 108], radius=12,
                        fill=(255, 255, 255), outline=INK, width=2)
    d.rectangle([tx + 5, y + 62, tx + 21, y + 104], fill=RED)
    d.ellipse([tx - 6, y + 96, tx + 32, y + 134], fill=RED, outline=INK,
              width=2)


def draw_eu_art(d, x, y, w, h):
    """Union Jack and EU stars, joined by an arrow."""
    import math
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(255, 253, 246))
    # Union Jack (simplified)
    ux, uy, uw, uh = x + 22, y + 34, 96, 64
    d.rectangle([ux, uy, ux + uw, uy + uh], fill=(0, 36, 125), outline=INK,
                width=2)
    d.line([ux, uy, ux + uw, uy + uh], fill=(255, 255, 255), width=12)
    d.line([ux + uw, uy, ux, uy + uh], fill=(255, 255, 255), width=12)
    d.line([ux + uw // 2, uy, ux + uw // 2, uy + uh], fill=(255, 255, 255),
           width=20)
    d.line([ux, uy + uh // 2, ux + uw, uy + uh // 2], fill=(255, 255, 255),
           width=20)
    d.line([ux + uw // 2, uy, ux + uw // 2, uy + uh], fill=(200, 16, 46),
           width=12)
    d.line([ux, uy + uh // 2, ux + uw, uy + uh // 2], fill=(200, 16, 46),
           width=12)
    # EU flag
    ex, ey, ew, eh = x + 190, y + 34, 96, 64
    d.rectangle([ex, ey, ex + ew, ey + eh], fill=(0, 51, 153), outline=INK,
                width=2)
    for i in range(12):
        ang = i * math.pi / 6 - math.pi / 2
        sx = ex + ew // 2 + int(22 * math.cos(ang))
        sy = ey + eh // 2 + int(20 * math.sin(ang))
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 204, 0))
    # handshake arrow between them
    d.line([x + 128, y + 66, x + 180, y + 66], fill=GOLD, width=6)
    d.polygon([(x + 180, y + 56), (x + 198, y + 66), (x + 180, y + 76)],
              fill=GOLD)
    d.text((x + 22, y + h - 30), "100,000 PLACES", font=font(SANS_B, 16),
           fill=BLUE)


def draw_houthi_art(d, x, y, w, h):
    """Interceptor arcs over the Riyadh skyline at night."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=NIGHT)
    for sx, sy, r in [(40, 24, 2), (120, 44, 2), (200, 20, 2), (280, 40, 2)]:
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                  fill=(255, 255, 220))
    # interceptor arcs (kept inside the art box)
    d.arc([x + 24, y + 26, x + 144, y + 146], 180, 360, fill=(255, 170, 60),
          width=4)
    d.arc([x + 156, y + 36, x + 276, y + 156], 180, 360, fill=(255, 170, 60),
          width=4)
    burst(d, x + 84, y + 40, 14, (255, 120, 40))
    burst(d, x + 216, y + 50, 12, (255, 120, 40))
    # Kingdom Centre tower silhouette
    tx = x + 130
    d.polygon([(tx, y + h - 96), (tx + 44, y + h - 96), (tx + 44, y + h - 14),
               (tx, y + h - 14)], fill=(8, 16, 34))
    d.polygon([(tx + 6, y + h - 96), (tx + 38, y + h - 96),
               (tx + 22, y + h - 74)], fill=(8, 16, 34))
    skyline(d, x + 16, y + h - 8, [40, 56, 34, 48], (8, 16, 34))
    skyline(d, x + 210, y + h - 8, [52, 38, 60], (8, 16, 34))
    d.text((x + 14, y + h - 30), "3rd NIGHT RUNNING", font=font(SANS_B, 15),
           fill=(255, 214, 90))


def draw_pill_art(d, x, y, w, h):
    """Capsule and a clear scan circle."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(232, 246, 232))
    # capsule
    cx, cy = x + 84, y + 78
    d.rounded_rectangle([cx - 78, cy - 24, cx + 78, cy + 24], radius=24,
                        fill=(255, 255, 255), outline=INK, width=2)
    d.rounded_rectangle([cx - 78, cy - 24, cx, cy + 24], radius=24,
                        fill=RED)
    d.rectangle([cx - 78, cy - 24, cx, cy + 24], fill=RED)
    d.ellipse([cx - 78, cy - 24, cx - 30, cy + 24], fill=RED)
    # scan circle with check
    sx, sy, r = x + 236, y + 78, 46
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255),
              outline=(46, 125, 50), width=4)
    d.line([sx - 22, sy + 2, sx - 6, sy + 18, sx + 26, sy - 18],
           fill=(46, 125, 50), width=7, joint="curve")
    d.text((x + 14, y + h - 30), "1 IN 12 CLEAR", font=font(SANS_B, 16),
           fill=(46, 125, 50))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin

    # ---- masthead ----
    d.rectangle([0, 0, W, 118], fill=INK)
    d.text((M, 12), "THE WORLD IN ONE PICTURE",
           font=font(SERIF, 58), fill=(246, 241, 231))
    d.text((M, 82), "SATURDAY  21  NOVEMBER  2026",
           font=font(SANS_B, 24), fill=GOLD)
    d.text((W - M - 300, 84), "THE DAY'S NEWS  •  ONE PAGE",
           font=font(SANS_B, 17), fill=(200, 200, 200))
    d.line([0, 118, W, 118], fill=RED, width=6)

    # ---- lead story ----
    ly = 132
    panel(d, M, ly, W - 2 * M, 312)
    ax, ay, aw, ah = M + 14, ly + 14, 420, 284
    draw_lead_art(d, ax, ay, aw, ah)
    tx = M + 14 + 420 + 22
    tw = W - M - tx - 14
    y = ly + 16
    y = kicker(d, tx, y, "WAR IN EUROPE  •  KYIV  •  WARSAW")
    y = headline(d, tx, y, "MISSILES FALL ON POLAND AS RUSSIA POUNDS UKRAINE",
                 font(SERIF, 38), tw, leading=1.02)
    y += 6
    y = para(d, tx, y,
             "Russia fired 400+ drones and 110 missiles at Ukraine "
             "overnight — its biggest barrage of the year. At least eight "
             "were killed in Kyiv.",
             font(SANS, 18), tw)
    y += 4
    y = para(d, tx, y,
             "Two Russian missiles and a suspected drone came down in "
             "Poland. PM Tusk called it a deliberate provocation as NATO "
             "jets scrambled.",
             font(SANS_B, 18), tw, fill=RED)

    # ---- middle row: 3 panels ----
    my = 460
    pw, ph, gap = 304, 252, 16
    cols = [M, M + pw + gap, M + 2 * (pw + gap)]

    panel(d, cols[0], my, pw, ph)
    draw_chart_art(d, cols[0] + 12, my + 12, pw - 24, 132)
    y = my + 156
    y = kicker(d, cols[0] + 14, y, "MARKETS  •  NEW YORK")
    headline(d, cols[0] + 14, y, "AI ROUT DRAGS WALL STREET INTO CORRECTION",
             font(SERIF, 23), pw - 28, leading=1.0)

    panel(d, cols[1], my, pw, ph)
    draw_quake_art(d, cols[1] + 12, my + 12, pw - 24, 132)
    y = my + 156
    y = kicker(d, cols[1] + 14, y, "DISASTER  •  PERU")
    headline(d, cols[1] + 14, y, "6.8 QUAKE SHAKES PERU, FELT IN LIMA",
             font(SERIF, 23), pw - 28, leading=1.0)

    panel(d, cols[2], my, pw, ph)
    draw_cop_art(d, cols[2] + 12, my + 12, pw - 24, 132)
    y = my + 156
    y = kicker(d, cols[2] + 14, y, "CLIMATE  •  ANTALYA")
    headline(d, cols[2] + 14, y, "COP31 TALKS MISS DEADLINE AS DRAFT DROPS FOSSIL FUELS",
             font(SERIF, 23), pw - 28, leading=1.0)

    # ---- bottom row: 3 panels ----
    by = 728
    panel(d, cols[0], by, pw, ph)
    draw_eu_art(d, cols[0] + 12, by + 12, pw - 24, 132)
    y = by + 156
    y = kicker(d, cols[0] + 14, y, "BRITAIN  •  BRUSSELS")
    headline(d, cols[0] + 14, y, "UK AND EU SEAL POST-BREXIT DEALS",
             font(SERIF, 23), pw - 28, leading=1.0)

    panel(d, cols[1], by, pw, ph)
    draw_houthi_art(d, cols[1] + 12, by + 12, pw - 24, 132)
    y = by + 156
    y = kicker(d, cols[1] + 14, y, "MIDDLE EAST  •  RIYADH")
    headline(d, cols[1] + 14, y, "HOUTHI MISSILES AIMED AT RIYADH SHOT DOWN",
             font(SERIF, 23), pw - 28, leading=1.0)

    panel(d, cols[2], by, pw, ph)
    draw_pill_art(d, cols[2] + 12, by + 12, pw - 24, 132)
    y = by + 156
    y = kicker(d, cols[2] + 14, y, "HEALTH  •  LONDON")
    headline(d, cols[2] + 14, y, "CANCER PILL MAKES TUMOURS UNDETECTABLE",
             font(SERIF, 23), pw - 28, leading=1.0)

    # ---- footer strip ----
    fy = 992
    d.line([M, fy, W - M, fy], fill=INK, width=2)
    d.text((M, fy + 8),
           "ALSO TODAY:  Iranian tankers mass at Kharg Island as a US "
           "blockade looms  •  Trump defers any Iran strike decision to "
           "the New Year",
           font=font(SANS, 14), fill=MUTED)

    img.save(os.path.join(HERE, "entry.png"), optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
