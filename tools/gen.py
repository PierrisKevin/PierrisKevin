#!/usr/bin/env python3
# ============================================================
#  PIXEL README GENERATOR — Kevin RAND
#  Modifie la CONFIG ci-dessous puis lance :  python3 tools/gen.py
#  (MAJUSCULES uniquement, caractères : A-Z 0-9 ! . , : @ - ' + < > / ? ( ) % _ | et * = coeur)
# ============================================================
NAME      = "KEVIN RAND"
SUBTITLES = ["WEB DEVELOPER", "BUG HUNTER", "HAPPY HARDCORE ADDICT"]
DIALOG    = ["HEY! WELCOME TO MY PROFILE.", "I BUILD STUFF FOR THE WEB.", "FUELED BY HAPPY HARDCORE @ 180 BPM."]
CLASS     = "WEB DEVELOPER"
LEVEL     = "07"
STATS     = [("FRONTEND",9),("BACKEND",7),("DEBUG",8),("UI / UX",6),("CAFFEINE",10),("BPM",10)]
# (label dans la case, icone, nom, description ligne 1, ligne 2, rareté 1-5)
ITEMS = [
 ("JS",   "sword",  "SWORD OF JAVASCRIPT", "MAIN WEAPON.",           "HITS EVERY BROWSER.", 5),
 ("TS",   "shield", "TYPESCRIPT SHIELD",   "BLOCKS 99% OF",          "RUNTIME BUGS.", 4),
 ("HTML", "scroll", "HTML SCROLL",         "THE MAP OF",             "EVERY LEVEL.", 3),
 ("CSS",  "gem",    "CSS GEM",             "MAKES ANYTHING",         "SHINE.", 4),
 ("REACT","ring",   "REACT RING",          "SUMMONS REUSABLE",       "COMPONENTS.", 5),
 ("NODE", "potion", "NODE POTION",         "RESTORES",               "BACKEND HP.", 4),
 ("PHP",  "hammer", "PHP HAMMER",          "OLD SCHOOL.",            "STILL HITS HARD.", 3),
 ("SQL",  "key",    "SQL KEY",             "OPENS EVERY",            "DATABASE.", 3),
 ("GIT",  "book",   "GIT BOOK",            "REWINDS TIME.",          "INFINITE SAVES.", 5),
 ("BASH", "bomb",   "BASH BOMB",           "ONE COMMAND.",           "BOOM.", 4),
]
TRACK = "*** NOW PLAYING: HAPPY HARDCORE MEGAMIX VOL. 180 *** STAY HAPPY, STAY HARDCORE ***"
# ============================================================
import random, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
F = {
'A':[".###.","#...#","#...#","#####","#...#","#...#","#...#"],'B':["####.","#...#","#...#","####.","#...#","#...#","####."],
'C':[".###.","#...#","#....","#....","#....","#...#",".###."],'D':["####.","#...#","#...#","#...#","#...#","#...#","####."],
'E':["#####","#....","#....","####.","#....","#....","#####"],'F':["#####","#....","#....","####.","#....","#....","#...."],
'G':[".###.","#...#","#....","#.###","#...#","#...#",".####"],'H':["#...#","#...#","#...#","#####","#...#","#...#","#...#"],
'I':["#####","..#..","..#..","..#..","..#..","..#..","#####"],'J':["..###","...#.","...#.","...#.","...#.","#..#.",".##.."],
'K':["#...#","#..#.","#.#..","##...","#.#..","#..#.","#...#"],'L':["#....","#....","#....","#....","#....","#....","#####"],
'M':["#...#","##.##","#.#.#","#.#.#","#...#","#...#","#...#"],'N':["#...#","##..#","#.#.#","#..##","#...#","#...#","#...#"],
'O':[".###.","#...#","#...#","#...#","#...#","#...#",".###."],'P':["####.","#...#","#...#","####.","#....","#....","#...."],
'Q':[".###.","#...#","#...#","#...#","#.#.#","#..#.",".##.#"],'R':["####.","#...#","#...#","####.","#.#..","#..#.","#...#"],
'S':[".####","#....","#....",".###.","....#","....#","####."],'T':["#####","..#..","..#..","..#..","..#..","..#..","..#.."],
'U':["#...#","#...#","#...#","#...#","#...#","#...#",".###."],'V':["#...#","#...#","#...#","#...#","#...#",".#.#.","..#.."],
'W':["#...#","#...#","#...#","#.#.#","#.#.#","##.##","#...#"],'X':["#...#","#...#",".#.#.","..#..",".#.#.","#...#","#...#"],
'Y':["#...#","#...#",".#.#.","..#..","..#..","..#..","..#.."],'Z':["#####","....#","...#.","..#..",".#...","#....","#####"],
'0':[".###.","#...#","#..##","#.#.#","##..#","#...#",".###."],'1':["..#..",".##..","..#..","..#..","..#..","..#..",".###."],
'2':[".###.","#...#","....#","...#.","..#..",".#...","#####"],'3':["####.","....#","....#",".###.","....#","....#","####."],
'4':["...#.","..##.",".#.#.","#..#.","#####","...#.","...#."],'5':["#####","#....","####.","....#","....#","#...#",".###."],
'6':[".###.","#....","#....","####.","#...#","#...#",".###."],'7':["#####","....#","...#.","..#..",".#...",".#...",".#..."],
'8':[".###.","#...#","#...#",".###.","#...#","#...#",".###."],'9':[".###.","#...#","#...#",".####","....#","....#",".###."],
'!':["..#..","..#..","..#..","..#..","..#..",".....","..#.."],'.':[".....",".....",".....",".....",".....",".....","..#.."],
',':[".....",".....",".....",".....",".....","..#..",".#..."],':':[".....","..#..",".....",".....",".....","..#..","....."],
'@':[".###.","#...#","#.###","#.#.#","#.###","#....",".###."],'-':[".....",".....",".....",".###.",".....",".....","....."],
"'":["..#..","..#..",".#...",".....",".....",".....","....."],'+':[".....","..#..","..#..","#####","..#..","..#..","....."],
'<':["...#.","..#..",".#...","#....",".#...","..#..","...#."],'>':[".#...","..#..","...#.","....#","...#.","..#..",".#..."],
'/':["....#","....#","...#.","..#..",".#...","#....","#...."],'?':[".###.","#...#","....#","...#.","..#..",".....","..#.."],
'(':["...#.","..#..",".#...",".#...",".#...","..#..","...#."],')':[".#...","..#..","...#.","...#.","...#.","..#..",".#..."],
'%':["##..#","##..#","...#.","..#..",".#...","#..##","#..##"],'_':[".....",".....",".....",".....",".....",".....","#####"],
'|':["..#..","..#..","..#..","..#..","..#..","..#..","..#.."],'*':[".....",".#.#.","#####","#####",".###.","..#..","....."],
'}':["#....","##...","###..","####.","###..","##...","#...."],' ':["....."]*7,
}
def tp(s,x0,y0,p):
    return "".join(f"M{x0+(i*6+c)*p} {y0+r*p}h{p}v{p}h-{p}z" for i,ch in enumerate(s) for r,row in enumerate(F[ch]) for c,v in enumerate(row) if v=='#')
