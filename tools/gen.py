#!/usr/bin/env python3
# ============================================================
#  PIXEL README GENERATOR — Kevin RAND
#  Pixel art discret, inspiré de GENIDRAW : polices pixel, ornements pixel à plusieurs
#  opacités, flore qui pousse depuis les coins, trames en demi-teinte, barres segmentées.
#  Fonds transparents ; chaque visuel existe en version claire ET sombre (assets/light, assets/dark).
#
#  Modifie la CONFIG ci-dessous puis lance :  python tools/gen.py
#  Dépendance : pip install fonttools  (les polices OFL sont téléchargées au 1er lancement)
# ============================================================
FIRST, LAST = "KEVIN", "RAND"
ROLES     = ["web developer", "bug hunter", "hardcore addict"]      # mot manuscrit qui tourne
BADGE     = "WEB DEVELOPER • BUG HUNTER • 180 BPM • "               # texte du badge circulaire
STATUS    = "CODING @ 180 BPM"
KICKER    = "N°07 — PLAYER ONE"
CLAIM     = "I BUILD STUFF FOR THE WEB."
NOTE      = ["FUELED BY HAPPY", "HARDCORE @ 180 BPM"]
HELLO     = "HEY! WELCOME TO MY PROFILE."
INTRO     = ["I BUILD STUFF FOR THE WEB, FUELED BY", "HAPPY HARDCORE @ 180 BPM."]    # une entrée = une ligne
CLASS     = "WEB DEVELOPER"
LEVEL     = "07"
COUNTERS  = [("07", "LEVEL"), ("10", "ITEMS IN BAG"), ("180", "BPM"), ("99+", "COFFEES")]
STATS     = [("FRONTEND", 9), ("BACKEND", 7), ("DEBUG", 8), ("UI / UX", 6), ("CAFFEINE", 10), ("BPM", 10)]
# (nom, icône, description ligne 1, ligne 2, rareté 1-5)
ITEMS = [
    ("JavaScript", "sword",  "MAIN WEAPON.",     "HITS EVERY BROWSER.", 5),
    ("TypeScript", "shield", "BLOCKS 99% OF",    "RUNTIME BUGS.",       4),
    ("HTML",       "scroll", "THE MAP OF",       "EVERY LEVEL.",        3),
    ("CSS",        "gem",    "MAKES ANYTHING",   "SHINE.",              4),
    ("React",      "ring",   "SUMMONS REUSABLE", "COMPONENTS.",         5),
    ("Node.js",    "potion", "RESTORES",         "BACKEND HP.",         4),
    ("PHP",        "hammer", "OLD SCHOOL.",      "STILL HITS HARD.",    3),
    ("SQL",        "key",    "OPENS EVERY",      "DATABASE.",           3),
    ("Git",        "book",   "REWINDS TIME.",    "INFINITE SAVES.",     5),
    ("Bash",       "bomb",   "ONE COMMAND.",     "BOOM.",               4),
]
TRACK     = ("HAPPY HARDCORE MEGAMIX", "VOL. 180 — STAY HAPPY, STAY HARDCORE")
SECTIONS  = {  # séparateurs : (texte gauche, texte droite)
    "profile": ("PLAYER 1", "PROFILE"),
    "stack":   ("INVENTORY", "STACK"),
    "scores":  ("HIGH SCORES", "GITHUB"),
    "music":   ("NOW PLAYING", "SOUNDTRACK"),
    "bonus":   ("BONUS STAGE", "CONTRIBUTIONS"),
    "contact": ("CONTINUE ?", "CONTACT"),
}
OUTRO     = ("LET'S BUILD", "SOMETHING", "together")
LINKS     = [("email", "EMAIL"), ("linkedin", "LINKEDIN"), ("portfolio", "PORTFOLIO")]
# Polices pixel (Google Fonts, licence OFL) : (fichier, axes variables)
FONT_DISPLAY = ("doto", {"ROND": 0, "wght": 700})   # titres : matrice de points carrés espacés
FONT_TEXT    = ("pixelify", {"wght": 400})          # noms, boutons
FONT_LABEL   = ("silkscreen", None)                 # petits libellés en capitales
FONT_ACCENT  = ("jacquard24", None)                 # mot d'accent en ambre
# ============================================================
import colorsys, datetime, math, os, urllib.request
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "assets")
FONT_DIR = os.path.join(ROOT, "fonts")
FONT_URLS = {
    "doto":       "https://github.com/google/fonts/raw/main/ofl/doto/Doto%5BROND,wght%5D.ttf",
    "pixelify":   "https://github.com/google/fonts/raw/main/ofl/pixelifysans/PixelifySans%5Bwght%5D.ttf",
    "silkscreen": "https://github.com/google/fonts/raw/main/ofl/silkscreen/Silkscreen-Regular.ttf",
    "jacquard24": "https://github.com/google/fonts/raw/main/ofl/jacquard24/Jacquard24-Regular.ttf",
}


