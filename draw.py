#!/usr/bin/env python3
"""news-22 b3 dense-late: draw 1024x1024 front page, 34 stories, 13 illustration panels."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 253, 248)
INK = (17, 17, 17)
GRAY = (100, 100, 100)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
GREEN = (20, 83, 45)
GOLD = (180, 83, 9)
BLUE = (29, 78, 216)
PURPLE = (109, 40, 217)
LGREEN = (21, 128, 61)
SEA = (186, 214, 235)
LAND = (232, 214, 178)
FD = "/usr/share/fonts/truetype/dejavu/"

def fb(s): return ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", s)
def fr(s): return ImageFont.truetype(FD + "DejaVuSans.ttf", s)
def fs(s): return ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


def clip(text, font, maxw):
    if d.textlength(text, font=font) <= maxw:
        return text
    while text and d.textlength(text + "…", font=font) > maxw:
        text = text[:-1]
    return text + "…"

def badge(x, y, label, color):
    f = fb(8)
    w = d.textlength(label, font=f) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=3, fill=color)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w

BCOL = {"CONFIRMED": LGREEN, "OFFICIAL": PURPLE, "REPORTED": BLUE, "CLAIM": GOLD}

# ---- top bar ----
d.rectangle([0, 0, W, 22], fill=(0, 0, 0))
d.text((10, 4), "THE WORLD IN ONE DAY", font=fb(12), fill=(255, 255, 255))
d.text((W - 10 - d.textlength("34 STORIES  ·  6 REGIONS  ·  EVERY ITEM DATED 22 NOV", font=fb(11)),
         5), "34 STORIES  ·  6 REGIONS  ·  EVERY ITEM DATED 22 NOV", font=fb(11), fill=(255, 200, 60))
# ---- masthead ----
d.text((10, 28), "SUNDAY 22 NOVEMBER 2026", font=fs(46), fill=INK)
d.text((W - 10 - d.textlength("LATE EDITION", font=fb(14)), 32), "LATE EDITION", font=fb(14), fill=RED)
d.text((W - 10 - d.textlength("WIRES TO 23:00 UTC", font=fb(11)), 52), "WIRES TO 23:00 UTC", font=fb(11), fill=RED)
d.rectangle([0, 82, W, 86], fill=RED)

# ---- heroes (3 panels) ----
def hero(x0, x1, tag, big, head, body, bdg, src, bg, accent, art):
    d.rectangle([x0, 92, x1, 254], fill=bg)
    d.rectangle([x0, 92, x1, 96], fill=accent)
    d.text((x0 + 10, 100), tag, font=fb(11), fill=(255, 210, 90))
    art(x1 - 84, 98, 72, 48)
    lines = wrap(head, fb(20), x1 - x0 - 118)
    y = 122
    for ln in lines[:2]:
        d.text((x0 + 10, y), ln, font=fb(20), fill=(255, 255, 255)); y += 22
    d.text((x0 + 10, y + 4), big, font=fb(30), fill=(255, 210, 90))
    d.text((x0 + 10, y + 40), clip(body, fr(11), x1 - x0 - 20), font=fr(11), fill=(235, 235, 235))
    bw = badge(x0 + 10, 236, bdg, BCOL[bdg])
    d.text((x0 + 14 + bw, 238), src, font=fr(9), fill=(220, 220, 220))

def art_tanker(x, y, w, h):
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(40, 90, 130))
    d.polygon([(x + 6, y + h - 14), (x + 20, y + h - 24), (x + w - 20, y + h - 24),
               (x + w - 6, y + h - 14)], fill=(20, 20, 20))
    d.rectangle([x + w // 2 - 6, y + h - 34, x + w // 2 + 6, y + h - 24], fill=(240, 240, 240))
    cx, cy, r = x + 11, y + 9, 5
    for dx, dy in [(0, -8), (0, 8), (-8, 0), (8, 0), (-6, -6), (6, -6), (-6, 6), (6, 6)]:
        d.line([cx, cy, cx + dx, cy + dy], fill=(255, 210, 90), width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 210, 90))
    d.ellipse([x + w - 18, y + 4, x + w - 8, y + 14], fill=(255, 120, 60))

def art_globe(x, y, w, h):
    cx, cy, r = x + w // 2, y + h // 2, 15
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 210, 90), width=2)
    d.line([cx - 4, cy - r + 3, cx + 3, cy - 3, cx - 3, cy + 5, cx + 5, cy + r - 3],
           fill=(255, 120, 60), width=2)
    for fx in range(4):
        d.rectangle([x + fx * 18, y + h - 8, x + fx * 18 + 11, y + h - 2],
                    fill=[(255, 255, 255), (255, 120, 60), (255, 210, 90), (120, 200, 255)][fx])

def art_capitol(x, y, w, h):
    cx = x + w // 2
    d.pieslice([cx - 14, y + 2, cx + 14, y + 24], 180, 360, fill=(255, 255, 255))
    d.rectangle([cx - 2, y, cx + 2, y + 4], fill=(255, 255, 255))
    for i in range(5):
        px = cx - 24 + i * 12
        d.rectangle([px, y + 26, px + 5, y + h - 3], fill=(255, 255, 255))
    d.rectangle([x + 4, y + h - 3, x + w - 4, y + h], fill=(255, 255, 255))

hero(8, 334, "GULF  ·  HORMUZ", "2 TANKERS", "HIT BY MINES",
     "Iran's navy says two supertankers hit mines and caught fire east of the Strait; UKMTO reports a tanker incident in the Gulf of Oman.",
     "REPORTED", "Iran navy · UKMTO", NAVY, (255, 210, 90), art_tanker)
hero(342, 668, "CLIMATE  ·  ANTALYA", "NO DEAL", "COP31 COLLAPSES",
     "Summit ends without agreement after the EU rejects a final text with no mention of fossil fuels — the first collapse since 2009.",
     "OFFICIAL", "COP31 presidency · EU", GREEN, (255, 210, 90), art_globe)
hero(676, 1016, "WASHINGTON", "258 SEATS", "DEMOCRATS WIN",
     "House flips: largest majority since 1992 after a North Carolina recount; divided government looms.",
     "CONFIRMED", "AP · Daily Summary", (120, 20, 20), (255, 210, 90), art_capitol)

# ---- verification legend ----
d.text((10, 260), "HOW WE KNOW:", font=fb(10), fill=INK)
lx = 100
for lab, col, desc in [("CONFIRMED", LGREEN, "confirmed by its source"),
                       ("OFFICIAL", PURPLE, "official record"),
                       ("REPORTED", BLUE, "reported by a named wire"),
                       ("CLAIM", GOLD, "one side alleges, not verified")]:
    w = badge(lx, 259, lab, col)
    d.text((lx + w + 4, 261), desc, font=fr(9), fill=GRAY)
    lx += w + 4 + d.textlength(desc, font=fr(9)) + 16

# ---- map + numbers ----
d.rectangle([8, 282, 620, 412], fill=SEA)
def ll(lon, lat):
    return (8 + (lon + 170) * 612 / 360, 282 + (75 - lat) * 130 / 130)
def poly_ll(pts):
    d.polygon([ll(a, b) for a, b in pts], fill=LAND, outline=(160, 140, 110))
poly_ll([(-168,66),(-150,70),(-125,71),(-110,68),(-95,69),(-85,66),(-75,62),(-65,60),(-55,47),(-60,42),(-70,38),(-75,32),(-81,25),(-90,21),(-97,16),(-105,20),(-115,28),(-125,40),(-140,58),(-158,58),(-168,60)])
poly_ll([(-58,64),(-45,60),(-30,68),(-20,70),(-35,76),(-55,74)])
poly_ll([(-79,9),(-72,11),(-62,10),(-52,5),(-44,-3),(-35,-8),(-40,-20),(-48,-28),(-58,-35),(-68,-40),(-73,-50),(-70,-30),(-75,-18),(-80,-5)])
poly_ll([(-10,36),(-2,44),(0,50),(5,53),(10,57),(18,55),(24,59),(30,70),(40,68),(35,60),(30,50),(28,45),(20,40),(12,44),(3,43),(-9,37)])
poly_ll([(-5,50),(-3,53),(-5,56),(-2,58),(0,53),(1,51),(-3,50)])
poly_ll([(-17,15),(-16,25),(-10,31),(-5,35),(10,37),(20,32),(30,31),(35,28),(43,12),(51,11),(48,0),(40,-15),(35,-25),(28,-33),(18,-35),(15,-27),(12,-18),(9,-1),(9,4),(-8,4),(-13,8),(-17,12)])
poly_ll([(30,36),(35,42),(40,45),(45,42),(50,40),(55,38),(60,25),(57,26),(52,28),(48,30),(56,27),(58,22),(60,15),(65,10),(70,8),(77,8),(80,13),(85,18),(90,22),(95,16),(100,8),(103,2),(105,-5),(110,-7),(115,-8),(120,-12),(125,-10),(130,-5),(135,0),(140,5),(142,15),(140,30),(138,38),(132,43),(128,38),(126,35),(120,32),(115,25),(108,20),(105,10),(100,15),(95,25),(90,30),(85,35),(80,40),(75,45),(70,50),(65,55),(60,60),(55,65),(50,68),(45,68),(40,65),(35,60),(30,55),(30,45),(30,36)])
poly_ll([(113,-22),(114,-30),(115,-35),(120,-34),(125,-32),(130,-32),(135,-35),(140,-38),(145,-38),(150,-37),(153,-32),(150,-25),(146,-19),(142,-15),(137,-12),(132,-12),(126,-14),(122,-17),(118,-20),(113,-22)])
poly_ll([(167,-45),(170,-42),(174,-38),(177,-38),(175,-41),(170,-44)])
poly_ll([(130,31),(133,34),(137,35),(140,38),(141,42),(143,44),(140,40),(136,37),(132,33)])
pins = [(1, 56, 26, 12, -10), (2, 20, 32, -16, 10), (3, 32, 15, 0, 0), (4, 30, 50, 0, 0),
        (5, 51, 35, 0, 0), (6, 47, 25, 0, 14), (7, 30, 37, 0, 0), (8, 4, 51, 0, 0),
        (9, 34, 31, 16, 10), (10, 106, -6, 0, 0), (11, -77, 39, 0, 0), (12, 4, 52, 14, -10),
        (13, 116, 40, 0, 0)]
for n, lon, lat, dx, dy in pins:
    px, py = ll(lon, lat)
    lx, ly = px + dx, py + dy
    if dx or dy:
        d.line([px, py, lx, ly], fill=RED, width=1)
    d.ellipse([lx - 8, ly - 8, lx + 8, ly + 8], fill=RED, outline=(255, 255, 255), width=1)
    t = str(n)
    d.text((lx - d.textlength(t, font=fb(8)) / 2, ly - 6), t, font=fb(8), fill=(255, 255, 255))
d.rectangle([8, 286, 330, 302], fill=SEA)
d.text((16, 288), "WHERE IT HAPPENED — EVERY STORY PINNED", font=fb(10), fill=INK)
d.text((16, 396), "Numbers are story numbers on this page.", font=fr(8), fill=GRAY)

# numbers strip
d.rectangle([628, 282, 1016, 412], fill=(245, 245, 240))
d.text((640, 288), "THE DAY IN NUMBERS", font=fb(11), fill=INK)
nums = [("2", "tankers hit mines"), ("258", "House seats, Dems"),
        ("1,661", "Gaza toll since Oct 2025"), ("130", "blockade days"),
        ("2,700", "drones in a week, Russia"), ("36", "missing, Cikande fire")]
for i, (v, lab) in enumerate(nums):
    cx = 640 + (i % 2) * 190
    cy = 304 + (i // 2) * 38
    d.text((cx, cy), v, font=fb(17), fill=RED)
    d.text((cx, cy + 20), lab, font=fr(9), fill=INK)

# ---- 9 mini illustration panels ----
d.text((10, 418), "THE DAY IN PICTURES", font=fb(10), fill=INK)
panels = [
    ("TANKERS", (30, 58, 95)), ("DRONES", (90, 40, 40)), ("MISSILES", (60, 60, 60)),
    ("SUMMIT", (20, 83, 45)), ("CAPITOL", (120, 20, 20)), ("FIRE", (180, 83, 9)),
    ("COURT", (109, 40, 217)), ("CHIPS", (29, 78, 216)), ("STREETS", (100, 100, 100)),
]
px = 10
for lab, col in panels:
    d.rectangle([px, 432, px + 106, 480], fill=col)
    d.rectangle([px, 432, px + 106, 436], fill=(255, 210, 90))
    # simple scene glyph: circle + lines
    d.ellipse([px + 44, 442, px + 62, 460], outline=(255, 255, 255), width=2)
    d.line([px + 24, 462, px + 82, 462], fill=(255, 255, 255), width=2)
    d.text((px + 53 - d.textlength(lab, font=fb(8)) / 2, 469), lab, font=fb(8), fill=(255, 255, 255))
    px += 112

# ---- grid: 31 stories, 3 columns ----
stories = [
    (4, "Benghazi: sea drone hits Russian corvette Merkury", "Explosion and fire at naval base; no group claims it; Kyiv claims the strike.", "CLAIM", "Libya govt · Kyiv"),
    (5, "Khartoum: drones kill 4, damage UN building", "RSF blamed for strikes; Omdurman home hit, 3 dead, 9 hurt; staff inside UN site.", "CLAIM", "UN · Reuters"),
    (6, "Zelenskyy: release Patriots as Russia strikes", "Partners paid, delivery awaits Washington; 165 missiles in a week; Dymer hit.", "REPORTED", "AP"),
    (7, "Iran unveils dual-missile launcher, missile city", "State footage shows twin launchers in tunnels as the US blockade bites.", "REPORTED", "Iran state media"),
    (8, "Saudi intercepts Houthi drone and missile", "Coalition stops both; Houthis say they hit Rabigh refinery on the Red Sea.", "CLAIM", "Saudi coalition"),
    (9, "Ex-Italian police chief found dead in inquiry", "Body found Saturday; Meloni shocked; he faced a Sicily bombing cover-up probe.", "REPORTED", "AP"),
    (10, "UAE condemns Iran attack on Bahrain", "Calls it a sovereignty violation; Bahrain says a civilian facility was hit.", "REPORTED", "UAE · Bahrain"),
    (11, "Europe protests, 3rd day over costs, housing", "Rallies from Portugal to France; in France, a sixth straight weekend.", "REPORTED", "AFP"),
    (12, "Settlers burn 12 vehicles in West Bank", "Ramallah villages hit; racist slogans sprayed; police probe arson at 4 sites.", "REPORTED", "Al Jazeera"),
    (13, "Benghazi naval base ammo depot explodes", "Blast and fire at the eastern port base; cause and casualties not disclosed.", "REPORTED", "Libya emergency"),
    (14, "Eisenkot, Likud open unity government talks", "No bloc holds a majority after October vote; Eisenkot has until early December.", "REPORTED", "AP"),
    (15, "Finland: war spilling over after ship strike", "Drone hit on Russian cargo ship Sparta II in the Baltic; windows scarce in Kyiv.", "REPORTED", "Finland · AP"),
    (16, "WCK: 3 killed in Gaza strike were not its team", "Founder Andres says the food van was not theirs; army says it hit militants.", "REPORTED", "WCK · IDF"),
    (17, "Ex-UN envoy: Iran war was perfectly avoidable", "De Soto tells MED Dialogues the war need not have happened; peace needs roots.", "REPORTED", "UN · MED"),
    (18, "Cikande candy factory fire: 3 dead, 36 missing", "Blaze at Fonusa Agung Mulia in Banten; 15 rescued alive; search goes on.", "REPORTED", "AP · Reuters"),
    (19, "Turkey: Israel may use Druze for Syria move", "Fidan says Israel arms a Druze tribe and may provoke the Syrian army.", "CLAIM", "Turkey FM"),
    (20, "Bahrain blames Iran for industrial strike", "Fire at a civilian site near Manama; Iran says it hit two Patriot radars.", "REPORTED", "Bahrain · IRGC"),
    (21, "Fidan: war fallout threatens global markets", "Turkish FM says the burden is growing; Hormuz diplomacy deadlocked.", "REPORTED", "Turkey FM"),
    (22, "Lebanon's Aoun demands Israeli withdrawal", "Every inch of territory, he says; all weapons under state control.", "REPORTED", "Lebanon"),
    (23, "Displaced Palestinians protest in Gaza", "Hundreds near the Yellow Line; 500 housing units destroyed in under a month.", "REPORTED", "Gaza ministry"),
    (24, "Pezeshkian: Iran in silent economic war", "President says the economic front is harder than missiles; day 130 of blockade.", "REPORTED", "Iran presidency"),
    (25, "Settlers attack homes in Hebron, Ramallah", "Doors forced, windows smashed; tear gas fired in a raid near Ramallah.", "REPORTED", "Al Jazeera"),
    (26, "Turkey: Israel blocking Gaza container homes", "Fidan says thousands of units held back; families left in tents in the cold.", "CLAIM", "Turkey FM"),
    (27, "Hind Rajab urges Germany to arrest soldier", "Complaint filed over war crimes; soldier sighted in Luneburg this week.", "REPORTED", "HRF · Berlin"),
    (28, "Fred Nile, NSW figurehead, dies aged 92", "Served 40+ years in the legislative council; died peacefully on 21 November.", "REPORTED", "Family · NSW"),
    (29, "Teen gamer, mother help rescue missing girl", "Online chat tip led to the FBI; the girl had been missing over a year.", "REPORTED", "FBI · AP"),
    (30, "Gaza toll since Oct 2025: 1,661 or 1,671", "Nine killed in 48 hours; 851 bodies recovered; 6,062 wounded since the ceasefire.", "REPORTED", "Gaza health min."),
    (31, "Kryvyi Rih: missile kills boy, 7, and woman, 20", "Russian strike on Zelenskyy's hometown wounds about 60, six of them children.", "REPORTED", "AP · CNN"),
    (32, "ICJ: Myanmar committed genocide on Rohingya", "First time the court finds a state responsible for genocide, over 2017.", "OFFICIAL", "ICJ"),
    (33, "Nvidia: US confirms China got AI chips", "Bessent presses the firm for answers as the chip scandal deepens.", "REPORTED", "NYT · Treasury"),
    (34, "China eases margin rules to calm stocks", "Exchanges cut the minimum margin ratio to 80% from 100% on 30 November.", "REPORTED", "Shanghai · AP"),
]
cols = [[], [], []]
for i, s in enumerate(stories):
    cols[i % 3].append(s)
colx = [10, 348, 686]
y0 = 490
for ci, col in enumerate(cols):
    y = y0
    for (n, head, body, bdg, src) in col:
        d.text((colx[ci], y), f"{n:02d}", font=fb(13), fill=RED)
        hx = colx[ci] + 26
        d.text((hx, y), clip(head, fb(12), 304), font=fb(12), fill=INK)
        d.text((hx, y + 14), clip(body, fr(10), 304), font=fr(10), fill=(60, 60, 60))
        bw = badge(hx, y + 27, bdg, BCOL[bdg])
        d.text((hx + bw + 4, y + 28), src, font=fr(8), fill=GRAY)
        y += 41

# ---- UTC timeline ----
d.rectangle([0, 946, W, 962], fill=(20, 20, 20))
d.text((10, 950), "22 NOV — FIRST REPORTED (UTC)", font=fb(9), fill=(255, 210, 90))
tl = "17:13 Hormuz tankers   ·   15:36 Benghazi ship   ·   15:03 Khartoum drones   ·   14:48 Patriots plea   ·   14:20 Iran missiles   ·   12:00 COP31 NO DEAL"
d.text((250, 950), tl, font=fr(9), fill=(255, 255, 255))
# ---- NOT YET strip ----
d.rectangle([0, 964, W, 980], fill=(255, 243, 200))
d.text((10, 968), "NOT YET — DO NOT READ AS DONE:", font=fb(9), fill=RED)
d.text((232, 968), "COP32 venue not set  ·  Cikande search goes on  ·  Merkury probe ongoing  ·  House recounts still open", font=fr(9), fill=INK)
# ---- footer ----
d.text((10, 986), "DATE CHECK — Every story dated 22 Nov 2026. EXCLUDED as not 22 Nov: Friday Wall St rout (20 Nov) · El Chapo Isidro (21 Nov) · EU–Indonesia deal (21 Nov) · Shenzhen trilateral (19–20 Nov) · Skubal $450M (date unconfirmed).", font=fr(8), fill=GRAY)
d.text((10, 996), "REPORTED = confirmed by its source  ·  CLAIM = one side alleges  ·  OFFICIAL = official record  ·  ONGOING = still developing.  No forecast shown as fact.", font=fr(8), fill=GRAY)
d.text((10, 1006), "SOURCES: AP · Reuters · AFP · Al Jazeera · BBC · CNN · NYT · Daily Summary · UKMTO · ICJ · WCK · UN News", font=fr(8), fill=GRAY)
d.text((W - 10 - d.textlength("THE WORLD IN ONE DAY · 22 NOV 2026", font=fb(8)), 1006),
       "THE WORLD IN ONE DAY · 22 NOV 2026", font=fb(8), fill=GRAY)

img.save("/home/hatch/workspace/makefun/news-22-b3-dense-late-build/entry.png")
print("saved", img.size)
import os
print("bytes:", os.path.getsize("/home/hatch/workspace/makefun/news-22-b3-dense-late-build/entry.png"))