def tw(s,p): return (len(s)*6-1)*p
def sp(rows,x0,y0,p):
    return "".join(f"M{x0+c*p} {y0+r*p}h{p}v{p}h-{p}z" for r,row in enumerate(rows) for c,v in enumerate(row) if v=='#')
def outline(rows):
    h=len(rows)+2; w=len(rows[0])+2; g=[["."]*w for _ in range(h)]
    for r,row in enumerate(rows):
        for c,v in enumerate(row):
            if v=='#':
                for dr in (-1,0,1):
                    for dc in (-1,0,1): g[r+1+dr][c+1+dc]='#'
    return ["".join(x) for x in g]
def svg(w,h,body,css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" shape-rendering="crispEdges">'
            f'<style>{BASE_CSS}{css}</style><rect width="{w}" height="{h}" fill="#000"/>{body}</svg>')
BASE_CSS=(".bl{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}"
          ".tw{animation:tw 1.6s steps(1) infinite}@keyframes tw{50%{opacity:0}}")
_k=[0]
def seq(items,D):
    """items=[(svg, t0, t1)] visible from t0 to t1 inside a D-second loop (wrap allowed)."""
    css=""; out=""
    for body,t0,t1 in items:
        _k[0]+=1; n=f"q{_k[0]}"; a=t0/D*100; b=t1/D*100
        if t0<t1: kf=f"0%{{opacity:{1 if a==0 else 0}}}{a:.3f}%{{opacity:1}}{b:.3f}%{{opacity:0}}100%{{opacity:{1 if b>=100 else 0}}}"
        else:     kf=f"0%{{opacity:1}}{b:.3f}%{{opacity:0}}{a:.3f}%{{opacity:1}}100%{{opacity:1}}"
        css+=f".{n}{{animation:{n} {D}s step-end infinite}}@keyframes {n}{{{kf}}}"
        out+=f'<g class="{n}">{body}</g>'
    return out,css
def box(x,y,w,h,t=4):
    return f'<path d="M{x} {y}h{w}v{h}h-{w}zM{x+t} {y+t}v{h-2*t}h{w-2*t}v-{h-2*t}z" fill="#fff" fill-rule="evenodd"/>'
def nbox(x,y,w,h):  # notched double frame
    return (f'<path d="M{x+4} {y}h{w-8}v4h4v{h-8}h-4v4h-{w-8}v-4h-4v-{h-8}h4z" fill="#fff"/>'
            f'<path d="M{x+4} {y+4}h{w-8}v{h-8}h-{w-8}z" fill="#000"/>'
            f'<path d="M{x+10} {y+10}h{w-20}v2h-{w-20}zM{x+10} {y+h-12}h{w-20}v2h-{w-20}z" fill="#fff"/>')
SCAN=('<defs><pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect y="3" width="4" height="1" fill="#000"/></pattern></defs>')
def scan(w,h): return f'<rect width="{w}" height="{h}" fill="url(#scan)" opacity=".55" pointer-events="none"/>'