def n(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# ---------------- FONTS → PATHS ----------------
# Le texte est vectorisé : GitHub n'affiche pas les polices web dans une image SVG.
def font_file(key):
    path = os.path.join(FONT_DIR, key + ".ttf")
    if not os.path.exists(path):
        os.makedirs(FONT_DIR, exist_ok=True)
        print("téléchargement de la police", key)
        urllib.request.urlretrieve(FONT_URLS[key], path)
    return path


def kern_lookups(font):
    if "GPOS" not in font:
        return []
    gpos = font["GPOS"].table
    indices = sorted({i for rec in gpos.FeatureList.FeatureRecord if rec.FeatureTag == "kern" for i in rec.Feature.LookupListIndex})
    lookups = []
    for i in indices:
        lookup = gpos.LookupList.Lookup[i]
        subtables = []
        for sub in lookup.SubTable:
            if lookup.LookupType == 9:
                if sub.ExtensionLookupType != 2:
                    continue
                sub = sub.ExtSubTable
            elif lookup.LookupType != 2:
                continue
            subtables.append((sub, {g: k for k, g in enumerate(sub.Coverage.glyphs)}))
        if subtables:
            lookups.append(subtables)
    return lookups


def pair_value(subtables, a, b):
    for sub, coverage in subtables:
        if a not in coverage:
            continue
        if sub.Format == 1:
            for rec in sub.PairSet[coverage[a]].PairValueRecord:
                if rec.SecondGlyph == b:
                    return (getattr(rec.Value1, "XAdvance", 0) or 0) if rec.Value1 else 0
            continue
        c1 = sub.ClassDef1.classDefs.get(a, 0) if sub.ClassDef1 else 0
        c2 = sub.ClassDef2.classDefs.get(b, 0) if sub.ClassDef2 else 0
        value = sub.Class1Record[c1].Class2Record[c2].Value1
        return (getattr(value, "XAdvance", 0) or 0) if value else 0
    return 0


class Face:
    def __init__(self, key, axes=None):
        font = TTFont(font_file(key))
        if axes and "fvar" in font:
            font = instancer.instantiateVariableFont(font, axes)
        self.upm = font["head"].unitsPerEm
        self.cmap = font.getBestCmap()
        self.glyphs = font.getGlyphSet()
        self.hmtx = font["hmtx"]
        self.lookups = kern_lookups(font)
        self.kerns = {}

    def name(self, ch):
        return self.cmap.get(ord(ch)) or self.cmap[ord("?")]

    def kern(self, a, b):
        if (a, b) not in self.kerns:
            self.kerns[a, b] = sum(pair_value(subtables, a, b) for subtables in self.lookups)
        return self.kerns[a, b]

    def layout(self, text, size, track=0.0):
        s = size / self.upm
        names = [self.name(ch) for ch in text]
        xs, x = [], 0.0
        for i, g in enumerate(names):
            xs.append(x)
            x += self.hmtx[g][0] * s + track * size
            if i + 1 < len(names):
                x += self.kern(g, names[i + 1]) * s
        return names, xs, (x - track * size if names else 0.0)

    def width(self, text, size, track=0.0):
        return self.layout(text, size, track)[2]

    def d(self, text, x, y, size, track=0.0, anchor="start"):
        names, xs, w = self.layout(text, size, track)
        ox = x - {"start": 0, "middle": w / 2, "end": w}[anchor]
        s = size / self.upm
        out = []
        for g, gx in zip(names, xs):
            pen = SVGPathPen(self.glyphs, ntos=n)
            self.glyphs[g].draw(TransformPen(pen, (s, 0, 0, -s, ox + gx, y)))
            out.append(pen.getCommands())
        return "".join(out)

    def wrap(self, text, size, track, max_width):
        lines, line = [], ""
        for word in text.split():
            test = f"{line} {word}".strip()
            if line and self.width(test, size, track) > max_width:
                lines.append(line)
                line = word
            else:
                line = test
        return lines + [line]


DISPLAY, TEXT, LABEL, ACCENT = (Face(*spec) for spec in (FONT_DISPLAY, FONT_TEXT, FONT_LABEL, FONT_ACCENT))


def text(face, s, x, y, size, color, alpha=1, track=0.0, anchor="start", extra=""):
    op = f' fill-opacity="{n(alpha)}"' if alpha < 1 else ""
    return f'<path d="{face.d(s, x, y, size, track, anchor)}" fill="{color}"{op}{extra}/>'


KICK = 11   # taille des petits libellés


def kicker(s, x, y, color, alpha=1, anchor="start", size=KICK, track=0.14):
    return text(LABEL, s, x, y, size, color, alpha, track, anchor)


# ---------------- PALETTE (tokens de genidraw-ui) ----------------
def hsl(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return "#%02x%02x%02x" % tuple(round(v * 255) for v in (r, g, b))


PRIMARY = hsl(33, 90, 48)
# fonds transparents : seules les encres changent entre le thème clair et le thème sombre de GitHub
THEMES = {
    "light": dict(fg=hsl(30, 12, 8), mfg=hsl(30, 6, 42), border=hsl(32, 12, 84)),
    "dark":  dict(fg=hsl(36, 18, 90), mfg=hsl(33, 8, 62), border=hsl(33, 8, 24)),
}


# ---------------- SVG ----------------
_ids = [0]


def uid():
    _ids[0] += 1
    return f"i{_ids[0]}"


KEYFRAMES = ("@keyframes fin{from{opacity:0}}"
             "@keyframes blink{50%{opacity:0}}"
             "@keyframes spin{to{transform:rotate(360deg)}}"
             "@keyframes spx{0%,100%{opacity:.15}30%{opacity:1}}"
             "@keyframes head{0%,100%{opacity:.35}50%{opacity:1}}"
             "@keyframes beat{0%,100%{opacity:1}50%{opacity:.55}}")


def svg(w, h, body, label, css="", defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">'
            f'<title>{label}</title><style>{KEYFRAMES}{css}@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>'
            f'<defs>{defs}</defs>{body}</svg>')


def anim(name, dur, delay=0.0, extra="both"):
    return f' style="animation:{name} {dur}s {extra} {n(delay)}s"'


def sq(x, y, s):
    return f"M{n(x)} {n(y)}h{n(s)}v{n(s)}h-{n(s)}z"


def cells_d(cells, cell, gap=0.0, ox=0.0, oy=0.0):
    return "".join(sq(ox + x * cell + gap, oy + y * cell + gap, cell - 2 * gap) for x, y in cells)


# ---------------- ORNEMENT (rosace pixel de genidraw) ----------------
ORN_PETAL = ["....333....", "...31123...", "...31123...", "....312...."]
ORN_BUDS = [(1, 1, "5"), (2, 2, "6")]
ORN_CENTER = ["444", "484", "444"]
ORN_OPACITY = {"1": .45, "2": .7, "3": 1, "4": .18, "5": .4, "6": .65, "8": .9}


def ornament_cells():
    size = 11
    grid = [["."] * size for _ in range(size)]

    def place(x, y, tone):
        column, row = x, y
        for _ in range(4):
            grid[row][column] = tone
            column, row = size - 1 - row, column

    for y, line in enumerate(ORN_PETAL):
        for x, tone in enumerate(line):
            if tone != ".":
                place(x, y, tone)
    for x, y, tone in ORN_BUDS:
        place(x, y, tone)
    for y, line in enumerate(ORN_CENTER):
        for x, tone in enumerate(line):
            grid[y + 4][x + 4] = tone
    return [(x, y, grid[y][x]) for y in range(size) for x in range(size) if grid[y][x] != "."]


def ornament(x, y, cell, color, bloom=None, alpha=1.0):
    """bloom = délai (s) : les pixels s'allument anneau par anneau depuis le cœur."""
    groups = {}
    for cx, cy, tone in ornament_cells():
        ring = max(abs(cx - 5), abs(cy - 5)) if bloom is not None else 0
        groups.setdefault((ring, tone), []).append((cx, cy))
    out = []
    for (ring, tone), cells in sorted(groups.items()):
        style = anim("fin", .5, bloom + ring * .12, "ease-out both") if bloom is not None else ""
        out.append(f'<path d="{cells_d(cells, cell, 0, x, y)}" fill="{color}" fill-opacity="{n(ORN_OPACITY[tone] * alpha)}"{style}/>')
    return f'<g shape-rendering="crispEdges">{"".join(out)}</g>'


# ---------------- FLORE (portage de genidraw flora.ts) ----------------
BLOSSOMS = [[".1.", "142", ".2."],
            [".11.", "1142", "1222", ".23."],
            [".112.", "11112", "11422", "12223", ".233."],
            ["..11..", ".1112.", "111422", "112223", ".1223.", "..33.."]]
LEAVES = [[".555..", "555566", "..666."], [".55...", "555666", ".5666.", "...66."]]
FLORA_OPACITY = {1: .34, 2: .58, 3: .85, 4: .14, 5: .22, 6: .42, 7: .5}
DITHERED = {1, 4, 5}
M32 = 0xFFFFFFFF


def mulberry(seed):
    state = [seed & M32]

    def nxt():
        state[0] = (state[0] + 0x6D2B79F5) & M32
        v = state[0]
        v = ((v ^ (v >> 15)) * (v | 1)) & M32
        v ^= (v + (((v ^ (v >> 7)) * (v | 61)) & M32)) & M32
        return ((v ^ (v >> 14)) & M32) / 4294967296
    return nxt


def jsround(v):
    return math.floor(v + .5)


def rotate(sprite, turns):
    for _ in range(turns % 4):
        h, w = len(sprite), len(sprite[0])
        sprite = ["".join(sprite[h - 1 - c][r] for c in range(h)) for r in range(w)]
    return sprite


def mirror(sprite):
    return [row[::-1] for row in sprite]


def grow_flora(size, seed, branches=4):
    nxt = mulberry(seed)
    grid = {}

    def plot(x, y, tone):
        if 0 <= x < size and 0 <= y < size:
            grid[y * size + x] = tone

    def stamp(sprite, cx, cy, shade):
        top, left = jsround(cy - len(sprite) / 2), jsround(cx - len(sprite[0]) / 2)
        for dy, row in enumerate(sprite):
            for dx, ch in enumerate(row):
                if ch == ".":
                    continue
                tone = int(ch)
                if shade and tone <= 3:
                    tone = min(3, tone + shade)
                plot(left + dx, top + dy, tone)

    blossoms, leaves = [], []

    def cluster(x, y, count, spread, scale):
        for _ in range(count):
            angle = nxt() * math.pi * 2
            radius = nxt() * spread
            pick = min(len(BLOSSOMS) - 1, math.floor(nxt() * len(BLOSSOMS) * scale + (1 - scale)))
            sprite = rotate(BLOSSOMS[pick], math.floor(nxt() * 4))
            if nxt() > .5:
                sprite = mirror(sprite)
            blossoms.append((x + math.cos(angle) * radius, y + math.sin(angle) * radius, sprite, 1 if nxt() < .35 else 0))

    for branch in range(branches):
        base = .26 + (1.05 * (branch + .5)) / branches + (nxt() - .5) * .2
        length = size * (.62 + nxt() * .36)
        bend = (nxt() - .5) * .9
        x, y = nxt() * 3, nxt() * 3
        side = 1 if nxt() > .5 else -1
        since_leaf = since_bloom = 0.0
        travelled = 0.0
        while travelled < length:
            progress = travelled / length
            heading = base + bend * progress
            x += math.cos(heading) * .5
            y += math.sin(heading) * .5
            plot(jsround(x), jsround(y), 7)
            if progress < .3:
                plot(jsround(x) + 1, jsround(y), 7)
            since_leaf += .5
            since_bloom += .5
            if since_leaf >= 6 + nxt() * 3 and progress > .08:
                since_leaf = 0
                normal = heading + side * math.pi / 2
                turns = jsround((math.fmod(normal, math.pi * 2) + math.pi * 2) / (math.pi / 2)) % 4
                sprite = rotate(LEAVES[math.floor(nxt() * len(LEAVES))], turns)
                if nxt() > .5:
                    sprite = mirror(sprite)
                leaves.append((x + math.cos(normal) * 3, y + math.sin(normal) * 3, sprite))
                side = -side
            if progress > .3 and since_bloom >= 4 + nxt() * 4:
                since_bloom = 0
                cluster(x, y, 1 + math.floor(nxt() * 3), 3 + progress * 3, .5 + progress * .5)
            travelled += .5
        cluster(x, y, 4 + math.floor(nxt() * 3), 5, 1)

    for lx, ly, sprite in leaves:
        stamp(sprite, lx, ly, 0)
    for bx, by, sprite, shade in blossoms:
        if shade:
            stamp(sprite, bx, by, 1)
    for bx, by, sprite, shade in blossoms:
        if not shade:
            stamp(sprite, bx, by, 0)
    cells = [(k % size, k // size, tone) for k, tone in grid.items()]
    cells = [(x, y, tone, math.hypot(x, y) + nxt() * 4) for x, y, tone in cells]
    return sorted(cells, key=lambda c: c[3])


def flora(ink, corner, x0, y0, size=56, cell=6, seed=7, branches=4, grow=.3, alpha=1.0, soft=.8):
    """Couche nette masquée depuis le coin + couche floue dessous, comme PixelFlora.tsx.
    grow = délai (s) avant la pousse, None = déjà poussée."""
    cells = grow_flora(size, seed, branches)
    side = size * cell
    flip_x, flip_y = corner.endswith("right"), corner.startswith("bottom")
    steps = 16
    groups = {}
    for i, (x, y, tone, _) in enumerate(cells):
        if tone in DITHERED and (x + y) % 2 == 1:
            continue
        px, py = (size - 1 - x if flip_x else x), (size - 1 - y if flip_y else y)
        progress = 1 - math.sqrt(max(0.0, 1 - i / len(cells)))   # inverse de l'ease-out
        bucket = min(steps - 1, int(progress * steps)) if grow is not None else 0
        groups.setdefault((bucket, tone), []).append((px, py))
    sharp = []
    for (bucket, tone), group in sorted(groups.items()):
        style = anim("fin", .45, grow + bucket / steps * 1.7, "ease-out both") if grow is not None else ""
        sharp.append(f'<path d="{cells_d(group, cell, 1)}" fill="{ink}" fill-opacity="{FLORA_OPACITY[tone]}"{style}/>')
    gid, mid, fid, lid = uid(), uid(), uid(), uid()
    defs = (f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="{side if flip_x else 0}" cy="{side if flip_y else 0}" r="{n(side * 1.4142)}">'
            f'<stop offset=".16" stop-color="#fff"/><stop offset=".64" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="0" y="0" width="{side}" height="{side}"><rect width="{side}" height="{side}" fill="url(#{gid})"/></mask>'
            f'<filter id="{fid}" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="7"/></filter>')
    body = (f'<g transform="translate({n(x0)} {n(y0)})" opacity="{n(alpha)}">'
            f'<use href="#{lid}" filter="url(#{fid})" opacity="{n(soft)}"/>'
            f'<g mask="url(#{mid})"><g id="{lid}" shape-rendering="crispEdges">{"".join(sharp)}</g></g></g>')
    return defs, body


# ---------------- TRAME DEMI-TEINTE (PixelField « stepped ») ----------------
STEP_SIDE, STEP_ALPHA = [0, .34, .56, .8], [0, .45, .7, 1]
FIELD_PERIOD = 90   # colonnes : la trame boucle horizontalement pour pouvoir dériver


def halftone(cols, rows, cell, color, intensity, phase=0.0):
    k1, k3 = 2 * math.pi * 4 / FIELD_PERIOD, 2 * math.pi * 2 / FIELD_PERIOD
    levels = {1: [], 2: [], 3: []}
    for r in range(rows):
        for c in range(cols):
            wave = math.sin(c * k1 + phase) * math.cos(r * .24 - phase * .85) + math.sin((c + r) * k3 + phase * 1.4)
            v = (wave + 2) / 4
            if v < .52:
                continue
            size = (v - .52) / .48
            level = 1 if size < .34 else 2 if size < .67 else 3
            if level == 1 and (r + c) % 2 == 1:
                continue
            levels[level].append((c, r))
    out = []
    for level, cells in levels.items():
        side = max(1, round(cell * STEP_SIDE[level]))
        off = round((cell - side) / 2)
        d = "".join(sq(c * cell + off, r * cell + off, side) for c, r in cells)
        out.append(f'<path d="{d}" fill="{color}" fill-opacity="{n(STEP_ALPHA[level] * intensity)}"/>')
    return "".join(out)


def haze(x, y, w, h, color, cell=9, intensity=.55, focus=(1, 0), drift=True):
    """Trame qui dérive d'une case par seconde, fondue en ellipse depuis un coin (CornerHaze)."""
    cols, rows = -(-w // cell) + (FIELD_PERIOD if drift else 0), -(-h // cell)
    gid, mid, fid, lid = uid(), uid(), uid(), uid()
    fx, fy = x + focus[0] * w, y + focus[1] * h
    defs = (f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="1" gradientTransform="translate({n(fx)} {n(fy)}) scale({w} {h})">'
            f'<stop offset=".12" stop-color="#fff"/><stop offset=".72" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="{x}" y="{y}" width="{w}" height="{h}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{gid})"/></mask>'
            f'<filter id="{fid}" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="5"/></filter>')
    move = f' class="drift" style="animation:drift {FIELD_PERIOD}s steps({FIELD_PERIOD}) infinite"' if drift else ""
    field = f'<g id="{lid}" shape-rendering="crispEdges"><g{move}>{halftone(cols, rows, cell, color, intensity)}</g></g>'
    body = (f'<g mask="url(#{mid})"><g transform="translate({x} {y})">'
            f'<use href="#{lid}" filter="url(#{fid})" opacity=".35"/>{field}</g></g>')
    css = f"@keyframes drift{{to{{transform:translateX(-{FIELD_PERIOD * cell}px)}}}}"
    return defs, body, css


# ---------------- PETITS COMPOSANTS ----------------
SPIN_STEPS = [0, 1, 2, 7, -1, 3, 6, 5, 4]


def spinner(x, y, size, color, gap=1.0):
    """PixelSpinner : 3×3 pixels qui s'allument en ronde autour du cœur."""
    cell = (size - 2 * gap) / 3
    out = []
    for i, step in enumerate(SPIN_STEPS):
        cx, cy = x + (i % 3) * (cell + gap), y + (i // 3) * (cell + gap)
        base = f'x="{n(cx)}" y="{n(cy)}" width="{n(cell)}" height="{n(cell)}" rx=".5" fill="{color}"'
        if step < 0:
            out.append(f'<rect {base} fill-opacity=".25"/>')
        else:
            out.append(f'<rect {base} opacity=".45" style="animation:spx 1.2s ease-in-out {n((step - 8) * .15)}s infinite"/>')
    return "".join(out)


def segments(x, y, w, h, count, ratio, fg, gap=2.0, start=None, head=True):
    """PixelProgress : barre segmentée, remplissage ambre, tête qui pulse."""
    sw = (w - (count - 1) * gap) / count
    filled = round(max(0, min(1, ratio)) * count)
    rect = lambda i: f'x="{n(x + i * (sw + gap))}" y="{n(y)}" width="{n(sw)}" height="{h}" rx="1"'
    out = [f'<rect {rect(i)} fill="{fg}" fill-opacity=".1"/>' for i in range(count)]
    for i in range(filled):
        style = anim("fin", .25, start + i * .035) if start is not None else ""
        tone = .4 + .6 * (i + 1) / count   # dégradé en paliers vers la tête
        out.append(f'<rect {rect(i)} fill="{PRIMARY}" fill-opacity="{n(tone)}"{style}/>')
    if head and filled < count:
        out.append(f'<rect {rect(filled)} fill="{PRIMARY}" opacity=".45" style="animation:head 1.1s ease-in-out infinite"/>')
    return "".join(out)


def rarity(x, y, value, fg, size=5.0, gap=2.0):
    return "".join(f'<rect x="{n(x + i * (size + gap))}" y="{n(y)}" width="{size}" height="{size}" rx=".5" '
                   f'fill="{PRIMARY if i < value else fg}"{"" if i < value else " fill-opacity=\".14\""}/>' for i in range(5))


def crossfade(items, slot, fade=.5):
    """items = fragments SVG qui se relaient en fondu ; le premier reste visible sans animation."""
    total = slot * len(items)
    css, out = "", []
    for i, body in enumerate(items):
        k = uid()
        a, a2, b1, b = (i * slot / total * 100, (i * slot + fade) / total * 100,
                        ((i + 1) * slot - fade) / total * 100, (i + 1) * slot / total * 100)
        css += (f".{k}{{animation:{k} {n(total)}s linear infinite}}"
                f"@keyframes {k}{{0%{{opacity:0}}{n(a)}%{{opacity:0}}{n(a2)}%{{opacity:1}}{n(b1)}%{{opacity:1}}{n(b)}%{{opacity:0}}100%{{opacity:0}}}}")
        out.append(f'<g class="{k}"{"" if i == 0 else " opacity=\"0\""}>{body}</g>')
    return "".join(out), css


def circle_text(cx, cy, radius, s, face, size, track, color):
    """Texte posé sur un cercle (CircleBadge), glyphe par glyphe."""
    names, xs, w = face.layout(s, size, track)
    scale = size / face.upm
    full = w + track * size
    extra = (2 * math.pi * radius - full) / len(names)
    out = []
    for i, g in enumerate(names):
        gw = face.hmtx[g][0] * scale
        theta = math.pi + (xs[i] + i * extra + gw / 2) / radius
        phi = theta + math.pi / 2
        c, sn = math.cos(phi), math.sin(phi)
        ax, ay = cx + radius * math.cos(theta), cy + radius * math.sin(theta)
        pen = SVGPathPen(face.glyphs, ntos=n)
        face.glyphs[g].draw(TransformPen(pen, (scale * c, scale * sn, scale * sn, -scale * c, ax - gw / 2 * c, ay - gw / 2 * sn)))
        out.append(pen.getCommands())
    return f'<path d="{"".join(out)}" fill="{color}"/>'


def arrow(cx, cy, size, color, width=1.6):
    h = size / 2
    return (f'<path d="M{n(cx - h)} {n(cy + h)}L{n(cx + h)} {n(cy - h)}M{n(cx - h * .6)} {n(cy - h)}H{n(cx + h)}V{n(cy + h * .6)}" '
            f'stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" fill="none"/>')


# ---------------- ICÔNES D'INVENTAIRE ----------------
# Sprites à nuances (centrés dans une case 12×12) : '#' contour, '=' ton moyen, '-' ton clair, 'o' ambre.
ICONS = {
    'sword':  ["..........##", ".........#-#", "........#-#.", ".......#-#..", "......#-#...", "..o..#-#....",
               "...o#-#.....", "....o#......", "...=.o......", "..=...o.....", ".#.........."],
    'shield': [".##########.", "#=====-----#", "#=====-----#", "#====oo----#", "#===oooo---#", ".#===oo---#.",
               ".#====----#.", "..#===---#..", "...#==--#...", "....#=-#....", ".....##....."],
    'scroll': [".##########.", "#-========-#", ".##########.", "..#------#..", "..#-====-#..", "..#------#..",
               "..#-oooo-#..", "..#------#..", "..#-===--#..", ".##########.", "#-========-#", ".##########."],
    'gem':    ["...######...", "..#o-====#..", ".#--=-====#.", "############", ".#--=-====#.", "..#-=-===#..",
               "...#-===#...", "....#-=#....", ".....##....."],
    'ring':   ["....####....", "...#oooo#...", "....#oo#....", "...######...", "..##....##..", ".#=......-#.",
               ".#=......-#.", ".#=......-#.", "..##....##..", "...######..."],
    'potion': ["....####....", "....#==#....", "....####....", "....#--#....", "...#----#...", "..#------#..",
               ".#--------#.", ".#oooooooo#.", ".#oo-ooooo#.", ".#ooooo-oo#.", "..#oooooo#..", "...######..."],
    'hammer': [".########...", "#-=======#..", "#-=======##.", "#-=======#..", ".########...", "...#oo#.....",
               "...#==#.....", "...#==#.....", "...#==#.....", "...#==#.....", "...#==#.....", "....##......"],
    'key':    [".###........", "#-=-#.......", "#=.=########", "#=.=-oooooo#", "#-=-########", ".###...##.#.",
               ".......#..#."],
    'book':   [".#########..", "#o#------#..", "#o#-====-#..", "#o#------#..", "#o#-===--#..", "#o#------#..",
               "#o#------#..", "#o########..", "#o#=======#.", ".##########."],
    'bomb':   ["........o...", ".......=oo..", "......=.....", "....####....", "..########..", ".#--======#.",
               ".#-=======#.", ".#========#.", ".#========#.", "..#======#..", "...######..."],
}
ICON_TONES = {"#": .88, "=": .5, "-": .24}


def icon(name, x, y, cell, fg, box=12):
    rows = ICONS[name]
    w = max(len(row) for row in rows)
    ox = x + (box - w) // 2 * cell
    oy = y + (box - len(rows)) // 2 * cell
    gap = cell * .1
    out = []
    for key, alpha in ICON_TONES.items():
        cells = [(c, r) for r, row in enumerate(rows) for c, v in enumerate(row) if v == key]
        out.append(f'<path d="{cells_d(cells, cell, gap, ox, oy)}" fill="{fg}" fill-opacity="{alpha}"/>')
    accent = [(c, r) for r, row in enumerate(rows) for c, v in enumerate(row) if v == "o"]
    out.append(f'<path d="{cells_d(accent, cell, gap, ox, oy)}" fill="{PRIMARY}"/>')
    return f'<g shape-rendering="crispEdges">{"".join(out)}</g>'


# ============ 1. HERO ============
def hero(T):
    W, H = 900, 440
    fg = T["fg"]
    defs, b = [], []
    hd, hb, css = haze(350, 0, 550, 280, fg, cell=9, intensity=.42)
    defs.append(hd); b.append(hb)
    fd, fb = flora(fg, "bottom-right", W - 316, H - 316, size=56, cell=6, seed=4, grow=.6, alpha=.9, soft=.3)
    defs.append(fd); b.append(fb)
    # barre du haut
    b.append(f'<rect x="32" y="26" width="28" height="28" rx="8" fill="{PRIMARY}"/>'
             + text(TEXT, FIRST[0], 46, 46, 17, "#fbfaf8", anchor="middle")
             + text(TEXT, f"{FIRST.title()} {LAST.title()}", 72, 46, 17, fg))
    sw = LABEL.width(STATUS, KICK, .14)
    px = W - 50 - sw - 22 - 16
    b.append(f'<rect x="{n(px)}" y="22.5" width="{n(W - 34 - px)}" height="35" rx="17.5" fill="none" stroke="{fg}" stroke-opacity=".16"/>'
             + spinner(px + 16, 34, 12, PRIMARY) + kicker(STATUS, W - 50, 44.5, fg, .8, "end"))
    # nom en matrice de points + mot d'accent qui tourne
    size, x0, y1 = 128, 30, 196
    b.append(text(DISPLAY, FIRST, x0, y1, size, fg, extra=anim("fin", .9, .15, "cubic-bezier(.16,1,.3,1) both")))
    b.append(text(DISPLAY, LAST, x0 + 84, y1 + 104, size, fg, .5, extra=anim("fin", .9, .3, "cubic-bezier(.16,1,.3,1) both")))
    roles, c = crossfade([text(ACCENT, r, x0 + 250, y1 + 142, 62, PRIMARY) for r in ROLES], 3.2, .6)
    b.append(roles); css += c
    # badge circulaire
    cx, cy = 780, 150
    b.append(f'<g style="transform-origin:{cx}px {cy}px;animation:spin 48s linear infinite">'
             + circle_text(cx, cy, 50, BADGE, LABEL, 9.5, .1, fg) + '</g>'
             + ornament(cx - 16.5, cy - 16.5, 3, fg, bloom=.8))
    for i, line in enumerate(NOTE):
        b.append(kicker(line, 836, 240 + i * 16, fg, .75, "end"))
    # bas gauche
    b.append(kicker(KICKER, 34, H - 72, fg, .6))
    b.append(text(DISPLAY, CLAIM, 32, H - 38, 24, fg))
    return svg(W, H, "".join(b), f"{FIRST} {LAST} — {', '.join(r.upper() for r in ROLES)}", css, "".join(defs))


# ============ 2. SÉPARATEUR ============
def divider(T, left, right):
    W, H, cx = 900, 118, 450
    b = [kicker(left, cx - 40, 39, T["fg"], .8, "end", 12),
         ornament(cx - 22, 12, 4, T["fg"], bloom=.2),
         kicker(right, cx + 40, 39, T["fg"], .8, "start", 12),
         f'<rect x="{cx - .5}" y="76" width="1" height="42" fill="{T["fg"]}" fill-opacity=".25" style="transform-origin:{cx}px 76px;animation:grow .9s cubic-bezier(.16,1,.3,1) .6s both"/>']
    return svg(W, H, "".join(b), f"{left} — {right}", "@keyframes grow{from{transform:scaleY(0)}}")


# ============ 3. PROFIL ============
def profile(T):
    W, P = 900, 12
    fg, mfg = T["fg"], T["mfg"]
    b = [kicker(f"PLAYER 1 — {CLASS}", P, 22, mfg)]
    lv = f"LV. {LEVEL}"
    lw = LABEL.width(lv, KICK, .14) + 28
    b.append(f'<rect x="{n(W - P - lw)}" y="4.5" width="{n(lw)}" height="27" rx="13.5" fill="none" stroke="{T["border"]}"/>'
             + kicker(lv, W - P - 14, 22, fg, 1, "end"))
    size, lead, y = 26, 36, 76
    b.append(text(DISPLAY, HELLO, P, y, size, fg))
    for i, line in enumerate(INTRO):
        b.append(text(DISPLAY, line, P, y + (i + 1) * lead, size, mfg))
    last = y + len(INTRO) * lead
    caret_x = P + DISPLAY.width(INTRO[-1], size) + 8
    b.append(f'<rect x="{n(caret_x)}" y="{last - 19}" width="10" height="20" fill="{PRIMARY}" style="animation:blink 1.1s steps(1) infinite"/>')
    # compteurs : filets haut / bas et séparateurs verticaux
    gy, gh, gw = last + 32, 104, (W - 2 * P) / len(COUNTERS)
    b.append(f'<rect x="{P}" y="{gy}" width="{W - 2 * P}" height="1" fill="{T["border"]}"/>'
             f'<rect x="{P}" y="{gy + gh}" width="{W - 2 * P}" height="1" fill="{T["border"]}"/>')
    for i, (value, label) in enumerate(COUNTERS):
        x = P + i * gw
        if i:
            b.append(f'<rect x="{n(x)}" y="{gy + 16}" width="1" height="{gh - 32}" fill="{T["border"]}"/>')
        b.append(text(DISPLAY, value, x + (22 if i else 0), gy + 58, 46, fg, extra=anim("fin", .6, .2 + i * .08, "ease-out both")))
        b.append(kicker(label, x + (23 if i else 1), gy + 84, mfg))
    # stats en barres segmentées
    sy, col = gy + gh + 44, (W - 2 * P - 48) / 2
    for i, (label, value) in enumerate(STATS):
        x, y = P + (i % 2) * (col + 48), sy + (i // 2) * 42
        b.append(kicker(label, x, y, mfg) + kicker(f"{value:02d}/10", x + col, y, fg, 1, "end"))
        b.append(segments(x, y + 10, col, 6, 28, value / 10, fg, start=.5 + i * .15))
    H = sy + (len(STATS) + 1) // 2 * 42 - 16
    return svg(W, H, "".join(b), f"Player 1 — {CLASS}, level {LEVEL}. {HELLO} {' '.join(INTRO)}")


# ============ 4. INVENTAIRE ============
def stack(T):
    W, cols = 900, 5
    cw, ch = W / cols, 162
    rows = -(-len(ITEMS) // cols)
    H = rows * ch
    fg, mfg = T["fg"], T["mfg"]
    b = []
    for c in range(1, cols):
        b.append(f'<rect x="{n(c * cw)}" y="16" width="1" height="{H - 32}" fill="{T["border"]}"/>')
    for r in range(1, rows):
        b.append(f'<rect x="16" y="{r * ch}" width="{W - 32}" height="1" fill="{T["border"]}"/>')
    # curseur : des coins ambre passent d'une case à l'autre
    step = 2.2
    vals = ";".join(f"{n((i % cols) * cw)} {(i // cols) * ch}" for i in range(len(ITEMS)))
    b.append(f'<g><animateTransform attributeName="transform" type="translate" values="{vals}" '
             f'dur="{n(step * len(ITEMS))}s" calcMode="discrete" repeatCount="indefinite"/>'
             f'<path d="M10 10h10v2h-8v8h-2zM{n(cw - 10)} 10v10h-2v-8h-8v-2zM10 {ch - 10}h10v-2h-8v-8h-2zM{n(cw - 10)} {ch - 10}v-10h-2v8h-8v2z" fill="{PRIMARY}"/></g>')
    desc = 10
    while max(LABEL.width(line, desc, .08) for item in ITEMS for line in item[2:4]) > cw - 44:
        desc -= .25
    for i, (name, ic, d1, d2, rar) in enumerate(ITEMS):
        x, y = (i % cols) * cw, (i // cols) * ch
        b.append(icon(ic, x + 22, y + 22, 4, fg))
        b.append(rarity(x + cw - 24 - 33, y + 28, rar, fg))
        b.append(text(TEXT, name, x + 22, y + 104, 19, fg))
        b.append(kicker(d1, x + 22, y + 126, mfg, 1, "start", desc, .08) + kicker(d2, x + 22, y + 140, mfg, 1, "start", desc, .08))
    return svg(W, H, "".join(b), "Inventory: " + ", ".join(item[0] for item in ITEMS))


# ============ 5. NOW PLAYING ============
def flipbook(items, dur):
    """Images qui se succèdent sans fondu ; la première reste affichée sans animation."""
    css, out = "", []
    for i, body in enumerate(items):
        k, a, b = uid(), i / len(items) * 100, (i + 1) / len(items) * 100
        frames = f"0%{{opacity:1}}{n(b)}%{{opacity:0}}100%{{opacity:0}}" if i == 0 else \
                 f"0%{{opacity:0}}{n(a)}%{{opacity:1}}{n(b)}%{{opacity:0}}100%{{opacity:0}}"
        css += f".{k}{{animation:{k} {n(dur)}s step-end infinite}}@keyframes {k}{{{frames}}}"
        out.append(f'<g class="{k}"{"" if i == 0 else " opacity=\"0\""}>{body}</g>')
    return "".join(out), css


def vinyl(x, y, ink, cell=5, grid=27):
    """Disque pixel : sillons en deux tons, reflet qui tourne, étiquette ambre qui bat à 180 BPM."""
    mid = grid // 2
    grooves, label, rim = {.12: [], .24: []}, [], []
    polar = []
    for r in range(grid):
        for c in range(grid):
            d = math.hypot(c - mid, r - mid)
            if d <= 1.1 or d > 13.4:
                continue
            if d <= 4.3:
                label.append((c, r))
            elif d > 12.4:
                rim.append((c, r))
            else:
                grooves[.12 if round(d) % 2 else .24].append((c, r))
                if 5.5 <= d <= 12:
                    polar.append((c, r, math.atan2(r - mid, c - mid)))
    gap = .5
    body = "".join(f'<path d="{cells_d(cells, cell, gap, x, y)}" fill="{ink}" fill-opacity="{a}"/>' for a, cells in grooves.items())
    body += f'<path d="{cells_d(rim, cell, gap, x, y)}" fill="{ink}" fill-opacity=".45"/>'
    frames = []
    for k in range(12):
        theta = k * math.pi / 12
        cells = [(c, r) for c, r, a in polar if abs(math.remainder(a - theta, math.pi)) < .2]
        frames.append(f'<path d="{cells_d(cells, cell, gap, x, y)}" fill="{ink}" fill-opacity=".4"/>')
    glint, css = flipbook(frames, 3)
    body += glint + (f'<path d="{cells_d(label, cell, gap, x, y)}" fill="{PRIMARY}" '
                     f'style="animation:beat .333s steps(1) infinite"/>')
    return f'<g shape-rendering="crispEdges">{body}</g>', css


def player(T):
    W, H = 900, 166
    fg, mfg = T["fg"], T["mfg"]
    b = []
    disc, css = vinyl(8, 16, fg)
    b.append(disc)
    x0 = 8 + 135 + 36
    b.append(spinner(x0, 18, 11, PRIMARY) + kicker("NOW PLAYING", x0 + 20, 27.5, mfg))
    b.append(text(DISPLAY, TRACK[0], x0, 72, 30, fg))
    b.append(kicker(TRACK[1], x0, 98, mfg))
    # égaliseur pixel
    ex, base, sq_s, gap = W - 8 - 16 * 11 + 4, 76, 7, 4
    pid, mid, gid = uid(), uid(), uid()
    defs = (f'<pattern id="{pid}" width="{sq_s + gap}" height="{sq_s + gap}" patternUnits="userSpaceOnUse" x="{ex}" y="{base}">'
            f'<rect width="{sq_s}" height="{sq_s}" rx="1" fill="{fg}"/></pattern>'
            f'<linearGradient id="{gid}" x1="0" y1="{base}" x2="0" y2="{base - 66}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="#fff" stop-opacity=".85"/><stop offset="1" stop-color="#fff" stop-opacity=".18"/></linearGradient>'
            f'<mask id="{mid}"><rect x="{ex - 2}" y="{base - 70}" width="200" height="72" fill="url(#{gid})"/></mask>')
    bars = []
    rng = mulberry(9)
    for i in range(16):
        hs = [(1 + math.floor(rng() * 6)) * (sq_s + gap) for _ in range(8)]
        hs.append(hs[0])
        dur = [.666, 1.0, 1.333][math.floor(rng() * 3)]
        bx = ex + i * (sq_s + gap)
        bars.append(f'<rect x="{bx}" y="{base - hs[0] + gap}" width="{sq_s}" height="{hs[0] - gap}" fill="url(#{pid})">'
                    f'<animate attributeName="height" values="{";".join(str(h - gap) for h in hs)}" dur="{dur}s" calcMode="discrete" repeatCount="indefinite"/>'
                    f'<animate attributeName="y" values="{";".join(str(base - h + gap) for h in hs)}" dur="{dur}s" calcMode="discrete" repeatCount="indefinite"/></rect>')
    b.append(f'<g mask="url(#{mid})" shape-rendering="crispEdges">{"".join(bars)}</g>')
    # progression
    py, pw = 124, W - 8 - x0
    count = 56
    sw = (pw - (count - 1) * 2) / count
    track = "".join(f'<rect x="{n(x0 + i * (sw + 2))}" y="{py}" width="{n(sw)}" height="6" rx="1"/>' for i in range(count))
    tid = uid()
    defs += f'<clipPath id="{tid}">{track}</clipPath>'
    b.append(f'<g fill="{fg}" fill-opacity=".1">{track}</g>'
             f'<rect x="{x0}" y="{py}" width="0" height="6" fill="{PRIMARY}" clip-path="url(#{tid})">'
             f'<animate attributeName="width" values="{n(pw * .05)};{n(pw)}" dur="90s" calcMode="linear" repeatCount="indefinite"/></rect>')
    b.append(kicker("SIDE A", x0, py + 30, mfg) + kicker("60:00", W - 8, py + 30, mfg, 1, "end"))
    heart = [".#.#.", "#####", "#####", ".###.", "..#.."]
    hx = x0 + pw / 2 - 40
    hc = [(c, r) for r, row in enumerate(heart) for c, v in enumerate(row) if v == "#"]
    b.append(f'<path d="{cells_d(hc, 2.4, .2, hx, py + 18.5)}" fill="{PRIMARY}" shape-rendering="crispEdges" style="animation:beat .333s steps(1) infinite"/>'
             + kicker("180 BPM", hx + 20, py + 30, fg))
    return svg(W, H, "".join(b), f"Now playing: {TRACK[0].title()} — {TRACK[1].title()}", css, defs)


# ============ 6. FIN / CONTACT ============
def outro(T):
    W, H = 900, 300
    fg = T["fg"]
    defs, b = [], []
    fd, fb = flora(fg, "top-right", W - 336 - 90, -30, size=56, cell=6, seed=37, grow=.4, alpha=.9, soft=.3)
    defs.append(fd); b.append(fb)
    b.append(kicker("CONTINUE ? — PRESS START", 14, 40, fg, .55))
    size = 58
    b.append(text(DISPLAY, OUTRO[0], 12, 112, size, fg))
    b.append(text(DISPLAY, OUTRO[1], 12 + 70, 174, size, fg, .5))
    b.append(text(ACCENT, OUTRO[2], 12 + 330, 212, 58, PRIMARY))
    b.append(f'<rect x="14" y="{H - 52}" width="{W - 28}" height="1" fill="{fg}" fill-opacity=".14"/>')
    b.append(kicker(f"© {datetime.date.today().year} {FIRST} {LAST}", 14, H - 20, fg, .45))
    digits, c = crossfade([kicker(f"CONTINUE ? {k}", W - 14, H - 20, fg, .6, "end") for k in range(9, -1, -1)], 1, .05)
    b.append(spinner(W - 14 - LABEL.width("CONTINUE ? 9", KICK, .14) - 22, H - 30, 11, PRIMARY) + digits)
    return svg(W, H, "".join(b), f"{OUTRO[0]} {OUTRO[1]} {OUTRO[2]}", c, "".join(defs))


def button(T, label, delay):
    """Pilule au trait fin (pas de fond), balayage de pixels PixelHover en boucle."""
    h, pad, dot = 52, 24, 38
    tw = TEXT.width(label, 15, .06)
    w = round(pad + tw + 18 + dot + 7)
    fg = T["fg"]
    clip = uid()
    cell, cols, rows = 4, -(-w // 4), -(-h // 4)
    rng = mulberry(len(label) * 31 + 7)
    buckets = {}
    for r in range(rows):
        for c in range(cols):
            delay_frac = min(1, max(0, c / (cols - 1) + (rng() - .5) * .7))
            buckets.setdefault(round(delay_frac * 12), []).append((c, r))
    sweep = "".join(f'<path class="sw" d="{cells_d(cells, cell, .5)}" style="animation:sweep 6s linear {n(delay + k * .045)}s infinite"/>'
                    for k, cells in sorted(buckets.items()))
    body = (f'<g clip-path="url(#{clip})"><g fill="{PRIMARY}" fill-opacity=".4" shape-rendering="crispEdges">{sweep}</g></g>'
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{(h - 1) / 2}" fill="none" stroke="{fg}" stroke-opacity=".28"/>'
            + text(TEXT, label, pad, h / 2 + 5, 15, fg, track=.06)
            + f'<circle cx="{n(w - 7 - dot / 2)}" cy="{h / 2}" r="{dot / 2}" fill="{PRIMARY}"/>' + arrow(w - 7 - dot / 2, h / 2, 8, "#171412"))
    css = ".sw{opacity:0}@keyframes sweep{0%{opacity:0}4%{opacity:1}9%{opacity:0}100%{opacity:0}}"
    defs = f'<clipPath id="{clip}"><rect width="{w}" height="{h}" rx="{h / 2}"/></clipPath>'
    return svg(w, h, body, label, css, defs)


# ============ ÉCRITURE ============
def build():
    files = {}
    for theme, T in THEMES.items():
        out = {"hero": hero(T), "profile": profile(T), "stack": stack(T), "player": player(T), "outro": outro(T)}
        for key, (left, right) in SECTIONS.items():
            out[f"divider-{key}"] = divider(T, left, right)
        for i, (key, label) in enumerate(LINKS):
            out[f"btn-{key}"] = button(T, label, 1.2 + i * .35)
        files[theme] = out
    for theme, out in files.items():
        folder = os.path.join(OUT, theme)
        os.makedirs(folder, exist_ok=True)
        for key, content in out.items():
            with open(os.path.join(folder, key + ".svg"), "w", encoding="utf-8") as fh:
                fh.write(content)
    print("OK:", ", ".join(files["light"]), "-> assets/light + assets/dark")


if __name__ == "__main__":
    build()
