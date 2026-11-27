#!/usr/bin/env python3
"""Render entry.png for news-image-20261127 — stdlib only.

Draws a 1024x1024 newspaper front page summing up Friday 27 November 2026:
masthead, two lead stories, markets strip, six region boxes (36 stories),
UTC timeline, schematic world map with pins, funny-but-true box, left-out box.
All text is set in an embedded 5x7 bitmap font (uppercase newspaper style).
"""
import struct
import zlib

W, H = 1024, 1024

# --- palette ---
PAPER = (250, 246, 236)
INK = (24, 24, 28)
NAVY = (16, 32, 64)
NAVY2 = (28, 52, 96)
RED = (178, 34, 34)
GOLD = (212, 175, 55)
BLUE = (30, 90, 168)
TEAL = (14, 110, 110)
GREEN = (34, 120, 60)
PURPLE = (104, 60, 140)
ORANGE = (200, 100, 20)
GREY = (110, 110, 112)
LIGHT = (232, 226, 214)
MAPSEA = (214, 230, 238)
MAPLAND = (196, 205, 178)
WHITE = (255, 255, 255)
BROWN = (122, 72, 28)

# --- 5x7 bitmap font: char -> 7 rows, 5 bits each ---
F = {
    'A': (0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    'B': (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    'C': (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E),
    'D': (0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E),
    'E': (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F),
    'F': (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10),
    'G': (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F),
    'H': (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    'I': (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    'J': (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C),
    'K': (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11),
    'L': (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F),
    'M': (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11),
    'N': (0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11),
    'O': (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    'P': (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    'Q': (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D),
    'R': (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11),
    'S': (0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E),
    'T': (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    'U': (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    'V': (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    'W': (0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11),
    'X': (0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11),
    'Y': (0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04),
    'Z': (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F),
    '0': (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E),
    '1': (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E),
    '2': (0x0E, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1F),
    '3': (0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E),
    '4': (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02),
    '5': (0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E),
    '6': (0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E),
    '7': (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08),
    '8': (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E),
    '9': (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C),
    ' ': (0, 0, 0, 0, 0, 0, 0),
    '.': (0, 0, 0, 0, 0, 0x0C, 0x0C),
    ',': (0, 0, 0, 0, 0x0C, 0x04, 0x08),
    ':': (0, 0x0C, 0x0C, 0, 0x0C, 0x0C, 0),
    ';': (0, 0x0C, 0x0C, 0, 0x0C, 0x04, 0x08),
    "'": (0x04, 0x04, 0x08, 0, 0, 0, 0),
    '!': (0x04, 0x04, 0x04, 0x04, 0x04, 0, 0x04),
    '?': (0x0E, 0x11, 0x01, 0x02, 0x04, 0, 0x04),
    '-': (0, 0, 0, 0x1F, 0, 0, 0),
    '(': (0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02),
    ')': (0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08),
    '/': (0x01, 0x01, 0x02, 0x04, 0x08, 0x10, 0x10),
    '%': (0x19, 0x19, 0x02, 0x04, 0x08, 0x13, 0x13),
    '$': (0x04, 0x0F, 0x14, 0x0E, 0x05, 0x1E, 0x04),
    '&': (0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D),
    '+': (0, 0x04, 0x04, 0x1F, 0x04, 0x04, 0),
    '=': (0, 0, 0x1F, 0, 0x1F, 0, 0),
    '*': (0, 0x04, 0x15, 0x0E, 0x15, 0x04, 0),
    '#': (0x0A, 0x0A, 0x1F, 0x0A, 0x1F, 0x0A, 0x0A),
    '"': (0x0A, 0x0A, 0x0A, 0, 0, 0, 0),
    '_': (0, 0, 0, 0, 0, 0, 0x1F),
    '<': (0x02, 0x04, 0x08, 0x10, 0x08, 0x04, 0x02),
    '>': (0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08),
    '|': (0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
}

buf = bytearray(W * H * 3)


def px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i], buf[i + 1], buf[i + 2] = c


def rect(x, y, w, h, c):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            px(xx, yy, c)


def hline(x, y, w, c, t=1):
    rect(x, y, w, t, c)


def vline(x, y, h, c, t=1):
    rect(x, y, t, h, c)


def box(x, y, w, h, c, t=1):
    hline(x, y, w, c, t)
    hline(x, y + h - t, w, c, t)
    vline(x, y, h, c, t)
    vline(x + w - t, y, h, c, t)


def circle(cx, cy, r, c, fill=True):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            d = (xx - cx) ** 2 + (yy - cy) ** 2
            if fill and d <= r * r:
                px(xx, yy, c)
            elif not fill and abs(d - r * r) <= r:
                px(xx, yy, c)


def poly(points, c):
    ys = [p[1] for p in points]
    for y in range(min(ys), max(ys) + 1):
        xs = []
        n = len(points)
        for i in range(n):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % n]
            if (y1 <= y < y2) or (y2 <= y < y1):
                xs.append(int(x1 + (y - y1) * (x2 - x1) / (y2 - y1)))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            for x in range(xs[i], xs[i + 1] + 1):
                px(x, y, c)


def text(x, y, s, c, scale=2, bold=False):
    s = s.upper()
    cx = x
    for ch in s:
        g = F.get(ch)
        if g is None:
            cx += 6 * scale
            continue
        for row in range(7):
            bits = g[row]
            for col in range(5):
                if bits & (1 << (4 - col)):
                    for dy in range(scale):
                        for dx in range(scale):
                            px(cx + col * scale + dx, y + row * scale + dy, c)
                            if bold:
                                px(cx + col * scale + dx + 1, y + row * scale + dy, c)
        cx += 6 * scale
    return cx


def tw(s, scale=2):
    return len(s) * 6 * scale


def center(y, s, c, scale=2, bold=False, x0=0, x1=W):
    text(x0 + (x1 - x0 - tw(s, scale)) // 2, y, s, c, scale, bold)


# ---------------- content (all real, first reported Fri 27 Nov 2026) ----------------
LEAD1_HEAD = ["EAGLES ERASE 21 POINTS", "TO STUN COWBOYS 39-38"]
LEAD1_BODY = [
    "DOWN 31-10 IN 3RD, PHILLY RALLIED",
    "FOR THE BIGGEST THANKSGIVING COMEBACK",
    "IN NFL HISTORY. MILTON: 331 YDS, 3 TD",
    "ELLIOTT 59-YD FG WINS IT, 2 SEC LEFT",
    "DALLAS FALLS TO 5-7; PLAYOFFS FADE.",
]
LEAD2_HEAD = ["TRUMP TO PUTIN:", "STOP THE WAR"]
LEAD2_BODY = [
    "TRUMP: I URGED PUTIN TO END FIGHTING",
    "IN EUROPE. KUSHNER: TALKS STALLED",
    "AND CALLS THE WAR A PROXY FIGHT.",
    "EU SPLIT OVER BUDGET; MERZ WANTS CUTS",
    "US OKs $621.9M IN F-16s FOR KYIV.",
]

MARKETS = [
    "MARKETS - BLACK FRIDAY: S&P FUT +0.54%  DOW +0.43%",
    "NASDAQ 100 +0.46%  S&P +3.9% THIS WEEK  BRENT $96.20",
    "GOLD $3,567  BITCOIN $60,399  NIFTY 25,885 +0.25%",
]

REGIONS = [
    ("EUROPE", RED, [
        "UK CALLS UP 100,000 RESERVISTS",
        "MERZ BLOCKS EU BUDGET, SEEKS CUTS",
        "UK GETS SWISS-STYLE SAY IN EU VOTES",
        "UK SANCTIONS HOUTHIS OVER SAUDI RAID",
        "TRAIN KNIFEMAN GUILTY, ATTACKED 14",
        "DEPARDIEU TO FACE SEX-ASSAULT TRIAL",
    ]),
    ("MIDDLE EAST", ORANGE, [
        "GAZA STRIKES KILL 9, INCL. A MINISTER",
        "SAUDI COALITION HITS 50 HOUTHI POSTS",
        "HOUTHI HIT ON SAUDI REFINERY KILLS 1",
        "NEW ISRAELI ROAD CUTS BY BETHLEHEM",
        "IRAN ENERGY CRISIS DEEPENS IN WAR",
        "IRAQ JAILS 8 FRENCHMEN FOR LIFE",
    ]),
    ("ASIA-PACIFIC", TEAL, [
        "KIM VOWS MORE NUCLEAR WARHEADS",
        "S. KOREA RAISES RATES, LIFTS GDP VIEW",
        "CHINA LOFTS NEW SPY SATELLITES",
        "NZ HUNG PARLIAMENT; CENTRISTS DECIDE",
        "14 DEAD IN INDONESIA MINE FLOOD",
        "BLAST AT THAILAND OIL PLANT",
    ]),
    ("AFRICA", GREEN, [
        "31 KILLED IN CAIRO FUEL TRUCK FIRE",
        "CONGO EBOLA TOPS 12,000 CASES",
        "KENYA HALTS US-FUNDED EBOLA CENTRE",
        "GUINEA ORDERS CLEAN-UP OF CONAKRY",
        "5 YEARS ON: DID THE ADF GET WEAKER?",
        "ZAMBIA 'COUP PLOT' POINTS AT RUSSIA",
    ]),
    ("AMERICAS", BLUE, [
        "US OKs $621.9M F-16s FOR UKRAINE",
        "FEDEX JET OFF RUNWAY IN MIAMI",
        "ICE HOLDS MAN WHO WON $1M LOTTERY PRIZE",
        "STORMS BATTER US ON THANKSGIVING DAY",
        "BRAZIL TAPS TRABUCO AS FINANCE CHIEF",
        "TRUMP FLOATS NEW TARIFFS ON CHINA, EU",
    ]),
    ("TECH AND SPORT", PURPLE, [
        "BEARS BEAT LIONS 39-35, 3 SECONDS LEFT",
        "BILLS BEAT CHIEFS 13-10 IN THE RAIN",
        "US CLOSES NVIDIA CHIP LOOPHOLE",
        "DRONE SETS 727 KM/H WORLD SPEED RECORD",
        "FRANCE: 'UNPRECEDENTED' CYBER THREAT",
        "DRONE BLAST IN KUWAIT KILLS STAFF",
    ]),
]

TIMELINE = [
    ("00:00", "BEARS WIN 39-35"),
    ("00:17", "850 KM IN BUDGIES"),
    ("02:14", "FAA HALTS MIAMI"),
    ("02:32", "MERZ BLOCKS BUDGET"),
    ("03:24", "DEPARDIEU TO TRIAL"),
    ("03:54", "TURKIYE REJECTS EU"),
    ("04:22", "IRAN ECONOMY BITES"),
    ("05:00", "UK CALLS 100,000 UP"),
]

FUNNY = [
    ("A MAN CROSSED 850 KM IN ONLY BUDGY SMUGGLERS.",
     "FERRY, TRAIN, BUS, BIKE, UBER SAID YES. PLANE: NO."),
    ("ALASKA'S 'TURKEY BOMBERS' DROPPED 42 FROZEN TURKEYS",
     "FROM A PLANE ONTO CABINS. ONE LANDED IN A BUSH."),
    ("A COUPLE PLANTED A TREE IN A 15-YEAR-OLD POTHOLE.",
     "IT WENT VIRAL - THE CREW FIXED IT IN 2 DAYS."),
]

LEFT_OUT = [
    "COP31 HOT-MIC GAFFE - 13 NOV",
    "GTA 6 FANS FEEL OLD - OLDER",
    "AI HARRY STYLES PHOTO - OLDER",
]

# ---------------- draw ----------------
rect(0, 0, W, H, PAPER)

# masthead: 0-66, summary 72, rule 92
rect(0, 0, W, 66, NAVY)
center(6, "THE WORLD IN ONE PICTURE", WHITE, 4, bold=True)
center(42, "FRIDAY 27 NOVEMBER 2026  -  41 STORIES  -  9 REGIONS", GOLD, 2, bold=True)
text(8, 72, "THANKSGIVING COMEBACKS, A WAR THAT WILL NOT END, AND A MAN IN BUDGY SMUGGLERS",
     INK, 2, bold=True)
hline(8, 92, W - 16, INK, 2)

# leads: y 100-250
LY, LH, LW = 100, 150, 500
for (bx, head, lines, body, accent) in [
    (8, "LEAD 1 - AMERICAN FOOTBALL", LEAD1_HEAD, LEAD1_BODY, RED),
    (516, "LEAD 2 - WAR AND DIPLOMACY", LEAD2_HEAD, LEAD2_BODY, BLUE),
]:
    rect(bx, LY, LW, LH, WHITE)
    box(bx, LY, LW, LH, INK, 2)
    rect(bx, LY, LW, 22, accent)
    text(bx + 8, LY + 4, head, WHITE, 2, bold=True)
    yy = LY + 30
    for ln in lines:
        text(bx + 10, yy, ln, INK, 3, bold=True)
        yy += 23
    yy += 1
    for ln in body:
        text(bx + 10, yy, ln, INK, 2)
        yy += 14
    if accent == RED:  # football pictogram
        cx, cy = bx + LW - 52, LY + 44
        for dy in range(-14, 15):
            wdt = int(26 * (1 - (dy / 15) ** 2) ** 0.5)
            for dx in range(-wdt, wdt + 1):
                px(cx + dx, cy + dy, BROWN)
        hline(cx - 18, cy, 36, WHITE, 2)
        for lx in (-12, -6, 0, 6, 12):
            vline(cx + lx, cy - 4, 8, WHITE, 2)
    else:  # globe pictogram
        cx, cy = bx + LW - 52, LY + 44
        circle(cx, cy, 20, BLUE)
        circle(cx, cy, 20, WHITE, fill=False)
        for k in range(-1, 2):
            vline(cx + k * 10, cy - 18, 36, WHITE, 1)
        hline(cx - 20, cy, 40, WHITE, 1)

# markets strip: y 256-306
MY = 256
rect(8, MY, W - 16, 50, NAVY2)
text(16, MY + 4, MARKETS[0], GOLD, 2, bold=True)
text(16, MY + 19, MARKETS[1], WHITE, 2)
text(16, MY + 34, MARKETS[2], WHITE, 2)

# region grid: 2 cols x 3 rows, y 312-696
RY, RH, RW, GAP = 312, 124, 500, 6
for idx, (name, color, stories) in enumerate(REGIONS):
    col, row = idx % 2, idx // 2
    bx = 8 + col * (RW + 8)
    by = RY + row * (RH + GAP)
    rect(bx, by, RW, RH, WHITE)
    box(bx, by, RW, RH, INK, 2)
    rect(bx, by, RW, 22, color)
    text(bx + 8, by + 4, name, WHITE, 2, bold=True)
    yy = by + 28
    for st in stories:
        text(bx + 10, yy, "* " + st, INK, 2)
        yy += 16

# timeline: y 702-758
TY = 702
rect(8, TY, W - 16, 56, LIGHT)
box(8, TY, W - 16, 56, INK, 2)
text(16, TY + 4, "THE DAY IN UTC", INK, 2, bold=True)
hline(16, TY + 22, W - 32, GREY, 1)
for i, (t, label) in enumerate(TIMELINE):
    cx = 16 + i * 124 + 62
    circle(cx, TY + 22, 4, RED)
    text(cx - tw(t, 1) // 2, TY + 30, t, RED, 1, bold=True)
    text(cx - tw(label, 1) // 2, TY + 42, label, INK, 1)

# map band: y 764-854
MAPY = 764
rect(8, MAPY, W - 16, 90, MAPSEA)
box(8, MAPY, W - 16, 90, INK, 2)
text(16, MAPY + 4, "WHERE IT HAPPENED", INK, 2, bold=True)
ox, oy = 8, MAPY + 20
poly([(ox + 60, oy + 14), (ox + 150, oy + 3), (ox + 235, oy + 9), (ox + 250, oy + 29),
      (ox + 200, oy + 41), (ox + 150, oy + 54), (ox + 90, oy + 45), (ox + 55, oy + 29)], MAPLAND)
poly([(ox + 280, oy + 34), (ox + 330, oy + 30), (ox + 350, oy + 51), (ox + 320, oy + 66),
      (ox + 290, oy + 54)], MAPLAND)
poly([(ox + 470, oy + 6), (ox + 530, oy + 3), (ox + 545, oy + 20), (ox + 500, oy + 29),
      (ox + 465, oy + 20)], MAPLAND)
poly([(ox + 470, oy + 30), (ox + 540, oy + 27), (ox + 560, oy + 53), (ox + 520, oy + 68),
      (ox + 480, oy + 57), (ox + 460, oy + 39)], MAPLAND)
poly([(ox + 550, oy + 5), (ox + 700, oy + 2), (ox + 780, oy + 14), (ox + 760, oy + 39),
      (ox + 650, oy + 45), (ox + 580, oy + 33), (ox + 545, oy + 20)], MAPLAND)
poly([(ox + 800, oy + 48), (ox + 870, oy + 45), (ox + 880, oy + 60), (ox + 820, oy + 63)], MAPLAND)
PINS = [
    (140, 30, "DALLAS"), (170, 21, "DETROIT"), (490, 12, "LONDON"), (540, 15, "KYIV"),
    (560, 33, "GAZA"), (585, 36, "RIYADH"), (620, 29, "TEHRAN"), (700, 17, "BEIJING"),
    (740, 20, "SEOUL"), (730, 50, "JAKARTA"), (530, 39, "CAIRO"), (520, 56, "CONGO"),
    (850, 57, "SYDNEY"), (320, 50, "BRASILIA"),
]
for (pxx, pyy, lab) in PINS:
    circle(ox + pxx, oy + pyy, 4, RED)
    text(ox + pxx + 6, oy + pyy - 4, lab, INK, 1, bold=True)

# funny + left out: y 860-976
FY, FH, FW = 860, 116, 656
rect(8, FY, FW, FH, WHITE)
box(8, FY, FW, FH, INK, 2)
rect(8, FY, FW, 20, GOLD)
text(16, FY + 3, "FUNNY BUT TRUE - REAL, 27 NOV", INK, 2, bold=True)
fy = FY + 26
for a, b in FUNNY:
    text(16, fy, a, INK, 2)
    fy += 15
    text(16, fy, b, INK, 2)
    fy += 17
LX = 8 + FW + 8
LW2 = W - 16 - FW - 8
rect(LX, FY, LW2, FH, WHITE)
box(LX, FY, LW2, FH, INK, 2)
rect(LX, FY, LW2, 20, GREY)
text(LX + 8, FY + 3, "LEFT OUT - OLDER NEWS", WHITE, 2, bold=True)
ly = FY + 28
for ln in LEFT_OUT:
    text(LX + 8, ly, ln, INK, 1)
    ly += 12

# footer
text(8, 984, "SOURCES: AP, NBC SPORTS, USA TODAY, REUTERS, AL JAZEERA, BLOOMBERG, B&T, KTUU, THE MERCURY,",
     GREY, 1)
text(8, 994, "MORNINGSTAR, UPSTOX - ALL STORIES FIRST REPORTED FRIDAY 27 NOVEMBER 2026 (ANY TIME ZONE).",
     GREY, 1)
hline(8, 1008, W - 16, INK, 1)


def write_png(path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw.extend(buf[y * W * 3:(y + 1) * W * 3])
    comp = zlib.compress(bytes(raw), 9)

    def chunk(typ, data):
        c = struct.pack('>I', len(data)) + typ + data
        return c + struct.pack('>I', zlib.crc32(typ + data) & 0xFFFFFFFF)

    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', comp)
    png += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)
    return len(png)


if __name__ == '__main__':
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else 'entry.png'
    n = write_png(out)
    print(f'wrote {out}: {n} bytes, {W}x{H}')