# ---------------- SPRITES ----------------
HEAD=["...######...","..#......#..",".#.######.#.","##.#.##.#.##","##.######.##","##.##..##.##","...######...","..########..",".##.####.##.",".#..####..#.","....####...."]
LA=["..##....##..","..##....##..",".##......##."]
LB=["....####....","....#..#....","...##..##..."]
BUG=["#......#",".#.####.","..####..","########","..####..",".#.##.#."]
COIN_A=[".####.","#....#","#.##.#","#.##.#","#.##.#","#.##.#","#....#",".####."]
COIN_B=["..##..",".#..#.",".#..#.",".#..#.",".#..#.",".#..#.",".#..#.","..##.."]
FACE=["....########....","..############..",".##############.","#.############.#","##.##......##.##","##.#........#.##",
      "##.#........#.##","##.#........#.##","##.#........#.##",".#.#..####..#.#.","...#........#...","....#......#....",
      ".....######.....","......#..#......","...##########...","..#..........#.."]
EYES=["................"]*6+["....#.##..##.#..".replace("#.##","..##").replace("##.#","##..")]+["................"]*9
EYES=[["."]*16 for _ in range(16)]
for r in (6,7):
    for c in (5,6,9,10): EYES[r][c]="#"
EYES_OPEN=["".join(r) for r in EYES]
EYES_TOP=["".join("#" if (r==6 and c in (5,6,9,10)) else "." for c in range(16)) for r in range(16)]
ICONS={
'sword':[".........#","........##",".......##.","......##..","#....##...",".#..##....","..###.....","..##......",".#..#.....","#........."],
'shield':["##########","#........#","#.######.#","#.######.#","#.######.#",".#.####.#.",".#.####.#.","..#.##.#..","...#..#...","....##...."],
'scroll':[".########.","#........#",".#.####.#.",".#......#.",".#.####.#.",".#......#.",".#.###..#.",".#......#.","#........#",".########."],
'gem':["..######..",".#..##..#.","#..#..#..#","##########","#.#....#.#",".#.#..#.#.","..#.##.#..","...#..#...","....##....",".........."],
'ring':["...####...","..#.##.#..","...####...","..#....#..",".#......#.",".#......#.",".#......#.","..#....#..","...####...",".........."],
'potion':["...####...","....##....","....##....","...#..#...","..#....#..",".#......#.",".#.####.#.",".#.####.#.","..#....#..","...####..."],
'hammer':[".######...","########..",".######...","...##.....","...##.....","...##.....","...##.....","...##.....","...##.....","...##....."],
'key':["..........","..........",".###......","#...#.....","#...######","#...#.#.#.",".###..#.#.","..........","..........",".........."],
'book':[".########.","#.#......#","#.#.####.#","#.#......#","#.#.####.#","#.#......#","#.#......#","#.########","#.#.......",".#########"],
'bomb':["......#.#.",".....#....","....##....","..######..",".########.","##.#######","#.########","##########",".########.","..######.."],
}

# ============ 1. BANNER ============
def banner():
    random.seed(3); W,H,G=900,320,284; T=3.0
    css=(".mt{animation:mt 40s linear infinite}@keyframes mt{to{transform:translateX(-900px)}}"
         ".gr{animation:gr .1s linear infinite}@keyframes gr{to{transform:translateX(-32px)}}"
         f".mov{{animation:mov {T}s linear infinite}}@keyframes mov{{from{{transform:translateX(920px)}}to{{transform:translateX(-40px)}}}}"
         f".jmp{{animation:jmp {T}s steps(14) infinite}}@keyframes jmp{{0%,76%{{transform:translateY(0)}}85%{{transform:translateY(-68px)}}94%,100%{{transform:translateY(0)}}}}"
         ".fa{animation:fa .24s steps(1) infinite}@keyframes fa{50%{opacity:0}}"
         ".fb{animation:fb .24s steps(1) infinite}@keyframes fb{0%{opacity:0}50%{opacity:1}}"
         ".ca{animation:fa .4s steps(1) infinite}.cb{animation:fb .4s steps(1) infinite}"
         f".got{{animation:got {T}s step-end infinite}}@keyframes got{{0%{{opacity:1}}83%{{opacity:0}}}}"
         f".dust{{animation:dust {T}s step-end infinite}}@keyframes dust{{0%{{opacity:1}}76%{{opacity:0}}94%{{opacity:1}}}}"
         f".pts{{opacity:0;animation:pts {T}s steps(1) infinite}}@keyframes pts{{0%,83%{{opacity:0;transform:translateY(0)}}84%{{opacity:1;transform:translateY(0)}}91%{{opacity:1;transform:translateY(-10px)}}97%,100%{{opacity:0}}}}"
         ".gl{opacity:0;animation:gl 5s steps(1) infinite}@keyframes gl{0%,89%{opacity:0;transform:translateX(0)}90%{opacity:1;transform:translateX(12px)}92%{transform:translateX(-10px)}94%{transform:translateX(6px)}95%,100%{opacity:0;transform:translateX(0)}}"
         ".gl2{animation-delay:.12s}")
    b=['<defs><pattern id="d1" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#fff"/><rect x="2" y="2" width="2" height="2" fill="#fff"/></pattern>'
       '<pattern id="d2" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#fff"/><rect x="4" y="4" width="2" height="2" fill="#fff"/></pattern>'
       '<pattern id="d3" width="12" height="12" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#fff"/><rect x="6" y="6" width="2" height="2" fill="#fff"/></pattern>'
       '<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect y="3" width="4" height="1" fill="#000"/></pattern></defs>']
    for _ in range(50):
        x=random.randrange(0,W,4); y=random.randrange(52,230,4); c=' class="tw"' if random.random()<.4 else ''
        dl=f' style="animation-delay:{random.uniform(0,1.6):.1f}s"' if c else ''
        b.append(f'<rect{c}{dl} x="{x}" y="{y}" width="2" height="2" fill="#fff"/>')
    ring=["...####...","..#....#..",".#......#.","#........#","#........#","#........#","#........#",".#......#.","..#....#..","...####..."]
    b.append(f'<path d="{sp(["...####...","..######..",".########.","##########","##########","##########","##########",".########.","..######..","...####..."],790,60,5)}" fill="url(#d1)"/><path d="{sp(ring,790,60,5)}" fill="#fff"/>')
    def mountains(seed,amp,step,fill,dur):
        random.seed(seed); h=[]; cur=amp//2
        for i in range(900//step): cur=max(8,min(amp,cur+random.choice([-8,-4,0,4,8]))); h.append(cur)
        d="".join(f"M{i*step+k} {G-hh}h{step}v{hh}h-{step}z" for k in (0,900) for i,hh in enumerate(h))
        return f'<g class="mt" style="animation-duration:{dur}s"><path d="{d}" fill="{fill}"/></g>'
    b.append(mountains(11,80,16,"url(#d3)",60))
    # city layer
    random.seed(21); x=0; bl=[]; wn=[]; ins=[]
    while x<900:
        bw=random.choice([24,32,40,48]); bh=random.choice([16,24,32,40,48,56])
        for k in (0,900):
            bl.append(f'M{x+k} {G-bh}h{bw}v{bh}h-{bw}z'); ins.append(f'M{x+k+2} {G-bh+2}h{bw-4}v{bh-2}h-{bw-4}z')
            for wy in range(G-bh+6,G-6,8):
                for wx in range(x+6,x+bw-6,8):
                    if random.random()<.3: wn.append(f'M{x+k+wx-x} {wy}h4v4h-4z')
        x+=bw+random.choice([8,16,24,40])
    b.append(f'<g class="mt" style="animation-duration:24s"><path d="{"".join(bl)}" fill="#fff"/><path d="{"".join(ins)}" fill="#000"/><path d="{"".join(wn)}" fill="#fff"/></g>')
    # HUD
    p=3; b.append(f'<path class="bl" d="{tp("1UP",24,18,p)}" fill="#fff"/>')
    items=[(f'<path d="{tp(f"{4200+i*100:06d}",24+tw("1UP ",p)+6,18,p)}" fill="#fff"/>', (i*T+2.55)%(6*T), ((i+1)*T+2.55)%(6*T)) for i in range(6)]
    g,c=seq(items,6*T); b.append(g); css+=c
    s="HI-SCORE 999999"; b.append(f'<path d="{tp(s,(W-tw(s,p))//2,18,p)}" fill="#fff"/>')
    s="STAGE 01  ***"; b.append(f'<path d="{tp(s,W-24-tw(s,p),18,p)}" fill="#fff"/>')
    b.append(f'<rect x="24" y="46" width="{W-48}" height="2" fill="#fff"/><rect x="24" y="50" width="{W-48}" height="2" fill="url(#d1)"/>')
    # TITLE + glitch
    p=9; x=(W-tw(NAME,p))//2; y=74
    b.append(f'<rect x="{x-18}" y="{y-12}" width="{tw(NAME,p)+36}" height="{7*p+24}" fill="#000"/>')
    b.append(f'<path d="{tp(NAME,x+5,y+5,p)}" fill="url(#d1)"/><path d="{tp(NAME,x,y,p)}" fill="#fff"/>')
    for i,(yy,hh) in enumerate([(y+18,18),(y+45,9)]):
        b.append(f'<clipPath id="gc{i}"><rect x="0" y="{yy}" width="{W}" height="{hh}"/></clipPath>'
                 f'<g clip-path="url(#gc{i})"><g class="gl{" gl2" if i else ""}"><rect x="0" y="{yy}" width="{W}" height="{hh}" fill="#000"/><path d="{tp(NAME,x,y,p)}" fill="#fff"/></g></g>')
    # rotating subtitle
    p=4; D=len(SUBTITLES)*3.2; items=[]
    for i,s in enumerate(SUBTITLES):
        t="} "+s; sx=(W-tw(t,p))//2
        items.append((f'<rect x="{sx-10}" y="146" width="{tw(t,p)+40}" height="36" fill="#000"/><path d="{tp(t,sx,150,p)}" fill="#fff"/><rect class="bl" x="{sx+tw(t,p)+10}" y="150" width="12" height="28" fill="#fff"/>', i*3.2, (i+1)*3.2))
    g,c=seq(items,D); b.append(g); css+=c
    # ground
    b.append(f'<rect x="0" y="{G}" width="{W}" height="{H-G}" fill="#000"/><rect x="0" y="{G}" width="{W}" height="4" fill="#fff"/>')
    gd="".join(f"M{i*32} {G+8}h12v4h-12zM{i*32+20} {G+16}h4v4h-4z" for i in range(30))
    b.append(f'<g class="gr"><path d="{gd}" fill="#fff"/></g>')
    s="PRESS START"; b.append(f'<path class="bl" d="{tp(s,(W-tw(s,2))//2,G+18,2)}" fill="#fff"/>')
    # enemies + coins (same track)
    coins="".join(f'<g transform="translate({cx},{cy})"><path d="{sp(outline(COIN_A),-3,-3,3)}" fill="#000"/><path class="ca" d="{sp(COIN_A,0,0,3)}" fill="#fff"/><path class="cb" d="{sp(COIN_B,0,0,3)}" fill="#fff"/></g>'
                  for cx,cy in [(-30,G-96),(6,G-106),(42,G-96)])
    b.append(f'<g class="mov"><path d="{sp(outline(BUG),-4,G-28,4)}" fill="#000"/><path d="{sp(BUG,0,G-24,4)}" fill="#fff"/><g class="got">{coins}</g></g>')
    px,py=96,G-56
    b.append(f'<g class="dust"><rect class="fa" x="{px-10}" y="{G-8}" width="4" height="4" fill="#fff"/><rect class="fb" x="{px-18}" y="{G-12}" width="4" height="4" fill="#fff"/></g>')
    b.append(f'<g class="jmp"><path d="{sp(outline(HEAD+LA),px-4,py-4,4)}" fill="#000"/><path d="{sp(outline(HEAD+LB),px-4,py-4,4)}" fill="#000"/><path d="{sp(HEAD,px,py,4)}" fill="#fff"/>'
             f'<path class="fa" d="{sp(LA,px,py+44,4)}" fill="#fff"/><path class="fb" d="{sp(LB,px,py+44,4)}" fill="#fff"/></g>')
    b.append(f'<g class="pts"><path d="{tp("+100",px,py-86,2)}" fill="#fff"/></g>')
    b.append(f'<rect width="{W}" height="{H}" fill="url(#scan)" opacity=".5"/>')
    return svg(W,H,"".join(b),css)

# ============ 2. DIALOG ============
def dialog():
    W,H=900,200; p=3
    b=[nbox(12,40,W-24,H-52)]
    nw=tw(NAME,p)+24; b.append(f'<rect x="36" y="16" width="{nw}" height="{7*p+14}" fill="#fff"/><path d="{tp(NAME,48,23,p)}" fill="#000"/>')
    # portrait
    b.append(box(36,64,112,112,4)+f'<path d="{sp(FACE,48,76,5.5)}" fill="#fff"/>')
    css=".blink{animation:blink 4s steps(1) infinite}@keyframes blink{0%,94%{opacity:1}95%,100%{opacity:0}}"
    b.append(f'<path class="blink" d="{sp(EYES_TOP,48,76,5.5)}" fill="#fff"/><path d="{sp([r if i==7 else "."*16 for i,r in enumerate(EYES_OPEN)],48,76,5.5)}" fill="#fff"/>')
    D=11.0; dt=.055; st=[.3]
    for L in DIALOG: st.append(st[-1]+len(L)*dt+.35)
    for i,L in enumerate(DIALOG):
        y=78+i*32; x=176
        kt=[0]+[(st[i]+k*dt)/D for k in range(len(L)+1)]+[10.5/D]; vals=[0]+[k*6*p for k in range(len(L)+1)]+[0]
        b.append(f'<clipPath id="c{i}"><rect x="{x}" y="{y}" width="0" height="{7*p}"><animate attributeName="width" dur="{D}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{";".join(f"{t:.4f}" for t in kt)}" values="{";".join(map(str,vals))}"/></rect></clipPath>'
                 f'<path clip-path="url(#c{i})" d="{tp(L,x,y,p)}" fill="#fff"/>')
    b.append(f'<path class="bl" d="M{W-56} {H-46}h16v4h-4v4h-4v4h-4v-4h-4v-4h-4z" fill="#fff"/>')
    return svg(W,H,"".join(b),css)

# ============ 3. CHARACTER SELECT ============
def select():
    W,H=900,430
    css=(".on{opacity:0;animation:on .01s forwards}@keyframes on{to{opacity:1}}"
         ".bob{animation:bob 1.2s steps(1) infinite}@keyframes bob{50%{transform:translateY(5px)}}"
         ".blink{animation:blink 4s steps(1) infinite}@keyframes blink{0%,94%{opacity:1}95%,100%{opacity:0}}")
    b=['<defs><pattern id="d1" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#fff"/><rect x="2" y="2" width="2" height="2" fill="#fff"/></pattern></defs>']
    # portrait card
    b.append(nbox(12,12,260,H-24))
    b.append(f'<rect x="36" y="36" width="212" height="212" fill="url(#d1)"/><rect x="44" y="44" width="196" height="196" fill="#000"/>')
    b.append(f'<g class="bob"><path d="{sp(outline(FACE),52,50,10)}" fill="#000"/><path d="{sp(FACE,62,60,10)}" fill="#fff"/>'
             f'<path class="blink" d="{sp(EYES_TOP,62,60,10)}" fill="#fff"/><path d="{sp([r if i==7 else "."*16 for i,r in enumerate(EYES_OPEN)],62,60,10)}" fill="#fff"/></g>')
    b.append(f'<rect x="36" y="36" width="44" height="30" fill="#fff"/><path d="{tp("P1",44,43,3)}" fill="#000"/>')
    nm=NAME.split()[0]; b.append(f'<path d="{tp(nm,142-tw(nm,4)//2,272,4)}" fill="#fff"/>')
    for k,(lab,val) in enumerate([("TYPE","HUMAN"),("MODE","CO-OP")]):
        b.append(f'<path d="{tp(lab,40,330+k*24,2)}" fill="#fff"/><path d="{tp(val,244-tw(val,2),330+k*24,2)}" fill="#fff"/>')
    # info panel
    X=300; b.append(nbox(X,12,W-X-12,H-24))
    b.append(f'<path d="{tp("CLASS",X+28,36,3)}" fill="url(#d1)"/><path d="{tp(CLASS,X+28+tw("CLASS ",3)+6,36,3)}" fill="#fff"/>')
    s=f"LV.{LEVEL}"; b.append(f'<rect x="{W-40-tw(s,3)-16}" y="30" width="{tw(s,3)+16}" height="33" fill="#fff"/><path d="{tp(s,W-40-tw(s,3)-8,36,3)}" fill="#000"/>')
    # HP / XP
    y=78
    for lab,full,anim in [("HP",1.0,False),("XP",.7,True)]:
        b.append(f'<path d="{tp(lab,X+28,y,2)}" fill="#fff"/>'+box(X+64,y-3,W-X-116,20,2))
        ww=int((W-X-124)*full)
        if anim: b.append(f'<rect x="{X+68}" y="{y+1}" width="0" height="12" fill="url(#d1)"><animate attributeName="width" values="0;{ww}" dur="2s" begin=".3s" fill="freeze" calcMode="discrete" keyTimes="0;1"/><animate attributeName="width" from="0" to="{ww}" dur="1.6s" begin=".3s" fill="freeze"/></rect>')
        else: b.append(f'<rect x="{X+68}" y="{y+1}" width="{ww}" height="12" fill="#fff"/>')
        y+=26
    b.append(f'<rect x="{X+28}" y="{y+2}" width="{W-X-68}" height="2" fill="url(#d1)"/>')
    y+=20
    for i,(lab,v) in enumerate(STATS):
        yy=y+i*34; b.append(f'<path d="{tp(lab,X+28,yy,3)}" fill="#fff"/>')
        for k in range(10):
            sx=X+230+k*26
            b.append(f'<rect x="{sx}" y="{yy-1}" width="20" height="23" fill="#fff"/><rect x="{sx+3}" y="{yy+2}" width="14" height="17" fill="#000"/>')
            if k<v:
                b.append(f'<rect class="on" style="animation-delay:{.4+i*.25+k*.07:.2f}s" x="{sx+3}" y="{yy+2}" width="14" height="17" fill="#fff"/>')
        b.append(f'<path d="{tp(f"{v:02d}",X+500,yy,3)}" fill="#fff"/>')
    b.append(f'<rect x="{W-48-tw("READY!",3)-12}" y="{H-62}" width="{tw("READY!",3)+24}" height="33" fill="#fff" class="bl"/><path d="{tp("READY!",W-48-tw("READY!",3),H-56,3)}" fill="#000"/>')
    return svg(W,H,"".join(b),css)

# ============ 4. INVENTORY ============
def inventory():
    W,H=900,280; S=76; gap=10; gx,gy=28,64; step=1.8; D=step*len(ITEMS)
    b=['<defs><pattern id="d1" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#fff"/><rect x="2" y="2" width="2" height="2" fill="#fff"/></pattern></defs>']
    b.append(nbox(12,12,W-24,H-24))
    b.append(f'<path d="{tp("ITEMS",32,32,3)}" fill="#fff"/><path d="{tp(f"{len(ITEMS)}/{len(ITEMS)}",32+tw("ITEMS ",3)+6,32,3)}" fill="url(#d1)"/>')
    s="GOLD 999999"; b.append(f'<path d="{tp(s,W-32-tw(s,3),32,3)}" fill="#fff"/>')
    pos=[]
    for i,(lab,ic,*_) in enumerate(ITEMS):
        c,r=i%5,i//5; x=gx+c*(S+gap); y=gy+r*(S+gap); pos.append((x,y))
        b.append(box(x,y,S,S,3)+f'<path d="{sp(ICONS[ic],x+S//2-15,y+10,3)}" fill="#fff"/><path d="{tp(lab,x+S//2-tw(lab,2)//2,y+S-22,2)}" fill="#fff"/>')
    vals=";".join(f"{x-6} {y-6}" for x,y in pos)
    b.append(f'<g><animateTransform attributeName="transform" type="translate" values="{vals}" dur="{D}s" calcMode="discrete" repeatCount="indefinite"/>'
             f'<rect x="3" y="3" width="{S+6}" height="{S+6}" fill="#fff" style="mix-blend-mode:difference"/>'
             f'<path d="M0 0h20v6h-14v14h-6zM{S+12} 0v20h-6v-14h-14v-6zM0 {S+12}h20v-6h-14v-14h-6zM{S+12} {S+12}v-20h-6v14h-14v6z" fill="#fff"/></g>')
    # description panel
    PX=gx+5*(S+gap)+14; PW=W-PX-32; PY=gy; PH=2*S+gap
    b.append(box(PX,PY,PW,PH,3))
    items=[]
    for i,(lab,ic,name,d1,d2,rar) in enumerate(ITEMS):
        g=(f'<path d="{sp(ICONS[ic],PX+18,PY+18,5)}" fill="#fff"/>'
           f'<path d="{tp(name[:18],PX+86,PY+22,2)}" fill="#fff"/>'
           f'<path d="{tp("*"*rar,PX+86,PY+44,2)}" fill="#fff"/><path d="{tp("*"*(5-rar),PX+86+rar*12,PY+44,2)}" fill="url(#d1)"/>'
           f'<rect x="{PX+18}" y="{PY+84}" width="{PW-36}" height="2" fill="url(#d1)"/>'
           f'<path d="{tp(d1,PX+18,PY+98,2)}" fill="#fff"/><path d="{tp(d2,PX+18,PY+118,2)}" fill="#fff"/>')
        items.append((g,i*step,(i+1)*step))
    g,css=seq(items,D); b.append(g)
    b.append(f'<path class="bl" d="{tp("} EQUIPPED",PX,H-44,2)}" fill="#fff"/>')
    return svg(W,H,"".join(b),css)

# ============ 5. NOW PLAYING ============
def player():
    random.seed(9); W,H=900,230
    css=(".r1{animation:bl .5s steps(1) infinite}.r2{animation:bl .5s steps(1) infinite;animation-delay:.25s}"
         ".beat{animation:beat .333s steps(1) infinite}@keyframes beat{50%{transform:scale(.8)}}"
         ".mq{animation:mq 14s linear infinite}@keyframes mq{from{transform:translateX(0)}to{transform:translateX(-"+str(tw(TRACK+"   ",3)+18)+"px)}}"
         ".ph{animation:ph 60s steps(60) infinite}@keyframes ph{to{transform:translateX(560px)}}")
    b=['<defs><pattern id="d1" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#fff"/><rect x="2" y="2" width="2" height="2" fill="#fff"/></pattern>'
       '<pattern id="seg" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#fff"/></pattern>'
       '<clipPath id="mqc"><rect x="276" y="40" width="596" height="34"/></clipPath></defs>']
    b.append(nbox(12,12,W-24,H-24))
    # cassette
    cx,cy=36,36; b.append(box(cx,cy,212,136,4)+f'<rect x="{cx+16}" y="{cy+14}" width="180" height="26" fill="#fff"/><path d="{tp("SIDE A * 180",cx+106-tw("SIDE A * 180",2)//2,cy+20,2)}" fill="#000"/>')
    b.append(box(cx+30,cy+52,152,48,3))
    for k,rx in enumerate((cx+66,cx+146)):
        b.append(f'<circle cx="{rx}" cy="{cy+76}" r="16" fill="#fff"/><circle cx="{rx}" cy="{cy+76}" r="10" fill="#000"/>'
                 f'<path class="r1" d="M{rx-2} {cy+66}h4v20h-4z" fill="#fff"/><path class="r2" d="M{rx-10} {cy+74}h20v4h-20z" fill="#fff"/>')
    b.append(f'<path d="M{cx+50} {cy+136}l12 -18h88l12 18z" fill="#fff"/><rect x="{cx+76}" y="{cy+124}" width="8" height="6" fill="#000"/><rect x="{cx+128}" y="{cy+124}" width="8" height="6" fill="#000"/>')
    # marquee
    b.append(box(272,36,604,42,3))
    t=TRACK+"   "; b.append(f'<g clip-path="url(#mqc)"><g class="mq"><path d="{tp(t,286,47,3)}" fill="#fff"/><path d="{tp(t,286+tw(t,3)+18,47,3)}" fill="#fff"/></g></g>')
    # progress
    b.append(f'<rect x="276" y="96" width="580" height="4" fill="url(#d1)"/><g class="ph"><rect x="276" y="90" width="12" height="16" fill="#fff"/></g>')
    b.append(f'<path d="{tp("03",276,118,3)}" fill="#fff"/><path class="bl" d="{tp(":",276+tw("03",3)+2,118,3)}" fill="#fff"/><path d="{tp("07",276+tw("03:",3)+6,118,3)}" fill="#fff"/>')
    # BPM
    b.append(f'<g transform="translate(470 126)"><g class="beat" style="transform-origin:15px 12px"><path d="{sp(F["*"],0,-7,6)}" fill="#fff"/></g></g><path d="{tp("180 BPM",510,118,3)}" fill="#fff"/>')
    # buttons
    bx=276; by=154
    icons=[ "M6 6h4v20h-4zM26 6v20l-14 -10z", "M8 6l18 10l-18 10z", "M8 6h6v20h-6zM18 6h6v20h-6z", "M6 6v20l14 -10zM22 6h4v20h-4z"]
    for k,d in enumerate(icons):
        x=bx+k*44
        if k==1: b.append(f'<rect x="{x}" y="{by}" width="32" height="32" fill="#fff"/><path d="{d}" transform="translate({x} {by})" fill="#000"/>')
        else: b.append(box(x,by,32,32,2)+f'<path d="{d}" transform="translate({x} {by})" fill="#fff"/>')
    # mini EQ
    ex=470; n=24
    for i in range(n):
        hs=[random.randrange(1,9)*4 for _ in range(8)]; hs.append(hs[0]); dur=random.choice([.66,.99,1.33])
        b.append(f'<rect x="{ex+i*16}" y="{190-hs[0]}" width="12" height="{hs[0]}" fill="url(#seg)"><animate attributeName="height" values="{";".join(map(str,hs))}" dur="{dur}s" calcMode="discrete" repeatCount="indefinite"/><animate attributeName="y" values="{";".join(str(190-h) for h in hs)}" dur="{dur}s" calcMode="discrete" repeatCount="indefinite"/></rect>')
    return svg(W,H,"".join(b),css)

# ============ 6. GAME OVER / CONTINUE ============
def gameover():
    W,H=900,240; D=12
    b=['<defs><pattern id="d1" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#fff"/><rect x="2" y="2" width="2" height="2" fill="#fff"/></pattern>'
       '<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect y="3" width="4" height="1" fill="#000"/></pattern></defs>']
    items=[]
    s="CONTINUE ?"; p=6
    cont=f'<path d="{tp(s,(W-tw(s,p))//2+4,44,p)}" fill="url(#d1)"/><path d="{tp(s,(W-tw(s,p))//2,40,p)}" fill="#fff"/>'
    for n in range(9,-1,-1):
        t=9-n; d=str(n); p=12
        items.append((cont+f'<path d="{tp(d,(W-tw(d,p))//2+6,108,p)}" fill="url(#d1)"/><path d="{tp(d,(W-tw(d,p))//2,102,p)}" fill="#fff"/>', t, t+1))
    s="GAME OVER"; p=10
    items.append((f'<path d="{tp(s,(W-tw(s,p))//2+6,86,p)}" fill="url(#d1)"/><path d="{tp(s,(W-tw(s,p))//2,80,p)}" fill="#fff"/>',10,12))
    g,css=seq(items,D); b.append(g)
    b.append(f'<rect x="24" y="200" width="{W-48}" height="2" fill="url(#d1)"/>')
    b.append(f'<path class="bl" d="{tp("INSERT COIN",24,212,2)}" fill="#fff"/>')
    s="CREDITS 00"; b.append(f'<path d="{tp(s,W-24-tw(s,2),212,2)}" fill="#fff"/>')
    b.append(f'<rect width="{W}" height="{H}" fill="url(#scan)" opacity=".35"/>')
    return svg(W,H,"".join(b),css)

# ============ 7. HEADERS + DIVIDER ============
def header(label):
    p=4; w=tw("} "+label,p)+48; h=7*p+28
    b=(f'<rect x="8" y="8" width="{w}" height="{h}" fill="url(#hd)"/><rect width="{w}" height="{h}" fill="#000"/>'+box(0,0,w,h,4)+
       f'<path class="bl" d="{tp("}",24,14,p)}" fill="#fff"/><path d="{tp(label,24+12*p,14,p)}" fill="#fff"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w+8}" height="{h+8}" viewBox="0 0 {w+8} {h+8}" shape-rendering="crispEdges">'
            f'<style>{BASE_CSS}</style><defs><pattern id="hd" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#000"/><rect x="2" y="2" width="2" height="2" fill="#000"/></pattern></defs>{b}</svg>')
def divider():
    W,H=900,28
    d="".join(f"M{i*16} 12h8v4h-8z" for i in range(60))
    css=".mv{animation:mv .6s linear infinite}@keyframes mv{to{transform:translateX(-16px)}}"
    b=(f'<g class="mv"><path d="{d}" fill="#fff"/></g><rect x="{W//2-44}" y="0" width="88" height="{H}" fill="#000"/>'
       f'<path class="bl" d="{tp("* * *",W//2-tw("* * *",2)//2,7,2)}" fill="#fff"/>')
    return svg(W,H,b,css)

os.makedirs(OUT,exist_ok=True)
files={"banner":banner(),"dialog":dialog(),"select":select(),"inventory":inventory(),"player":player(),"gameover":gameover(),"divider":divider()}
for k,lab in [("player1","PLAYER 1"),("inventory","INVENTORY"),("scores","HIGH SCORES"),("music","NOW PLAYING"),("bonus","BONUS STAGE"),("continue","CONTINUE ?")]:
    files["h-"+k]=header(lab)
for k,v in files.items(): open(os.path.join(OUT,k+".svg"),"w").write(v)
print("OK:",", ".join(files))
